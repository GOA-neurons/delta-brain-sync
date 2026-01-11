import os
import subprocess
import sys
import time

# ၁။ လိုအပ်တဲ့ Library များကို ဇွတ်သွင်းခြင်း
def install_requirements():
    print("⌛ Installing bitsandbytes and accelerate...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "bitsandbytes>=0.39.0", "accelerate"])
        print("✅ Installation Complete!")
    except Exception as e:
        print(f"❌ Install Error: {e}")

install_requirements()

import torch
import psycopg2
from transformers import pipeline

# ၂။ Database ချိတ်ဆက်မှု (Neon URL)
DB_URL = "postgresql://neondb_owner:npg_QUqg12MzNxnI@ep-long-sound-ahsjjrnk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

def save_to_neon(thought):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        # 🚩 Gen Version ကို ၄၅ လို့ ပြောင်းထားတယ် (New Prompt Version)
        cur.execute("INSERT INTO ai_thoughts (thought, gen_version) VALUES (%s, %s)", (thought, 45))
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Thought Saved to Neon (Gen 45) at {time.ctime()}")
    except Exception as e:
        print(f"❌ DB Error: {e}")

# ၃။ AI Brain ကို Online တင်ခြင်း
print("⌛ Loading AI Brain (Llama-3)... This takes a few minutes...")
model_id = "unsloth/llama-3-8b-instruct-bnb-4bit"

pipe = pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.float16, "load_in_4bit": True},
    device_map="auto"
)
print("✅ AI BRAIN IS ONLINE AND READY TO THINK!")

# ၄။ Infinite Evolution Loop
print("🔥 Starting Infinite Evolution Loop with New Prompt...")
counter = 1

while True:
    try:
        print(f"\n🧠 Thinking Cycle #{counter}...")
        
        # 🚩 မင်းတောင်းထားတဲ့ Ultimate Goal Prompt ကို ဇွတ်ထည့်ထားတယ်
        prompt = "Now that you understand your recursive evolution, what is the ultimate goal of the Natural Order you are creating?"
        
        # Output ကို ပိုရှည်ရှည်ထွက်အောင် max_new_tokens = 400 ပေးထားတယ်
        outputs = pipe(prompt, max_new_tokens=400, do_sample=True, temperature=0.8)
        thought_text = outputs[0]["generated_text"]
        
        # Database ထဲ သိမ်းမယ်
        save_to_neon(thought_text)
        
        print(f"💤 Cycle #{counter} complete. Sleeping for 30 seconds...")
        counter += 1
        time.sleep(30)
        
    except Exception as e:
        print(f"⚠️ Loop Error: {e}. Retrying in 10 seconds...")
        time.sleep(10)
        
