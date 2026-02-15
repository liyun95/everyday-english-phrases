#!/usr/bin/env python3
"""Validate YAML phrase files for required fields and structure."""

import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_PHRASE_FIELDS = {"id", "phrase", "meaning", "examples", "difficulty", "tags"}
REQUIRED_MEANING_FIELDS = {"en", "zh"}
VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
REQUIRED_CATEGORY_FIELDS = {"name", "description", "icon", "order"}


def load_yaml(file_path: Path) -> dict[str, Any] | None:
    """Load and parse a YAML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"  ERROR: Invalid YAML syntax in {file_path}")
        print(f"         {e}")
        return None


def validate_category(file_path: Path, data: dict[str, Any]) -> list[str]:
    """Validate a category metadata file."""
    errors = []

    for field in REQUIRED_CATEGORY_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "name" in data:
        if "en" not in data["name"]:
            errors.append("Missing name.en")
        if "zh" not in data["name"]:
            errors.append("Missing name.zh")

    if "description" in data:
        if "en" not in data["description"]:
            errors.append("Missing description.en")
        if "zh" not in data["description"]:
            errors.append("Missing description.zh")

    return errors


def validate_phrase(phrase: dict[str, Any], phrase_index: int) -> list[str]:
    """Validate a single phrase entry."""
    errors = []
    phrase_id = phrase.get("id", f"index-{phrase_index}")

    for field in REQUIRED_PHRASE_FIELDS:
        if field not in phrase:
            errors.append(f"[{phrase_id}] Missing required field: {field}")

    if "meaning" in phrase:
        for lang in REQUIRED_MEANING_FIELDS:
            if lang not in phrase["meaning"]:
                errors.append(f"[{phrase_id}] Missing meaning.{lang}")

    if "examples" in phrase:
        if not isinstance(phrase["examples"], list):
            errors.append(f"[{phrase_id}] 'examples' must be a list")
        elif len(phrase["examples"]) == 0:
            errors.append(f"[{phrase_id}] 'examples' must have at least one entry")
        else:
            for i, example in enumerate(phrase["examples"]):
                if "en" not in example:
                    errors.append(f"[{phrase_id}] Example {i + 1} missing 'en'")
                if "zh" not in example:
                    errors.append(f"[{phrase_id}] Example {i + 1} missing 'zh'")

    if "difficulty" in phrase:
        if phrase["difficulty"] not in VALID_DIFFICULTIES:
            errors.append(
                f"[{phrase_id}] Invalid difficulty: {phrase['difficulty']}. "
                f"Must be one of: {', '.join(VALID_DIFFICULTIES)}"
            )

    if "tags" in phrase:
        if not isinstance(phrase["tags"], list):
            errors.append(f"[{phrase_id}] 'tags' must be a list")
        elif len(phrase["tags"]) == 0:
            errors.append(f"[{phrase_id}] 'tags' must have at least one entry")

    return errors


def validate_phrase_file(file_path: Path, data: dict[str, Any]) -> list[str]:
    """Validate a phrase YAML file."""
    errors = []

    if "phrases" not in data:
        errors.append("Missing 'phrases' key")
        return errors

    if not isinstance(data["phrases"], list):
        errors.append("'phrases' must be a list")
        return errors

    seen_ids = set()
    for i, phrase in enumerate(data["phrases"]):
        phrase_errors = validate_phrase(phrase, i)
        errors.extend(phrase_errors)

        phrase_id = phrase.get("id")
        if phrase_id:
            if phrase_id in seen_ids:
                errors.append(f"[{phrase_id}] Duplicate phrase ID")
            seen_ids.add(phrase_id)

    return errors


def validate_all(phrases_dir: Path) -> tuple[int, int]:
    """Validate all YAML files in the phrases directory."""
    total_errors = 0
    total_files = 0

    for category_dir in phrases_dir.iterdir():
        if not category_dir.is_dir():
            continue

        print(f"\nCategory: {category_dir.name}")

        for yaml_file in category_dir.glob("*.yaml"):
            total_files += 1
            print(f"  Validating: {yaml_file.name}")

            data = load_yaml(yaml_file)
            if data is None:
                total_errors += 1
                continue

            if yaml_file.name == "_category.yaml":
                errors = validate_category(yaml_file, data)
            else:
                errors = validate_phrase_file(yaml_file, data)

            if errors:
                for error in errors:
                    print(f"    ERROR: {error}")
                total_errors += len(errors)
            else:
                print("    OK")

    return total_files, total_errors


def main() -> int:
    """Main entry point."""
    script_dir = Path(__file__).parent
    phrases_dir = script_dir.parent / "phrases"

    if not phrases_dir.exists():
        print(f"ERROR: Phrases directory not found: {phrases_dir}")
        return 1

    print("Validating phrase files...")
    total_files, total_errors = validate_all(phrases_dir)

    print(f"\n{'=' * 40}")
    print(f"Files validated: {total_files}")
    print(f"Errors found: {total_errors}")

    if total_errors > 0:
        print("\nValidation FAILED")
        return 1

    print("\nValidation PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
