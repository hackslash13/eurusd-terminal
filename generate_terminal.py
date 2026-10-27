import os
from datetime import datetime
import random

# Use the day of the year as a seed so the trade setup refreshes daily but remains consistent throughout the day
today = datetime.utcnow()
day_seed = today.timetuple().tm_yday
random.seed(day_seed)

current_date_str = today.strftime('%B %d, %Y')
timestamp_str = today.strftime('%Y-%m-%d %H:%M:%S')

# Dynamically generate fresh daily price points and bias based on day seed
is_bearish = day_seed % 2 == 0
base_pips = 1.1150 + (random.randint(0, 80) * 0.0001)

if is_bearish:
    bias = "Short / Bearish"
    badge_class = "bg-rose-500/10 text-rose-400 border-rose-500/25"
    entry = round(base_pips + 0.0020, 5)
    stop_loss = round(entry + 0.0030, 5)
    take_profit = round(entry - 0.0050, 5)
    rrr = "1 : 1.67"
    fund_summary = "Persistent policy divergence between the ECB and Federal Reserve, coupled with regional Eurozone fiscal pressures, continues to support dollar strength during major session overlaps."
    tech_summary = "Daily and H4 structures remain downward. M15 is testing localized overhead supply near resistance, offering clean continuation short setups toward lower structural liquidity."
else:
    bias = "Long / Bullish"
    badge_class = "bg-emerald-500/10 text-emerald-400 border-emerald-500/25"
    entry = round(base_pips, 5)
    stop_loss = round(entry - 0.0030, 5)
    take_profit = round(entry + 0.0050, 5)
    rrr = "1 : 1.67"
    fund_summary = "Recent macroeconomic data pointing to resilient regional growth and softer US inflation prints are providing fundamental tailwinds for the shared currency against the dollar."
    tech_summary = "Price is holding above key daily demand zones with H4 higher lows forming. M15 shows bullish impulse continuation following a clean test of local support."

# High-performance terminal template with dynamic daily injection
html_template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUR/USD Professional Analysis Terminal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col">
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur p-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
            <div class="bg-blue-600 text-white p-2 rounded-lg font-bold">EUR/USD</div>
            <h1 class="text-xl font-semibold tracking-tight">Institutional Analysis Terminal</h1>
        </div>
        <div class="text-sm text-slate-400">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
            NPT Live Sync | Updated: {current_date_str}
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
                <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AEURUSD&interval=15&theme=dark" class="w-full h-full border-0"></iframe>
            </div>
        </div>

        <!-- Trade HUD Panel -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
            <div>
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-bold text-slate-200">Execution HUD</h2>
                    <span class="px-3 py-1 rounded text-xs font-semibold {badge_class}">{bias}</span>
                </div>
                
                <div class="space-y-4 text-sm">
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Entry Price</span>
                        <span class="font-mono font-bold text-slate-100">{entry:.5f}</span>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Stop Loss (SL)</span>
                        <span class="font-mono font-bold text-rose-400">{stop_loss:.5f}</span>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Take Profit (TP)</span>
                        <span class="font-mono font-bold text-emerald-400">{take_profit:.5f}</span>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex justify-between">
                        <span class="text-slate-400">Risk-to-Reward</span>
                        <span class="font-mono font-bold text-blue-400">{rrr}</span>
                    </div>
                </div>

                <div class="mt-6 space-y-3">
                    <div>
                        <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Fundamental Outlook</h3>
                        <p class="text-xs text-slate-300 leading-relaxed">{fund_summary}</p>
                    </div>
                    <div>
                        <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Technical Structure</h3>
                        <p class="text-xs text-slate-300 leading-relaxed">{tech_summary}</p>
                    </div>
                </div>
            </div>

            <div class="mt-6 pt-4 border-t border-slate-800 text-center text-xs text-slate-500">
                Auto-synced daily via GitHub Actions (Synced: {timestamp_str} UTC)
            </div>
        </div>
    </main>
</body>
</html>
"""

try:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("index.html successfully updated with fresh daily trade parameters!")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    exit(1)
    
