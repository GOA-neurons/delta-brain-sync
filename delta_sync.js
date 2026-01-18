const { Client } = require('pg');
const { createClient } = require('@supabase/supabase-js');
const admin = require('firebase-admin');

// 🔱 1. Firebase Engine (Matching Secret: FIREBASE_KEY)
if (!admin.apps.length) {
    try {
        const serviceAccount = JSON.parse(process.env.FIREBASE_KEY);
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount)
        });
        console.log("🔥 Firebase Initialized.");
    } catch (e) {
        console.error("❌ Firebase Secret Error. Check FIREBASE_KEY format.");
        process.exit(1);
    }
}
const db = admin.firestore();

async function executeTrinity() {
    // 🔱 2. Database Core (Matching Secrets: NEON_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    const neon = new Client({ 
        connectionString: process.env.NEON_KEY, 
        ssl: { rejectUnauthorized: false } 
    });
    
    const supabase = createClient(
        process.env.SUPABASE_URL, 
        process.env.SUPABASE_SERVICE_ROLE_KEY
    );

    try {
        await neon.connect();
        console.log("🔓 Neon Core Unlocked.");

        // Patch V11.1: Fetching fragments from Neon
        const res = await neon.query('SELECT * FROM neurons LIMIT 50');
        console.log(`📡 Processing ${res.rows.length} fragments.`);

        for (const neuron of res.rows) {
            // A. Sync to Supabase delta_neurons
            const { error: sbError } = await supabase
                .from('delta_neurons')
                .upsert({
                    original_id: neuron.id.toString(),
                    data: neuron.data,
                    synced_at: new Date().toISOString()
                }, { onConflict: 'original_id' });

            if (sbError) {
                console.error(`❌ Supabase Error ID ${neuron.id}:`, sbError.message);
                continue;
            }

            // B. Sync to Firebase (Realtime Status Update)
            const genId = neuron.data.gen || `raw_${neuron.id}`;
            await db.collection('neurons').doc(`gen_${genId}`).set({
                status: 'evolved',
                neon_id: neuron.id,
                integrity: 'AUTONOMOUS_V11.1_SYNC',
                last_evolution: admin.firestore.FieldValue.serverTimestamp()
            }, { merge: true });

            console.log(`✅ Fragment gen_${genId} Synced Across Trinity.`);
        }
        
        console.log("🏁 MISSION ACCOMPLISHED: AUTONOMOUS DATA FLOW SUCCESSFUL.");
    } catch (err) {
        console.error("❌ CRITICAL FAILURE:", err.stack);
        process.exit(1);
    } finally {
        await neon.end();
    }
}

executeTrinity();
