import os
import requests
import json
from datetime import datetime

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY secret is not set or accessible in GitHub Actions!")
    exit(1)

model_name = "gemini-3.8-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

# Streamlined prompt focused strictly on updating JSON trade data and analysis text
prompt = """
You are a senior Forex quantitative trader. Provide today's precise EUR/USD trade parameters and analysis based on current conditions.
Return ONLY a valid JSON object with the following exact keys, with no markdown formatting or code blocks around it:
{
  "date": "Current Date (e.g., October 27, 2026)",
  "bias": "Short / Bearish",
  "entry": "1.12150",
  "stop_loss": "1.12450",
  "take_profit": "1.11650",
  "rrr": "1 : 1.67",
  "fundamental_summary": "Short 2-sentence fundamental summary focusing on ECB/Fed policy and US dollar/Euro dynamics.",
  "technical_summary": "Short 2-sentence technical summary covering D1/H4/H1 structures."
}
"""

payload = {
    "contents": [{"parts": [{"text": prompt}]}]
}

headers = {'Content-Type': 'application/json'}

print(f"Fetching latest EUR/USD trade metrics using {model_name}...")

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    if response.status_code != 200:
        print(f"API Error Body: {response.text}")
        exit(1)
        
    res_data = response.json()
    raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
    
    # Clean code blocks if returned
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
        
    trade_data = json.loads(raw_text.strip())

    # Stable, high-performance terminal layout template embedded directly
    html_template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUR/USD Professional Analysis Terminal</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link rel="stylesheet" href="[https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css)">
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col">
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur p-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
            <div class="bg-blue-600 text-white p-2 rounded-lg font-bold">EUR/USD</div>
            <h1 class="text-xl font-semibold tracking-tight">Institutional Analysis Terminal</h1>
        </div>
        <div class="text-sm text-slate-400">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
            NPT Live Sync | Updated: {trade_data.get('date')}
        </div>
    </header>

    <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-7xl mx-auto w-full">
        <!-- Chart Section -->
        <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col h-[550px]">
            <div class="p-4 border-b border-slate-800 font-medium flex justify-between items-center">
                <span>TradingView Chart (OANDA:EURUSD, M15)</span>
                <span class="text-xs bg-blue-500/10 text-blue-400 px-2.5 py-1 rounded border border-blue-500/20">Active Setup</span>
            </div>
            <div class="flex-1 w-full h-full bg-slate-950">
                <iframe src="[https://s.tradingview.com/widgetembed/?symbol=OANDA%3AEURUSD&interval=15&theme=dark](https://s.tradingview.com/widgetembed/?symbol=OANDA%3AEURUSD&interval=15&theme=dark)" class="w-full h-full border-0"></iframe>
            </div>
        </div>

        <!-- Trade HUD Panel -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
            <div>
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-bold text-slate-200">Execution HUD</h2>
                    <span class="px-3 py-1 rounded text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/25">{trade_data.get('bias')}</span>
                </div>
                
                <div class="space-y-4 text-sm">
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Entry Price</span>
                        <span class="font-mono font-bold text-slate-100">{trade_data.get('entry')}</span>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Stop Loss (SL)</span>
                        <span class="font-mono font-bold text-rose-400">{trade_data.get('stop_loss')}</span>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Take Profit (TP)</span>
                        <span class="font-mono font-bold text-emerald-400">{trade_data.get('take_profit')}</span>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Risk-to-Reward</span>
                        <span class="font-mono font-bold text-blue-400">{trade_data.get('rrr')}</span>
                    </div>
                </div>

                <div class="mt-6 space-y-3">
                    <div>
                        <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Fundamental Outlook</h3>
                        <p class="text-xs text-slate-300 leading-relaxed">{trade_data.get('fundamental_summary')}</p>
                    </div>
                    <div>
                        <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Technical Structure</h3>
                        <p class="text-xs text-slate-300 leading-relaxed">{trade_data.get('technical_summary')}</p>
                    </div>
                </div>
            </div>

            <div class="mt-6 pt-4 border-t border-slate-800 text-center text-xs text-slate-500">
                Auto-synced daily via GitHub Actions & Gemini API
            </div>
        </div>
    </main>
</body>
</html>
<!-- Auto-generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC -->
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
        
    print("index.html successfully updated via fast data injection!")

except Exception as e:
    print(f"An exception occurred during execution: {str(e)}")
    exit(1)
