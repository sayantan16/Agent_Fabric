"""
Configuration Validator
Ensures all required settings are present and valid
"""

import os
import sys


def validate_config():
    """Validate configuration on startup."""
    errors = []

    # Check API keys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config

    if not config.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY not found in environment variables")

    if not config.ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY not found in environment variables")

    # Check directories exist
    for dir_path in [config.GENERATED_AGENTS_DIR, config.GENERATED_TOOLS_DIR]:
        if not os.path.exists(dir_path):
            errors.append(f"Directory {dir_path} does not exist")

    # Check registry files exist
    for file_path in [config.AGENTS_REGISTRY_PATH, config.TOOLS_REGISTRY_PATH]:
        if not os.path.exists(file_path):
            errors.append(f"Registry file {file_path} does not exist")

    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Configuration validated successfully")
        return True


if __name__ == "__main__":
    validate_config()
