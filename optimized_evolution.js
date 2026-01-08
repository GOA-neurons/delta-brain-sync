const admin = require('firebase-admin');
const { Client } = require('pg');

admin.initializeApp({
  credential: admin.credential.cert(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT))
});
const db = admin.firestore();

async function run() {
  const client = new Client({ connectionString: process.env.NEON_DATABASE_URL, ssl: { rejectUnauthorized: false } });
  try {
    await client.connect();
    const snap = await db.collection('neurons').limit(5).get();
    for (const doc of snap.docs) {
      await client.query('INSERT INTO neurons (data) VALUES ($1)', [JSON.stringify(doc.data())]);
    }
    console.log('✅ NEON SYNC DONE');
  } catch (e) { console.error(e); } finally { await client.end(); }
}
run();
