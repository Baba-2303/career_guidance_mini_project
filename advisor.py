import json
import sys

from groq import Groq

from config import secret
from scoring import CAREERS, CLUSTER_ORDER, QUESTIONS, ROUTES, UI, tr

LANG_NAMES = {"en": "English", "mr": "Marathi", "hi": "Hindi"}
# We don't know the student's gender, so each language uses its neutral/respectful form
ADDRESS_RULES = {
    "en": "Use 'you'; avoid he/she and other gendered words.",
    "mr": "Address the student with the respectful 'तुम्ही' form only, never 'तू'.",
    "hi": "Address the student with the respectful 'आप' form only, never 'तुम' or 'तू'.",
}
ROUTE_LABELS = {
    "SHORT": "learn a skill and start earning soon",
    "MEDIUM": "finish Class 12, then a diploma or degree",
    "LONG": "study long for a professional degree",
}
QUESTION_TEXT = {q["id"]: q["text"]["en"] for q in QUESTIONS}
ROUTE_QUESTION = next(q["id"] for q in QUESTIONS if "route" in q["options"][0])

GUIDANCE_PROMPT = """You are a kind career counsellor for Class 8-10 students
from low-income families in Maharashtra, India.
Rules:
- Write in {language}, in very simple words a 13-year-old understands.
- 100-130 words. Plain text, no headings, no bullet symbols, no markdown.
- Speak directly to the student by first name. {address_rule}
- Mention ONLY careers from the list given, plus any career the student wrote
  in their own words. Never invent others.
- If the student typed their own answers, show you read them.
- Be encouraging and realistic. Never say money is a reason to give up;
  mention help by name only: scholarships.gov.in, government ITI, Skill India.
- Never state fees, eligibility rules, salaries or scheme details.
- End with one small thing the student can do this week."""

CLASSIFY_PROMPT = f"""You score a school student's typed survey answers.
Career clusters:
- HEALTH: doctors, nurses, labs, caring for people, plants, animals
- TECH: computers, engineering, machines, coding, inventing
- BIZ: business, shops, selling, money, accounts
- ARTS: drawing, design, music, dance, films, fashion, writing
- SERVE: teaching, police, army, government jobs, social work, law
- SKILL: hands-on trades: electrician, mechanic, cooking, beauty, tailoring
Answers may be in English, Marathi, Hindi or Hinglish.
For each answer give at most 2 clusters: 2 = clear match, 1 = partial match.
For question {ROUTE_QUESTION} instead give one route:
- SHORT: skill course / ITI / start earning soon after Class 10
- MEDIUM: Class 12 then a diploma or 3-year degree (B.Com, BA, B.Sc, BCA)
- LONG: professional degree of 4+ years (engineering, MBBS, nursing degree, CA, law)
Meaningless or unrelated answer → {{}}.
Reply with JSON only, e.g. {{"q3": {{"HEALTH": 2, "SERVE": 1}}, "q5": {{}}, "{ROUTE_QUESTION}": "SHORT"}}"""


def _chat(system, user, json_mode=False):
    """One Groq call. Returns text, or None when offline / no key / any failure."""
    api_key = secret("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        model = secret("GROQ_MODEL", "openai/gpt-oss-120b")
        resp = Groq(api_key=api_key, timeout=8, max_retries=0).chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2 if json_mode else 0.6,
            # Reasoning models think before answering; hide that and leave room for it
            include_reasoning=False,
            max_tokens=2000,
            **({"reasoning_effort": "low"} if model.startswith("openai/gpt-oss") else {}),
            **({"response_format": {"type": "json_object"}} if json_mode else {}),
        )
        return resp.choices[0].message.content.strip() or None
    except Exception as e:
        print(f"AI call failed, using offline fallback: {e!r}", file=sys.stderr)
        return None


def classify_typed(typed):
    """typed: {"q3": "I want to fly planes"} → {"q3": {"points": {...}}, "q10": {"route": ...}}.
    Anything the AI gets wrong or skips scores 0 rather than failing."""
    user = "\n".join(f'{qid}. Question: {QUESTION_TEXT[qid]}\n    Answer: {text}' for qid, text in typed.items())
    raw = _chat(CLASSIFY_PROMPT, user, json_mode=True)
    try:
        parsed = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return {}
    custom = {}
    for qid in typed:
        value = parsed.get(qid)
        if qid == ROUTE_QUESTION:
            if value in ROUTES:
                custom[qid] = {"route": value}
        elif isinstance(value, dict):
            points = {c: p for c, p in value.items() if c in CLUSTER_ORDER and p in (1, 2)}
            custom[qid] = {"points": dict(list(points.items())[:2])}
    return custom


def _facts(result):
    lines = []
    for t in result["top"]:
        c = CAREERS[t["cluster"]]
        careers = ", ".join(c["routes"][result["route"]])
        lines.append(f'- {c["name"]["en"]} ({t["match"]}% match). Careers: {careers}. '
                     f'Subjects to focus on: {", ".join(c["subjects_to_focus"])}.')
    return "\n".join(lines)


def ai_message(profile, result, typed=None):
    lang = profile["lang"]
    user = (f'Student: {profile["name"]}, Class {profile["grade"]}.\n'
            f'After Class 10 they want to: {ROUTE_LABELS[result["route"]]}.\n'
            f'Their top career areas:\n{_facts(result)}\n')
    if typed:
        user += "In their own words:\n" + "\n".join(
            f'- {QUESTION_TEXT[qid]} → "{text}"' for qid, text in typed.items()) + "\n"
    system = GUIDANCE_PROMPT.format(language=LANG_NAMES[lang], address_rule=ADDRESS_RULES[lang])
    return _chat(system, user + "Write the guidance message.")


def offline_message(profile, result):
    lang = profile["lang"]
    first = CAREERS[result["top"][0]["cluster"]]
    intro = tr(UI["offline_intro"], lang).format(name=profile["name"], area=tr(first["name"], lang))
    return f'{intro} {tr(first["next_steps"], lang)}'
