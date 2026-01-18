const { Client } = require('pg');
const { createClient } = require('@supabase/supabase-js');
const admin = require('firebase-admin');

// 🔱 Firebase Auth Engine
if (!admin.apps.length) {
    try {
        const serviceAccount = JSON.parse(process.env.FIREBASE_KEY);
        admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });
    } catch (e) { process.exit(1); }
}
const db = admin.firestore();

async function executeTrinitySync() {
    const neon = new Client({ connectionString: process.env.NEON_KEY, ssl: { rejectUnauthorized: false } });
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

    try {
        await neon.connect();
        console.log("🔓 Neon Unlocked. Syncing to Supabase Master Table: neurons");

        // Neon ကနေ raw fragments ၅၀ ယူမယ်
        const res = await neon.query('SELECT * FROM neurons LIMIT 50');

        for (const neuron of res.rows) {
            // Supabase 'neurons' table နဲ့ Match လုပ်ခြင်း
            const { error: sbError } = await supabase
                .from('neurons')
                .upsert({
                    id: neuron.id,
                    data: neuron.data,
                    synced_at: new Date().toISOString() // အသစ်တိုးထားတဲ့ column
                }, { onConflict: 'id' });

            if (sbError) {
                console.error(`❌ Sync Error ID ${neuron.id}:`, sbError.message);
                continue;
            }

            // Firebase Update
            const genId = neuron.data.gen || `raw_${neuron.id}`;
            await db.collection('neurons').doc(`gen_${genId}`).set({
                status: 'trinity_synced',
                last_evolution: admin.firestore.FieldValue.serverTimestamp(),
                neon_id: neuron.id
            }, { merge: true });

            console.log(`✅ Locked & Synced: gen_${genId}`);
        }
        console.log("🏁 MASTER TRINITY SYNC COMPLETE.");
    } catch (err) { console.error(err.stack); process.exit(1); } finally { await neon.end(); }
}

executeTrinitySync();
