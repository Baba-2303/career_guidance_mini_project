# Project Rules — Career Guidance AI

Working rules for AI agents and humans on this project. Adapted (relaxed) from
`virar_veggies_bk/dev_docs/project_rules.md`. This is a college field-work
project, not a product: ~100 students, one survey tenure, then done.

Add new rules at the bottom, dated. Don't delete a rule silently — strike it
through and mark it `SUPERSEDED [date]`.

**Companion documents:**

| File | Purpose |
|---|---|
| `dev_docs/project_description_&_requirements.md` | What we're building, the 10 questions, scoring, career data |
| `dev_docs/project_rules.md` (this file) | How we work |
| `dev_docs/guides/01_run_and_use.md` | Run the app and survey students |
| `dev_docs/guides/02_host_online.md` | Free hosting: GitHub + Streamlit Cloud + Supabase |
| `CLAUDE.md` / `AGENTS.md` | Load the two files above every session |

---

## Rule 0 — No secrets in committed files

API keys (Groq, Supabase) live only in `.streamlit/secrets.toml`
(gitignored) or Streamlit Cloud's Secrets box. Never put them in code, docs,
commits or chat. `secrets.toml.example` holds
placeholders only.

## Rule 1 — Student data is private. Collect the minimum.

The users are minors. Collect only: first name, class, school name, answers,
result. **Never** collect surname, phone, address, photo, caste, religion or
family income.

- `data/responses.csv` is gitignored; the Supabase table has RLS on with no
  policies (server secret key only). Neither is ever shared publicly.
- Summary page is locked by `SUMMARY_PASSWORD` when hosted.
- Test data is fabricated ("Test Student 1"), never a real child's answers.
- Only first name, class and cluster results go to the LLM. Nothing else.
- Get the school's permission before survey day.

## Rule 2 — Single source of truth; data over hardcoding

| Concern | Lives in |
|---|---|
| The 10 questions, options, translations | `data/questions.json` |
| Option → cluster points | `data/questions.json` (`points` per option) |
| Careers, routes, next steps per cluster | `data/careers.json` |
| Scoring logic | `scoring.py` — one function, used by app and summary page |
| UI labels (en/mr/hi) | `data/ui_text.json` |
| LLM model name | `.streamlit/secrets.toml` (`GROQ_MODEL`) — swap models without code edits |
| Where responses are saved | `storage.py` only |

Changing a question or a career = edit JSON, not Python.

## Rule 3 — Build the minimum, then stop

Simplest thing that works on survey day. No login, no self-run database, no
admin panel, no React. When a nicety is skipped on purpose, say so in one line.

## Rule 4 — The app must work without internet

School Wi-Fi can't be trusted. Scoring is local and always works. The LLM only
writes the friendly explanation; if the call fails or times out (8 s), show
the offline template from `careers.json`. The child always gets a result.

## Rule 5 — The AI never invents careers

The LLM may only mention careers from `careers.json` for the student's top
clusters. It explains and encourages; it does not decide. Every result page
shows: *"This is guidance, not a final decision. Talk to your teachers and
parents."*

## Rule 6 — Docs stay terse and current

No filler. Tables and bullets over prose. If a decision changes, fix the doc
the same session and mark old text `SUPERSEDED [date]`.

## Rule 7 — Comments only for non-obvious WHY

Default to no comments. Naming explains WHAT.

## Rule 8 — Hand-off by default

Claude writes the guide and the commands; the human runs them and pastes
output. Exception: the user says "do it directly" for a given request.
Guides are disposable — delete one once its job is done (move any lasting
fact into the requirements doc first).

## Rule 9 — Git: Claude reads, the human writes

Claude may run `git status/log/diff`. `add`, `commit`, `push`, branches —
hand over the exact commands instead.

## Rule 10 — Design: plain, big, phone-friendly

Flat and readable. Large text and buttons (children, shared phone/laptop).
No gradients, no glassy cards, no emoji-as-icons. One question per screen.

<!-- Add new rules below this line, numbered and dated. -->
