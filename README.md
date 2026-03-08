# 🎓 Dynamisk Penningtvättsutbildning

En AI-driven utbildningsplattform som automatiskt uppdateras med de senaste rapporterna om penningtvätt från pålitliga källor som Finansinspektionen, FATF, Europol och EBA.

## ✨ Funktioner

- ✅ **100% Gratis** - Inga API-kostnader för användare
- ✅ **Automatisk uppdatering** - Ny innehåll varje vecka via GitHub Actions
- ✅ **Obegränsat användare** - Fungerar via GitHub Pages
- ✅ **Dynamiskt innehåll** - Baserat på aktuella rapporter
- ✅ **Flera teman** - Välj specifikt område (kryptovalutor, fastigheter, etc.)
- ✅ **Interaktivt quiz** - 10 frågor per tema med förklaringar

## 🚀 Snabbstart (för att deploya din egen version)

### Steg 1: Forka detta repository
Klicka på "Fork" längst upp till höger på GitHub.

### Steg 2: Skaffa Anthropic API-nyckel
1. Gå till [console.anthropic.com](https://console.anthropic.com)
2. Skapa ett konto (får $5 gratis kredit)
3. Generera en API-nyckel under "API Keys"

### Steg 3: Lägg till API-nyckel i GitHub
1. Gå till ditt forkade repository
2. `Settings` → `Secrets and variables` → `Actions`
3. Klicka `New repository secret`
4. Namn: `ANTHROPIC_API_KEY`
5. Value: Din API-nyckel (sk-ant-...)
6. Klicka `Add secret`

### Steg 4: Aktivera GitHub Pages
1. Gå till `Settings` → `Pages`
2. Under "Source", välj `main` branch
3. Root directory
4. Klicka `Save`

### Steg 5: Kör första gången (manuellt)
1. Gå till `Actions` fliken
2. Välj "Uppdatera Penningtvättsutbildning"
3. Klicka `Run workflow` → `Run workflow`
4. Vänta 2-3 minuter

### Steg 6: Besök din webbplats!
Din utbildning finns nu på:
```
https://[ditt-användarnamn].github.io/[repo-namn]/
```

## 🔄 Automatiska Uppdateringar

GitHub Actions kör automatiskt varje **måndag kl 07:00** och:
- Söker efter nya penningtvättsrapporter
- Genererar nya quiz-frågor
- Uppdaterar webbplatsen automatiskt

Du kan också köra manuellt när som helst via Actions-fliken.

## 💰 Kostnad

- **GitHub Pages**: Gratis (obegränsat)
- **GitHub Actions**: 2000 minuter/månad gratis
- **Anthropic API**: ~$0.10-0.20 per uppdatering
- **Total kostnad per månad**: ~$1-2 (4-5 uppdateringar)

Med $5 gratis kredit = **flera månaders gratis drift!**

## 🛠️ Lokal utveckling

### Kör lokalt
```bash
# Installera dependencies
pip install anthropic

# Sätt API-nyckel
export ANTHROPIC_API_KEY='sk-ant-...'

# Generera data
python generate_data.py

# Starta lokal server
python -m http.server 8000

# Öppna http://localhost:8000 i webbläsaren
```

### Projektstruktur
```
penningtvatt-utbildning/
├── index.html              # Huvudwebbsida
├── generate_data.py        # Python script för datag enerering
├── data/                   # Genererad JSON-data
│   ├── allmän.json
│   ├── kryptovalutor.json
│   ├── fastigheter.json
│   └── last_update.json
├── .github/
│   └── workflows/
│       └── update-data.yml # GitHub Actions workflow
└── README.md
```

## 📝 Lägg till fler teman

Redigera `generate_data.py` och lägg till i `THEMES` dictionary:

```python
THEMES = {
    "allmän": "allmän penningtvätt",
    "kryptovalutor": "kryptovalutor och digitala tillgångar",
    "ditt-tema": "beskrivning av ditt tema"  # ← Lägg till här
}
```

Uppdatera även `index.html` med ett nytt `<option>` i select-elementet.

## 🔒 Säkerhet

- API-nyckeln lagras säkert i GitHub Secrets
- Exponeras aldrig för slutanvändare
- Endast tillgänglig för GitHub Actions

## 📜 Licens

MIT License - Fri att använda, modifiera och distribuera.

## 🤝 Bidra

Pull requests välkomnas! För större ändringar, öppna gärna en issue först.

## 📧 Support

Om du stöter på problem:
1. Kontrollera att API-nyckeln är korrekt satt i Secrets
2. Kolla Actions-loggen för felmeddelanden
3. Öppna en issue på GitHub

## 🌟 Credits

Skapad med Claude AI från Anthropic.
Data från Finansinspektionen, FATF, Europol, EBA och andra myndigheter.

---

**Uppdateras automatiskt varje vecka med färska rapporter!** 🚀
