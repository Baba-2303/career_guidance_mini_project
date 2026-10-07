import json
from datetime import datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st

from advisor import ai_message, classify_typed, offline_message
from scoring import CAREERS, OTHER, QUESTIONS, UI, score, tr
from storage import save_response

LANGS = {"English": "en", "मराठी": "mr", "हिंदी": "hi"}
GRADES = [8, 9, 10]
FREE_LINKS = {"Scholarships": "https://scholarships.gov.in",
              "Skill India": "https://www.skillindiadigital.gov.in",
              "Career Service": "https://www.ncs.gov.in"}

st.set_page_config(page_title="Disha · Career Guidance", page_icon="🧭", layout="centered")
st.html(f"<style>{(Path(__file__).parent / 'style.css').read_text()}</style>")
st.html('<div class="brand"><div class="mark">D</div><div>'
        '<div class="name">Disha · दिशा</div><div class="sub">Career Guidance</div></div></div>')

s = st.session_state
s.setdefault("step", 0)  # 0 = profile, 1..10 = questions, 11 = result
s.setdefault("answers", {})
s.setdefault("typed", {})


def ui(key, **kw):
    return tr(UI[key], s.profile["lang"]).format(**kw)


def answer(qid, idx, text=None):
    s.answers[qid] = idx
    if text:
        s.typed[qid] = text
    else:
        s.typed.pop(qid, None)
    s.step += 1


def next_student():
    s.step, s.answers, s.typed = 0, {}, {}
    s.pop("result", None)


def finish():
    typed = {qid: text for qid, text in s.typed.items() if s.answers.get(qid) == OTHER}
    r = score(s.answers, classify_typed(typed) if typed else None)
    msg = ai_message(s.profile, r, typed)
    r["source"] = "ai" if msg else "offline"
    r["message"] = msg or offline_message(s.profile, r)
    r["saved_to"] = save_response({
        "created_at": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds"),
        "name": s.profile["name"], "grade": s.profile["grade"],
        "school": s.profile["school"], "lang": s.profile["lang"],
        **{q["id"]: s.answers[q["id"]] for q in QUESTIONS},
        "typed_answers": json.dumps(typed, ensure_ascii=False) if typed else "",
        "top1": r["top"][0]["cluster"], "top2": r["top"][1]["cluster"],
        "route": r["route"], "source": r["source"],
    })
    return r


def route_label(route, lang):
    q10 = next(q for q in QUESTIONS if "route" in q["options"][0])
    return next(tr(o["text"], lang) for o in q10["options"] if o["route"] == route)


def welcome():
    st.html('<div class="hero"><h1>Find the career path that suits you</h1>'
            '<p>तुमच्यासाठी योग्य करिअरचा मार्ग शोधा</p></div>'
            '<div class="steps"><span><b>1</b>Answer 10 questions</span>'
            '<span><b>2</b>See your career areas</span><span><b>3</b>Get personal advice</span></div>')
    last = s.get("profile", {})
    with st.form("profile_form"):
        name = st.text_input("Student's first name / विद्यार्थ्याचे पहिले नाव", placeholder="e.g. Asha")
        grade = st.segmented_control("Class / इयत्ता", GRADES, default=last.get("grade", 9),
                                     format_func=lambda g: f"Class {g}", width="stretch")
        school = st.text_input("School / शाळा", value=last.get("school", ""))
        lang = st.segmented_control("Language / भाषा", list(LANGS), width="stretch",
                                    default=next((k for k, v in LANGS.items() if v == last.get("lang")), "English"))
        started = st.form_submit_button("Start  →", type="primary", width="stretch")
    if started:
        if not name.strip():
            st.error("Please enter the student's first name.")
        else:
            s.profile = {"name": name.strip().split()[0].title(), "grade": grade or 9,
                         "school": school.strip(), "lang": LANGS[lang or "English"]}
            s.step = 1
            st.rerun()
    st.page_link("pages/1_Survey_Summary.py", label="Volunteer: Survey summary", icon=":material/bar_chart:")


def question():
    q = QUESTIONS[s.step - 1]
    lang = s.profile["lang"]
    pct = round(s.step * 100 / len(QUESTIONS))
    st.html(f'<div class="qmeta"><span>{escape(ui("question_of", n=s.step, total=len(QUESTIONS)))}</span>'
            f'<span>{pct}%</span></div><div class="bar"><div style="width:{pct}%"></div></div>'
            f'<div class="question">{escape(tr(q["text"], lang))}</div>')
    for i, opt in enumerate(q["options"]):
        st.button(tr(opt["text"], lang), key=f'{q["id"]}_{i}', width="stretch",
                  on_click=answer, args=(q["id"], i))

    st.html(f'<div class="or">{escape(ui("other_title"))}</div>')
    with st.form(f'other_{q["id"]}', border=False, clear_on_submit=True):
        typed = st.text_input(ui("other_title"), value=s.typed.get(q["id"], ""), max_chars=200,
                              placeholder=ui("other_placeholder"), label_visibility="collapsed")
        if st.form_submit_button(ui("other_next"), type="primary", width="stretch"):
            if typed.strip():
                answer(q["id"], OTHER, typed.strip())
                st.rerun()
            st.warning(ui("other_empty"))

    if s.step > 1 and st.button(ui("back"), type="tertiary"):
        s.step -= 1
        st.rerun()


def result():
    # Streamlit reruns the script on every click; compute and save only once per student
    if "result" not in s:
        with st.spinner(ui("preparing")):
            s.result = finish()
    r = s.result
    lang = s.profile["lang"]

    st.html(f'<div class="rtitle">{escape(ui("result_title", name=s.profile["name"]))}</div>'
            f'<div class="path">{escape(ui("your_path"))}: {escape(route_label(r["route"], lang))}</div>')
    for top in r["top"]:
        c = CAREERS[top["cluster"]]
        chips = "".join(f"<span>{escape(name)}</span>" for name in c["routes"][r["route"]])
        st.html(f'<div class="card" style="--c:{c["color"]}">'
                f'<div class="head"><div class="title">{escape(tr(c["name"], lang))}</div>'
                f'<div class="pct">{top["match"]}%<small>{escape(ui("match"))}</small></div></div>'
                f'<div class="bar"><div style="width:{top["match"]}%"></div></div>'
                f'<div class="label">{escape(ui("careers_for_you"))}</div><div class="chips">{chips}</div></div>')

    st.html(f'<div class="advice"><div class="label">{escape(ui("advice"))}</div>'
            f'<p>{escape(r["message"])}</p></div>')
    links = "".join(f'<a href="{url}" target="_blank">{name}</a>' for name, url in FREE_LINKS.items())
    st.html(f'<div class="links">{escape(ui("free_help"))}: {links}</div>'
            f'<div class="note">{escape(ui("disclaimer"))}</div>')
    if r["saved_to"] == "csv_fallback":
        st.warning("Volunteer note: online database unreachable — this response was saved only on this device.")
    st.button(ui("next_student"), on_click=next_student, type="primary", width="stretch")


if s.step == 0:
    welcome()
elif s.step <= len(QUESTIONS):
    question()
else:
    result()
