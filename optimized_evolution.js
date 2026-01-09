// optimized_evolution.js ထဲမှာ ဒါကို သေချာလဲပါ
const query = 'INSERT INTO neurons (data, evolved_at) VALUES ($1, NOW())';
await client.query(query, [JSON.stringify(doc.data())]);
