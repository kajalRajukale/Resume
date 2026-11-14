"""Run: python scripts/test_fetch_projects.py  (no network needed)"""
from fetch_projects import merge, sections, bullets, code_blocks, tags_for, score

# manual edits win, GitHub facts are refreshed, empty manual values don't clobber
auto = {"name": "x", "title": "x", "pitch": "auto", "stars": 5, "features": ["a"]}
old = {"name": "x", "title": "Nice X", "pitch": "", "stars": 1, "featured": False}
m = merge(auto, old)
assert m["title"] == "Nice X" and m["pitch"] == "auto" and m["stars"] == 5 and m["featured"] is False, m

md = "# T\nintro text\n## Features\n- one\n- **two**\n## Run\n```bash\npip install x\n```\n"
s = sections(md)
assert bullets(s["features"]) == ["one", "two"]
assert code_blocks(s["run"]) == "pip install x"

assert tags_for(["Python"], ["Streamlit"], ["Ollama (local LLMs)"], "") == ["ai", "data-science", "python"]

e = {"name": "big", "files": 50, "demo": "https://x", "screenshots": [], "stack": ["Django"], "stars": 99,
     "tags": ["ai", "data-science"]}
total, reason = score(e, "word " * 400, {"updatedAt": "2099-01-01T00:00:00Z"})
assert total == 10 and "relevance 1.5" in reason, (total, reason)
print("ok")
