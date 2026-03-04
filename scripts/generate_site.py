#!/usr/bin/env python3
"""Generate GitHub Pages site from phrase YAML files."""

import sys
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Everyday English Phrases</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --primary: #6366f1;
            --surface: #ffffff;
            --bg: #f8fafc;
            --text: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --radius: 16px;
            --shadow: 0 4px 24px rgba(99,102,241,0.08);
            --shadow-hover: 0 8px 32px rgba(99,102,241,0.18);
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 64px 20px 84px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: '';
            position: absolute;
            inset: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/svg%3E");
        }
        .hero-content { position: relative; max-width: 640px; margin: 0 auto; }
        .hero h1 {
            font-size: clamp(2em, 5vw, 3em);
            font-weight: 800;
            color: white;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }
        .hero-zh { font-size: 1.1em; color: rgba(255,255,255,0.85); margin-bottom: 14px; }
        .hero-desc { color: rgba(255,255,255,0.7); font-size: 0.95em; }
        .search-wrap {
            max-width: 600px;
            margin: -28px auto 0;
            padding: 0 20px;
            position: relative;
            z-index: 10;
        }
        .search-icon {
            position: absolute;
            left: 36px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 1.1em;
            pointer-events: none;
        }
        .search-box {
            width: 100%;
            padding: 16px 20px 16px 52px;
            font-size: 16px;
            border: none;
            border-radius: 14px;
            background: white;
            box-shadow: 0 8px 40px rgba(0,0,0,0.15);
            color: var(--text);
        }
        .search-box:focus { outline: 3px solid var(--primary); outline-offset: 2px; }
        main { max-width: 920px; margin: 0 auto; padding: 44px 20px 60px; }
        .section-title {
            font-size: 0.78em;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 20px;
        }
        .categories {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 20px;
        }
        .category-card {
            background: var(--surface);
            border-radius: var(--radius);
            padding: 28px 24px;
            text-decoration: none;
            color: inherit;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
            transition: all 0.25s ease;
            display: flex;
            flex-direction: column;
        }
        .category-card:hover {
            box-shadow: var(--shadow-hover);
            transform: translateY(-4px);
            border-color: var(--primary);
        }
        .category-icon { font-size: 2.4em; margin-bottom: 14px; }
        .category-name { font-size: 1.15em; font-weight: 700; margin-bottom: 4px; }
        .category-name-zh { color: var(--text-muted); font-size: 0.88em; margin-bottom: 10px; }
        .category-desc { color: var(--text-muted); font-size: 0.9em; flex: 1; line-height: 1.55; }
        .phrase-count {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin-top: 18px;
            padding: 4px 12px;
            background: #eef2ff;
            color: var(--primary);
            border-radius: 20px;
            font-size: 0.78em;
            font-weight: 600;
            width: fit-content;
        }
        footer {
            background: var(--surface);
            border-top: 1px solid var(--border);
            text-align: center;
            padding: 24px;
            color: var(--text-muted);
            font-size: 0.85em;
        }
        footer a { color: var(--primary); text-decoration: none; }
        footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="hero">
        <div class="hero-content">
            <h1>📖 Everyday English</h1>
            <p class="hero-zh">日常英语表达</p>
            <p class="hero-desc">Real-world English expressions with bilingual explanations</p>
        </div>
    </div>

    <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-box" placeholder="Search categories... 搜索分类..." id="search" autocomplete="off">
    </div>

    <main>
        <p class="section-title">All Categories · 所有分类</p>
        <div class="categories">
            {% for cat in categories %}
            <a href="categories/{{ cat.slug }}.html" class="category-card">
                <div class="category-icon">{{ cat.icon }}</div>
                <div class="category-name">{{ cat.name_en }}</div>
                <div class="category-name-zh">{{ cat.name_zh }}</div>
                <div class="category-desc">{{ cat.desc_en }}</div>
                <span class="phrase-count">✦ {{ cat.phrase_count }} phrases</span>
            </a>
            {% endfor %}
        </div>
    </main>

    <footer>
        <p>
            <a href="https://github.com/liyun95/everyday-english-phrases">GitHub</a> ·
            <a href="https://github.com/liyun95/everyday-english-phrases/releases">Download Anki Deck</a>
        </p>
        <p style="margin-top:6px">Community-driven · CC BY 4.0</p>
    </footer>

    <script>
        document.getElementById('search').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.category-card').forEach(card => {
                card.style.display = card.textContent.toLowerCase().includes(query) ? '' : 'none';
            });
        });
    </script>
</body>
</html>
"""

CATEGORY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ category.name_en }} - Everyday English Phrases</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --primary: #6366f1;
            --surface: #ffffff;
            --bg: #f8fafc;
            --text: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --radius: 16px;
            --shadow: 0 2px 16px rgba(0,0,0,0.06);
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }
        .top-nav {
            background: white;
            border-bottom: 1px solid var(--border);
            padding: 12px 20px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 8px rgba(0,0,0,0.06);
        }
        .nav-inner {
            max-width: 760px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9em;
        }
        .back-link {
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }
        .back-link:hover { text-decoration: underline; }
        .nav-sep { color: var(--border); }
        .nav-current { color: var(--text-muted); }
        .category-hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 44px 20px 54px;
            text-align: center;
        }
        .category-hero h1 {
            font-size: clamp(1.6em, 4vw, 2.2em);
            font-weight: 800;
            color: white;
            margin-bottom: 6px;
        }
        .category-hero .subtitle { color: rgba(255,255,255,0.8); font-size: 0.95em; }
        .search-wrap {
            max-width: 700px;
            margin: -24px auto 0;
            padding: 0 20px;
            position: relative;
        }
        .search-icon {
            position: absolute;
            left: 34px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }
        .search-box {
            width: 100%;
            padding: 14px 18px 14px 48px;
            font-size: 15px;
            border: none;
            border-radius: 12px;
            background: white;
            box-shadow: 0 6px 32px rgba(0,0,0,0.12);
            color: var(--text);
        }
        .search-box:focus { outline: 3px solid var(--primary); outline-offset: 2px; }
        main { max-width: 760px; margin: 0 auto; padding: 36px 20px 60px; }
        .phrase-list { list-style: none; display: flex; flex-direction: column; gap: 12px; }
        .phrase-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: box-shadow 0.2s, border-color 0.2s;
        }
        .phrase-card:hover { box-shadow: 0 4px 24px rgba(99,102,241,0.12); }
        .phrase-card.open { border-color: var(--primary); }
        .card-summary {
            padding: 18px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            user-select: none;
        }
        .card-summary:hover { background: #fafaff; }
        .card-main { flex: 1; min-width: 0; }
        .phrase-text { font-size: 1.2em; font-weight: 700; }
        .pronunciation { color: var(--text-muted); font-style: italic; font-size: 0.85em; margin-top: 2px; }
        .card-meta { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
        .difficulty {
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.72em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .beginner { background: #dcfce7; color: #15803d; }
        .intermediate { background: #fef9c3; color: #a16207; }
        .advanced { background: #fee2e2; color: #b91c1c; }
        .chevron { color: var(--text-muted); font-size: 0.75em; transition: transform 0.25s; flex-shrink: 0; }
        .phrase-card.open .chevron { transform: rotate(180deg); }
        .card-body {
            display: none;
            padding: 0 20px 20px;
            border-top: 1px solid var(--border);
        }
        .phrase-card.open .card-body { display: block; }
        .meaning {
            margin: 16px 0;
            padding: 14px 16px;
            background: #f8fafc;
            border-radius: 10px;
        }
        .meaning-en { font-size: 0.95em; margin-bottom: 4px; }
        .meaning-zh { color: var(--text-muted); font-size: 0.9em; }
        .examples-label {
            font-size: 0.72em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            margin: 14px 0 8px;
        }
        .example {
            padding: 10px 14px;
            border-left: 3px solid var(--primary);
            margin-bottom: 8px;
            background: #fafaff;
            border-radius: 0 8px 8px 0;
        }
        .example-en { font-size: 0.92em; margin-bottom: 3px; }
        .example-zh { color: var(--text-muted); font-size: 0.85em; }
        .cultural-note {
            margin-top: 14px;
            padding: 12px 16px;
            background: #fffbeb;
            border-radius: 10px;
            border-left: 3px solid #f59e0b;
        }
        .cultural-note-label {
            font-size: 0.72em;
            font-weight: 700;
            color: #b45309;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .cultural-note-text { font-size: 0.88em; color: #78350f; }
        .tags { margin-top: 14px; display: flex; flex-wrap: wrap; gap: 6px; }
        .tag {
            padding: 3px 10px;
            background: #eef2ff;
            color: var(--primary);
            border-radius: 20px;
            font-size: 0.78em;
            font-weight: 500;
        }
        footer {
            background: white;
            border-top: 1px solid var(--border);
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-size: 0.85em;
        }
        footer a { color: var(--primary); text-decoration: none; }
        footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="nav-inner">
            <a href="../index.html" class="back-link">← Home</a>
            <span class="nav-sep">/</span>
            <span class="nav-current">{{ category.name_en }}</span>
        </div>
    </nav>

    <div class="category-hero">
        <h1>{{ category.icon }} {{ category.name_en }}</h1>
        <p class="subtitle">{{ category.name_zh }}</p>
    </div>

    <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-box" placeholder="Search in this category..." id="search" autocomplete="off">
    </div>

    <main>
        <ul class="phrase-list">
            {% for phrase in phrases %}
            <li class="phrase-card" data-search="{{ phrase.phrase|lower }} {{ phrase.meaning_en|lower }} {{ phrase.meaning_zh }}">
                <div class="card-summary" onclick="toggleCard(this.parentElement)">
                    <div class="card-main">
                        <div class="phrase-text">{{ phrase.phrase }}</div>
                        {% if phrase.pronunciation %}
                        <div class="pronunciation">{{ phrase.pronunciation }}</div>
                        {% endif %}
                    </div>
                    <div class="card-meta">
                        <span class="difficulty {{ phrase.difficulty }}">{{ phrase.difficulty }}</span>
                        <span class="chevron">▼</span>
                    </div>
                </div>

                <div class="card-body">
                    <div class="meaning">
                        <div class="meaning-en">{{ phrase.meaning_en }}</div>
                        <div class="meaning-zh">{{ phrase.meaning_zh }}</div>
                    </div>

                    {% if phrase.examples %}
                    <div class="examples-label">Examples · 例句</div>
                    {% for example in phrase.examples %}
                    <div class="example">
                        <div class="example-en">{{ example.en }}</div>
                        <div class="example-zh">{{ example.zh }}</div>
                    </div>
                    {% endfor %}
                    {% endif %}

                    {% if phrase.cultural_note_en %}
                    <div class="cultural-note">
                        <div class="cultural-note-label">💡 Cultural Note</div>
                        <div class="cultural-note-text">{{ phrase.cultural_note_en }}</div>
                    </div>
                    {% endif %}

                    {% if phrase.tags %}
                    <div class="tags">
                        {% for tag in phrase.tags %}
                        <span class="tag"># {{ tag }}</span>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
            </li>
            {% endfor %}
        </ul>
    </main>

    <footer>
        <a href="../index.html">← All Categories</a> ·
        <a href="https://github.com/liyun95/everyday-english-phrases">GitHub</a>
    </footer>

    <script>
        function toggleCard(card) {
            card.classList.toggle('open');
        }
        document.getElementById('search').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.phrase-card').forEach(item => {
                item.style.display = item.dataset.search.includes(query) ? '' : 'none';
            });
        });
    </script>
</body>
</html>
"""


def load_category_metadata(category_dir: Path) -> dict[str, Any] | None:
    """Load category metadata from _category.yaml."""
    meta_file = category_dir / "_category.yaml"
    if not meta_file.exists():
        return None

    try:
        with open(meta_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        return None


def load_phrases_from_category(category_dir: Path) -> list[dict[str, Any]]:
    """Load all phrases from a category directory."""
    phrases = []

    for yaml_file in category_dir.glob("*.yaml"):
        if yaml_file.name == "_category.yaml":
            continue

        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError:
            continue

        if data and "phrases" in data:
            for phrase in data["phrases"]:
                phrases.append({
                    "phrase": phrase.get("phrase", ""),
                    "pronunciation": phrase.get("pronunciation", ""),
                    "meaning_en": phrase.get("meaning", {}).get("en", ""),
                    "meaning_zh": phrase.get("meaning", {}).get("zh", ""),
                    "context_en": phrase.get("context", {}).get("en", "") if isinstance(phrase.get("context"), dict) else "",
                    "context_zh": phrase.get("context", {}).get("zh", "") if isinstance(phrase.get("context"), dict) else "",
                    "cultural_note_en": phrase.get("cultural_note", {}).get("en", "") if isinstance(phrase.get("cultural_note"), dict) else "",
                    "cultural_note_zh": phrase.get("cultural_note", {}).get("zh", "") if isinstance(phrase.get("cultural_note"), dict) else "",
                    "examples": phrase.get("examples", []),
                    "difficulty": phrase.get("difficulty", "intermediate"),
                    "tags": phrase.get("tags", []),
                })

    return phrases


def generate_site(phrases_dir: Path, docs_dir: Path) -> None:
    """Generate the static site."""
    docs_dir.mkdir(exist_ok=True)
    categories_dir = docs_dir / "categories"
    categories_dir.mkdir(exist_ok=True)

    env = Environment(loader=FileSystemLoader("."))

    categories = []

    for category_dir in sorted(phrases_dir.iterdir()):
        if not category_dir.is_dir():
            continue

        meta = load_category_metadata(category_dir)
        if not meta:
            continue

        phrases = load_phrases_from_category(category_dir)

        category_data = {
            "slug": category_dir.name,
            "icon": meta.get("icon", "📁"),
            "name_en": meta.get("name", {}).get("en", category_dir.name),
            "name_zh": meta.get("name", {}).get("zh", ""),
            "desc_en": meta.get("description", {}).get("en", ""),
            "desc_zh": meta.get("description", {}).get("zh", ""),
            "order": meta.get("order", 99),
            "phrase_count": len(phrases),
        }

        categories.append(category_data)

        category_html = env.from_string(CATEGORY_TEMPLATE).render(
            category=category_data,
            phrases=phrases
        )

        category_file = categories_dir / f"{category_dir.name}.html"
        with open(category_file, "w", encoding="utf-8") as f:
            f.write(category_html)

        print(f"  Generated: {category_file.name} ({len(phrases)} phrases)")

    categories.sort(key=lambda x: x["order"])

    index_html = env.from_string(INDEX_TEMPLATE).render(categories=categories)

    index_file = docs_dir / "index.html"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"  Generated: index.html")


def main() -> int:
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    phrases_dir = project_dir / "phrases"
    docs_dir = project_dir / "docs"

    if not phrases_dir.exists():
        print(f"ERROR: Phrases directory not found: {phrases_dir}")
        return 1

    print("Generating GitHub Pages site...")
    generate_site(phrases_dir, docs_dir)

    print(f"\nSite generated in: {docs_dir}")
    print("To preview locally, run:")
    print(f"  cd {docs_dir} && python -m http.server")

    return 0


if __name__ == "__main__":
    sys.exit(main())
