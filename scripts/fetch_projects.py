#!/usr/bin/env python3
"""Discover, analyse and score the GitHub repos of a user for the portfolio site.

Writes:
  _data/projects.yml   one entry per selected repo (auto fields + your manual edits)
  _data/github.yml     account stats for the home page
  _projects/<repo>.md  detail-page stub per project (only created if missing)

Manual edits survive a refresh: every non-empty field you set in projects.yml is
kept, except the AUTO fields below, which always come fresh from GitHub.

Usage:  python scripts/fetch_projects.py [--user kajalRajukale]
Needs:  gh (authenticated), PyYAML  (pip install -r scripts/requirements.txt)
"""
import argparse
import base64
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data" / "projects.yml"
STATS = ROOT / "_data" / "github.yml"
PAGES = ROOT / "_projects"

TOPICS = {"python", "ai", "artificial-intelligence", "data-science", "machine-learning",
          "deep-learning", "llm", "nlp", "computer-vision", "pandas", "jupyter"}
LANGS = {"Python", "Jupyter Notebook"}
AI_WORDS = r"\b(ai|llm|llms|ollama|gemini|openai|gpt|machine learning|deep learning|nlp|" \
           r"data science|pandas|numpy|jupyter|streamlit|dataset|model|anaconda|conda)\b"
TUTORIAL = re.compile(r"tutorial|learn|course|hello|test|exam", re.I)
JUNK_DIRS = re.compile(r"(^|/)(\.venv[^/]*|venv|site-packages|node_modules|staticfiles|__pycache__|migrations)(/|$)")
SOURCE_EXT = (".py", ".ipynb", ".js", ".ts", ".html", ".css", ".php", ".java")

# keyword in requirements/README/file tree -> stack label
STACK = {
    "django": "Django", "djangorestframework": "Django REST Framework", "flask": "Flask",
    "fastapi": "FastAPI", "streamlit": "Streamlit", "pandas": "Pandas", "numpy": "NumPy",
    "matplotlib": "Matplotlib", "folium": "Folium", "scikit-learn": "scikit-learn",
    "ollama": "Ollama", "google-genai": "Google Gemini", "gemini": "Google Gemini",
    "openai": "OpenAI", "fpdf": "PDF export", "reportlab": "PDF export", "pytest": "pytest",
    "unittest": "unittest", "psycopg": "PostgreSQL", "postgres": "PostgreSQL",
    "db.sqlite3": "SQLite", "sqlite": "SQLite", "gtts": "Text-to-speech", "geopy": "Geocoding",
    "environment.yml": "Anaconda", "justfile": "just",
}
MODELS = {"gemini": "Google Gemini", "ollama": "Ollama (local LLMs)", "llama": "Llama",
          "gpt": "OpenAI GPT", "rule-based": "Rule-based engine"}
# Always refreshed from GitHub; everything else keeps your manual edits.
AUTO = {"url", "homepage", "language", "languages", "topics", "stars", "forks",
        "updated", "score", "score_reason", "files", "screenshots"}


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def gh_json(*args):
    out = gh(*args)
    return json.loads(out) if out else None


def file_text(owner, repo, path):
    data = gh_json("api", f"repos/{owner}/{repo}/contents/{path}")
    if isinstance(data, dict) and data.get("content"):
        return base64.b64decode(data["content"]).decode("utf-8", "replace")
    return ""


def readme(owner, repo):
    data = gh_json("api", f"repos/{owner}/{repo}/readme")
    return base64.b64decode(data["content"]).decode("utf-8", "replace") if data else ""


def tree(owner, repo):
    data = gh_json("api", f"repos/{owner}/{repo}/git/trees/HEAD?recursive=1") or {}
    return [t["path"] for t in data.get("tree", []) if not JUNK_DIRS.search(t["path"])]


def sections(md):
    """{heading_lower: body} plus '' for text before the first heading."""
    out, key = {"": []}, ""
    for line in md.splitlines():
        m = re.match(r"^#{1,4}\s+(.*)", line)
        if m:
            key = m.group(1).strip().lower()
            out.setdefault(key, [])
        else:
            out[key].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def plain(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)|<[^>]+>", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[*_`>#]", "", text).strip()


def first_paragraph(md):
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    for para in re.split(r"\n\s*\n", md):
        p = plain(para)
        if len(p) > 40 and not p.startswith(("-", "|", "git ")):
            return " ".join(p.split())[:240]
    return ""


def pick(secs, pattern):
    return next((v for k, v in secs.items() if re.search(pattern, k)), "")


def bullets(text):
    return [plain(m)[:160] for m in re.findall(r"^\s*[-*]\s+(.+)$", text, re.M)][:8]


def code_blocks(text):
    return "\n".join(b.strip() for b in re.findall(r"```[\w-]*\n(.*?)```", text, re.S))


def analyse(owner, repo):
    name = repo["name"]
    md = readme(owner, name)
    md = re.sub(r"^(<<<<<<<|=======|>>>>>>>).*$", "", md, flags=re.M)  # stray merge markers
    files = tree(owner, name)
    reqs = file_text(owner, name, "requirements.txt") if "requirements.txt" in files else ""
    secs = sections(md)
    haystack = " ".join([name.replace("_", " ").replace("-", " "), md, reqs, " ".join(files), repo.get("description") or ""]).lower()

    stack = sorted({label for key, label in STACK.items() if key in haystack})
    langs = [l["node"]["name"] for l in repo.get("languages", [])]
    models = sorted({label for key, label in MODELS.items() if re.search(rf"\b{key}\b", haystack)})
    if "ai_engine.py" in haystack and "Rule-based engine" not in models:
        models.append("Rule-based engine")

    run = code_blocks(pick(secs, r"run|start|setup|install|usage|getting started|quick"))
    if not run:
        if "Streamlit" in stack and "app.py" in files:
            run = "pip install -r requirements.txt\nstreamlit run app.py"
        elif "manage.py" in files or any(f.endswith("/manage.py") for f in files):
            run = "pip install -r requirements.txt\npython manage.py migrate\npython manage.py runserver"
        elif "app.py" in files:
            run = "pip install -r requirements.txt\npython app.py"

    raw = f"https://raw.githubusercontent.com/{owner}/{name}/HEAD/"
    shots = re.findall(r"!\[[^\]]*\]\(([^)\s]+)|<img[^>]+src=\"([^\"]+)\"", md)
    shots = [s for pair in shots for s in pair if s]
    shots = [s if s.startswith("http") else raw + s.lstrip("./") for s in shots][:6]

    homepage = repo.get("homepageUrl") or ""
    demo = homepage if homepage and "github.com" not in homepage else ""
    src_files = [f for f in files if f.endswith(SOURCE_EXT)]

    entry = {
        "name": name,
        "title": name.replace("_", " ").replace("-", " ").strip(),
        "pitch": repo.get("description") or first_paragraph(md),
        "problem": "",
        "approach": "",
        "features": bullets(pick(secs, r"feature")),
        "stack": stack,
        "models": models,
        "datasets": [f for f in files if f.endswith((".csv", ".xlsx", ".parquet"))][:5],
        "results": "",
        "how_to_run": run,
        "screenshots": shots,
        "demo": demo,
        "url": repo["url"],
        "homepage": homepage,
        "language": (repo.get("primaryLanguage") or {}).get("name") or "",
        "languages": langs,
        "topics": [t["name"] for t in repo.get("repositoryTopics") or []],
        "stars": repo.get("stargazerCount", 0),
        "forks": repo.get("forkCount", 0),
        "updated": repo["updatedAt"][:10],
        "files": len(src_files),
        "tags": tags_for(langs, stack, models, haystack),
    }
    entry["score"], entry["score_reason"] = score(entry, md, repo)
    return entry


def tags_for(langs, stack, models, haystack):
    tags = []
    if models or re.search(r"\b(ai|llm|ollama|gemini)\b", haystack):
        tags.append("ai")
    if {"Pandas", "NumPy", "Matplotlib", "Streamlit", "Anaconda", "scikit-learn"} & set(stack) \
            or "Jupyter Notebook" in langs:
        tags.append("data-science")
    if "Python" in langs or {"Django", "Flask", "Streamlit"} & set(stack):
        tags.append("python")
    return tags


def score(e, md, repo):
    """0-10 interestingness. ponytail: heuristic weights, tune here if rankings feel off."""
    words = len(md.split())
    parts = {
        "readme": 2 if words > 300 else 1 if words > 80 else 0,
        "originality": 0.5 if TUTORIAL.search(e["name"]) else 2,
        "complexity": 2 if e["files"] >= 20 else 1 if e["files"] >= 5 else 0.5 if e["files"] else 0,
        "demo": min(2, (1 if e["demo"] else 0) + (1 if e["screenshots"] or {"Streamlit", "Flask", "Django"} & set(e["stack"]) else 0)),
        "recency": recency(repo["updatedAt"]),
        "stars": min(1, e["stars"] / 5),
        # site focus: AI / data work ranks above plain CRUD apps
        "relevance": (1 if "ai" in e["tags"] else 0) + (0.5 if "data-science" in e["tags"] else 0),
    }
    total = min(10, round(sum(parts.values()), 1))
    return total, ", ".join(f"{k} {v:g}" for k, v in parts.items())


def recency(iso):
    days = (datetime.now(timezone.utc) - datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    return 1 if days <= 180 else 0.5 if days <= 365 else 0


def selected(repo, md_cache, skip):
    if repo["name"] in skip:
        return False
    if repo["isFork"]:  # ponytail: forks skipped outright; check own commits if a fork ever matters
        return False
    topics = {t["name"].lower() for t in repo.get("repositoryTopics") or []}
    if topics & TOPICS:
        return True
    if (repo.get("primaryLanguage") or {}).get("name") in LANGS:
        return True
    text = " ".join([repo["name"].replace("_", " "), repo.get("description") or "", md_cache(repo["name"])])
    return bool(re.search(AI_WORDS, text, re.I))


def merge(auto, old):
    keep = {k: v for k, v in old.items() if k not in AUTO and v not in (None, "", [], {})}
    return {**auto, **keep}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="kajalRajukale")
    ap.add_argument("--featured", type=int, default=5)
    ap.add_argument("--skip", nargs="*", default=["Resume"], help="repos to ignore (this site itself)")
    args = ap.parse_args()

    fields = "name,description,repositoryTopics,primaryLanguage,languages,stargazerCount," \
             "forkCount,updatedAt,homepageUrl,isFork,url"
    repos = gh_json("repo", "list", args.user, "--limit", "200", "--visibility", "public", "--json", fields)
    if repos is None:
        sys.exit("gh repo list failed - run `gh auth status`")

    cache = {}
    md_cache = lambda n: cache.setdefault(n, readme(args.user, n))
    skip = set(args.skip) | {args.user}  # profile README repo
    chosen = [r for r in repos if selected(r, md_cache, skip)]
    entries = [analyse(args.user, r) for r in chosen]
    entries.sort(key=lambda e: e["score"], reverse=True)

    old = {e["name"]: e for e in (yaml.safe_load(DATA.read_text()) or [])} if DATA.exists() else {}
    if not old:  # first run: auto-feature the top N
        for e in entries[: args.featured]:
            e["featured"] = True
    entries = [merge(e, old.get(e["name"], {})) for e in entries]

    header = "# Generated by scripts/fetch_projects.py - manual edits are kept on refresh\n" \
             "# (except: " + ", ".join(sorted(AUTO)) + ")\n"
    DATA.write_text(header + yaml.safe_dump(entries, sort_keys=False, allow_unicode=True, width=100))

    STATS.write_text(yaml.safe_dump({
        "public_repos": len(repos),
        "total_stars": sum(r["stargazerCount"] for r in repos),
        "languages": sorted({l["node"]["name"] for r in repos for l in r.get("languages", [])}),
        "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }, sort_keys=False))

    min_score = (yaml.safe_load((ROOT / "_config.yml").read_text()) or {}).get("min_score", 0)
    PAGES.mkdir(exist_ok=True)
    for e in entries:
        page = PAGES / f"{e['name']}.md"
        title = f"title: {json.dumps(e['title'], ensure_ascii=False)}"
        if page.exists():  # keep the body, sync the <title> with projects.yml
            page.write_text(re.sub(r"^title: .*$", title, page.read_text(), count=1, flags=re.M))
        elif e["score"] >= min_score:
            page.write_text(f"---\nname: {e['name']}\n{title}\n---\n")

    print(f"{'repo':42} {'score':>5}  {'tags':28} reasoning")
    for e in entries:
        flag = "*" if e.get("featured") else " "
        print(f"{flag}{e['name']:41} {e['score']:>5}  {','.join(e['tags']):28} {e['score_reason']}")
    print(f"\n{len(entries)} of {len(repos)} repos selected -> {DATA.relative_to(ROOT)}  (* = featured)")


if __name__ == "__main__":
    main()
