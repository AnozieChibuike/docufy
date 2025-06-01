# geminitool/generate_readme.py

import os
import glob

# Defaults
DEFAULT_EXCLUDES = [
    "node_modules/",
    "__pycache__/",
    ".mypy_cache/",
    ".git/",
    ".venv/",
    "dist/",
    "build/",
    "*.log",
    "*.env",
    ".DS_Store",
    ".idea/",
    ".vscode/",
    "*.pyc",
]

MAX_CODE_SIZE = 25000  # max characters to feed Gemini at once

def load_readmeignore(folder):
    ignore_path = os.path.join(folder, ".readmeignore")
    excludes = []
    if os.path.isfile(ignore_path):
        with open(ignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    excludes.append(line)
    return excludes

def should_include_file(file_path, include_exts, excludes):
    # Extension check
    if include_exts:
        if not any(file_path.endswith(ext) for ext in include_exts):
            return False
    # Exclusion pattern check
    for pattern in excludes:
        if glob.fnmatch.fnmatch(file_path, pattern):
            return False
    return True

def collect_project_code(root_dir, include_exts, excludes):
    all_code = []
    total_len = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Prune excluded dirs early
        dirnames[:] = [d for d in dirnames if not any(glob.fnmatch.fnmatch(os.path.join(dirpath, d), pat) for pat in excludes)]

        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
            if should_include_file(rel_path, include_exts, excludes):
                try:
                    with open(os.path.join(dirpath, filename), "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    snippet = f"\n\n# File: {rel_path}\n" + content
                    # Limit total size to MAX_CODE_SIZE to avoid too large prompt
                    if total_len + len(snippet) > MAX_CODE_SIZE:
                        break
                    all_code.append(snippet)
                    total_len += len(snippet)
                except Exception:
                    continue
        else:
            continue
        break

    return "\n".join(all_code)

def generate_readme(root_dir, model, output_path, include_exts=None, user_excludes=None):
    if include_exts is None:
        include_exts = []
    if user_excludes is None:
        user_excludes = []

    # Load excludes from .readmeignore plus defaults and user excludes
    readmeignore_excludes = load_readmeignore(root_dir)
    excludes = set(DEFAULT_EXCLUDES + readmeignore_excludes + user_excludes)

    print("Collecting project code...")
    project_code = collect_project_code(root_dir, include_exts, excludes)

    if not project_code.strip():
        print("No code found to summarize.")
        return

    prompt = (
        "You are a senior software engineer and technical writer.\n"
        "Given the following project source code snippets, generate a professional, comprehensive README file in Markdown format.\n"
        "The README should include:\n"
        "- Project title\n"
        "- Short description\n"
        "- Installation instructions\n"
        "- Usage examples\n"
        "- Features overview\n"
        "- File structure summary\n"
        "- Any important notes\n\n"
        "Avoid including raw code snippets. Write clearly and concisely.\n\n"
        "Project source code snippets:\n"
        f"{project_code}\n\n"
        "Generate the README now:\n"
    )

    print("Generating README from Gemini model...")
    response = response = model.generate_content(prompt)

    readme_content = response.text.strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✅ README generated successfully at {output_path}")
