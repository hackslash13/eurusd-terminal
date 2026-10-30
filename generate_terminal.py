import json
from datetime import datetime

today = datetime.utcnow()
current_date_str = today.strftime('%B %d, %Y')

# Load the comprehensive analysis.json
try:
    with open("analysis.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading analysis.json: {e}")
    exit(1)

is_short = "short" in data.get("bias", "").lower() or "bear" in data.get("bias", "").lower()
badge_class = "bg-rose-500/10 text-rose-400 border-rose-500/25" if is_short else "bg-emerald-500/10 text-emerald-400 border-emerald-500/25"

fund = data.get("fundamental", {})
tech = data.get("technical_top_down", {})
rules = data.get("actionable_rules", {})

html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUR/USD Institutional Analysis Terminal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur p-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
            <div class="bg-blue-600 text-white px-3 py-1.5 rounded-lg font-bold">EUR/USD</div>
            <h1 class="text-xl font-semibold tracking-tight">Institutional Analysis Terminal</h1>
        </div>
        <div class="text-sm text-slate-400">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
            NPT Live Sync | Updated: {data.get('date', current_date_str)}
        </div>
    </header>

    <!-- Main Grid -->
    <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-7xl mx-auto w-full">
        
        <!-- Left 2 Columns: Chart & Detailed Breakdown -->
        <div class="lg:col-span-2 space-y-6 flex flex-col">
            <!-- TradingView Chart -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col h-[500px]">
                <div class="p-4 border-b border-slate-800 font-medium flex justify-between items-center text-sm">
                    <span>TradingView Chart (OANDA:EURUSD, M15)</span>
                    <span class="text-xs bg-blue-500/10 text-blue-400 px-2.5 py-1 rounded border border-blue-500/20">{data.get('setup_type', 'Active Setup')}</span>
                </div>
                <div class="flex-1 w-full h-full bg-slate-950">
                    <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AEURUSD&interval=15&theme=dark" class="w-full h-full border-0"></iframe>
                </div>
            </div>

            <!-- Detailed Analysis Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Fundamental Analysis -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-bold uppercase tracking-wider text-blue-400 mb-3 flex items-center">
                            <i class="fa-solid fa-globe mr-2"></i> Fundamental Analysis
                        </h2>
                        <div class="space-y-3 text-xs text-slate-300 leading-relaxed">
                            <p><strong class="text-slate-200">Macro Environment:</strong> {fund.get('macro_environment', '')}</p>
                            <p><strong class="text-slate-200">Driver Dynamics:</strong> {fund.get('driver_dynamics', '')}</p>
                        </div>
                    </div>
                </div>

                <!-- Actionable Rules & Invalidation -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                    <div>
                        <h2 class="text-sm font-bold uppercase tracking-wider text-amber-400 mb-3 flex items-center">
                            <i class="fa-solid fa-crosshairs mr-2"></i> Execution & Invalidation
                        </h2>
                        <div class="space-y-3 text-xs text-slate-300 leading-relaxed">
                            <p><strong class="text-slate-200">Entry Rules:</strong> {rules.get('entry_rules', '')}</p>
                            <p><strong class="text-slate-200">Exit / Management:</strong> {rules.get('exit_management', '')}</p>
                            <p><strong class="text-rose-400">Invalidation:</strong> {rules.get('invalidation_criteria', '')}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Top-Down Technical Analysis -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <h2 class="text-sm font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center">
                    <i class="fa-solid fa-chart-line mr-2"></i> Top-Down Technical Analysis (D1, H4, H1, M15)
                </h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <span class="font-bold text-blue-400 block mb-1">D1 (Daily)</span>
                        <p class="text-slate-300 leading-relaxed">{tech.get('d1', '')}</p>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <span class="font-bold text-purple-400 block mb-1">H4 (4-Hour)</span>
                        <p class="text-slate-300 leading-relaxed">{tech.get('h4', '')}</p>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <span class="font-bold text-amber-400 block mb-1">H1 (1-Hour)</span>
                        <p class="text-slate-300 leading-relaxed">{tech.get('h1', '')}</p>
                    </div>
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <span class="font-bold text-emerald-400 block mb-1">M15 (Execution)</span>
                        <p class="text-slate-300 leading-relaxed">{tech.get('m15', '')}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Right Column: Execution HUD Panel -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between h-fit">
            <div>
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-lg font-bold text-slate-200">Execution HUD</h2>
                    <span class="px-3 py-1 rounded text-xs font-semibold border {badge_class}">{data.get('bias', 'N/A')}</span>
                </div>
                
                <div class="space-y-4">
                    <div class="bg-slate-950 p-3.5 rounded-lg border border-slate-800 flex justify-between items-center">
                        <span class="text-slate-400 text-sm">Entry Price</span>
                        <span class="font-mono font-bold text-slate-100 text-base">{data.get('entry', 'N/A')}</span>
                    </div>
                    <div class="bg-slate-950 p-3.5 rounded-lg border border-slate-800 flex justify-between items-center">
                        <span class="text-slate-400 text-sm">Stop Loss (SL)</span>
                        <span class="font-mono font-bold text-rose-400 text-base">{data.get('sl', 'N/A')}</span>
                    </div>
                    <div class="bg-slate-950 p-3.5 rounded-lg border border-slate-800 flex justify-between items-center">
                        <span class="text-slate-400 text-sm">Take Profit (TP)</span>
                        <span class="font-mono font-bold text-emerald-400 text-base">{data.get('tp', 'N/A')}</span>
                    </div>
                    <div class="bg-slate-950 p-3.5 rounded-lg border border-slate-800 flex justify-between items-center">
                        <span class="text-slate-400 text-sm">Risk-to-Reward</span>
                        <span class="font-mono font-bold text-blue-400 text-base">{data.get('rrr', 'N/A')}</span>
                    </div>
                </div>
            </div>

            <div class="mt-8 pt-4 border-t border-slate-800 text-center text-xs text-slate-500">
                Synced from analysis.json via GitHub Actions
            </div>
        </div>

    </main>
</body>
</html>
"""

try:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html successfully updated with full institutional breakdown!")
except Exception as e:
    print(f"Error writing index.html: {e}")
