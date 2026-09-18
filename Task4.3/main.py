import random

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="Should I? — Decision Maker", description="A tiny API that makes your hard decisions for you.")

# Weighted pool of verdicts. Mostly yes/no, with the occasional chaotic answer.
VERDICTS = [
    ("Yessss", "#91AE6E"),
    ("Absolutely :D", "#91AE6E"),
    ("Yah go for it!", "#91AE6E"),
    ("No.", "#D96868"),
    ("Ow hell nahhh", "#D96868"),
    ("Nuh uh", "#D96868"),
    ("Maybe? Perhaps? Sure?", "#FFEA88"),
    ("If it makes you happy lol", "#FFEA88"),
    ("Follow your heart lil bro", "#B1E5E6"),
    ("The fact that you're here is concerning I can't lie.", "#B1E5E6"),
]


def decide() -> dict:
    text, color = random.choice(VERDICTS)
    return {"verdict": text, "color": color}


@app.get("/api/decide")
def api_decide(question: str | None = None):
    """Return a decision as JSON. Optionally pass ?question= to echo it back."""
    result = decide()
    if question:
        result["question"] = question
    return result


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    question = request.query_params.get("question", "")
    result = decide() if question else None

    verdict_block = ""
    if result:
        verdict_block = f"""
        <div class="card" style="border-color:{result['color']}">
          <p class="q">"{question}"</p>
          <p class="verdict" style="color:{result['color']}">{result['verdict']}</p>
        </div>
        """

    return f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Should I?</title>
      <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap" rel="stylesheet">
      <style>
        :root {{ color-scheme: light dark; }}
        body {{
          font-family: system-ui, -apple-system, sans-serif;
          max-width: 720px; margin: 8vh auto; padding: 0 20px;
          text-align: center; background: #fff0f5; color: #23202b;
        }}
        h1 {{ font-size: 2.4rem; margin-bottom: 4px; }}
        .sub {{ color: #6b6577; margin-top: 0; }}
        form {{ margin: 28px 0; display: flex; gap: 8px; }}
        input {{
          flex: 1; padding: 12px 14px; font-size: 1rem;
          border: 2px solid #f5c2d8; border-radius: 10px; background: #fff;
          color: #000;
        }}
        button {{
          padding: 12px 18px; font-size: 1rem; font-weight: 600;
          border: 0; border-radius: 10px; background: #e58fb5; color: #fff; cursor: pointer;
        }}
        .card {{
          border: 3px solid; border-radius: 14px; padding: 22px; background: #fff;
        }}
        .q {{ color: #6b6577; font-style: italic; margin: 0 0 10px; }}
        .verdict {{ font-size: 1.8rem; font-weight: 700; margin: 0; }}
        footer {{ margin-top: 40px; font-size: .8rem; color: #9a94a6; }}
      </style>
    </head>
    <body>
      <h1>🔮 Should I?</h1>
      <p class="sub">Got a dilemma? Let your destiny decide ^^</p>
      <form action="/" method="get">
        <input name="question" placeholder="Should I get bubble tea?" value="{question}" required>
        <button type="submit">Decide</button>
      </form>
      {verdict_block}
      <footer>SWE40006 Task 4.3 &middot; FastAPI &middot; Made by Hayley Nguyen</footer>
    </body>
    </html>
    """
