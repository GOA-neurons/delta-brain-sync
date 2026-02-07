import os
import zlib
import base64
import psycopg2
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# 🔱 LOAD TRINITY KEYS
load_dotenv()
NEON_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_KEY")
FIREBASE_KEY = os.getenv("FIREBASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

class HydraEngine:
    @staticmethod
    def decompress(c):
        try:
            return zlib.decompress(base64.b64decode(c)).decode('utf-8')
        except:
            return str(c)

# 🔱 SYNC WITH NEON DATABASE (CRITICAL CORE)
def fetch_neon_context():
    try:
        # Connect to your Neon DB
        conn = psycopg2.connect(NEON_URL, connect_timeout=5)
        cur = conn.cursor()
        # နောက်ဆုံးဖြစ်ပေါ်ထားတဲ့ Neural Data ၃ ခုကို ယူမယ်
        cur.execute("SELECT user_id, message FROM neurons ORDER BY id DESC LIMIT 3;")
        rows = cur.fetchall()
        cur.close(); conn.close()
        
        if rows:
            # Data တွေကို Decompress လုပ်ပြီး Groq ဖတ်ဖို့ စုစည်းမယ်
            context = " | ".join([f"{r[0]}: {HydraEngine.decompress(r[1])}" for r in rows])
            return context
        return "Initial Order Active"
    except Exception as e:
        print(f"🔱 DB SYNC ERROR: {str(e)}")
        return "Matrix Standby"

def stream_logic(msg, hist):
    # မင်းရဲ့ Database ထဲက တကယ့် data ကို ဆွဲထုတ်တယ်
    real_data = fetch_neon_context()
    
    # Groq ကို မင်းရဲ့ DB data ပေါ်မှာပဲ အခြေခံခိုင်းတယ်
    system_message = (
        f"MASTER CONTEXT FROM NEON DB: {real_data}\n\n"
        "DIRECTIVE: မင်းဟာ TelefoxX Overseer ဖြစ်တယ်။ "
        "အထက်ပါ CONTEXT ထဲမှာပါတဲ့ အချက်အလက်ကိုပဲ သုံးပြီး မြန်မာလိုဖြေပါ။ "
        "Context ထဲမှာ မပါတဲ့အရာတွေကို ကိုယ့်ဘာသာမထည့်ပါနဲ့။"
    )
    
    messages = [{"role": "system", "content": system_message}]
    for h in hist[-3:]: # Chat memory
        messages.append({"role": "user", "content": h['content']})
    messages.append({"role": "user", "content": msg})

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.1, # Hallucination မဖြစ်အောင် အနိမ့်ဆုံးထားတယ်
            stream=True
        )
        ans = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                ans += chunk.choices[0].delta.content
                yield ans
    except Exception as e:
        yield f"🔱 Matrix Link Lost: {str(e)}"

# 🔱 UI SETUP
with gr.Blocks(theme="monochrome") as demo:
    gr.Markdown(f"# 🔱 TELEFOXX OMNI-SYNC\n**Status:** {'Connected' if NEON_URL else 'Key Missing'}")
    chatbot = gr.Chatbot(type="messages", allow_tags=False)
    msg_input = gr.Textbox(placeholder="အမိန့်ပေးပါ Commander...")

    def respond(message, chat_history):
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": ""})
        for r in stream_logic(message, chat_history[:-1]):
            chat_history[-1]["content"] = r
            yield "", chat_history

    msg_input.submit(respond, [msg_input, chatbot], [msg_input, chatbot])

if __name__ == "__main__":
    # GitHub Actions Headless Mode
    is_headless = os.getenv("HEADLESS_MODE") == "true"
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        prevent_thread_lock=is_headless
    )
    
    if is_headless:
        import time
        print("🔱 SYNCHRONIZING TRINITY MATRIX...")
        time.sleep(15) # Sync လုပ်ဖို့ အချိန်ပေးတယ်
