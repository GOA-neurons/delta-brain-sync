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

        // ၂။ Pruning Logic: Bias အရမ်းနည်းရင် ဖျက်ပစ်မယ်
        if (currentBias < 0.1 && snapshot.size > 1000) {
            batch.delete(doc.ref);
            console.log(`🗑️ Pruned weak neuron: ${doc.id}`);
        } else {
            // ၃။ Mutation Logic: Bias ကို ဇွတ်ပြောင်းမယ်
            const mutation = (Math.random() - 0.5) * 0.1;
            const newBias = Math.max(0, Math.min(1, currentBias + mutation)).toFixed(4);
            
            batch.update(doc.ref, {
                bias: newBias,
                last_evolved: admin.firestore.FieldValue.serverTimestamp(),
                gen: (data.gen || 0) + 1
            });
            count++;
        }
    });

    // ၄။ Growth Logic: ဆင့်ကဲဖြစ်စဉ်အတွက် neuron သစ် တစ်ခုပဲ ထည့်မယ်
    const newRef = db.collection('neurons').doc();
    batch.set(newRef, {
        bias: Math.random().toFixed(4),
        type: 'Smart_Growth',
        gen: 1,
        created_at: admin.firestore.FieldValue.serverTimestamp()
    });

    await batch.commit();
    console.log(`🔥 Evolution Step: ${count} neurons mutated. Brain is stable.`);
}

// ၅ မိနစ်တစ်ခါပဲ Run မယ် (24 နာရီလုံး Run ရင်တောင် Daily Write Limit မကျော်ဘူး)
setInterval(startEvolution, 300000); 
startEvolution();
