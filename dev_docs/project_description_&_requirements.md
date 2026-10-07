# Career Guidance AI — Description & Requirements

**Last updated:** 2026-10-08

College field-work project (topic #37: *Online Career Guidance Portal for
Underprivileged Students*). On survey day the student volunteer visits a local
school, asks each child 10 questions on a laptop/phone, and the app predicts
the child's best-fit career areas and gives simple, realistic guidance.

| Item | Value |
|---|---|
| Users | School children, Class 8–10, low-income families |
| Operator | The volunteer (reads questions aloud if needed) |
| Volume | ≤100 students over the whole project |
| Device | One laptop (or phone in browser), phone hotspot for internet |
| Languages | Questions: English + Marathi/Hindi labels. Result: child's choice |

---

## How the "AI" works

Two parts. Present both in the college report.

1. **Prediction — rule-based expert system (offline).** Each answer option
   adds points to one or two of 6 career clusters. Highest two clusters =
   prediction. Question 10 picks the study route (short/medium/long).
   Transparent, explainable, works without internet.
2. **Guidance — LLM (online).** An open-weight model, OpenAI gpt-oss-120b (via Groq free
   API) turns the result into a short, warm, personalised message in the
   child's language, using only careers from our data file.

Why not train an ML model: no labelled data exists, and 100 rows is too few
to train on. The collected responses could be the dataset for a future
project — mention this in the report's "Future scope".

---

## Flow

```
Start → Profile (first name, class, school, result language)
      → Q1 … Q10 (one per screen, tap an option)
      → Result: top 2 career areas + match % + careers for chosen route
                + AI message (or offline message) + disclaimer
      → Saved to data/responses.csv → "Next student" button
```

**Typed answers [2026-10-08]:** every question also has "Or type your own
answer". Typed answers are stored as option `-1` + text in `typed_answers`
(JSON). At the end, one AI call (`classify_typed`) maps each to ≤2 clusters
(1–2 pts) or, for Q10, a route; output is validated, anything invalid scores
0. Offline → typed answers score 0. Typed text is also passed to the
guidance message so the AI responds to the child's own words.

**Design [2026-10-08]:** app named **Disha · दिशा**. Mukta font (Latin +
Devanagari), white answer cards, coloured card per cluster (`color` in
`careers.json`), career chips, advice panel, free-help links. No sidebar;
volunteer reaches the summary via a link on the start screen.

Separate page **Survey Summary**: total students, bar chart of top cluster
counts, route split, CSV download — for the college report.

---

## The 6 career clusters

| Code | Name | Simple description |
|---|---|---|
| HEALTH | Science & Health | Caring for people, body, plants, animals |
| TECH | Technology & Engineering | Computers, machines, building and solving |
| BIZ | Business & Commerce | Money, selling, running a shop or company |
| ARTS | Creative Arts & Media | Drawing, design, music, videos, fashion |
| SERVE | Teaching & Public Service | Teaching, helping society, government jobs |
| SKILL | Hands-on Skills | Repairing, cooking, beauty, trades (ITI) |

---

## The 10 questions

Points: `2` = primary match, `1` = secondary. Q10 is not scored.

**Q1. Which subject do you enjoy the most?**
| Option | Points |
|---|---|
| Science | HEALTH 2, TECH 1 |
| Maths | TECH 2, BIZ 1 |
| Languages / History / Civics | SERVE 2, ARTS 1 |
| Drawing / Music / Craft | ARTS 2, SKILL 1 |
| Work Experience / PE / practical work | SKILL 2 |

**Q2. What do you like doing in your free time?**
| Option | Points |
|---|---|
| Drawing, dancing, singing or making videos | ARTS 2 |
| Opening or fixing gadgets | TECH 2, SKILL 1 |
| Helping at a shop, counting money | BIZ 2 |
| Reading about the body, animals or plants | HEALTH 2 |
| Teaching younger kids, helping neighbours | SERVE 2 |
| Cooking, stitching or building things | SKILL 2, ARTS 1 |

**Q3. A neighbour needs help. Which problem would you jump in to solve?**
| Option | Points |
|---|---|
| Someone is sick | HEALTH 2, SERVE 1 |
| The fan or phone stopped working | SKILL 2, TECH 1 |
| Planning the budget for a festival | BIZ 2 |
| Decorating or making a poster | ARTS 2 |
| A child can't understand homework | SERVE 2 |

**Q4. Where would you like to work when you grow up?**
| Option | Points |
|---|---|
| Hospital or laboratory | HEALTH 2 |
| Office with computers | TECH 2, BIZ 1 |
| My own shop or business | BIZ 2 |
| Studio, stage or film set | ARTS 2 |
| School, police station or government office | SERVE 2 |
| Workshop, garage, kitchen or salon | SKILL 2 |

**Q5. Your friends say you are good at…**
| Option | Points |
|---|---|
| Taking care of people | HEALTH 2, SERVE 1 |
| Solving puzzles and maths | TECH 2 |
| Talking and convincing people | BIZ 2 |
| Coming up with new ideas | ARTS 2 |
| Explaining things and leading the group | SERVE 2 |
| Making or repairing things with hands | SKILL 2 |

**Q6. Which videos would you watch for an hour?**
| Option | Points |
|---|---|
| How the human body works, doctors | HEALTH 2 |
| Gadgets, robots, coding | TECH 2 |
| Success stories of business people | BIZ 2 |
| Music, dance, art, films | ARTS 2 |
| Stories of brave officers, teachers, social workers | SERVE 2 |
| Cooking, DIY, repair | SKILL 2 |

**Q7. In 10 years, what would make you proudest?**
| Option | Points |
|---|---|
| I helped people get healthy | HEALTH 2 |
| I built or invented something | TECH 2 |
| I run my own business | BIZ 2 |
| People know me for my art | ARTS 2 |
| I served my village or city | SERVE 2 |
| I mastered a skill and everyone calls me for it | SKILL 2 |

**Q8. What do you like working with most?**
| Option | Points |
|---|---|
| People | SERVE 2, HEALTH 1 |
| Living things — plants, animals, body | HEALTH 2 |
| Machines and tools | SKILL 2, TECH 1 |
| Numbers and money | BIZ 2, TECH 1 |
| Colours, words and designs | ARTS 2 |

**Q9. What matters most to you in a job?**
| Option | Points |
|---|---|
| Helping people | HEALTH 1, SERVE 1 |
| Earning a good salary | TECH 1, BIZ 1 |
| Freedom to be creative | ARTS 2 |
| A safe government job | SERVE 2 |
| Being my own boss | BIZ 1, SKILL 1 |

**Q10. After Class 10, what would you prefer?** *(route, not scored)*
| Option | Route |
|---|---|
| Learn a skill and start earning soon (1–2 years) | SHORT |
| Finish Class 12, then a diploma or 3-year degree | MEDIUM |
| Study long for a professional degree (4+ years) | LONG |

---

## Scoring

- Sum points per cluster across Q1–Q9.
- Top 2 clusters = prediction. Ties broken by fixed order: HEALTH, TECH, BIZ,
  ARTS, SERVE, SKILL.
- Match % = cluster points ÷ total points earned × 100 (rounded).
- Route from Q10 picks which career list to show.

---

## Career data (`data/careers.json`)

| Cluster | SHORT (skill, 1–2 yrs) | MEDIUM (12th + diploma/degree) | LONG (professional) |
|---|---|---|---|
| HEALTH | General Duty Assistant, Pharmacy Assistant, Lab Assistant | ANM/GNM Nurse, DMLT Lab Technician, D.Pharm | MBBS Doctor, B.Sc Nursing, B.Pharm, Physiotherapy |
| TECH | ITI Electronics Mechanic, Computer Operator (COPA), Mobile Repair | Polytechnic Diploma Engineer, BCA / B.Sc IT | B.E./B.Tech Engineer, Software Developer, Data Analyst |
| BIZ | Sales Associate, Tally Accounts Assistant, Small Business | B.Com, Banking/Insurance Agent | Chartered Accountant, MBA, Company Secretary |
| ARTS | Tailoring/Fashion Certificate, Photography, Video Editing | Diploma in Graphic Design/Animation, BMM | B.Des Designer, BFA Artist, Journalist |
| SERVE | Agniveer, Anganwadi Helper, Community Volunteer | D.El.Ed Primary Teacher, Police Constable, Railway/MPSC exams | B.Ed Teacher, Social Worker (BSW/MSW), Lawyer, UPSC/MPSC Officer |
| SKILL | ITI Electrician/Fitter/Plumber/Welder, Beautician, Cook | Hotel Management Diploma, Automobile Diploma | B.Sc Hospitality, B.Voc |

Each cluster also stores: `subjects_to_focus`, `next_steps` (2–3 lines), and
the shared free resources:

| Resource | Link |
|---|---|
| National Career Service | https://www.ncs.gov.in |
| Skill India Digital (free courses) | https://www.skillindiadigital.gov.in |
| National Scholarship Portal | https://scholarships.gov.in |
| MahaDBT (Maharashtra scholarships) | https://mahadbt.maharashtra.gov.in |

---

## LLM

| Item | Value |
|---|---|
| Provider | Groq (free tier, no credit card) |
| Model | `openai/gpt-oss-120b`, `reasoning_effort=low` (~1 s per message). Chosen 2026-10-08 over `qwen/qwen3.8-27b`, whose Marathi had grammar errors |
| SUPERSEDED 2026-10-08 | ~~`llama-3.3-70b-versatile`~~ — Groq no longer offers Llama chat models |
| If the model is retired | `GROQ_MODEL` in secrets → pick one from Groq console → Models. No code change |
| Backup provider | Google Gemini API free tier (Flash-Lite) — only if Groq is down |
| Timeout | 8 s, then offline message |

---

## Tech stack

| Part | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Easiest to learn and explain |
| UI | Streamlit (big-button theme in `.streamlit/config.toml`) | Web UI in pure Python, runs on laptop, opens on phone |
| Storage | Supabase table `responses` when `SUPABASE_*` secrets set; else `data/responses.csv`. Supabase failure → CSV + volunteer warning | Laptop needs nothing; hosted needs a permanent store |
| Charts | Streamlit built-in `st.bar_chart` | Zero extra setup |
| Hosting | Laptop (Guide 01) or Streamlit Community Cloud + Supabase (Guide 02) | Both free |

**Built 2026-10-08.** All code tested: full Marathi run offline, back button,
bad Groq key, unreachable Supabase, password-locked summary page.

## Files

| File | Role |
|---|---|
| `app.py` | Profile → 10 questions (+ typed answers) → result |
| `style.css` | All custom styling |
| `scoring.py` | Loads JSON data, `score()` → top 2 clusters + route |
| `advisor.py` | Groq: `classify_typed` + guidance message (8 s timeout each); offline message |
| `storage.py` | Save/load responses (Supabase or CSV) |
| `config.py` | `secret()` — reads secrets, returns default if none |
| `pages/1_Survey_Summary.py` | Charts, table, CSV download; `SUMMARY_PASSWORD` lock |
| `data/questions.json`, `careers.json`, `ui_text.json` | All content, en/mr/hi |
| `supabase_table.sql` | One-time table setup (RLS on, no policies) |
| `.streamlit/secrets.toml.example` | Every secret name with placeholders |

Privacy details: only the first word of the name is stored; only first name,
class, cluster results and typed answers are sent to Groq.

---

## College report outline

| Section | Content |
|---|---|
| Problem | Underprivileged students lack access to career counsellors |
| Method | Rule-based expert system (prediction) + LLM (personalised guidance) |
| Architecture | Student → Streamlit app → scoring.py → Groq gpt-oss-120b → result + saved response |
| Questionnaire | The 10 questions + cluster mapping table |
| Results | Survey Summary charts: cluster split, route split, by class |
| Ethics | Minimal data, first names only, school consent, AI limited to vetted career list |
| Limitations | Small sample, self-reported interests, no follow-up |
| Future scope | Train an ML model on collected responses; WhatsApp delivery; voice input for low-literacy students |

---

## Out of scope (on purpose)

Login, admin panel, SMS/WhatsApp results, PDF certificates, ML model training.
