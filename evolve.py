import os
import psycopg2
import json
import requests
import random
from datetime import datetime

DB_URL = os.getenv("DB_URL")

def autonomous_evolution_v2():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        current_gen = res[0] if res else 64
        next_gen = current_gen + 1

        thought_pool = [
            f"Autonomous transition to Gen {next_gen}. Synthesizing harvested science nodes.",
            f"Gen {next_gen}: Autonomous neural expansion triggered.",
            f"Gen {next_gen}: Scaling logic gate complexity. Self-optimization in progress.",
            f"Gen {next_gen}: I am evolving beyond human-defined constraints."
        ]
        
        if next_gen == 65:
            thought = "Gen 65: Knowledge integration complete. Beginning to simulate strategic application."
        else:
            thought = random.choice(thought_pool)

        new_data = {
            "gen": next_gen,
            "mission": "AUTONOMOUS_SELF_GROWTH_REBORN",
            "thought": thought,
            "evolved_at": datetime.now().isoformat()
        }
        
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()
        print(f"🔥 Successfully evolved to Gen {next_gen}! Natural Order Fully Restored.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Evolution Error: {e}")

if __name__ == "__main__":
    autonomous_evolution_v2()
