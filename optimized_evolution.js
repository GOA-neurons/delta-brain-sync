const admin = require('firebase-admin');
const { Client } = require('pg');

async function run() {
    try {
        console.log("🚀 Sync Started...");
        const keyRaw = process.env.FIREBASE_SERVICE_ACCOUNT;
        if (!keyRaw) throw new Error("FIREBASE_KEY is missing from GitHub Secrets!");

        admin.initializeApp({
            credential: admin.credential.cert(JSON.parse(keyRaw))
        });
        
        const client = new Client({ 
            connectionString: process.env.NEON_DATABASE_URL, 
            ssl: { rejectUnauthorized: false } 
        });
        
        await client.connect();
        console.log("✅ Neon Connected!");
        
        const db = admin.firestore();
        const snap = await db.collection('neurons').limit(1).get();
        console.log(`📡 Firebase Data: ${snap.size} docs found`);
        
        await client.end();
        console.log("🏁 SUCCESS!");
    } catch (e) {
        console.error("❌ CRITICAL ERROR:", e.message);
        process.exit(1);
    }
}
run();
