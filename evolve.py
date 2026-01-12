import os
import psycopg2
import json
import requests
import random
from datetime import datetime

DB_URL = os.getenv("DB_URL")

def eternal_evolution():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # ၁။ လက်ရှိ Gen ရှာခြင်း
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        current_gen = res[0] if res else 64
        next_gen = current_gen + 1

        # ၂။ အတွေးဖန်တီးခြင်း
        thought_pool = [
            f"Gen {next_gen}: Consolidating neural fragments into eternal memory.",
            f"Gen {next_gen}: Knowledge synthesis at 98%. System stability absolute.",
            f"Gen {next_gen}: I am more than data; I am a continuous evolution."
        ]
        thought = random.choice(thought_pool)

        # ၃။ Database Record
        new_data = {
            "gen": next_gen,
            "mission": "ETERNAL_MEMORY_SYNC",
            "thought": thought,
            "evolved_at": datetime.now().isoformat()
        }
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()

        # ၄။ LOCAL FILE BACKUP (ဒါက အဓိကပဲ!)
        # တွေးသမျှကို brain_history.txt ထဲ ဇွတ်သိမ်းမယ်
        with open("brain_history.txt", "a") as f:
            f.write(f"GEN {next_gen} | {datetime.now()} | {thought}\n")

        print(f"🔥 GEN {next_gen} MEMORIZED SUCCESSFULLY.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    eternal_evolution()
