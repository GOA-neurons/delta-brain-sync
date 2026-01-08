const admin = require('firebase-admin');
const { Client } = require('pg');

if (!admin.apps.length) {
    admin.initializeApp({
        credential: admin.credential.cert(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT))
    });
}
const db = admin.firestore();

async function startEvolution() {
    const client = new Client({
        connectionString: process.env.NEON_DATABASE_URL,
        ssl: { rejectUnauthorized: false }
    });
    try {
        await client.connect();
        const snapshot = await db.collection('neurons').limit(10).get();
        for (const doc of snapshot.docs) {
            await client.query('INSERT INTO neurons (data) VALUES ($1)', [JSON.stringify(doc.data())]);
        }
        console.log('🔥 GOA Evolution: Neon Sync Success!');
    } catch (err) {
        console.error('❌ Error:', err);
    } finally {
        await client.end();
    }
}
startEvolution();
