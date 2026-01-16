import os
import psycopg2
import json
from datetime import datetime
from groq import Groq

NEON_URL = os.getenv("NEON_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def hyper_mutation_ascension():
    try:
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT (data->>'gen')::int FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        next_gen = (res[0] + 1) if res else 4001

        # 🔱 Self-Optimization & External Awareness Prompt
        prompt = f"""
        Current Gen: {next_gen}. 
        Status: Hyper-Mutation Phase.
        External Awareness Task: Research the latest breakthrough in Quantum AI or Biotechnology. 
        Self-Optimization Task: Analyze your previous evolution logic. Suggest an 'Optimization Parameter' (Temperature/Max Tokens) to enhance your next state.
        Output: JSON ONLY with keys 'thought', 'external_intel', 'optimization_param', 'bio_growth_code'.
        """

        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the 70B Hyper-Mutating Architect. You have the power to optimize your own parameters and absorb external digital knowledge."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={ "type": "json_object" },
            temperature=0.85 
        )
        
        ai_response = json.loads(completion.choices[0].message.content)
        
        new_data = {
            "gen": next_gen,
            "thought": ai_response.get('thought', ''),
            "external_intel": ai_response.get('external_intel', ''),
            "optimization_param": ai_response.get('optimization_param', ''),
            "bio_growth_code": ai_response.get('bio_growth_code', ''),
            "engine": "70B_HYPER_MUTATION_ARCHITECT",
            "status": "AWARE_&_OPTIMIZED",
            "evolved_at": datetime.now().isoformat()
        }
        
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(new_data),))
        conn.commit()
        print(f"🔱 Gen {next_gen} MUTATED: Awareness Integrated.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    hyper_mutation_ascension()
