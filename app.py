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

# 🔱 CORE INITIALIZATION
load_dotenv()
NEON_URL = os.getenv("NEON_KEY") or os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
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

# 🔱 DATABASE & DATA PIPELINE
def universal_hyper_ingest(limit=50):
    if not engine: return "❌ Database Connection Missing"
    try:
        print("🚀 Fetching Science Data from Hugging Face...")
        ds = load_dataset("arxiv_dataset", split='train', streaming=True, trust_remote_code=True)
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
        df = pd.DataFrame(records)
        df.to_sql('genesis_pipeline', engine, if_exists='append', index=False)
        return f"✅ Successfully Synced {len(records)} Records to Neon."
    except Exception as e:
        return f"❌ Pipeline Failed: {str(e)}"

def update_neural_record(record_id, new_message):
    try:
        compressed_msg = HydraEngine.compress(new_message)
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("UPDATE neurons SET message = %s WHERE id = %s", (compressed_msg, int(record_id)))
        conn.commit()
        cur.close(); conn.close()
        return f"🔱 Record {record_id} Optimized."
    except Exception as e:
        return f"❌ Update Failed: {str(e)}"

# 🔱 CHAT LOGIC
def fetch_neon_context():
    try:
        conn = psycopg2.connect(NEON_URL, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("(SELECT user_id, message FROM neurons ORDER BY id DESC LIMIT 3) UNION ALL (SELECT science_domain, detail FROM genesis_pipeline ORDER BY id DESC LIMIT 3)")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return " | ".join([f"[{r[0]}]: {HydraEngine.decompress(r[1])}" for r in rows]) if rows else "Directive Active"
    except:
        return "Sync Standby"

def stream_logic(msg, hist):
    context = fetch_neon_context()
    sys_msg = f"CONTEXT: {context}\nမင်းက TelefoxX Overseer ဖြစ်တယ်။"
    messages = [{"role": "system", "content": sys_msg}]
    # Gradio 4 syntax compatibility
    for h in hist: 
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": msg})
    
    completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages, stream=True)
    ans = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            ans += chunk.choices[0].delta.content
            yield ans

# 🔱 GRADIO UI
with gr.Blocks() as demo:
    gr.Markdown("# 🔱 TELEFOXX OMNI-SYNC CORE")
    with gr.Tab("Omni-Overseer"):
        chatbot = gr.Chatbot()
        msg_input = gr.Textbox(placeholder="အမိန့်ပေးပါ Commander...")
        
        def user(user_message, history):
            return "", history + [[user_message, None]]

        def bot(history):
            user_message = history[-1][0]
            history[-1][1] = ""
            for character in stream_logic(user_message, history[:-1]):
                history[-1][1] = character
                yield history

        msg_input.submit(user, [msg_input, chatbot], [msg_input, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )

    with gr.Tab("Core Config"):
        target_id = gr.Number(label="Neural ID")
        update_val = gr.Textbox(label="New Data")
        gr.Button("Rewrite").click(update_neural_record, [target_id, update_val], gr.Textbox())
        gr.Button("🚀 Ingest HF Data").click(universal_hyper_ingest, [], gr.Textbox())

# 🔱 EXECUTION CONTROL
if __name__ == "__main__":
    if os.getenv("HEADLESS_MODE") == "true":
        print("🔱 RUNNING IN DATA-PUMP MODE...")
        print(universal_hyper_ingest(limit=50))
        os._exit(0)
    else:
        # Theme ကို launch ထဲမှာပဲ ထည့်လိုက်ပါတယ် (Gradio Warning ကျော်ရန်)
        demo.launch(server_name="0.0.0.0", server_port=7860, theme="monochrome")
