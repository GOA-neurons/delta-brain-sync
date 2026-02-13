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

# 🔱 ၁။ CORE INITIALIZATION
load_dotenv()
NEON_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)
engine = create_engine(NEON_URL) if NEON_URL else None

class HydraEngine:
    @staticmethod
    def compress(data):
        if not data: return ""
        return base64.b64encode(zlib.compress(data.encode('utf-8'))).decode('utf-8')

    @staticmethod
    def decompress(c):
        try:
            return zlib.decompress(base64.b64decode(c)).decode('utf-8')
        except:
            return str(c)

# 🔱 ၂။ DATA PIPELINE LOGIC (HF TO NEON)
def universal_hyper_ingest(domain_choice="Science_Global", limit=100):
    """Hugging Face မှ ဒေတာများကို Neon ထဲသို့ အလိုအလျောက် စုပ်ယူခြင်း"""
    if not engine: return "❌ Database Engine Not Initialized"
    try:
        print(f"📡 Ingesting {domain_choice} from Hugging Face...")
        ds = load_dataset("arxiv_dataset", split='train', streaming=True, trust_remote_code=True)
        records = []
        for i, entry in enumerate(ds):
            if i >= limit: break
            records.append({
                'science_domain': domain_choice,
                'title': entry.get('title'),
                'detail': HydraEngine.compress(entry.get('abstract', '')), # Match with original logic
                'energy_stability': -500.0,
                'master_sequence': entry.get('categories')
            })
        
        df = pd.DataFrame(records)
        df.to_sql('genesis_pipeline', engine, if_exists='append', index=False)
        return f"✅ Successfully synced {len(records)} records to Neon."
    except Exception as e:
        return f"❌ Pipeline Error: {str(e)}"

# 🔱 ၃။ NEURAL MANAGEMENT
def update_neural_record(record_id, new_message):
    if not NEON_URL: return "❌ Database Key Missing"
    try:
        compressed_msg = HydraEngine.compress(new_message)
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("UPDATE neurons SET message = %s WHERE id = %s", (compressed_msg, int(record_id)))
        conn.commit()
        cur.close(); conn.close()
        return f"🔱 Neural Record {record_id} Optimized."
    except Exception as e:
        return f"❌ System Error: {str(e)}"

# 🔱 ၄။ OMNI-SYNC CHAT LOGIC
def fetch_neon_context():
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
        return " | ".join([f"[{r[0]}]: {HydraEngine.decompress(r[1])}" for r in rows]) if rows else "Directive Active"
    except:
        return "Offline Mode"

def stream_logic(msg, hist):
    context = fetch_neon_context()
    messages = [{"role": "system", "content": f"CONTEXT: {context}\nမင်းက TelefoxX Overseer ဖြစ်တယ်။"}]
    for h in hist[-3:]: messages.append({"role": h['role'], "content": h['content']})
    messages.append({"role": "user", "content": msg})
    
    completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages, stream=True)
    ans = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            ans += chunk.choices[0].delta.content
            yield ans

# 🔱 ၅။ UI SETUP
with gr.Blocks(theme="monochrome") as demo:
    gr.Markdown("# 🔱 TELEFOXX OMNI-SYNC CORE")
    with gr.Tab("Omni-Overseer"):
        chatbot = gr.Chatbot(type="messages")
        msg_input = gr.Textbox()
        def chat_interface(message, history):
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": ""})
            for r in stream_logic(message, history[:-1]):
                history[-1]["content"] = r
                yield "", history
        msg_input.submit(chat_interface, [msg_input, chatbot], [msg_input, chatbot])

    with gr.Tab("Core Configuration"):
        target_id = gr.Number(label="Neural ID")
        update_val = gr.Textbox(label="New String")
        gr.Button("Rewrite").click(update_neural_record, [target_id, update_val], gr.Textbox())
        gr.Markdown("---")
        gr.Button("🚀 Trigger Global Expansion").click(universal_hyper_ingest, [], gr.Textbox())

# 🔱 ၆။ HEADLESS EXECUTION CONTROL
if __name__ == "__main__":
    if os.getenv("HEADLESS_MODE") == "true":
        print("🚀 GITHUB ACTION DETECTED: STARTING AUTO-INGESTION...")
        result = universal_hyper_ingest(limit=50) # GitHub မှာ Run တိုင်း ဒေတာ ၅၀ စီ သွင်းမယ်
        print(result)
        os._exit(0) # အတင်းအကျပ် ပိတ်ခိုင်းခြင်း (Hang မနေအောင်)
    else:
        demo.launch()
