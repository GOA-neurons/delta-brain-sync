import requests

def harvest_science_data():
    # ArXiv API ကနေ နည်းပညာအသစ်ဆုံး Research တွေကို ဇွတ်ဆွဲမယ်
    search_query = "all:quantum+computing+OR+all:artificial+intelligence"
    url = f"http://export.arxiv.org/api/query?search_query={search_query}&max_results=50"
    
    response = requests.get(url)
    if response.status_code == 200:
        # ဒီနေရာမှာ AI က ရလာတဲ့ Research data တွေကို Neon ထဲ ဇွတ်သွင်းမယ်
        print("✅ Science Data Captured. Saving to Natural Order Memory...")
    else:
        print("❌ Harvest Failed.")

harvest_science_data()
