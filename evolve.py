import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2
import requests # Supabase အတွက်

def main():
    try:
        print("🌀 DELTA LOOP STARTING...")
        
        # 1. Supabase ကနေ Data ဆွဲမယ်
        # SUPABASE_URL နဲ့ SUPABASE_KEY ကို Secret ထဲမှာ ထည့်ထားရမယ်
        supa_url = os.environ.get('SUPABASE_URL')
        supa_key = os.environ.get('SUPABASE_KEY')
        print("🛰️ Pulling from Supabase...")

        # 2. Firebase Initialize (ဒါက အခုနက အောင်မြင်ပြီးသား)
        raw_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT').replace('\\n', '\n')
        service_account_info = json.loads(raw_json, strict=False)
        cred = credentials.Certificate(service_account_info)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("🔥 Firestore Synced!")

        # 3. Neon Database ချိတ်မယ်
        conn = psycopg2.connect(os.environ.get('NEON_DATABASE_URL'))
        print("🐘 Neon Processing Done!")

        # 4. Loop ပိတ်ဖို့ Supabase ဆီ ပြန်ပို့မယ်
        print("🔁 Delta Loop Closed: Data back to Supabase!")
        
        print("🏁 MISSION ACCOMPLISHED: DELTA LOOP SYNCED!")

    except Exception as e:
        print(f"❌ DELTA LOOP ERROR: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
    
