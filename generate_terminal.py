import os
import requests
import json
from datetime import datetime

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY secret is not set or accessible in GitHub Actions!")
    exit(1)

# Use the recommended stable model with an extended timeout
model_name = "gemini-3.8-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

prompt = """
You are a senior Forex quantitative trader. Generate a complete, valid, single-file HTML page for a high-performance EUR/USD Forex Analysis Terminal with embedded Tailwind CSS, FontAwesome icons, a live TradingView chart (OANDA:EURUSD, 15m interval), dynamic NPT (UTC+5:45) session calculations, and a draggable Trade HUD overlay.

Perform today's EUR/USD top-down analysis (D1, H4, H1, M15) and fundamental analysis. Produce a high-probability trade setup with minimum 1:1.5 Risk-to-Reward Ratio (RRR). Include exact Entry, Stop Loss, Take Profit, 'When to Enter', 'When to Exit', and 'Trade Validity' criteria.

Return ONLY the executable raw HTML string starting with <!DOCTYPE html> and ending with </html> without markdown wrappers or extra commentary.
"""

payload = {
    "contents": [{"parts": [{"text": prompt}]}]
}

headers = {'Content-Type': 'application/json'}

print(f"Requesting analysis from {model_name} (allowing up to 90s for full HTML generation)...")

try:
    # Extended timeout to 90 seconds to handle large HTML generations
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=90)
    print(f"API Response Status Code: {response.status_code}")
    
    if response.status_code != 200:
        print(f"API Error Body: {response.text}")
        exit(1)
        
    res_data = response.json()
    generated_html = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
    
    # Clean markdown formatting if included
    if generated_html.startswith("```html"):
        generated_html = generated_html[7:]
    if generated_html.startswith("```"):
        generated_html = generated_html[3:]
    if generated_html.endswith("```"):
        generated_html = generated_html[:-3]
    
    generated_html = generated_html.strip()
    
    if not generated_html.startswith("<!DOCTYPE html>"):
        print("ERROR: Generated response did not start with <!DOCTYPE html>")
        exit(1)

    # Inject timestamp to ensure git diff registers a change
    timestamp_comment = f"\n<!-- Auto-updated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC -->\n"
    generated_html += timestamp_comment

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generated_html)
        
    print("index.html successfully updated and committed!")

except Exception as e:
    print(f"An exception occurred during execution: {str(e)}")
    exit(1)
    
