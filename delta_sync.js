const { Client } = require('pg');
const { createClient } = require('@supabase/supabase-js');
const admin = require('firebase-admin');

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT))
    });
}
const db = admin.firestore();

async function execute() {
    const neon = new Client({ 
        connectionString: process.env.NEON_DATABASE_URL,
        ssl: { rejectUnauthorized: false } 
    });
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

    try {
        await neon.connect();
        // Neon ကနေ နောက်ဆုံး Neuron ၅၀ ကို ယူမယ်
        const res = await neon.query('SELECT * FROM neurons ORDER BY evolved_at DESC LIMIT 50');
        
        for (const neuron of res.rows) {
            // ၁။ Supabase ထဲကို ဒေတာအကုန် Upsert လုပ်မယ်
            const { error: sbError } = await supabase
                .from('delta_neurons')
                .upsert({
                    original_id: neuron.id,
                    data: neuron.data,
                    synced_at: new Date()
                });

            if (!sbError) {
                // ၂။ အောင်မြင်ရင် Firestore ထဲက Status ကို 'evolved' လို့ ဇွတ်ပြောင်းမယ်
                // neuron.id သို့မဟုတ် data ထဲက gen ကို သုံးပြီး Doc ကို ရှာမယ်
                const docRef = db.collection('neurons').doc(`gen_${neuron.data.gen}`);
                await docRef.set({
                    status: 'evolved',
                    last_evolution: admin.firestore.FieldValue.serverTimestamp(),
                    neon_id: neuron.id
                }, { merge: true });
                
                console.log(`✅ Gen ${neuron.data.gen} Synced & Evolved.`);
            }
        }
        console.log("🏁 MISSION ACCOMPLISHED: TRINITY SYNC COMPLETE.");
    } catch (err) {
        console.error("❌ CRITICAL ERROR:", err.message);
        process.exit(1);
    } finally {
        await neon.end();
    }
}
execute();
