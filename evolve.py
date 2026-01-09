import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2

def main():
    try:
        print("🚀 Starting Evolution...")
        
        # GitHub Secret ကနေ FIREBASE_KEY ကို ယူမယ်
        raw_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        
        if not raw_json:
            print("❌ Error: FIREBASE_SERVICE_ACCOUNT secret is missing!")
            return

        # 🔥 Escape Character ပြဿနာကို ရှင်းဖို့ raw string အနေနဲ့ 处理 လုပ်မယ်
        try:
            # JSON ထဲမှာ \n တွေပါရင် ဇွတ်ပြင်မယ်
            fixed_json = raw_json.replace('\\n', '\n')
            service_account_info = json.loads(fixed_json)
        except Exception as json_err:
            print(f"⚠️ JSON Normal Parse Failed, trying raw: {json_err}")
            service_account_info = json.loads(raw_json, strict=False)
        
        # Firebase Initialize
        cred = credentials.Certificate(service_account_info)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Connected!")

        # Neon Database Connection
        neon_url = os.environ.get('NEON_DATABASE_URL')
        conn = psycopg2.connect(neon_url)
        print("✅ Neon Connected!")
        
        print("🏁 MISSION ACCOMPLISHED!")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
    
