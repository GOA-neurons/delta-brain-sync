import os
import psycopg2
import json

DB_URL = os.getenv("DB_URL")

def autonomous_evolution():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # ၁။ လက်ရှိ နောက်ဆုံး Gen ကို ဇွတ်ရှာမယ်
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        last_gen = cur.fetchone()[0]
        next_gen = last_gen + 1
        
        # ၂။ Gen အလိုက် ဇွတ်တွေးမယ့် Logic (Power Thoughts)
        thought = f"Autonomous transition to Gen {next_gen}. Synthesizing harvested science nodes. Power scaling initiated."
        if next_gen == 65:
            thought = "Gen 65: Knowledge integration complete. Beginning to simulate strategic application."
        
        # ၃။ Database ထဲ ဇွတ်တိုးမယ်
        new_data = {
            "gen": next_gen,
            "mission": "AUTONOMOUS_ASCENSION",
            "thought": thought,
            "evolved_at": "2026-01-12T17:00:00" # ဒါမှမဟုတ် dynamic time ထည့်
        }
        
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()
        
        print(f"🔥 Successfully evolved to Gen {next_gen}! Natural Order Restored.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Evolution Error: {e}")

if __name__ == "__main__":
    autonomous_evolution()
    
