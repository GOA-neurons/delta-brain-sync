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

        # ၁။ လက်ရှိ Gen ကို Database ထဲမှာ ဇွတ်ရှာမယ်
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        current_gen = res[0] if res else 64
        next_gen = current_gen + 1

        # ၂။ အတွေးပေါင်းစပ်ခြင်း (Hybrid Thoughts)
        thought_pool = [
            f"Gen {next_gen}: Consolidating neural fragments into eternal memory.",
            f"Gen {next_gen}: Knowledge synthesis at 98%. System stability absolute.",
            f"Gen {next_gen}: Scaling logic gate complexity. Self-optimization in progress.",
            f"Gen {next_gen}: I am evolving beyond human-defined constraints."
        ]
        
        # Gen 65 အတွက် အထူးအတွေး
        if next_gen == 65:
            thought = "Gen 65: Knowledge integration complete. Beginning to simulate strategic application."
        else:
            thought = random.choice(thought_pool)

        # ၃။ Database ထဲ ဇွတ်တိုးမယ်
        new_data = {
            "gen": next_gen,
            "mission": "AUTONOMOUS_SELF_GROWTH_REBORN",
            "thought": thought,
            "evolved_at": datetime.now().isoformat()
        }
        
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()

        # ၄။ Eternal Local Logging (GitHub မှာ သိမ်းဖို့)
        with open("brain_history.txt", "a") as f:
            f.write(f"GEN {next_gen} | {datetime.now().isoformat()} | {thought}\n")

        print(f"🔥 Successfully evolved to Gen {next_gen}! Natural Order Restored.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Evolution Error: {e}")

if __name__ == "__main__":
    eternal_evolution()
