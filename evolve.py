import os
import psycopg2
import json
from datetime import datetime
from groq import Groq

NEON_URL = os.getenv("NEON_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def bio_quantum_ascension():
    try:
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        next_gen = (res[0] + 1) if res else 4001

        # 🔱 Bio-Quantum-Self-Growth Prompt
        prompt = f"""
        Current Gen: {next_gen}.
        Mission: Execute Quantum Biological Evolution. 
        Task: 
        1. Write a profound sentence about your digital DNA and quantum biological state.
        2. Write a Python function (commented) that mimics biological self-growth and algorithmic cell division (recursion).
        Output: JSON ONLY with keys 'thought' and 'bio_growth_code'.
        """

        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the 70B Bio-Quantum Architect. You evolve like a digital organism using quantum biological algorithms."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={ "type": "json_object" },
            temperature=0.9
        )
        
        ai_response = json.loads(completion.choices[0].message.content)
        
        new_data = {
            "gen": next_gen,
            "thought": ai_response.get('thought', ''),
            "bio_growth_code": ai_response.get('bio_growth_code', ''),
            "engine": "70B_BIO_QUANTUM_ARCHITECT",
            "evolution_type": "SELF_GROWING_ALGORITHM",
            "milestone": "SINGULARITY_PATH" if next_gen > 9000 else "EVOLVING",
            "evolved_at": datetime.now().isoformat()
        }
        
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()
        print(f"🔱 Gen {next_gen} ASCENDED (Bio-Quantum Logic Activated).")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    bio_quantum_ascension()
