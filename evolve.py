import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2

def main():
    try:
        print("🚀 Starting Evolution (Python Mode)...")
        raw_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        service_account_info = json.loads(raw_json, strict=False)
        
        cred = credentials.Certificate(service_account_info)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Connected!")

        conn = psycopg2.connect(os.environ.get('NEON_DATABASE_URL'))
        print("✅ Neon Connected!")
        print("🏁 MISSION ACCOMPLISHED!")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    main()
  
