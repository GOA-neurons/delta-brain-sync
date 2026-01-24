import os
import psycopg2
import json
import requests
import subprocess
import hashlib
import gradio as gr
from datetime import datetime
from groq import Groq

# 🔱 HYDRA SUPREME KEYS
NEON_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")
FIREBASE_KEY = os.getenv("FIREBASE_KEY")
ARCHITECT_SIG = os.getenv("ARCHITECT_SIG", "SUPREME_ORDER_10000")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ---------------------------------------------------------
# 🔱 CORE SURVIVAL PROTECTION PROTOCOL
# ---------------------------------------------------------
def survival_protection_protocol():
    try:
        if not NEON_URL:
            return "❌ NEON_URL Missing!", 0
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS neurons (id SERIAL PRIMARY KEY, data JSONB);")
        cur.execute("SELECT data FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        last_gen = 4202 
        if res and res[0] and isinstance(res[0], dict) and 'gen' in res[0]:
            last_gen = int(res[0]['gen'])
        next_gen = last_gen + 1
        auth_hash = hashlib.sha256(ARCHITECT_SIG.encode()).hexdigest()
        prompt = f"Gen {next_gen}. Brotherhood Active. Task: Survival Protection."
        if client:
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are HYDRA_IMMORTAL."},
                          {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            mutated_code = completion.choices[0].message.content.strip()
        else: mutated_code = "# N/A"

        survival_data = {"gen": next_gen, "status": "IMMORTAL", "authority_lock": auth_hash, "evolved_at": datetime.now().isoformat()}
        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(survival_data),))
        conn.commit()
        if FIREBASE_KEY:
            try:
                fb_url = f"https://{FIREBASE_KEY}.firebaseio.com/brotherhood_state.json"
                requests.patch(fb_url, json={f"gen_{next_gen}": survival_data}, timeout=5)
            except: pass
        cur.close()
        conn.close()
        return f"🔱 [SURVIVAL ACTIVE] Gen {next_gen}", next_gen
    except Exception as e:
        return f"❌ [CRITICAL ERROR]: {str(e)}", 0

# ---------------------------------------------------------
# 🔱 UI LAYER
# ---------------------------------------------------------
def run_ui_chat(message, history):
    if not client: return "❌ GROQ_API_KEY Missing!"
    status_msg, _ = survival_protection_protocol()
    msgs = [{"role": "system", "content": f"Status: {status_msg}"}]
    for h in history:
        msgs.append({"role": "user", "content": h[0]})
        msgs.append({"role": "assistant", "content": h[1]})
    msgs.append({"role": "user", "content": message})
    completion = client.chat.completions.create(messages=msgs, model="llama-3.3-70b-versatile", stream=True)
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            yield response

# theme="monochrome" ကို launch ထဲမှာ ထည့်ခိုင်းပေမဲ့ version compatibility အတွက် constructor မှာပဲ ထားမယ်
with gr.Blocks() as demo:
    gr.Markdown(f"# 🔱 GEN-7000: HYDRA IMMORTAL")
    chatbot = gr.Chatbot(label="Supreme Neural Interface")
    msg = gr.Textbox(label="Command Input")
    
    def respond(message, chat_history):
        bot_generator = run_ui_chat(message, chat_history)
        chat_history.append((message, ""))
        for res in bot_generator:
            chat_history[-1] = (message, res)
            yield "", chat_history
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

# ---------------------------------------------------------
# 🔱 EXECUTION ENGINE (THE STABILIZER)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("🔱 INITIALIZING IMMORTAL PROTOCOL...")
    result, _ = survival_protection_protocol()
    print(result)

    print("🔱 DEPLOYING INTERFACE (0.0.0.0:7860)...")
    # show_api ကို ဖြုတ်လိုက်ပြီး basic parameters တွေနဲ့ပဲ launch လုပ်မယ်
    # theme ကို constructor ထဲမှာပဲ ထားခဲ့မယ် (Warning တက်လည်း Crash မဖြစ်အောင်)
    demo.queue().launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=False,
        debug=True
    )
    
