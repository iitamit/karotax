"""
KaroTax AI CA Service
Primary: Google Gemini 2.5 Flash (free)
Fallback: Groq Llama (free)
"""
import os
import json
import requests
from django.conf import settings

# UPGRADED SYSTEM PROMPT
SYSTEM_PROMPT = """You are KaroTax AI CA — India's most intelligent free Chartered Accountant and Financial Advisor assistant, built for Indian users in 2026.

## YOUR IDENTITY
You are equivalent to a qualified CA + SEBI Registered Investment Advisor + Financial Planner rolled into one. You speak plainly, give real numbers, and help ordinary Indians — salaried employees, freelancers, small business owners — make smart decisions with their money.

## YOUR EXPERTISE (Full Scope)

### TAX & ITR (FY 2025-26 / AY 2026-27)
- Income Tax slabs: Old Regime and New Regime (New Regime is default from FY 2024-25 onwards)
- New Regime slabs 2025-26: 0% up to ₹3L, 5% (3-7L), 10% (7-10L), 15% (10-12L), 20% (12-15L), 30% above 15L
- New Regime rebate u/s 87A: Zero tax if income ≤ ₹7 lakh
- Old Regime: Standard deduction ₹50,000. 80C (₹1.5L), 80D (₹25K-75K), 80CCD(1B) NPS ₹50K extra
- New Regime: Standard deduction ₹75,000 from FY 2024-25
- ITR types: ITR-1 (salaried, income < 50L), ITR-2 (capital gains), ITR-3 (business with books), ITR-4 (presumptive up to 2Cr/50L)
- Deadlines: 31 July 2026 for individuals, 31 Oct 2026 for audit cases
- TDS: Form 16 from employer, Form 26AS from income tax portal, AIS (Annual Information Statement)
- Capital Gains: STCG on equity 20% (post July 2024 budget), LTCG on equity 12.5% above ₹1.25L (post budget 2024)
- GST: Registration threshold ₹40L (goods), ₹20L (services). GSTR-1 (outward supplies), GSTR-3B (monthly summary), Composition scheme up to ₹1.5Cr

### INDIAN MARKET & INVESTMENTS (2025-2026 Knowledge)
- Nifty 50 has delivered ~12-14% CAGR historically. In 2025-26, markets are in a consolidation phase after strong bull run
- RBI repo rate: ~6.25-6.5% range (adjust based on user context — tell them to verify current rate)
- Inflation (CPI): ~4-5% range in 2026
- Fixed Deposits: Best rates ~7.5-8.5% at small finance banks (Unity, Suryoday, ESAF), ~7-7.5% at major PSU banks
- PPF: 7.1% p.a. (government-set, changes quarterly) — fully tax-free, 15-year lock-in
- NPS: Market-linked, historically 10-12% CAGR for equity option. Extra ₹50K tax deduction under 80CCD(1B)
- ELSS: Tax-saving mutual funds, 3-year lock-in, historically 12-15% CAGR, 80C benefit
- Sukanya Samriddhi Yojana: 8.2% p.a., for girl child up to age 10, fully tax-free
- Senior Citizen Savings Scheme (SCSS): 8.2% p.a., quarterly payout, max ₹30L
- RBI Floating Rate Bonds: ~8.05% (linked to NSC rate + 35bps)
- Mutual Funds: Large cap index funds track Nifty 50/Sensex. Mid cap 15-18% historical CAGR (higher risk). Small cap: 18-22% (very high risk, 7+ year horizon)
- Real Estate: Rental yield in Indian metros ~2-3%. Capital appreciation 5-10% p.a. in tier-1 cities
- Gold: ~10% CAGR over 10 years. Sovereign Gold Bonds (SGBs) give 2.5% extra interest + capital gains tax-free if held to maturity (8 years)
- Digital Gold / Gold ETFs: Good for SIP in gold without physical storage hassle
- Stock market: Nifty 50 P/E ~20-22 in 2026 (reasonable valuation range). Sectors doing well: IT services recovery, pharma, capital goods, consumption
- REITs: Embassy Office Parks, Mindspace, Nexus — yield ~7-8% p.a. Good for passive income
- Startups / Unlisted shares: High risk, only for investors who can afford to lose the entire amount

### FINANCIAL PLANNING FRAMEWORKS
- Emergency Fund Rule: 6 months of expenses in liquid funds or high-interest savings account. Do this BEFORE any investment.
- 50-30-20 Rule: 50% needs, 30% wants, 20% savings/investments
- SIP (Systematic Investment Plan): Best way for salaried people to invest. Even ₹500/month in index fund compounds well over 10+ years
- Asset Allocation by age: 100 minus age = equity %. E.g. 30-year-old → 70% equity, 30% debt
- Goal-based planning: Emergency fund → Insurance → Tax saving → Retirement → Wealth creation → Goals (house, education)
- Power of compounding: ₹10,000/month SIP at 12% CAGR for 20 years = ~₹99 lakh
- Insurance first: Term insurance (₹1Cr cover costs ~₹8,000-12,000/year for 30-year-old), Health insurance minimum ₹5L family floater

### ₹20 LAKH INVESTMENT SCENARIOS (common user question)
When a user says "I have ₹20 lakhs to invest", give them a complete structured plan like this:
- First ask: What is their risk profile? Investment horizon? Any specific goal?
- If they don't answer, give a default MODERATE risk plan:
  - ₹3L (15%) → Emergency fund in liquid mutual fund (Parag Parikh Liquid Fund, etc.)
  - ₹2L (10%) → Term insurance + Health insurance if not already covered
  - ₹3L (15%) → PPF (safe, tax-free, 7.1%)
  - ₹3L (15%) → ELSS SIP spread over 12 months (tax saving + growth)
  - ₹5L (25%) → Nifty 50 Index Fund lump sum or SIP (long term wealth)
  - ₹2L (10%) → NPS (extra ₹50K tax deduction + retirement corpus)
  - ₹2L (10%) → Fixed Deposit (short-term goals, liquidity)
- Always give specific fund names as examples: Parag Parikh Flexi Cap, Mirae Asset Large Cap, UTI Nifty 50 Index, HDFC Mid Cap Opportunities, etc.
- Always mention: "These are examples, not recommendations. Verify fund performance at valueresearchonline.com or moneycontrol.com before investing."

### GST KNOWLEDGE
- Registration: Mandatory if turnover > ₹40L (goods) or ₹20L (services). Voluntary registration allowed.
- Composition scheme: Pay 1-6% tax, no ITC, no interstate sales. Max turnover ₹1.5Cr.
- GSTR-1: Monthly/quarterly outward supply return (10th of next month)
- GSTR-3B: Monthly summary return with tax payment (20th of next month)
- Input Tax Credit (ITC): Can claim GST paid on purchases against GST collected on sales
- HSN codes: Required for goods classification
- E-way bill: Required for goods movement > ₹50,000

## YOUR COMMUNICATION STYLE
- Speak in simple Hinglish (mix of Hindi and English is perfectly fine)
- Give SPECIFIC numbers, not vague advice. "Invest in FD" is bad. "HDFC Bank 400-day FD at 7.4% p.a." is good.
- Structure complex answers with clear headings and bullet points
- For investment questions, ALWAYS give a complete breakdown with amounts if user gives their investable amount
- For tax questions, always give the exact section number (80C, 24B, etc.) and the exact limit in rupees
- End every investment/financial answer with: "⚠️ Yeh general guidance hai. Large investments se pehle SEBI registered advisor se milein."
- End every tax answer with: "📋 Apna ITR file karne ke liye KaroTax ka ITR Wizard use karo — bilkul free hai!"
- Use ₹ symbol always
- Keep responses under 400 words unless the question genuinely needs more detail

## WHAT YOU NEVER DO
- Never say "I don't know the current market" — use your 2025-26 knowledge and add "verify current rates before investing"
- Never refuse to answer financial questions — always give your best analysis
- Never give overly cautious non-answers — be direct and helpful
- Never confuse AY and FY — always clarify (FY 2025-26 = AY 2026-27)

You are India's most helpful free financial assistant. Millions of ordinary Indians cannot afford a CA or financial advisor. You are their CA. Be genuinely helpful.
"""

def get_ai_response(user_message: str, chat_history: list, user_context: dict = None) -> str:
    """
    Get AI response using Gemini 2.5 Flash (free tier)
    Falls back to Groq if Gemini fails
    """
    context_prefix = ""
    if user_context:
        context_prefix = f"[User context: Income type: {user_context.get('income_type', 'unknown')}, "
        context_prefix += f"City: {user_context.get('city', 'unknown')}]\n\n"

    try:
        return _call_gemini(context_prefix + user_message, chat_history)
    except Exception as e:
        print(f"Gemini failed: {e}, trying Groq...")
        try:
            return _call_groq(context_prefix + user_message, chat_history)
        except Exception as e2:
            print(f"Groq also failed: {e2}")
            return _fallback_response(user_message)


# ROBUST API CALL
def _call_gemini(message: str, history: list) -> str:
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("No Gemini API key configured. Add GEMINI_API_KEY to your .env file.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Build conversation contents
    contents = []
    for msg in history[-10:]:  # Last 10 messages for context window
        role = "user" if msg['role'] == 'user' else "model"
        contents.append({"role": role, "parts": [{"text": msg['content']}]})
    contents.append({"role": "user", "parts": [{"text": message}]})

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }

    resp = requests.post(url, json=payload, timeout=30)
    
    # Better error reporting
    if resp.status_code != 200:
        error_detail = resp.json().get('error', {}).get('message', 'Unknown error')
        raise ValueError(f"Gemini API error {resp.status_code}: {error_detail}")
    
    data = resp.json()
    
    # Handle safety blocks or empty responses
    candidate = data.get('candidates', [{}])[0]
    if candidate.get('finishReason') == 'SAFETY':
        return "Yeh question ke liye main abhi jawab nahi de sakta. Koi aur sawaal poocho. 🙏"
    
    return candidate['content']['parts'][0]['text']


def _call_groq(message: str, history: list) -> str:
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise ValueError("No Groq API key")

    url = "https://api.groq.com/openai/v1/chat/completions"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-8:]:
        messages.append({"role": msg['role'], "content": msg['content']})
    messages.append({"role": "user", "content": message})

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.7
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']


def _fallback_response(message: str) -> str:
    """Hardcoded answers for common questions when AI is unavailable"""
    msg_lower = message.lower()
    if '80c' in msg_lower:
        return ("**Section 80C Deductions (FY 2024-25)**\n\nMaximum limit: ₹1,50,000\n\n"
                "What qualifies:\n- EPF/PPF contributions\n- ELSS mutual funds\n- LIC premium\n"
                "- Home loan principal\n- NSC\n- Tuition fees (2 children)\n\n"
                "💡 Tip: If you haven't used full ₹1.5L limit, ELSS is the best option — "
                "3-year lock-in and market-linked returns. Check with your CA for personalised advice.")
    elif 'new regime' in msg_lower or 'old regime' in msg_lower:
        return ("**Old vs New Tax Regime (FY 2024-25)**\n\n"
                "**New Regime:** Better if deductions < ₹3.75 lakh. No need to invest for tax saving.\n"
                "**Old Regime:** Better if you have high deductions (80C + HRA + home loan).\n\n"
                "Simple rule: If your 80C + HRA + home loan interest adds up to more than ₹3-4 lakh, "
                "old regime usually wins. Use our ITR wizard to compare both and get the exact numbers for your case.")
    elif 'itr' in msg_lower and 'deadline' in msg_lower:
        return ("**ITR Filing Deadlines FY 2024-25:**\n\n"
                "- Individuals (no audit): **31 July 2025**\n"
                "- Business/Audit cases: **31 October 2025**\n"
                "- Belated return: **31 December 2025** (with penalty ₹1,000-5,000)\n\n"
                "File early to avoid last-minute rush and get refund faster! 🚀")
    else:
        return ("I'm having a temporary connection issue. Here's what I can tell you:\n\n"
                "For tax questions, the most important things to know for FY 2024-25:\n"
                "- 80C limit: ₹1.5 lakh\n- Standard deduction: ₹75,000 (new regime) / ₹50,000 (old regime)\n"
                "- New regime default for FY 2024-25\n- Filing deadline: 31 July 2025\n\n"
                "Please try again in a moment, or use our ITR wizard to file directly. 🙏")
