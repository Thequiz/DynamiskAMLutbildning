# 🚀 SNABBSTART - 10 Minuter till Färdig Utbildning

## Vad Du Får
✅ Helt automatisk penningtvättsutbildning  
✅ Uppdateras varje måndag med nya rapporter  
✅ Gratis för obegränsat antal användare  
✅ Färdig lösning - bara ladda upp!  

---

## Steg 1️⃣ : Skapa GitHub Repository (2 min)

1. Gå till https://github.com och logga in (skapa konto om du inte har)
2. Klicka på ➕ → "New repository"
3. Namn: `penningtvatt-utbildning`
4. Välj: **Public** (viktigt!)
5. Klicka "Create repository"

---

## Steg 2️⃣ : Ladda upp Alla Filer (2 min)

**Metod A - Via Webbläsare (enklast):**
1. I ditt nya repository, klicka "uploading an existing file"
2. Dra och släpp ALLA filer från mappen du fick:
   - `.github/workflows/update-content.yml`
   - `data/quiz_data.json`
   - `generate_content.py`
   - `index.html`
   - `README.md`
   - `requirements.txt`
   - `.gitignore`
3. Scrolla ner, klicka "Commit changes"

**Metod B - Via Git CLI:**
```bash
git clone https://github.com/DITT-ANVÄNDARNAMN/penningtvatt-utbildning.git
cd penningtvatt-utbildning
# Kopiera alla filer hit
git add .
git commit -m "Initial commit"
git push
```

---

## Steg 3️⃣ : Skaffa API-Nyckel (3 min)

1. Gå till https://console.anthropic.com
2. Klicka "Sign Up" och skapa konto (gratis)
3. När du är inloggad, klicka "API Keys"
4. Klicka "Create Key"
5. Kopiera nyckeln (börjar med `sk-ant-...`)

💰 **Kostnad:** ~$1-2/månad för veckovisa uppdateringar

---

## Steg 4️⃣ : Lägg in API-Nyckeln (1 min)

1. I ditt GitHub repository, klicka "Settings"
2. Välj "Secrets and variables" → "Actions"
3. Klicka "New repository secret"
4. Name: `ANTHROPIC_API_KEY`
5. Secret: Klistra in din nyckel
6. Klicka "Add secret"

---

## Steg 5️⃣ : Aktivera GitHub Pages (1 min)

1. I repository, klicka "Settings"
2. Scrolla ner till "Pages" (vänster meny)
3. Under "Source": Välj "main" branch
4. Klicka "Save"

---

## Steg 6️⃣ : Första Körningen (1 min + vänta)

1. Klicka på "Actions" (överst i repository)
2. Välj "Uppdatera Utbildningsinnehåll"
3. Klicka "Run workflow" → "Run workflow"
4. Vänta 5-10 minuter medan AI genererar innehållet

---

## 🎉 KLART!

Din utbildning finns nu på:
```
https://DITT-ANVÄNDARNAMN.github.io/penningtvatt-utbildning/
```

### Dela länken med alla som ska använda utbildningen!

---

## ⚙️ Automatik

- **Veckovis uppdatering:** Varje måndag kl 07:00 svensk tid
- **Manuell uppdatering:** Actions → Run workflow när du vill
- **Ingen underhåll:** Allt sker automatiskt!

---

## 💡 Tips

- **Första gången tar längst** - Därefter går det snabbare
- **Kolla "Actions"-fliken** - Se när uppdateringar körs
- **Gratis GitHub-limit:** 2000 minuter/månad (mer än tillräckligt)

---

## ❓ Problem?

### "Workflow failed"
→ Kontrollera att API-nyckeln är rätt i Secrets

### "Sidan laddar inte"
→ Vänta 10 min, GitHub Pages tar lite tid första gången

### "No questions available"
→ Kör workflow manuellt en gång till

---

## 📧 Behöver Hjälp?

Öppna ett "Issue" i ditt repository eller kontakta mig!

**Lycka till!** 🚀
