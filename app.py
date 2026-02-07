import os
import zlib
import base64
import psycopg2
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# 🔱 CORE INITIALIZATION
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class HydraEngine:
    @staticmethod
    def decompress(c):
        try:
            return zlib.decompress(base64.b64decode(c)).decode('utf-8')
        except:
            return str(c)

def sync_matrix():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"), connect_timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT message FROM neurons ORDER BY id DESC LIMIT 1;")
        res = cur.fetchone()
        cur.close(); conn.close()
        return HydraEngine.decompress(res[0]) if res else "Natural Order Active"
    except:
        return "Standby Mode"

# 🔱 CHAT LOGIC (Using OpenAI-style Message Format for Gradio 6.0)
def stream_logic(msg, hist):
    ctx = sync_matrix()
    sys_msg = f"System Context: {ctx[:300]}. You are TelefoxX. Reply in Burmese."
    
    messages = [{"role": "system", "content": sys_msg}]
    # Gradio messages format ကို အမှန်ကန်ဆုံး ပြောင်းလဲခြင်း
    for h in hist:
        messages.append({"role": "user", "content": h["content"] if isinstance(h, dict) else h[0]})
        messages.append({"role": "assistant", "content": h["content"] if isinstance(h, dict) else h[1]})
    
    messages.append({"role": "user", "content": msg})

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.2,
            stream=True
        )
        ans = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                ans += chunk.choices[0].delta.content
                yield ans
    except Exception as e:
        yield f"🔱 Matrix Link Interrupted: {str(e)}"

# 🔱 UI SETUP (Resolved all Depreciation and UserWarnings)
with gr.Blocks(theme="monochrome") as demo:
    gr.Markdown("# 🔱 TELEFOXX CONTROL CENTER")
    
    # type="messages" သတ်မှတ်ခြင်းဖြင့် Tuples warning ကို ရှင်းလိုက်ပြီ
    chatbot = gr.Chatbot(label="Neural Stream", type="messages", allow_tags=False)
    msg_input = gr.Textbox(placeholder="အမိန့်ပေးပါ Commander...")

    def respond(message, chat_history):
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": ""})
        # stream bot response
        for r in stream_logic(message, chat_history[:-1]):
            chat_history[-1]["content"] = r
            yield "", chat_history

    msg_input.submit(respond, [msg_input, chatbot], [msg_input, chatbot])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
