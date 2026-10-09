# Guide 01 — How to run and use the app

For the volunteer (your sister). No coding needed.

---

## A. One-time setup on the laptop (10 min)

Already done on this Mac (2026-10-08). On a new laptop:

1. Install Python 3.11 or newer — macOS: `brew install python`; Windows:
   python.org → Download → tick **"Add python.exe to PATH"**.
2. Copy the whole `career guidance ai` folder to the laptop.
3. Open Terminal in that folder and run:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4. **AI messages (optional but recommended):** copy
   `.streamlit/secrets.toml.example` → `.streamlit/secrets.toml`, paste your
   Groq key in `GROQ_API_KEY`, delete the Supabase lines. Without a key the app
   still works and shows a ready-made message.

---

## B. Start the app (every time)

```bash
cd ~/Projects/"career guidance ai"
source .venv/bin/activate
streamlit run app.py
```

The browser opens `http://localhost:8501` by itself. Keep the Terminal window
open while surveying; closing it stops the app.

**Use a phone as the screen:** connect the laptop and phone to the same
Wi-Fi/hotspot, then open the **Network URL** printed in Terminal
(looks like `http://192.168.x.x:8501`) on the phone.

**Stop:** press `Ctrl + C` in Terminal.

---

## C. Surveying a student (3–5 min each)

1. **Start screen:** type the child's **first name only**, choose Class,
   School, and the language the child is comfortable in → **Start**.
2. **10 questions:** one per screen. Read aloud if needed; the child taps an
   answer and the next question appears. **← Back** fixes a wrong tap.
   - None of the options fit? The child types their own answer in the box
     under the options (any language, even Hinglish) → **Next →**. The AI
     reads it and scores it. Without internet a typed answer scores nothing,
     so prefer tapping an option when offline.
3. **Result:** two best-fit career areas with % match, careers for the route
   the child picked, and a personal advice message. Let the child read it or
   take a photo of the screen.
4. Tap **Next student**. School and language stay filled in.

Responses save automatically. Nothing to click.

---

## D. Survey Summary (for the report)

On the start screen, tap **Volunteer: Survey summary** (bottom). **Back to
survey** returns. (There's no sidebar, so children can't wander in.)

- Total students, schools, charts of career areas, routes, by class
- Full table of responses, newest first
- **Download CSV** → opens in Excel

**Deleting a mistaken or fake entry:** in *All responses*, tick the box at the
left of each bad row → **Delete N selected** → check the names in the popup →
**Yes, delete**. Charts update straight away. There's no undo, so download
the CSV first if unsure.

Screenshot the charts for the college report.

---

## E. Where the data is

| Mode | Location |
|---|---|
| Laptop | `data/responses.csv` in the project folder |
| Hosted online (Guide 02) | Supabase table `responses` |

At the end of each survey day, download the CSV and keep a copy on a pen drive
or private Google Drive. **Don't share it publicly** — it has children's names.

Delete `data/responses.csv` after any practice run so test answers don't mix
with real ones.

---

## F. Survey day checklist

- [ ] School permission taken
- [ ] Laptop charged + charger; phone hotspot with data
- [ ] App started and one practice student done at home that morning
- [ ] Practice row removed (delete the CSV, or delete the row in Supabase)
- [ ] Internet gone? Carry on — results still appear (ready-made message instead of AI)
- [ ] End of day: Download CSV and back it up

---

## G. Changing questions or careers

Edit the files in `data/` with any text editor (VS Code recommended), save,
and refresh the browser. Keep the punctuation (`"` `,` `{ }`) exactly as it is.

| To change | File |
|---|---|
| A question or answer text (English/Marathi/Hindi) | `data/questions.json` |
| Which career area an answer points to | `points` in `data/questions.json` |
| Career names, courses, advice | `data/careers.json` |
| Buttons and labels | `data/ui_text.json` |
| Colours, fonts, spacing | `style.css`, `.streamlit/config.toml` (theme) |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: streamlit` | Run `source .venv/bin/activate` first |
| Phone can't open Network URL | Same Wi-Fi on both? Mac may ask to allow incoming connections → Allow |
| Advice is always the short ready-made one | No internet, or Groq key missing/wrong in `.streamlit/secrets.toml` |
| Page shows a red error after editing JSON | A comma or quote is missing; undo the last edit |
