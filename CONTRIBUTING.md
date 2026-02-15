# Contributing to Everyday English Phrases

Thank you for your interest in contributing! This guide will help you add new phrases to the collection.

## Ways to Contribute

### 1. Suggest a Phrase (Easiest)

[Open an issue](../../issues/new?template=new-phrase.md) using our template. We'll add it for you!

### 2. Add Phrases Directly

1. Fork this repository
2. Add your phrases to the appropriate YAML file
3. Run validation: `python scripts/validate.py`
4. Submit a pull request

## Adding a New Phrase

### Find the Right Category

Browse `phrases/` to find the appropriate category:

- `food-and-dining/` - Restaurant menus, cooking, food descriptions
- `daily-life/` - Signs, apps, transport, general life

### YAML Format

Add your phrase to the relevant `.yaml` file:

```yaml
- id: your-phrase-id          # lowercase, hyphens, unique within file
  phrase: "your phrase"
  pronunciation: "/IPA here/"

  meaning:
    en: "English definition"
    zh: "中文定义"

  context:
    en: "When and how to use this phrase"
    zh: "使用场景说明"

  cultural_note:              # Optional
    en: "Background information"
    zh: "文化背景"

  examples:
    - en: "Example sentence in English."
      zh: "例句的中文翻译。"

  difficulty: intermediate    # beginner, intermediate, or advanced

  tags:
    - relevant
    - tags
```

### Required Fields

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (lowercase, hyphens only) |
| `phrase` | The English expression |
| `meaning.en` | English definition |
| `meaning.zh` | Chinese definition |
| `examples` | At least one example with `en` and `zh` |
| `difficulty` | One of: `beginner`, `intermediate`, `advanced` |
| `tags` | At least one tag |

### Optional Fields

| Field | Description |
|-------|-------------|
| `pronunciation` | IPA pronunciation |
| `context.en/zh` | Usage context |
| `cultural_note.en/zh` | Cultural background |
| `related_phrases` | List of related expressions |

## Creating a New Category

1. Create a new directory under `phrases/`
2. Add a `_category.yaml` file:

```yaml
name:
  en: "Category Name"
  zh: "分类名称"

description:
  en: "What phrases belong in this category"
  zh: "这个分类包含哪些类型的短语"

icon: "🎯"    # Emoji for the category
order: 10     # Display order (lower = first)
```

3. Add your phrase files (e.g., `topic-name.yaml`)

## Quality Guidelines

### Good Phrases

- Real-world expressions you've encountered
- Not easily found in dictionaries
- Have cultural or contextual nuance
- Include accurate Chinese translations

### Phrase Sources

Please include source information in the file's `metadata` section:

```yaml
metadata:
  source: "Restaurant Name / App Name / Location"
  source_url: "https://example.com"  # Optional
  region: "UK"                        # UK, US, AU, etc.
  date_added: "2024-01-15"
```

### Translation Quality

- Translations should be natural, not literal
- Include context when direct translation doesn't work
- Use simplified Chinese (简体中文)

## Validation

Before submitting, run the validator:

```bash
python scripts/validate.py
```

This checks:

- Required fields are present
- IDs are unique
- YAML syntax is valid
- Difficulty values are valid

## Pull Request Process

1. Ensure validation passes
2. Use a descriptive PR title: "Add [category]: [brief description]"
3. List the phrases you've added in the PR description
4. One reviewer approval required for merge

## Code of Conduct

- Be respectful and constructive
- Ensure translations are accurate
- Credit sources appropriately
- No offensive or inappropriate content

## Questions?

Open an issue with the `question` label, and we'll help you out!
