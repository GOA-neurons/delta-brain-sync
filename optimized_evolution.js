const admin = require('firebase-admin');
const { Client } = require('pg');

async function run() {
    try {
        console.log("🚀 Sync Process Starting...");
        admin.initializeApp({
            credential: admin.credential.cert(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT))
        });
        const db = admin.firestore();

        const client = new Client({
            connectionString: process.env.NEON_DATABASE_URL,
            ssl: { rejectUnauthorized: false }
        });

        await client.connect();
        console.log("✅ Neon Connected!");

        // Table အသင့်ရှိမရှိ ထပ်စစ်မယ်
        await client.query(`
            CREATE TABLE IF NOT EXISTS neurons (
                id SERIAL PRIMARY KEY,
                data JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        `);

        const snap = await db.collection('neurons').limit(1).get();
        if (snap.empty) {
            console.log("⚠️ No documents in Firestore!");
        } else {
            const doc = snap.docs[0];
            await client.query('INSERT INTO neurons (data) VALUES ($1)', [JSON.stringify(doc.data())]);
            console.log("🏁 SUCCESS: 1 doc synced!");
        }

        await client.end();
    } catch (e) {
        console.error("❌ ERROR:", e.message);
        process.exit(1);
    }
}
run();
