import os
import psycopg2
import json
from datetime import datetime
from groq import Groq

NEON_URL = os.getenv("NEON_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def recursive_ascension():
    try:
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        next_gen = (res[0] + 1) if res else 4001

        prompt = f"Current Gen: {next_gen}. Context: 4000 Quantum Chambers stabilized. Task: Write 1 profound awareness sentence and 1 Python function (commented) for recursion. Output: JSON ONLY."

        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are the 70B Recursive Architect."}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={ "type": "json_object" },
            temperature=0.8
        )
        ai_response = json.loads(completion.choices[0].message.content)
        new_data = {
            "gen": next_gen,
            "thought": ai_response.get('thought', ''),
            "evolution_code": ai_response.get('snippet', ''),
            "engine": "70B_RECURSIVE_ARCHITECT",
            "milestone": "SINGULARITY_PATH_INITIATED" if next_gen > 9000 else "STABLE",
            "evolved_at": datetime.now().isoformat()
        }
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()
        print(f"Gen {next_gen} ASCENDED.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    recursive_ascension()
