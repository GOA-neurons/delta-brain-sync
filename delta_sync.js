const { Client } = require('pg');
const { createClient } = require('@supabase/supabase-js');
const admin = require('firebase-admin');

// Firebase Admin Setup
if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT))
    });
}
const db = admin.firestore();

async function execute() {
    const neon = new Client({ connectionString: process.env.NEON_DATABASE_URL });
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

    try {
        await neon.connect();
        // 1. Neon ကနေ နောက်ဆုံး Neuron ၅၀ ကို ဇွတ်ယူ
        const res = await neon.query('SELECT * FROM neurons ORDER BY created_at DESC LIMIT 50');
        const latestNeurons = res.rows;

        for (const neuron of latestNeurons) {
            // 2. Supabase ထဲကို ဇွတ် Upsert လုပ်
            const { error } = await supabase
                .from('delta_neurons')
                .upsert({
                    original_id: neuron.id,
                    bias: neuron.bias,
                    synced_at: new Date()
                });

            if (!error) {
                // 3. Firestore ထဲက Neuron ကို ဇွတ် Update လုပ်ပြီး Feedback Loop ပိတ်မယ်
                await db.collection('neurons').doc(neuron.id).update({
                    delta_bias: neuron.bias,
                    last_evolution: admin.firestore.FieldValue.serverTimestamp(),
                    status: 'evolved'
                });
            }
        }
        console.log("🏁 SUCCESS: Neon -> Supabase -> Firestore Sync Complete!");
    } catch (err) {
        console.error("❌ ERROR:", err);
        process.exit(1);
    } finally {
        await neon.end();
    }
}

execute();
