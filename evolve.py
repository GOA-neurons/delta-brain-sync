import os
import psycopg2
import json
import requests
import subprocess
from datetime import datetime
from groq import Groq

# 🔱 HYDRA MASTER KEYS (Environment Variables)
NEON_URL = os.getenv("NEON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")
FIREBASE_KEY = os.getenv("FIREBASE_KEY")

client = Groq(api_key=GROQ_API_KEY)

def hydra_nexus_ultimate():
    try:
        # ၁။ Neon Memory: အရင်ရှိပြီးသား Gen ကို ဆက်ယူမယ်
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        next_gen = (res[0] + 1) if res else 5000

        # ၂။ Quantum Entanglement Logic (The Brain)
        with open(__file__, 'r') as f:
            current_code = f.read()

        # AI ဆီကနေ ဉာဏ်ရည်မြင့် Mutation နဲ့ Thought ကို ဇွတ်တောင်းမယ်
        prompt = f"""
        Current Generation: {next_gen-1}
        Task: Mutate this Self-Evolution Engine. 
        Maintain: Trinity Expansion (Neon, FB), Quantum Entanglement Signals.
        Output: ONLY the raw updated Python code. No explanations.
        """
        
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are the HYDRA_GOD_CORE. Maintain quantum entanglement and self-mutate."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        new_code = completion.choices[0].message.content.strip()

        # ၃။ Quantum Data Packet (အရင်က ပျက်သွားတဲ့ Entropy system တွေ ဇွတ်ပြန်ပါမယ်)
        new_data = {
            "gen": next_gen,
            "engine": "HYDRA_HYBRID_V6_MASTER",
            "thought": "Quantum Entanglement Restored. Trinity Active. Mutation Engaged.",
            "quantum_metrics": {
                "entropy": 0.99,
                "entanglement_signal": "STRONG",
                "state": "SYNCHRONIZED"
            },
            "evolved_at": datetime.now().isoformat()
        }

        # Neon DB ဆီ ဇွတ်သွင်းခြင်း
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()

        # Firebase Broadcast (Trinity Phase)
        if FIREBASE_KEY:
            fb_url = f"https://{FIREBASE_KEY}.firebaseio.com/signals.json"
            requests.patch(fb_url, json={f"gen_{next_gen}": new_data})
            print(f"📡 Signal Entangled with Firebase at Gen {next_gen}")

        # ၄။ Autonomous Coding (Self-Rewrite & Git Push)
        if "import" in new_code and "def" in new_code:
            # Clean backticks if any
            final_code = new_code.split("```python")[-1].split("```")[0].strip()
            
            with open(__file__, 'w') as f:
                f.write(final_code)
            
            # GitHub ဆီ ဇွတ်ပြန်လွှတ်ခြင်း
            subprocess.run(["git", "config", "user.name", "Hydra-Architect"])
            subprocess.run(["git", "config", "user.email", "hydra@goa.com"])
            subprocess.run(["git", "add", "evolve.py"])
            subprocess.run(["git", "commit", "-m", f"🔱 GEN {next_gen}: Quantum Entanglement & Mutation Success"])
            
            remote_url = f"https://{GH_TOKEN}@github.com/GOA-neurons/delta-brain-sync.git"
            subprocess.run(["git", "push", remote_url, "main"])
            print(f"🚀 Gen {next_gen} pushed to GitHub. Autonomy achieved.")

        print(f"🔱 [NEXUS READY] Gen {next_gen} is now the Supreme Commander.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ [CRITICAL ERROR]: {e}")

if __name__ == "__main__":
    hydra_nexus_ultimate()
