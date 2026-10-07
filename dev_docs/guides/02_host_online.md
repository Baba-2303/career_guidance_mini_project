# Guide 02 — Host the app online (free)

Gives a public link (`https://<name>.streamlit.app`) your sister opens on any
phone, with no laptop needed. All three services are free.

| Service | Role |
|---|---|
| GitHub | Holds the code (not the data) |
| Streamlit Community Cloud | Runs the app |
| Supabase | Stores responses permanently (Streamlit Cloud's own disk resets) |

Rule 9: Claude doesn't push. You run the git commands.

---

## Step 1 — Supabase database (10 min)

1. https://supabase.com → Sign in with GitHub → **New project**.
   Name `career-guidance`, region **Mumbai (ap-south-1)**, set any DB password.
2. Left menu → **SQL Editor** → paste all of `supabase_table.sql` → **Run**.
   Expect "Success. No rows returned".
3. **Project Settings → API Keys**: copy the **Project URL** and a **secret
   key** (`sb_secret_…`; if only legacy keys are shown, use `service_role`).
   Never use this key in a browser or commit it.

## Step 2 — Push code to GitHub

Create an **empty private repo** on github.com named `career-guidance-ai`, then:

```bash
cd ~/Projects/"career guidance ai"
git init
git add .
git status
```
`git status` must **not** list `.streamlit/secrets.toml`, `data/responses.csv`
or `.venv` (they're in `.gitignore`). If one shows, stop and ask.

```bash
git commit -m "Career guidance survey app"
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/career-guidance-ai.git
git push -u origin main
```

## Step 3 — Deploy on Streamlit Community Cloud

1. https://share.streamlit.io → sign in with GitHub → **Create app** →
   "Deploy a public app from GitHub".
2. Repo `career-guidance-ai`, branch `main`, main file `app.py`.
   Pick a custom URL, e.g. `career-guidance-virar`.
3. **Advanced settings → Python 3.12**, and in **Secrets** paste:

```toml
GROQ_API_KEY = "<PASTE_GROQ_KEY>"
GROQ_MODEL = "openai/gpt-oss-120b"
SUMMARY_PASSWORD = "<CHOOSE_A_PASSWORD>"
SUPABASE_URL = "https://<PROJECT_REF>.supabase.co"
SUPABASE_KEY = "<SUPABASE_SECRET_KEY>"
```
4. **Deploy**. First build takes ~2–3 min.

## Verify

1. Open the app link → do one test student.
2. Supabase → **Table Editor → responses** → the row is there.
3. App → Survey Summary → password → shows 1 student.
4. Delete the test row in Supabase (row checkbox → Delete).

If the result page shows "online database unreachable", the Supabase URL/key
in Secrets is wrong — the row went to the temporary disk only.

## Good to know

| Fact | What to do |
|---|---|
| Streamlit apps sleep after ~12 h unused | Open the link the morning of survey day; "Wake up" takes ~30 s |
| Supabase free projects pause after 7 days unused | Supabase dashboard → **Restore project** before survey day |
| The app link is public | Fine — no data is visible without the summary password. Don't post the link publicly |
| Updating the app | Edit locally → `git add .` → `git commit -m "<what changed>"` → `git push`; Streamlit redeploys itself |

## Rollback

- Bad update: `git revert HEAD` then `git push`.
- Take it offline: Streamlit dashboard → app ⋮ → **Delete**. Data stays in Supabase.
