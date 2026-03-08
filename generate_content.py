#!/usr/bin/env python3
"""
Genererar utbildningsinnehåll om penningtvätt genom att söka aktuella rapporter
och skapa quiz-frågor med AI.
"""

import os
import json
import requests
from datetime import datetime

# API-nycklar från GitHub Secrets (miljövariabler)
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

# Teman som ska genereras
THEMES = {
    'allmän': 'allmän penningtvätt',
    'kryptovalutor': 'kryptovalutor och digitala tillgångar',
    'fastigheter': 'fastighetsmarknaden',
    'kontanthantering': 'kontantintensiva verksamheter',
    'skalbolag': 'skalbolag och komplex ägarstruktur',
    'handelsbaserad': 'handelsbaserad penningtvätt (TBML)',
    'casinon': 'casinon och spelverksamhet',
    'konstmarknad': 'konst, antikviteter och lyxvaror',
    'hawala': 'informella värdeöverföringssystem (Hawala)',
    'korruption': 'korruptionsrelaterad penningtvätt',
    'organiserad-brottslighet': 'organiserad brottslighet',
    'narkotikahandel': 'narkotikahandel',
    'terrorismfinansiering': 'terrorismfinansiering',
    'skattebrott': 'skattebrott och undandragande',
    'banker': 'bankernas roll och ansvar',
    'virtuella-banker': 'neobanker och fintech',
    'smurfing': 'smurfing och strukturering',
    'tredjepartsbetalningar': 'tredjepartsbetalningar'
}


def call_anthropic_api(messages, use_search=False):
    """
    Anropar Anthropic API med Claude.
    """
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4000,
        "messages": messages
    }
    
    if use_search:
        payload["tools"] = [{
            "type": "web_search_20250305",
            "name": "web_search"
        }]
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def search_reports(theme_name):
    """
    Söker efter aktuella rapporter om ett specifikt penningtvättstema.
    """
    print(f"🔍 Söker rapporter om: {theme_name}")
    
    messages = [{
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

Returnera resultatet som JSON med följande struktur:
{{
    "theme": "{theme_name}",
    "reports": [
        {{
            "title": "Rapportens titel",
            "source": "Källa/organisation",
            "url": "URL till rapporten",
            "snippet": "Kort beskrivning av rapportens innehåll",
            "date": "Publiceringsdatum",
            "key_methods": ["Metod 1", "Metod 2", "Metod 3"]
        }}
    ]
}}

Returnera ENDAST JSON, ingen annan text."""
    }]
    
    result = call_anthropic_api(messages, use_search=True)
    
    # Extrahera textinnehållet
    text_content = ""
    for content in result.get("content", []):
        if content.get("type") == "text":
            text_content += content.get("text", "")
    
    # Rensa bort markdown-kodblock
    text_content = text_content.replace("```json", "").replace("```", "").strip()
    
    try:
        reports_data = json.loads(text_content)
        print(f"✅ Hittade {len(reports_data.get('reports', []))} rapporter")
        return reports_data
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON-parsningsfel: {e}")
        # Returnera minimal fallback-data
        return {
            "theme": theme_name,
            "reports": [{
                "title": f"Penningtvätt genom {theme_name} - Aktuell riskanalys",
                "source": "Finansinspektionen",
                "url": "https://www.fi.se",
                "snippet": f"Analys av penningtvättsrisker relaterade till {theme_name}",
                "date": datetime.now().strftime("%Y"),
                "key_methods": ["Typologi 1", "Typologi 2", "Varningssignaler"]
            }]
        }


def generate_questions(theme_name, reports_data):
    """
    Genererar quiz-frågor baserat på rapporter.
    """
    print(f"💡 Genererar frågor om: {theme_name}")
    
    messages = [{
        "role": "user",
        "content": f"""Baserat på följande rapporter om penningtvätt med fokus på "{theme_name}", 
skapa 10 utbildningsfrågor på svenska om konkreta metoder och tillvägagångssätt:

{json.dumps(reports_data.get('reports', []), ensure_ascii=False, indent=2)}

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
            "explanation": "Förklaring av det korrekta svaret och varför det är viktigt inom {theme_name}"
        }}
    ]
}}

Alla frågor ska vara på svenska och baserade på verklig information från rapporterna."""
    }]
    
    result = call_anthropic_api(messages, use_search=False)
    
    # Extrahera textinnehållet
    text_content = ""
    for content in result.get("content", []):
        if content.get("type") == "text":
            text_content += content.get("text", "")
    
    # Rensa bort markdown-kodblock
    text_content = text_content.replace("```json", "").replace("```", "").strip()
    
    try:
        questions_data = json.loads(text_content)
        print(f"✅ Genererade {len(questions_data.get('questions', []))} frågor")
        return questions_data
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON-parsningsfel: {e}")
        return None


def main():
    """
    Huvudfunktion som genererar innehåll för alla teman.
    """
    if not ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY saknas i miljövariabler!")
        exit(1)
    
    print("🚀 Startar innehållsgenerering...")
    print(f"📅 Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Antal teman: {len(THEMES)}")
    print("-" * 60)
    
    all_data = {
        "generated_at": datetime.now().isoformat(),
        "themes": {}
    }
    
    for theme_key, theme_name in THEMES.items():
        print(f"\n{'='*60}")
        print(f"📌 Bearbetar tema: {theme_name}")
        print(f"{'='*60}")
        
        try:
            # Sök rapporter
            reports_data = search_reports(theme_name)
            
            # Generera frågor
            questions_data = generate_questions(theme_name, reports_data)
            
            if questions_data:
                # Kombinera rapporter och frågor
                all_data["themes"][theme_key] = {
                    "name": theme_name,
                    "reports": reports_data.get("reports", []),
                    "questions": questions_data.get("questions", [])
                }
                print(f"✅ Tema '{theme_name}' klart!")
            else:
                print(f"⚠️  Kunde inte generera frågor för '{theme_name}'")
        
        except Exception as e:
            print(f"❌ Fel vid bearbetning av '{theme_name}': {e}")
            continue
    
    # Spara till JSON-fil
    output_file = "data/quiz_data.json"
    os.makedirs("data", exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ Innehållsgenerering klar!")
    print(f"📁 Data sparad till: {output_file}")
    print(f"📊 Totalt antal teman: {len(all_data['themes'])}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
