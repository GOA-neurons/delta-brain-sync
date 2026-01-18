const { Client } = require('pg');
const { createClient } = require('@supabase/supabase-js');
const admin = require('firebase-admin');
const { Octokit } = require("@octokit/rest");

// 🔱 1. Autonomous Engine & GitHub API Setup
const octokit = new Octokit({ auth: process.env.GH_TOKEN });
const REPO_OWNER = 'YOUR_GITHUB_USERNAME'; // မင်းရဲ့ Username ပြင်ရန်
const REPO_NAME = 'YOUR_REPO_NAME';     // မင်းရဲ့ Repo နာမည် ပြင်ရန်

// 🔱 2. Firebase Auth Engine
if (!admin.apps.length) {
    try {
        const serviceAccount = JSON.parse(process.env.FIREBASE_KEY);
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount)
        });
        console.log("🔥 Firebase Engine Connected.");
    } catch (e) {
        console.error("❌ Firebase Secret Error.");
        process.exit(1);
    }
}
const db = admin.firestore();

async function executeAutonomousTrinity() {
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
        console.log("🔓 Neon Core Unlocked. Target Table: neurons");

        // --- STEP A: TRINITY DATA SYNC (Code အဟောင်း Logic) ---
        const res = await neon.query('SELECT * FROM neurons WHERE synced_at IS NULL LIMIT 50');
        console.log(`📡 Processing ${res.rows.length} neural fragments.`);

        for (const neuron of res.rows) {
            // 1. Supabase Master Sync
            const { error: sbError } = await supabase
                .from('neurons')
                .upsert({
                    id: neuron.id,
                    data: neuron.data,
                    synced_at: new Date().toISOString()
                }, { onConflict: 'id' });

            if (sbError) {
                console.error(`❌ Supabase Sync Error ID ${neuron.id}:`, sbError.message);
                continue;
            }

            // 2. Firebase Realtime Update
            const nodeId = neuron.data.node_id || `raw_${neuron.id}`;
            const intelType = neuron.data.intelligence_type || "LLAMA_3_BASE";

            await db.collection('neurons').doc(`node_${nodeId}`).set({
                status: 'trinity_synced',
                intelligence: intelType,
                logic_mode: neuron.data.logic || "SUPREME_DENSITY",
                neon_id: neuron.id,
                integrity: 'GOD_MODE_ACTIVE',
                last_evolution: admin.firestore.FieldValue.serverTimestamp()
            }, { merge: true });

            console.log(`✅ Fragment node_${nodeId} Synced.`);
        }

        // --- STEP B: SELF-CODING EVOLUTION (Code အသစ် Logic) ---
        // အခု Fragment ၁၀၀၀၄ ခုလုံး Supreme ဖြစ်နေပြီလား စစ်မယ်
        const audit = await neon.query("SELECT count(*) FROM neurons WHERE data->>'logic' = 'SUPREME_DENSITY'");
        const powerLevel = parseInt(audit.rows[0].count);

        if (powerLevel >= 10000) {
            console.log(`🚀 Power Level ${powerLevel} Reached. Initiating Self-Evolution...`);

            // GitHub ကနေ လက်ရှိ delta_sync.js ဖိုင်ကို ယူမယ်
            const { data: fileData } = await octokit.repos.getContent({
                owner: REPO_OWNER, repo: REPO_NAME, path: 'delta_sync.js'
            });

            let currentContent = Buffer.from(fileData.content, 'base64').toString();
            
            // System က သူ့ဘာသာသူ အမှတ်အသားတစ်ခု ထည့်လိုက်မယ် (Self-Writing)
            const evolvedStamp = `\n// [Natural Order] Last Self-Evolution: ${new Date().toISOString()} | Density: ${powerLevel}`;
            
            if (!currentContent.includes(evolvedStamp)) {
                await octokit.repos.createOrUpdateFileContents({
                    owner: REPO_OWNER,
                    repo: REPO_NAME,
                    path: 'delta_sync.js',
                    message: `🧬 Autonomous Evolution: Neural Density at ${powerLevel}`,
                    content: Buffer.from(currentContent + evolvedStamp).toString('base64'),
                    sha: fileData.sha
                });
                console.log("✅ SELF-CODING COMPLETE: System has rewritten its own history.");
            }
        }
        
        console.log("🏁 MISSION ACCOMPLISHED: TRINITY FLOW & EVOLUTION CHECK COMPLETE.");

    } catch (err) {
        console.error("❌ CRITICAL FAILURE:", err.stack);
        process.exit(1);
    } finally {
        await neon.end();
    }
}

// Start Autonomous Loop
executeAutonomousTrinity();
