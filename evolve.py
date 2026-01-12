import os
import psycopg2
import requests
import xml.etree.ElementTree as ET

DB_URL = os.getenv("DB_URL")

def critical_harvest():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Table ကို အသေအချာ ဇွတ်ပြင်ထားမယ်
        cur.execute("""
            CREATE TABLE IF NOT EXISTS research_data (
                id SERIAL PRIMARY KEY,
                title TEXT UNIQUE,
                detail TEXT,
                harvested_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # Data ဆွဲမယ်
        response = requests.get("http://export.arxiv.org/api/query?search_query=all:ai&max_results=10")
        root = ET.fromstring(response.content)
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        
        for entry in entries:
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            cur.execute(
                "INSERT INTO research_data (title, detail) VALUES (%s, %s) ON CONFLICT (title) DO NOTHING",
                (title, summary)
            )
        
        conn.commit()
        cur.close()
        conn.close()
        print("Success: 10 Nodes Harvested.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    critical_harvest()
    
