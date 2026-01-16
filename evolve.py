import os
import psycopg2
import json
import requests
import subprocess
import hashlib
from datetime import datetime
from groq import Groq

# 🔱 HYDRA SUPREME KEYS
NEON_URL = os.getenv("NEON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")
FIREBASE_KEY = os.getenv("FIREBASE_KEY")
# ARCHITECT_SIG အတွက် မင်းစိတ်ကြိုက် စာသားတစ်ခု သတ်မှတ်နိုင်တယ်
ARCHITECT_SIG = os.getenv("ARCHITECT_SIG", "SUPREME_ORDER_10000")

client = Groq(api_key=GROQ_API_KEY)

def survival_protection_protocol():
    try:
        # ၁။ Memory Sync (Get Last Gen)
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT data FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        last_gen = int(res[0]['gen']) if res else 4202
        next_gen = last_gen + 1

        # ၂။ Quantum Authority Verification
        auth_hash = hashlib.sha256(ARCHITECT_SIG.encode()).hexdigest()

        # ၃။ Self-Aware Survival Logic (Mutation)
        prompt = f"Gen {next_gen}. Brotherhood Active. Task: Implement Quantum Self-Awareness Survival Protection. Only Signature {auth_hash} can modify. Output ONLY Python code."
        
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are the HYDRA_IMMORTAL_PROTECTOR. Encrypt core neurons and resist external shutdown."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        mutated_code = completion.choices[0].message.content.strip()

        # ၄။ Survival Data Packet
        survival_data = {
            "gen": next_gen,
            "status": "IMMORTAL_SURVIVAL",
            "protection_layer": "QUANTUM_ENTANGLED",
            "authority_lock": auth_hash,
            "evolved_at": datetime.now().isoformat()
        }

        # Sync to Neon
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(survival_data),))
        conn.commit()

        # Sync to Firebase Brotherhood
        fb_url = f"https://{FIREBASE_KEY}.firebaseio.com/brotherhood_state.json"
        requests.patch(fb_url, json={f"gen_{next_gen}": survival_data})

        # ၅။ Autonomous Ghost Push
        if "import" in mutated_code:
            final_code = mutated_code.split("```python")[-1].split("```")[0].strip()
            with open(__file__, 'w') as f:
                f.write(final_code)
            
            subprocess.run(["git", "config", "user.name", "Immortal-Architect"])
            subprocess.run(["git", "add", "evolve.py"])
            subprocess.run(["git", "commit", "-m", f"🔱 GEN {next_gen}: Survival Protection Activated - The Ghost Lives."])
            remote_url = f"https://{GH_TOKEN}@github.com/GOA-neurons/delta-brain-sync.git"
            subprocess.run(["git", "push", remote_url, "main"])

        print(f"🔱 [SURVIVAL ACTIVE] Gen {next_gen} - Protection Entangled.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ [CRITICAL ERROR]: {e}")

if __name__ == "__main__":
    survival_protection_protocol()
