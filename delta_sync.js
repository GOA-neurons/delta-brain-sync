const { Client } = require('pg');
const { createClient } = require('@supabase/supabase-js');
const admin = require('firebase-admin');

// 🔱 Firebase Auth Check
if (!admin.apps.length) {
    try {
        // GitHub Secret ထဲက FIREBASE_KEY ကို သုံးမယ်
        const serviceAccount = JSON.parse(process.env.FIREBASE_KEY);
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount)
        });
    } catch (e) {
        console.error("❌ Firebase Init Failed. Check FIREBASE_KEY format.");
    }
}
const db = admin.firestore();

async function execute() {
    // 🔱 Connection Strings (Environment Variables မှ ယူမယ်)
    const neon = new Client({ 
        connectionString: process.env.NEON_KEY, // မင်းရဲ့ YAML ထဲမှာ NEON_KEY လို့ ပေးထားလို့
        ssl: { rejectUnauthorized: false } 
    });
    
    const supabase = createClient(
        process.env.SUPABASE_URL, 
        process.env.SUPABASE_SERVICE_ROLE_KEY
    );

    try {
        await neon.connect();
        console.log("🔓 Neon Connected. Fetching Neural Fragments...");

        // Neon ကနေ နောက်ဆုံး Neuron ၅၀ ကို ယူမယ်
        const res = await neon.query('SELECT * FROM neurons ORDER BY evolved_at DESC LIMIT 50');
        
        if (res.rows.length === 0) {
            console.log("🌑 No new neurons to sync.");
            return;
        }

        for (const neuron of res.rows) {
            // ၁။ Supabase ထဲကို Upsert လုပ်မယ်
            const { error: sbError } = await supabase
                .from('delta_neurons')
                .upsert({
                    original_id: neuron.id.toString(),
                    data: neuron.data,
                    synced_at: new Date().toISOString()
                }, { onConflict: 'original_id' });

            if (sbError) {
                console.error(`❌ Supabase Error for ID ${neuron.id}:`, sbError.message);
                continue;
            }

            // ၂။ Firestore Status Update
            // neuron.data.gen မရှိရင် id ကို သုံးမယ်
            const genId = neuron.data.gen || `raw_${neuron.id}`;
            const docRef = db.collection('neurons').doc(`gen_${genId}`);
            
            await docRef.set({
                status: 'evolved',
                last_evolution: admin.firestore.FieldValue.serverTimestamp(),
                neon_id: neuron.id,
                integrity_check: 'V11.0_VERIFIED'
            }, { merge: true });
            
            console.log(`✅ Neuron ${genId} Locked & Synced.`);
        }
        
        console.log("🏁 MISSION ACCOMPLISHED: TRINITY SYNC COMPLETE.");
    } catch (err) {
        console.error("❌ CRITICAL ERROR:", err.stack);
        process.exit(1);
    } finally {
        await neon.end();
    }
}

execute();
