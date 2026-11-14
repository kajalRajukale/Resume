---
layout: page
title: About
permalink: /about/
eyebrow: "$ cat about.md"
heading: About me
description: Bio, focus areas and timeline of Kajal Rajukale.
---
{% assign r = site.data.resume %}
<section class="about">
  <img class="about-img reveal" src="{{ r.profile.avatar | relative_url }}" alt="Avatar of {{ r.profile.name }}" width="220" height="220" loading="lazy">
  <div class="reveal">
    <p class="lead">{{ r.summary }}</p>
    <p class="lead">{{ r.profile.tagline }}</p>
  </div>
</section>

<section>
  <div class="section-head"><h2 class="reveal">Focus areas</h2></div>
  <div class="focus">
    {% for f in r.focus %}<div class="focus-card reveal"><span class="focus-icon" aria-hidden="true">{{ f.icon }}</span><h3>{{ f.title }}</h3><p>{{ f.text }}</p></div>{% endfor %}
  </div>
</section>

<section>
  <div class="section-head"><h2 class="reveal">Timeline</h2></div>
  <div class="timeline">
    {% for j in r.experience %}
    <div class="tl-item reveal"><span class="when">{{ j.start }} – {{ j.end | default: "Present" }}</span><h3>{{ j.role }} · {{ j.company }}</h3>
      <ul>{% for h in j.highlights %}<li>{{ h }}</li>{% endfor %}</ul></div>
    {% endfor %}
    {% for t in r.timeline %}
    <div class="tl-item reveal"><span class="when">{{ t.year }}</span><h3>{{ t.title }}</h3><p>{{ t.text }}</p></div>
    {% endfor %}
    {% for e in r.education %}
    <div class="tl-item reveal edu"><span class="when">Education{% unless e.start contains "TODO" %} · {{ e.start }} – {{ e.end }}{% endunless %}</span>
      <h3>{{ e.degree }}</h3><p>{% unless e.school contains "TODO" %}<em>{{ e.school }}</em> · {% endunless %}{{ e.details }}</p></div>
    {% endfor %}
  </div>
</section>
