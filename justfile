# Local tasks. Install just: brew install just

chrome := env_var_or_default("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
port := env_var_or_default("PORT", "4000")
url := "http://localhost:" + port + "/Resume/"

# List recipes
default:
    @just --list

# Install Ruby gems (once, or after Gemfile changes)
install:
    bundle install

# Dev server with live reload, opens the browser
serve: install
    bundle exec jekyll serve --livereload --open-url --port {{port}}

# Production build into _site/
build: install
    JEKYLL_ENV=production bundle exec jekyll build

# Serve the production build as deployed (no rebuild on change)
run: build
    @echo "Serving {{url}}  (Ctrl+C to stop)"
    JEKYLL_ENV=production bundle exec jekyll serve --skip-initial-build --no-watch --port {{port}}

# Open the local site in the browser
open:
    open {{url}}

# Remove build output and caches
clean:
    bundle exec jekyll clean
    rm -rf .cache/pdf

# Build + check internal links and images
check: build
    bundle exec htmlproofer ./_site --disable-external --swap-urls "^/Resume/:/"

# Re-scan GitHub repos -> _data/projects.yml, _data/github.yml, _projects/
projects:
    python3 scripts/fetch_projects.py

# Render all VHS tapes -> assets/vhs/
vhs:
    for t in vhs/[!_]*.tape; do vhs "$t"; done

# Render one tape: just tape intro
tape name:
    vhs vhs/{{name}}.tape

# Print the resume page to assets/resume.pdf with headless Chrome
pdf:
    #!/usr/bin/env bash
    set -euo pipefail
    bundle exec jekyll build -q -d .cache/pdf/Resume
    python3 -m http.server 4010 -d .cache/pdf >/dev/null 2>&1 & srv=$!
    trap 'kill $srv' EXIT
    sleep 1
    "{{chrome}}" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=5000 \
      --print-to-pdf=assets/resume.pdf http://localhost:4010/Resume/resume/
