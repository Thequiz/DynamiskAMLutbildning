#!/usr/bin/env python3
"""
Penningtvättsutbildning - Data Generator
Söker efter aktuella rapporter och genererar quiz-frågor via Anthropic API
"""

import os
import json
import sys
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
    "allmän": "fastigheter"
}

def generate_theme_data(client: anthropic.Anthropic, theme_key: str, theme_name: str) -> Dict[str, Any]:
    """Genererar rapporter och frågor för ett specifikt tema"""
    
    print(f"📚 Genererar innehåll för tema: {theme_name}")
    
    # Steg 1: Sök rapporter
    print("  🔍 Söker efter aktuella rapporter...")
    search_message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Sök efter aktuella, seriösa rapporter om PENNINGTVÄTT med fokus på: "{theme_name}"

Sök rapporter från de senaste 12 månaderna från pålitliga källor som:
- Finansinspektionen (FI)
- FATF (Financial Action Task Force)  
- Europol
- EBA (European Banking Authority)
- FIU (Financial Intelligence Units)
- Andra pålitliga myndigheter och organisationer

Hitta rapporter som specifikt beskriver metoder, modus operandi, och tillvägagångssätt 
relaterade till "{theme_name}".

Returnera ENDAST JSON med följande struktur:
{{
    "theme": "{theme_name}",
    "reports": [
        {{
            "title": "Rapportens titel",
            "source": "Källa/organisation",
            "url": "URL till rapporten",
            "snippet": "Kort beskrivning av rapportens innehåll (2-3 meningar)",
            "date": "Publiceringsdatum",
            "key_methods": ["Metod 1", "Metod 2", "Metod 3"]
        }}
    ]
}}

Returnera minst 3-5 rapporter. ENDAST JSON, ingen annan text."""
        }],
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search"
        }]
    )
    
    # Extrahera text från svaret
    reports_text = ""
    for block in search_message.content:
        if block.type == "text":
            reports_text += block.text
    
    # Rensa och parse JSON
    reports_text = reports_text.replace("```json", "").replace("```", "").strip()
    
    try:
        reports_data = json.loads(reports_text)
    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON parse fel, använder fallback data: {e}")
        reports_data = {
            "theme": theme_name,
            "reports": [{
                "title": f"Penningtvätt genom {theme_name} - Aktuell analys",
                "source": "Finansinspektionen",
                "url": "https://www.fi.se",
                "snippet": f"Analys av penningtvättsrisker relaterade till {theme_name}",
                "date": "2024",
                "key_methods": ["Typologi 1", "Typologi 2", "Varningssignaler"]
            }]
        }
    
    print(f"  ✓ Hittade {len(reports_data.get('reports', []))} rapporter")
    
    # Steg 2: Generera quiz-frågor
    print("  💡 Genererar quiz-frågor...")
    quiz_message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Baserat på följande rapporter om "{theme_name}", skapa 10 utbildningsfrågor på svenska om konkreta metoder och tillvägagångssätt:

{json.dumps(reports_data['reports'], indent=2, ensure_ascii=False)}

Alla frågor MÅSTE vara direkt relaterade till temat "{theme_name}".

Skapa frågor som testar förståelse av:
- Specifika penningtvättsmetoder inom {theme_name}
- Varningssignaler (red flags) specifika för {theme_name}
- Aktuella trender och modus operandi inom {theme_name}
- Regelverket och ansvar relaterat till {theme_name}
- Praktiska fall och scenarion från {theme_name}

Returnera ENDAST JSON med följande struktur:
{{
    "theme": "{theme_name}",
    "questions": [
        {{
            "question": "Frågetexten här (måste vara relaterad till {theme_name})",
            "options": ["Alternativ A", "Alternativ B", "Alternativ C", "Alternativ D"],
            "correctAnswer": 0,
            "explanation": "Förklaring av det korrekta svaret och varför det är viktigt inom {theme_name} (2-3 meningar)"
        }}
    ]
}}

Alla frågor ska vara på svenska och baserade på verklig information från rapporterna.
ENDAST JSON, ingen annan text."""
        }]
    )
    
    # Extrahera quiz data
    quiz_text = ""
    for block in quiz_message.content:
        if block.type == "text":
            quiz_text += block.text
    
    quiz_text = quiz_text.replace("```json", "").replace("```", "").strip()
    
    try:
        quiz_data = json.loads(quiz_text)
        questions = quiz_data.get("questions", [])
        print(f"  ✓ Genererade {len(questions)} frågor")
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Quiz JSON parse fel: {e}")
        questions = []
    
    # Kombinera data
    return {
        "theme": theme_name,
        "generated_date": datetime.now().isoformat(),
        "reports": reports_data.get("reports", []),
        "questions": questions
    }

def main():
    """Huvudfunktion - genererar data för alla teman"""
    
    print("🚀 Penningtvättsutbildning - Data Generator")
    print("=" * 60)
    
    # Hämta API-nyckel från miljövariabel
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY miljövariabel saknas!")
        print("   Sätt den med: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)
    
    # Skapa Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Skapa data mapp
    os.makedirs("data", exist_ok=True)
    
    # Generera data för varje tema
    for theme_key, theme_name in THEMES.items():
        try:
            theme_data = generate_theme_data(client, theme_key, theme_name)
            
            # Spara till JSON-fil
            output_file = f"data/{theme_key}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, ensure_ascii=False, indent=2)
            
            print(f"  💾 Sparad till: {output_file}")
            print()
            
        except Exception as e:
            print(f"  ❌ Fel vid generering av {theme_name}: {e}")
            print()
            continue
    
    # Spara senaste uppdateringsdatum
    update_info = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "themes": list(THEMES.keys())
    }
    
    with open("data/last_update.json", 'w', encoding='utf-8') as f:
        json.dump(update_info, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print("✅ Data generering klar!")
    print(f"📅 Senast uppdaterad: {update_info['date']}")

if __name__ == "__main__":
    main()
