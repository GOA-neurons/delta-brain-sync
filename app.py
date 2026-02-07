import os
import zlib
import base64
import psycopg2
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# 🔱 LOAD CORE ONLY
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class HydraEngine:
    @staticmethod
    def decompress(c):
        try: return zlib.decompress(base64.b64decode(c)).decode('utf-8')
        except: return str(c)

def sync_matrix():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"), connect_timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT message FROM neurons ORDER BY id DESC LIMIT 1;")
        res = cur.fetchone()
        cur.close(); conn.close()
        return HydraEngine.decompress(res[0]) if res else "Order Initialized"
    except: return "Standby Mode"

def stream_logic(msg, hist):
    ctx = sync_matrix()
    # 🔱 THE BOX BYPASS: Logic ကို System Message ထဲ တိုတိုပဲ ထည့်မယ်
    sys_msg = f"Data: {ctx[:200]}. Role: TelefoxX. Reply Burmese."
    
    msgs = [{"role": "system", "content": sys_msg}]
    for h in hist[-2:]:
        msgs.append({"role": "user", "content": h[0]})
        msgs.append({"role": "assistant", "content": h[1]})
    msgs.append({"role": "user", "content": msg})

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=msgs,
            temperature=0.2,
            stream=True
        )
        ans = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                ans += chunk.choices[0].delta.content
                yield ans
    except Exception as e:
        yield f"🔱 Offline: {str(e)}"

# 🔱 UI: FASTEST RENDERING
with gr.Blocks() as demo:
    gr.Markdown("# 🔱 TELEFOXX CORE")
    chat = gr.Chatbot(label="Neural Stream")
    input = gr.Textbox(placeholder="Command here...")
    
    def process(m, h):
        return "", h + [[m, ""]]
    
    def bot(h):
        for res in stream_logic(h[-1][0], h[:-1]):
            h[-1][1] = res
            yield h

    input.submit(process, [input, chat], [input, chat]).then(bot, chat, chat)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
