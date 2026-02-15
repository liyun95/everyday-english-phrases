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
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        h1 { font-size: 2em; margin-bottom: 10px; }
        .subtitle { color: #666; }
        .search-box {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
        }
        .search-box:focus {
            outline: none;
            border-color: #4a90d9;
        }
        .categories {
            display: grid;
            gap: 20px;
        }
        .category-card {
            background: #fff;
            border: 1px solid #eee;
            border-radius: 12px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transition: box-shadow 0.2s, transform 0.2s;
        }
        .category-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .category-icon { font-size: 2em; margin-bottom: 10px; }
        .category-name { font-size: 1.2em; font-weight: bold; margin-bottom: 5px; }
        .category-name-zh { color: #666; font-size: 0.9em; }
        .category-desc { color: #888; font-size: 0.9em; margin-top: 10px; }
        .phrase-count { color: #4a90d9; font-size: 0.85em; margin-top: 10px; }
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #888;
            font-size: 0.9em;
        }
        footer a { color: #4a90d9; }
    </style>
</head>
<body>
    <header>
        <h1>Everyday English Phrases</h1>
        <p class="subtitle">日常英语表达</p>
        <p>Real-world English expressions with bilingual explanations</p>
    </header>

    <input type="text" class="search-box" placeholder="Search phrases... 搜索短语..." id="search" autocomplete="off">

    <div class="categories">
        {% for cat in categories %}
        <a href="categories/{{ cat.slug }}.html" class="category-card">
            <div class="category-icon">{{ cat.icon }}</div>
            <div class="category-name">{{ cat.name_en }}</div>
            <div class="category-name-zh">{{ cat.name_zh }}</div>
            <div class="category-desc">{{ cat.desc_en }}</div>
            <div class="phrase-count">{{ cat.phrase_count }} phrases</div>
        </a>
        {% endfor %}
    </div>

    <footer>
        <p>
            <a href="https://github.com/yourusername/everyday-english-phrases">GitHub</a> ·
            <a href="https://github.com/yourusername/everyday-english-phrases/releases">Download Anki Deck</a>
        </p>
        <p>Community-driven learning resource</p>
    </footer>

    <script>
        document.getElementById('search').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.category-card').forEach(card => {
                const text = card.textContent.toLowerCase();
                card.style.display = text.includes(query) ? '' : 'none';
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
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: #4a90d9;
            text-decoration: none;
        }
        .back-link:hover { text-decoration: underline; }
        header {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        h1 { font-size: 1.8em; margin-bottom: 5px; }
        .subtitle { color: #666; }
        .search-box {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
        }
        .search-box:focus {
            outline: none;
            border-color: #4a90d9;
        }
        .phrase-list { list-style: none; }
        .phrase-item {
            background: #fff;
            border: 1px solid #eee;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .phrase-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .phrase-text {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }
        .pronunciation {
            color: #888;
            font-style: italic;
            font-size: 0.9em;
        }
        .difficulty {
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75em;
        }
        .beginner { background: #d4edda; color: #155724; }
        .intermediate { background: #fff3cd; color: #856404; }
        .advanced { background: #f8d7da; color: #721c24; }
        .meaning {
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .meaning-en { font-size: 1em; margin-bottom: 5px; }
        .meaning-zh { color: #666; }
        .example {
            margin: 10px 0;
            padding-left: 15px;
            border-left: 3px solid #4a90d9;
        }
        .example-en { margin-bottom: 3px; }
        .example-zh { color: #666; font-size: 0.9em; }
        .cultural-note {
            margin-top: 15px;
            padding: 15px;
            background: #fffbf0;
            border-radius: 8px;
            border-left: 3px solid #f5a623;
        }
        .cultural-note-label {
            font-size: 0.85em;
            color: #856404;
            margin-bottom: 5px;
        }
        .tags {
            margin-top: 15px;
        }
        .tag {
            display: inline-block;
            padding: 2px 10px;
            background: #e9ecef;
            border-radius: 15px;
            font-size: 0.8em;
            color: #666;
            margin-right: 5px;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <a href="../index.html" class="back-link">← Back to categories</a>

    <header>
        <h1>{{ category.icon }} {{ category.name_en }}</h1>
        <p class="subtitle">{{ category.name_zh }}</p>
    </header>

    <input type="text" class="search-box" placeholder="Search in this category..." id="search" autocomplete="off">

    <ul class="phrase-list">
        {% for phrase in phrases %}
        <li class="phrase-item" data-search="{{ phrase.phrase|lower }} {{ phrase.meaning_en|lower }} {{ phrase.meaning_zh }}">
            <div class="phrase-header">
                <div>
                    <span class="phrase-text">{{ phrase.phrase }}</span>
                    {% if phrase.pronunciation %}
                    <span class="pronunciation">{{ phrase.pronunciation }}</span>
                    {% endif %}
                </div>
                <span class="difficulty {{ phrase.difficulty }}">{{ phrase.difficulty }}</span>
            </div>

            <div class="meaning">
                <div class="meaning-en">{{ phrase.meaning_en }}</div>
                <div class="meaning-zh">{{ phrase.meaning_zh }}</div>
            </div>

            {% for example in phrase.examples %}
            <div class="example">
                <div class="example-en">{{ example.en }}</div>
                <div class="example-zh">{{ example.zh }}</div>
            </div>
            {% endfor %}

            {% if phrase.cultural_note_en %}
            <div class="cultural-note">
                <div class="cultural-note-label">💡 Cultural Note</div>
                <div>{{ phrase.cultural_note_en }}</div>
            </div>
            {% endif %}

            {% if phrase.tags %}
            <div class="tags">
                {% for tag in phrase.tags %}
                <span class="tag">{{ tag }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </li>
        {% endfor %}
    </ul>

    <script>
        document.getElementById('search').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.phrase-item').forEach(item => {
                const text = item.dataset.search;
                item.style.display = text.includes(query) ? '' : 'none';
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
