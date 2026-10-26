import os
import requests
import json

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

prompt = """
You are a senior Forex quantitative trader. Generate a complete, valid, single-file HTML page for a high-performance EUR/USD Forex Analysis Terminal with embedded Tailwind CSS, FontAwesome icons, a live TradingView chart (OANDA:EURUSD, 15m interval), dynamic NPT (UTC+5:45) session calculations, and a draggable Trade HUD overlay.

Perform today's EUR/USD top-down analysis (D1, H4, H1, M15) and fundamental analysis. Produce a high-probability trade setup with minimum 1:1.5 Risk-to-Reward Ratio (RRR). Include exact Entry, Stop Loss, Take Profit, 'When to Enter', 'When to Exit', and 'Trade Validity' criteria.

Return ONLY the executable raw HTML string starting with <!DOCTYPE html> and ending with </html> without markdown wrappers or extra commentary.
"""

payload = {
    "contents": [{"parts": [{"text": prompt}]}]
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    res_data = response.json()
    try:
        generated_html = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected API response structure: {res_data}") from e
    
    # Remove markdown code fence if wrapped
    if generated_html.startswith("```html"):
        generated_html = generated_html[7:]
    if generated_html.startswith("```"):
        generated_html = generated_html[3:]
    if generated_html.endswith("```"):
        generated_html = generated_html[:-3]
    
    generated_html = generated_html.strip()
    
    if not generated_html.startswith("<!DOCTYPE html>"):
        raise ValueError("Generated content does not start with <!DOCTYPE html>")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generated_html)
    print("index.html successfully updated and verified!")
else:
    raise Exception(f"Gemini API Error {response.status_code}: {response.text}")
    
