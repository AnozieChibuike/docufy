# geminitool/utils.py

import os
from dotenv import load_dotenv, set_key, unset_key
import mimetypes

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")


def is_text_file(filepath):
    """Check if file is text-based"""
    mime, _ = mimetypes.guess_type(filepath)
    if mime and mime.startswith('text/'):
        return True

    # Check common code extensions
    code_extensions = [
    # General programming languages
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.php', '.cs',
    '.cpp', '.c', '.h', '.hpp', '.swift', '.kt', '.kts', '.rs', '.dart', '.scala',
    '.lua', '.sh', '.bash', '.zsh', '.pl', '.r', '.m', '.jl', '.groovy',

    # Markup and templating
    '.html', '.htm', '.xml', '.xhtml', '.md', '.markdown', '.rst', '.adoc',
    '.njk', '.ejs', '.hbs', '.pug', '.jade', '.twig',

    # Config and environment files
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env', '.conf',

    # Build & package management
    '.gradle', '.pom', '.make', '.mk', '.cmake', '.bazel',

    # Docker & DevOps
    'dockerfile', '.dockerignore', '.compose', '.yml', '.yaml',

    # CI/CD
    '.gitlab-ci.yml', '.circleci/config.yml', '.travis.yml', 'Jenkinsfile',

    # Scripts
    '.bat', '.ps1', '.cmd',

    # Data formats (readable)
    '.csv', '.tsv',

    # Web & frontend specific
    '.vue', '.svelte', '.scss', '.sass', '.less', '.css',

    # Notebooks (code + markdown)
    '.ipynb',

    # Type hint/stub files
    '.pyi',

    # Protobuf, Thrift, GraphQL
    '.proto', '.thrift', '.graphql', '.gql',

    # SQL and migrations
    '.sql',

    # Terraform
    '.tf', '.tfvars',

    # Assembly languages
    '.asm', '.s',

    # Misc
    '.nix', '.bzl'
]

    if any(filepath.endswith(ext) for ext in code_extensions):
        return True

    # Check common config files
    config_files = ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle',
                    'dockerfile', 'docker-compose.yml', '.env', 'config.yml']
    if any(filepath.lower().endswith(f) for f in config_files):
        return True

    return False

def ensure_api_key():
    """Ensure Gemini API key is set, prompt and store if missing."""
    load_dotenv(ENV_PATH)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Gemini API key not found.")
        api_key = input("Please enter your Gemini API key: ").strip()
        if api_key:
            set_key(ENV_PATH, "GEMINI_API_KEY", api_key)
            print("API key saved securely in .env file.")
        else:
            print("No API key provided. Exiting.")
            exit(1)
    return api_key

def delete_api_key():
    """Delete the stored Gemini API key from .env."""
    load_dotenv(ENV_PATH)
    if os.getenv("GEMINI_API_KEY"):
        unset_key(ENV_PATH, "GEMINI_API_KEY")
        print("API key deleted from .env.")
    else:
        print("No API key found to delete.")
