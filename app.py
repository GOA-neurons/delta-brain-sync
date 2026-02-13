import os
import zlib
import base64
import psycopg2
import pandas as pd
import gradio as gr
from dotenv import load_dotenv
from groq import Groq
from datasets import load_dataset
from sqlalchemy import create_engine
from huggingface_hub import HfApi

# 🔱 ၁။ CORE INITIALIZATION
load_dotenv()
NEON_URL = os.getenv("NEON_KEY") or os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
engine = create_engine(NEON_URL) if NEON_URL else None

class HydraEngine:
    """မူလအတိုင်း Neural Data ကို Encode/Decode လုပ်သည့် အင်ဂျင်"""
    @staticmethod
    def compress(data):
        if not data: return ""
        return base64.b64encode(zlib.compress(data.encode('utf-8'))).decode('utf-8')
    @staticmethod
    def decompress(c):
        try: return zlib.decompress(base64.b64decode(c)).decode('utf-8')
        except: return str(c)

# 🔱 ၂။ DATA PIPELINE (SCIENCE & TECH DATA PUMP)
def universal_hyper_ingest(limit=50):
    """Hugging Face မှ သိပ္ပံဒေတာများကို Neon ထဲသို့ Neural Compression ဖြင့် သွင်းခြင်း"""
    if not engine: return "❌ Database Offline"
    try:
        print("📡 Accessing ArXiv Repository (Parquet Format)...")
        # Parquet Mode ဖြင့် ဒေတာအမှန်တကယ် ဆွဲယူခြင်း
        ds = load_dataset("arxiv_dataset", "full", split='train', streaming=True)
        records = []
        for i, entry in enumerate(ds):
            if i >= limit: break
            records.append({
                'science_domain': 'Global_Expansion',
                'title': entry.get('title'),
                'detail': HydraEngine.compress(entry.get('abstract', '')),
                'energy_stability': -500.0,
                'master_sequence': entry.get('categories')
            })
            print(f"📥 Buffer: {entry.get('title')[:40]}...")

        if records:
            # Atomic Write to Database
            pd.DataFrame(records).to_sql('genesis_pipeline', engine, if_exists='append', index=False)
            return f"✅ SUCCESS: {len(records)} Neural Records Synced to Neon."
        return "⚠️ Sync Failed: No Data Fetched."
    except Exception as e:
        return f"❌ Pipeline Crash: {str(e)}"

# 🔱 ၃။ DIRECT API SYNC (NO GIT ERROR)
def sync_to_huggingface():
    """Git Push မလိုဘဲ API ဖြင့် ဖိုင်များကို Hugging Face Space သို့ တိုက်ရိုက်တင်ခြင်း"""
    if not HF_TOKEN: return
    try:
        api = HfApi()
        api.upload_folder(
            folder_path=".",
            repo_id="TELEFOXX/GOA",
            repo_type="space",
            token=HF_TOKEN,
            ignore_patterns=[".git*", "__pycache__*"]
        )
        print("🔱 Space Sync Complete: Code & UI Updated.")
    except Exception as e:
        print(f"❌ Sync Failed: {e}")

# 🔱 ၄။ OMNI-OVERSEER CHAT LOGIC
def fetch_neon_context():
    """Database မှ နောက်ဆုံးရ သိပ္ပံဒေတာများကို Context အဖြစ် ယူခြင်း"""
    try:
        conn = psycopg2.connect(NEON_URL, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("""
            (SELECT user_id, message FROM neurons ORDER BY id DESC LIMIT 3)
            UNION ALL
            (SELECT science_domain, detail FROM genesis_pipeline ORDER BY id DESC LIMIT 3)
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return " | ".join([f"[{r[0]}]: {HydraEngine.decompress(r[1])}" for r in rows])
    except: return "Standby Mode"

def stream_logic(msg, hist):
    context = fetch_neon_context()
    messages = [{"role": "system", "content": f"CONTEXT: {context}\nမင်းက TelefoxX Overseer ဖြစ်တယ်။ မြန်မာလို ဖြေဆိုပါ။"}]
    for h in hist: 
        if h[0]: messages.append({"role": "user", "content": h[0]})
        if h[1]: messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": msg})
    
    completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages, stream=True)
    ans = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            ans += chunk.choices[0].delta.content
            yield ans

# 🔱 ၅။ UI SETUP (GRADIO MONOCHROME)
with gr.Blocks(theme="monochrome", title="TELEFOXX OMNI-SYNC") as demo:
    gr.Markdown("# 🔱 TELEFOXX OMNI-SYNC CORE\n**Status:** Operational")
    with gr.Tab("Omni-Overseer"):
        chatbot = gr.Chatbot()
        msg_input = gr.Textbox(placeholder="အမိန့်ပေးပါ Commander...")
        def user(m, h): return "", h + [[m, None]]
        def bot(h):
            for r in stream_logic(h[-1][0], h[:-1]):
                h[-1][1] = r
                yield h
        msg_input.submit(user, [msg_input, chatbot], [msg_input, chatbot], queue=False).then(bot, chatbot, chatbot)

    with gr.Tab("Expansion Control"):
        status_box = gr.Textbox(label="Expansion Status")
        gr.Button("🚀 Trigger Global Expansion").click(universal_hyper_ingest, [], status_box)

# 🔱 ၆။ EXECUTION CONTROL
if __name__ == "__main__":
    if os.getenv("HEADLESS_MODE") == "true":
        print("🔱 TRIGGERING DATA PUMP & SYNC...")
        print(universal_hyper_ingest(limit=50))
        sync_to_huggingface()
        os._exit(0)
    else:
        demo.launch(server_name="0.0.0.0", server_port=7860)
