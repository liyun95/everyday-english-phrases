#!/usr/bin/env python3
"""Generate Anki deck from phrase YAML files."""

import hashlib
import random
import sys
from pathlib import Path
from typing import Any

import genanki
import yaml

MODEL_ID = 1607392319
DECK_ID = 2059400110

CARD_CSS = """
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  padding: 20px;
  background: #fafafa;
}

.front {
  text-align: center;
}

.phrase {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.pronunciation {
  font-size: 16px;
  color: #666;
  font-style: italic;
  margin-bottom: 15px;
}

.context {
  font-size: 14px;
  color: #888;
  padding: 10px;
  background: #f0f0f0;
  border-radius: 5px;
}

.back {
  text-align: left;
}

.section {
  margin: 15px 0;
  padding: 10px;
  background: #fff;
  border-radius: 5px;
  border-left: 3px solid #4a90d9;
}

.label {
  font-size: 12px;
  color: #999;
  text-transform: uppercase;
  margin-bottom: 5px;
}

.meaning-en, .example-en {
  font-size: 16px;
  color: #333;
  margin-bottom: 5px;
}

.meaning-zh, .example-zh {
  font-size: 14px;
  color: #666;
}

.cultural {
  border-left-color: #f5a623;
  background: #fffbf0;
}

.meta {
  margin-top: 20px;
  font-size: 12px;
}

.difficulty {
  padding: 2px 8px;
  border-radius: 10px;
  margin-right: 10px;
}

.beginner { background: #d4edda; color: #155724; }
.intermediate { background: #fff3cd; color: #856404; }
.advanced { background: #f8d7da; color: #721c24; }

.tags {
  color: #999;
}

hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 15px 0;
}
"""

FRONT_TEMPLATE = """
<div class="card front">
  <div class="phrase">{{Phrase}}</div>
  {{#Pronunciation}}
  <div class="pronunciation">{{Pronunciation}}</div>
  {{/Pronunciation}}
  {{#Context}}
  <div class="context">{{Context}}</div>
  {{/Context}}
</div>
"""

BACK_TEMPLATE = """
<div class="card back">
  <div class="phrase">{{Phrase}}</div>
  {{#Pronunciation}}
  <div class="pronunciation">{{Pronunciation}}</div>
  {{/Pronunciation}}

  <hr>

  <div class="section">
    <div class="label">Meaning 含义</div>
    <div class="meaning-en">{{MeaningEN}}</div>
    <div class="meaning-zh">{{MeaningZH}}</div>
  </div>

  {{#Example}}
  <div class="section">
    <div class="label">Example 例句</div>
    <div class="example-en">{{Example}}</div>
    <div class="example-zh">{{ExampleZH}}</div>
  </div>
  {{/Example}}

  {{#CulturalNote}}
  <div class="section cultural">
    <div class="label">💡 Cultural Note 文化背景</div>
    <div class="note">{{CulturalNote}}</div>
  </div>
  {{/CulturalNote}}

  <div class="meta">
    <span class="difficulty {{Difficulty}}">{{Difficulty}}</span>
    <span class="tags">{{Tags}}</span>
  </div>
</div>
"""

phrase_model = genanki.Model(
    MODEL_ID,
    "Everyday English Phrase",
    fields=[
        {"name": "Phrase"},
        {"name": "Pronunciation"},
        {"name": "MeaningEN"},
        {"name": "MeaningZH"},
        {"name": "Context"},
        {"name": "Example"},
        {"name": "ExampleZH"},
        {"name": "CulturalNote"},
        {"name": "Difficulty"},
        {"name": "Tags"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": FRONT_TEMPLATE,
            "afmt": BACK_TEMPLATE,
        },
    ],
    css=CARD_CSS,
)


def generate_note_id(phrase_id: str) -> int:
    """Generate a stable note ID from the phrase ID."""
    hash_bytes = hashlib.md5(phrase_id.encode()).digest()
    return int.from_bytes(hash_bytes[:8], byteorder="big") % (2**31)


def create_note(phrase: dict[str, Any], category: str) -> genanki.Note:
    """Create an Anki note from a phrase entry."""
    phrase_id = phrase.get("id", "")
    phrase_text = phrase.get("phrase", "")
    pronunciation = phrase.get("pronunciation", "")

    meaning = phrase.get("meaning", {})
    meaning_en = meaning.get("en", "")
    meaning_zh = meaning.get("zh", "")

    context = phrase.get("context", {})
    context_text = context.get("en", "") if isinstance(context, dict) else ""

    examples = phrase.get("examples", [])
    example_en = examples[0].get("en", "") if examples else ""
    example_zh = examples[0].get("zh", "") if examples else ""

    cultural_note = phrase.get("cultural_note", {})
    cultural_text = cultural_note.get("en", "") if isinstance(cultural_note, dict) else ""

    difficulty = phrase.get("difficulty", "intermediate")
    tags = phrase.get("tags", [])
    tags_text = ", ".join(tags) if tags else ""

    note = genanki.Note(
        model=phrase_model,
        fields=[
            phrase_text,
            pronunciation,
            meaning_en,
            meaning_zh,
            context_text,
            example_en,
            example_zh,
            cultural_text,
            difficulty,
            tags_text,
        ],
        guid=str(generate_note_id(phrase_id)),
        tags=[category] + tags,
    )

    return note


def load_phrases(phrases_dir: Path) -> list[tuple[str, dict[str, Any]]]:
    """Load all phrases from YAML files."""
    phrases = []

    for category_dir in phrases_dir.iterdir():
        if not category_dir.is_dir():
            continue

        category_name = category_dir.name

        for yaml_file in category_dir.glob("*.yaml"):
            if yaml_file.name == "_category.yaml":
                continue

            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Warning: Skipping {yaml_file} due to YAML error: {e}")
                continue

            if data and "phrases" in data:
                for phrase in data["phrases"]:
                    phrases.append((category_name, phrase))

    return phrases


def generate_deck(phrases_dir: Path, output_path: Path) -> int:
    """Generate the Anki deck."""
    deck = genanki.Deck(DECK_ID, "Everyday English Phrases")

    phrases = load_phrases(phrases_dir)
    print(f"Found {len(phrases)} phrases")

    for category, phrase in phrases:
        note = create_note(phrase, category)
        deck.add_note(note)
        print(f"  Added: {phrase.get('phrase', 'unknown')}")

    package = genanki.Package(deck)
    package.write_to_file(str(output_path))

    return len(phrases)


def main() -> int:
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    phrases_dir = project_dir / "phrases"
    output_dir = project_dir / "output"

    if not phrases_dir.exists():
        print(f"ERROR: Phrases directory not found: {phrases_dir}")
        return 1

    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "everyday-english.apkg"

    print("Generating Anki deck...")
    count = generate_deck(phrases_dir, output_path)

    print(f"\nGenerated deck with {count} cards")
    print(f"Output: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
