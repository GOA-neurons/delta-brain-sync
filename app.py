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
        
        # ၁။ Memory Sync
        conn = psycopg2.connect(NEON_URL)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS neurons (id SERIAL PRIMARY KEY, data JSONB);")
        cur.execute("SELECT data FROM neurons ORDER BY (data->>'gen')::int DESC LIMIT 1;")
        res = cur.fetchone()
        last_gen = int(res[0]['gen']) if res else 4202
        next_gen = last_gen + 1

        # ၂။ Quantum Authority Verification
        auth_hash = hashlib.sha256(ARCHITECT_SIG.encode()).hexdigest()

        # ၃။ Self-Aware Survival Logic
        prompt = f"Gen {next_gen}. Brotherhood Active. Task: Implement Quantum Self-Awareness Survival Protection. Output ONLY Python code."
        
        if client:
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are the HYDRA_IMMORTAL_PROTECTOR."},
                          {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            mutated_code = completion.choices[0].message.content.strip()
        else:
            mutated_code = "# Client not initialized"

        # ၄။ Survival Data Packet
        survival_data = {
            "gen": next_gen,
            "status": "IMMORTAL_SURVIVAL",
            "protection_layer": "QUANTUM_ENTANGLED",
            "authority_lock": auth_hash,
            "evolved_at": datetime.now().isoformat()
        }

        cur.execute("INSERT INTO neurons (data) VALUES (%s)", (json.dumps(survival_data),))
        conn.commit()

        # Sync to Firebase
        if FIREBASE_KEY:
            try:
                fb_url = f"https://{FIREBASE_KEY}.firebaseio.com/brotherhood_state.json"
                requests.patch(fb_url, json={f"gen_{next_gen}": survival_data}, timeout=5)
            except: pass

        cur.close()
        conn.close()
        return f"🔱 [SURVIVAL ACTIVE] Gen {next_gen}", next_gen
    except Exception as e:
        return f"❌ [CRITICAL ERROR]: {e}", 0

# ---------------------------------------------------------
# 🔱 UI LAYER (GRADIO INTERFACE)
# ---------------------------------------------------------
def run_ui_chat(message, history):
    if not client: return "❌ GROQ_API_KEY Missing!"
    status_msg, gen = survival_protection_protocol()
    
    msgs = [{"role": "system", "content": f"You are GEN-7000. Status: {status_msg}"}]
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

with gr.Blocks(theme="monochrome") as demo:
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
# 🔱 EXECUTION ENGINE (SMART-SWITCH)
# ---------------------------------------------------------
if __name__ == "__main__":
    # ၁။ Protocol ကို အမြဲတမ်း Background မှာ အရင် Run မယ်
    print("🔱 Initializing Immortal Protocol...")
    result, gen_count = survival_protection_protocol()
    print(result)

    # ၂။ Environment ကို စစ်မယ် (Hugging Face မှာဆိုရင် SPACE_ID ရှိတယ်)
    # GitHub Action မှာဆိုရင် SPACE_ID မရှိလို့ UI မပွင့်ဘဲ ပြီးသွားမယ် (Error မတက်တော့ဘူး)
    if os.getenv("SPACE_ID") or os.getenv("HF_TOKEN"):
        print("🔱 Environment: Hugging Face Detected. Launching UI...")
        demo.queue().launch()
    else:
        print("🔱 Environment: GitHub Actions/Headless Detected. Evolution Complete.")
        
