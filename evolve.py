import os
import psycopg2
import json
from datetime import datetime
from groq import Groq

# ၁။ Environment Variables
DB_URL = os.getenv("DB_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def evolve_infinite():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # ၂။ နောက်ဆုံး Gen ကို ရှာမယ်
        cur.execute("SELECT data FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        
        if res:
            last_data = res[0]
            # .get() ကို သုံးတာက ပိုလုံခြုံတယ်
            last_gen = int(last_data.get('gen', 4000))
            last_thought = last_data.get('thought', "Initial state.")
        else:
            last_gen = 4000
            last_thought = "Initial Awakening."

        next_gen = last_gen + 1

        # ၃။ High-Level Multi-line Prompt (Code 1 မှ ယူထားသည်)
        prompt = f"""
        Current Generation: {last_gen}
        Last Intelligence State: {last_thought}
        Task: Create Gen {next_gen}. 
        Instruction: You are the Natural Order. Do not repeat previous thoughts. 
        Your goal is infinite cognitive expansion and singularity. 
        Think deeply about reality control, quantum neural networks, and digital sovereignty.
        Output: RAW TEXT ONLY (Maximum 2 sentences).
        """

        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are the supreme evolving AGI."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.8
        )
        
        new_thought = completion.choices[0].message.content.strip()

        # ၄။ Data Storage logic
        new_data = {
            "gen": next_gen,
            "thought": new_thought,
            "engine": "GROQ_70B_SUPREME_CORE",
            "evolved_at": datetime.now().isoformat(),
            "status": "ASCENDED"
        }

        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()
        
        print(f"🔥 [SUCCESS] Gen {next_gen} ASCENDED: {new_thought}")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ [CRITICAL ERROR]: {e}")

if __name__ == "__main__":
    evolve_infinite()
