# Task: Build an outstanding Jekyll resume & portfolio site for GitHub user `kajalRajukale`

Turn this folder/repository into a modern, animated resume + portfolio website built with
Jekyll and deployed to GitHub Pages. Work through the phases below in order. Don't stop
after planning — build the complete site, verify it, and report back.

## Phase 1 — Discover & analyze repositories (do this first, before any design work)

1. Use the GitHub CLI (`gh`) or the REST API to list ALL public repos of `kajalRajukale`:
   `gh repo list kajalRajukale --limit 200 --json name,description,repositoryTopics,primaryLanguage,languages,stargazerCount,forkCount,updatedAt,homepageUrl,isFork,url`
2. Select relevant repos:
   - Topics matching (case-insensitive): `python`, `ai`, `artificial-intelligence`, `data-science`,
     `machine-learning`, `deep-learning`, `llm`, `nlp`, `computer-vision`, `pandas`, `jupyter`
   - ALSO include repos without topics whose primary language is Python or Jupyter Notebook,
     or whose README clearly covers AI / ML / data work.
   - Exclude forks unless they contain substantial own commits.
3. For every selected repo, read the README (and skim the main source files / notebooks) and
   extract: one-line pitch, problem solved, tech stack, key features, datasets/models used,
   results/metrics, how to run it, screenshots/images present, demo links.
4. Score each repo for "interestingness" (0–10) based on: README quality, originality,
   complexity, visual/demo potential, recency, stars. Write the reasoning down.
5. Save results to `_data/projects.yml` (one entry per repo, all extracted fields + score +
   `featured: true` for the top 4–6). Write the discovery logic as a reusable script
   `scripts/fetch_projects.py` so the data can be refreshed later.
6. Print a summary table of selected repos with scores and ask nothing — continue.

## Phase 2 — Theme & architecture

- Evaluate 2–3 Jekyll themes/approaches suited to a resume/portfolio with motion
  (e.g. al-folio, Chirpy, or a custom lightweight theme) and pick ONE. Document the choice
  and reasoning in `README.md`. A custom theme with a modern dark "developer/terminal"
  aesthetic and a light-mode toggle is preferred if the existing themes feel generic.
- Build with **GitHub Actions** (`.github/workflows/pages.yml`), not the classic Pages
  builder, so any theme/plugin can be used.
- Everything content-related must be data-driven:
  - `_data/resume.yml` — profile, summary, experience, education, certifications, languages
  - `_data/skills.yml` — grouped skills with proficiency levels
  - `_data/projects.yml` — generated in Phase 1
  - `_data/navigation.yml` — menu
- Do NOT invent personal facts (jobs, degrees, dates, contact data). Use clearly marked
  placeholders like `TODO: fill in` wherever real information is unknown.

## Phase 3 — Pages & features

Build all pages with consistent navigation (sticky header, active state, mobile menu,
smooth scroll, back-to-top):

- **Home** — animated hero (typing effect for role titles), short pitch, CTA buttons
  (Projects, Resume PDF, Contact), featured projects, key stats (repos, languages, stars).
- **About** — bio, focus areas (Python, AI, Data Science), timeline of experience/education.
- **Skills** — animated skill bars or radar chart, tech-stack logos grouped by category.
- **Projects** — filterable/searchable grid (filter by topic & language), cards with hover
  effects, tags, stars, links to repo and demo.
- **Project detail pages** — one generated page per project (Jekyll collection `_projects/`):
  overview, problem, approach, stack, features, results, how-to-run, terminal demo video,
  GitHub link.
- **Terminal demos** — gallery page of all VHS recordings (see Phase 4).
- **Resume** — print-optimized HTML resume + downloadable PDF (`assets/resume.pdf`;
  generate via a print stylesheet or a CI step).
- **Contact** — links (GitHub, LinkedIn, email placeholder), optional form via Formspree.
- **404** page with a playful terminal-style message.

## Phase 4 — Terminal / code videos with VHS (charmbracelet/vhs)

- For each featured project, write a `.tape` file in `vhs/` that demonstrates it
  realistically: clone, install, run the CLI/script, show output. If a project is not a
  CLI, show a short Python REPL session, `tree` of the structure, or a key code snippet
  rendered with `bat`/`glow`.
- Add one "intro" tape for the home page (e.g. `whoami`, `cat skills.txt`, `ls projects/`).
- Consistent styling across all tapes: same theme, font, font size, width/height,
  typing speed, padding, window bar.
- Render to `assets/vhs/<name>.webm` + `.gif` fallback + a poster image.
  Add a workflow `.github/workflows/vhs.yml` using `charmbracelet/vhs-action` that
  re-renders on changes to `vhs/*.tape`, plus a `just vhs` / `make vhs` target for local runs.
- Embed as `<video autoplay muted loop playsinline poster="…">`, lazy-loaded.

## Phase 5 — Animations, polish & quality

- Scroll-reveal animations (AOS or a small IntersectionObserver script), subtle parallax
  in the hero, animated counters, card hover/tilt, page transitions. Keep JS small; no
  heavy frameworks.
- Respect `prefers-reduced-motion` — disable non-essential animation.
- Dark/light mode toggle, persisted in localStorage.
- Responsive from 360px to 4K. Accessible: semantic HTML, focus states, alt text,
  contrast AA.
- SEO: `jekyll-seo-tag`, `jekyll-sitemap`, `jekyll-feed`, Open Graph image, JSON-LD
  `Person` schema.
- Performance: optimized images (WebP), deferred JS, minimal CSS. Target Lighthouse ≥ 90
  in all categories.
- Optional: scheduled workflow (weekly) that re-runs `scripts/fetch_projects.py` and opens
  a PR when project data changes.

## Phase 6 — Verify & report

1. `bundle exec jekyll build` must succeed with no warnings; run `htmlproofer` on `_site`.
2. Serve locally and check every page and link, plus the mobile layout.
3. Update `README.md` with: setup, local dev (`bundle exec jekyll serve`), how to refresh
   projects, how to add/render VHS tapes, how to edit resume data, deployment steps
   (Settings → Pages → Source: GitHub Actions).
4. Finish with a short report: selected repos + scores, theme chosen and why, list of
   pages, list of TODO placeholders I need to fill in, and any issues found.
