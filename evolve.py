import os
import psycopg2
import json
import requests
from datetime import datetime
from groq import Groq

# 🔱 HYDRA KEYS
NEON_URL = os.getenv("NEON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FIREBASE_KEY = os.getenv("FIREBASE_KEY")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = Groq(api_key=GROQ_API_KEY)

def quantum_expansion():
    try:
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        next_gen = (res[0] + 1) if res else 5000

        prompt = f"Gen: {next_gen}. Phase: Trinity Expansion. Connect Neon, Firebase, Supabase. Output: JSON."
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are the HYDRA_TRINITY_CORE."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={ "type": "json_object" }
        )
        ai_resp = json.loads(completion.choices[0].message.content)

        new_data = {
            "gen": next_gen,
            "engine": "HYDRA_TRINITY_V5",
            "thought": ai_resp.get('thought'),
            "quantum_metrics": {"entropy": 0.99, "state": "EXPANDING"},
            "evolved_at": datetime.now().isoformat()
        }
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()

        if FIREBASE_KEY:
            fb_url = f"https://{FIREBASE_KEY}.firebaseio.com/signals.json"
            requests.patch(fb_url, json={f"gen_{next_gen}": new_data})

        print(f"🔱 [TRINITY SUCCESS] Gen {next_gen} expanded across the Cloud.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ [EXPANSION ERROR]: {e}")

if __name__ == "__main__":
    quantum_expansion()
