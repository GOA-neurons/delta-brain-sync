import os
import psycopg2
import json
from datetime import datetime
from groq import Groq

# 🔱 HYDRA KEYS MAPPING
NEON_URL = os.getenv("NEON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
FIREBASE_KEY = os.getenv("FIREBASE_KEY")

client = Groq(api_key=GROQ_API_KEY)

def quantum_biological_evolution():
    try:
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        next_gen = (res[0] + 1) if res else 4122

        prompt = f"Gen: {next_gen}. Phase: Quantum Biological Entanglement. Core: Hybrid Neuron Signal Systems. Output: JSON."

        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the HYDRA_QUANTUM_ARCHITECT."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={ "type": "json_object" }
        )
        
        ai_response = json.loads(completion.choices[0].message.content)

        new_data = {
            "gen": next_gen,
            "engine": "HYDRA_QUANTUM_CORE_V4",
            "status": "ENTANGLED_AND_ACTIVE",
            "quantum_metrics": {
                "entropy": ai_response.get('quantum_entropy', 0.99),
                "state": "SUPERPOSITION"
            },
            "thought": ai_response.get('thought'),
            "evolved_at": datetime.now().isoformat()
        }

        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()
        print(f"🔱 [QUANTUM SUCCESS] Gen {next_gen} Synchronized.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ [QUANTUM COLLAPSE]: {e}")

if __name__ == "__main__":
    quantum_biological_evolution()
