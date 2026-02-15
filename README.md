# Everyday English Phrases 日常英语表达

A community-driven collection of real-world English phrases with bilingual (English-Chinese) explanations, designed for language learners who want to understand everyday expressions found in menus, signs, apps, and daily life.

## Features

- **Real-world phrases** - Expressions from restaurant menus, street signs, app interfaces, and daily life
- **Bilingual support** - English and Chinese explanations for each phrase
- **Cultural context** - Background information to help you understand usage
- **Anki flashcards** - Auto-generated decks for spaced repetition learning
- **Browsable site** - GitHub Pages site for easy browsing
- **Community-driven** - Open for contributions

## Quick Start

### Browse Phrases

Visit our [GitHub Pages site](https://yourusername.github.io/everyday-english-phrases/) to browse all phrases by category.

### Download Anki Deck

1. Go to the [Releases](../../releases) page
2. Download the latest `everyday-english.apkg` file
3. Import into Anki

### Build Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/everyday-english-phrases.git
cd everyday-english-phrases

# Install dependencies
pip install -r requirements.txt

# Validate phrase files
python scripts/validate.py

# Generate Anki deck
python scripts/generate_anki.py

# Generate GitHub Pages site
python scripts/generate_site.py
```

## Categories

### Food & Dining 餐饮美食

Phrases from restaurant menus, food packaging, and cooking shows.

- Restaurant menus
- Cooking terms
- Food descriptions

### Daily Life 日常生活

Expressions from everyday situations.

- Street signs
- App interfaces
- Public transport

## Phrase Structure

Each phrase includes:

| Field | Description |
|-------|-------------|
| `phrase` | The English expression |
| `pronunciation` | IPA pronunciation |
| `meaning` | Definition in English and Chinese |
| `context` | When and how to use it |
| `cultural_note` | Background information |
| `examples` | Example sentences with translations |
| `difficulty` | beginner, intermediate, or advanced |
| `tags` | Categories for filtering |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution

1. Found a phrase you'd like to add? [Open an issue](../../issues/new?template=new-phrase.md)
2. Want to add phrases directly? Fork, add to YAML files, submit PR

## Project Structure

```
everyday-english-phrases/
├── phrases/              # Source data (YAML)
│   ├── food-and-dining/
│   └── daily-life/
├── scripts/              # Build scripts
├── templates/            # Templates for new phrases
├── docs/                 # GitHub Pages site (generated)
└── output/               # Generated files (Anki deck)
```

## License

This project is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - you are free to share and adapt the content with attribution.

## Acknowledgments

- Initial phrases sourced from [Blacklock](https://theblacklock.com) restaurant menu
- Built with [genanki](https://github.com/kerrickstaley/genanki) for Anki deck generation
