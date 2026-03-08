#!/usr/bin/env python3
"""
Penningtvättsutbildning - Data Generator (Haiku + Webbsök)
Använder den billigaste modellen (Haiku) för att utföra dyra sökningar.
"""

import os
import json
import sys
import time
from datetime import datetime
from typing import List, Dict, Any

# Kräver: pip install anthropic
try:
    import anthropic
except ImportError:
    print("❌ Anthropic library saknas. Installera med: pip install anthropic")
    sys.exit(1)

# Teman att generera innehåll för
THEMES = {
    "allmän": "Monero"
}

def generate_theme_data(client: anthropic.Anthropic, theme_key: str, theme_name: str) -> Dict[str, Any]:
    """Genererar data med Webbsök men med den billigaste modellen (Haiku)"""
    
    # Haiku är betydligt billigare än Sonnet för Webbsök
    MODEL = "claude-3-5-haiku-20260210"
    
    print(f"🌐 Startar WEBBSÖK för tema: {theme_name} (Modell: Haiku)")
    
    # Steg 1: Sök efter rapporter på webben
    # Vi sänker max_tokens till 2000 för att begränsa hur mycket webbinnehåll den läser in
    search_message = client.messages.create(
        model=MODEL,
        max_tokens=2000, 
        messages=[{
            "role": "user",
            "content": f"""Använd web_search för att hitta 3-5 aktuella rapporter (senaste 12 mån) om penningtvätt via "{theme_name}". 
            Fokusera på FI, FATF och Europol. 
            
            Returnera ENDAST ett JSON-objekt med denna struktur:
            {{
                "reports": [
                    {{"title": "...", "source": "...", "url": "...", "snippet": "...", "date": "..."}}
                ]
            }}"""
        }],
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search"
        }]
    )
    
    # Extrahera texten (Haiku kan ibland skicka text i block)
    reports_text = ""
    for block in search_message.content:
        if block.type == "text":
            reports_text += block.text
    
    # Rensa JSON-strängen
    reports_text = reports_text.replace("```json", "").replace("```", "").strip()
    
    try:
        reports_data = json.loads(reports_text)
    except Exception as e:
        print(f"  ⚠️ JSON-fel vid sökning, använder enkel fallback: {e}")
        reports_data = {"reports": []}

    # Steg 2: Generera frågor baserat på sökresultaten
    print(f"  💡 Skapar quiz-frågor baserat på hittad webbdata...")
    quiz_message = client.messages.create(
        model=MODEL,
        max_tokens=2500,
        messages=[{
            "role": "user",
            "content": f"""Skapa 10 pedagogiska frågor på svenska om "{theme_name}" baserat på denna data:
            {json.dumps(reports_data)}
            
            Returnera som JSON:
            {{ "questions": [ {{ "question": "...", "options": [], "correctAnswer": 0, "explanation": "..." }} ] }}"""
        }]
    )
    
    quiz_text = quiz_message.content[0].text.replace("```json", "").replace("```", "").strip()
    
    try:
        quiz_json = json.loads(quiz_text)
        questions = quiz_json.get("questions", [])
    except:
        questions = []

    return {
        "theme": theme_name,
        "generated_date": datetime.now().isoformat(),
        "reports": reports_data.get("reports", []),
        "questions": questions
    }

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY saknas!")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    os.makedirs("data", exist_ok=True)
    
    for theme_key, theme_name in THEMES.items():
        try:
            data = generate_theme_data(client, theme_key, theme_name)
            with open(f"data/{theme_key}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ Sparad: data/{theme_key}.json\n")
            time.sleep(5) # Liten paus för att undvika Rate Limits
        except Exception as e:
            print(f"  ❌ Fel vid {theme_name}: {e}")

if __name__ == "__main__":
    main()
