import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2
import requests
import time
import random

# --- ⚙️ CONFIGURATION (RECALLED SECRETS) ---
NEON_URL = "postgresql://neondb_owner:npg_QUqg12MzNxnI@ep-long-sound-ahsjjrnk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
SUPABASE_URL = "https://qwnmnzukxozmevforxva.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3bm1uenVreG96bWV2Zm9yeHZhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzQ0MjQ4MCwiZXhwIjoyMDgzMDE4NDgwfQ.Wk2oULsXE5ZHize0t5Jf_UvybaFN-caODA15i1_GpBc"

# Firebase Private Key Formatting (ခုနက Error မတက်အောင် ဇွတ်ပြင်ထားတယ်)
clean_private_key = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQClPqbuI2bmqOZn\n"
    "kZdHP/hIBAmgyO7Bgr8xL/dOAYvj7iWF/ndUHQYTnRml31n+y/+wmgSRxi9v1+j9\n"
    "d0+4d/ynsyTpGneWcy3HqahPMQp3fmg+2yKv+RYGVyOuCiM4xXhkHajySQiyuIUB\n"
    "VCzdiB4qYksB1wRZbL65uPD0yaMa6E5XKOfM7YaEjthRkHP/xLFE41ICcLcKPoPC\n"
    "f8PZe9DSYgyIxKHCO+LVWOPOp/elboeowcu8QtWzeKjyrUbLvMA1q92mfMJmHSdI\n"
    "Vg/oXPKzheTSjgO+VOfF221dtUOqWkzLa5eABTHQA13ONPvDVEgQ97RvjIhc0Wko\n"
    "IKEVK0bLAgMBAAECggEADcaQ1QZ3hCAtgRHWmjZ/hMVtZg2KNfCn7rpQdBzV5C0M\n"
    "zMRff1AiGw18P2NE1eR8zuSwH9T1TG4j+slxCHBcTEC3gYVW1eCJPv1qThvJAxgz\n"
    "KZZMKH5r8yBdlZs7v3Za6IG+fWBQTNHsKKWzTc6UsTTbiu45axkRN1tvHwEWS15T\n"
    "Km6dAJbW1vlSm28nZEKiy9WRu/o7CEK+i+bYsVGz9nsAp3bfHCuOj9+QoOPBSSZ/\n"
    "9foCbN8kHoz8WLG3DRn+jNPPtqhaBXL4rGgVIyAIeG7R0T4Jr3WD6oCeO2ZfaJpK\n"
    "pKf26zg7G4qahqb12Bwz2tarigZuhNm7zcwA5/BC0QKBgQDO+oXvRvF0qGbW9Mb/\n"
    "FU9LR73Nt0tLDoTc4cJSHUOgL5SF6M+l8IxfxsP3mwbhvvk+914TLpgVMkB72xHI\n"
    "mMAeTh3e6LlnVJ+OtK9TX3p3t0AbSaIk7D3ykq1nYr7Ns/2esW53Vi70tdnwA0La\n"
    "2cvwE9HVOI79krvQFdoYYOEJ8QKBgQDMYbsa3BE6kEPDkfrr+2VY8NRhthj7IUqE\n"
    "ensdVs2+EDzTtIaWI4MyxZLQZP94NZvRcciJfd+PP+uMG8xUS3GaNHnYTAofu+hg\n"
    "QtXfON6QPIXICFSrC2K7AOC5BJA6pK6S1WLM8BRO3xbk3chhMihoJwNSMPiAxbcC\n"
    "0ytBCkOAewKBgQCYxkZSJbVX/G1cQPUZl6sdz+iDjcXfsunS+Disz7j45eXlKcEL\n"
    "pRCYKWjAvQdJXeMv3Prtgbjz/FGomjz4Kfe05sgZnwIrCUV02l2HVrRY5URGYAV0\n"
    "54OaJzYjV7mqsC6GEkWNhGnIaupgxKd2Tsi/foGltsek18gVgeunjurMoQKBgQDH\n"
    "WfxaspTLfrPaKqWJT+kG28EMncW4DjzVA3LapzR/Uu9BwDAWegUanMQbKKhW5FNb\n"
    "85QbJ//LhhmGzAZ9oijotI60f1bQpUR/wDFETgAoyB/lgNq1C6H9rVmEngLgcIkn\n"
    "B6QbKYFlfQyjqAAvbfEjxgnjPYjmcfOUec0S36P/yQKBgQCjmM5CNTaOxKMrWpkY\n"
    "Q0v1UKXqGoXNBLdUZDEIAAZtJlmV2kTvpY9bTQRbNCSSi0QScUO0TiYCeXLxqcy4\n"
    "M5racd5edE0D4xkfB0JyNP9HMda55/IHrf3HgI/6mhsN9Or1aDILitdhPLz4YHpU\n"
    "EFQXnDFmI44M2LF0c9vKlPzmGg==\n"
    "-----END PRIVATE KEY-----\n"
)

FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "april-5061f",
    "private_key": clean_private_key,
    "client_email": "firebase-adminsdk-fbsvc@april-5061f.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}

def start_evolution():
    print("🔋 ENGINE STARTING: SELF-EVOLUTION MODE ON")
    try:
        # 1. Neon: Fetch Latest Gen
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("SELECT (data->>'gen')::int, (data->>'bias')::float FROM neurons ORDER BY evolved_at DESC LIMIT 1;")
        row = cur.fetchone()
        
        if not row:
            print("⚠️ Table empty. Initializing Gen 1...")
            current_gen, current_bias = 0, 0.1
        else:
            current_gen, current_bias = row[0], row[1]

        print(f"📡 Current State: Gen {current_gen} | Bias {current_bias}")

        # 2. Firebase: Sync Current State
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CONFIG)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        db.collection('evolution_stats').document('latest').set({
            'gen': current_gen,
            'bias': current_bias,
            'last_sync': firestore.SERVER_TIMESTAMP
        }, merge=True)
        print("✅ Firebase: Synced.")

        # 3. Mutation: Generate NEW Generation (ဒါက Self-Evolving အသက်ပဲ)
        next_gen = current_gen + 1
        # Bias ကို အနည်းငယ် ပြောင်းလဲမယ် (Mutation)
        mutation_factor = random.uniform(-0.01, 0.01)
        next_bias = round(current_bias + mutation_factor, 4)

        print(f"🧬 Mutating: Creating Gen {next_gen} with Bias {next_bias}...")
        
        # Neon ထဲကို Gen အသစ် ဇွတ်သွင်းမယ်
        cur.execute("""
            INSERT INTO neurons (data, evolved_at) 
            VALUES (%s, NOW());
        """, [json.dumps({"gen": next_gen, "bias": next_bias})])
        conn.commit()
        
        # 4. Supabase: Log the Evolution
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}
        payload = {"gen": next_gen, "bias": next_bias, "status": "EVOLVED"}
        requests.post(f"{SUPABASE_URL}/rest/v1/evolution_logs", headers=headers, json=payload)

        print(f"🏁 DONE: Gen {next_gen} is now in Database. Loop Ready for next run!")

    except Exception as e:
        print(f"☢️ CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    start_evolution()
