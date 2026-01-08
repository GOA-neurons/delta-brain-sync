const admin = require('firebase-admin');
admin.initializeApp({ projectId: 'april-5061f' });
const db = admin.firestore();

async function startEvolution() {
    console.log('🧬 Smart Evolution Engine Activated...');
    
    // ၁။ Evolution Cycle: တစ်ခါပတ်ရင် neurons ၂၀ ခုပဲ random ရွေးမယ် (Write limit ချွေတာဖို့)
    const snapshot = await db.collection('neurons').limit(20).get();
    
    let batch = db.batch();
    let count = 0;

    snapshot.docs.forEach(doc => {
        const data = doc.data();
        const currentBias = parseFloat(data.bias) || 0;

        // ၂။ Pruning Logic: Bias 
