# geminitool/generate_readme.py

import os
import glob
from .utils import is_text_file
from .ai_analysis import ai_suggest_framework

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
                    # Normalize folder patterns to end with slash
                    if os.path.isdir(os.path.join(folder, line)) and not line.endswith('/'):
                        line += '/'
                    excludes.append(line)
    print(excludes)
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
            full_path = os.path.join(dirpath, filename)

            if not should_include_file(rel_path, include_exts, excludes):  # skip based on .readmeignore
                continue

            if not is_text_file(full_path):  # now the default filter
                continue

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                snippet = f"\n\n# File: {rel_path}\n" + content
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
    # for filename in filenames:
    #         rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
    #         if not is_text_file(rel_path):
    #             continue
    #         if should_include_file(rel_path, include_exts, excludes):
    #             try:
    #                 with open(os.path.join(dirpath, filename), "r", encoding="utf-8", errors="ignore") as f:
    #                     content = f.read()
    #                 snippet = f"\n\n# File: {rel_path}\n" + content
    #                 # Limit total size to MAX_CODE_SIZE to avoid too large prompt
    #                 if total_len + len(snippet) > MAX_CODE_SIZE:
    #                     break
    #                 all_code.append(snippet)
    #                 total_len += len(snippet)
    #             except Exception:
    #                 continue
    #     else:
    #         continue
    #     break

    # return "\n".join(all_code)

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
    
    # print("Detecting stack using Gemini...")
    # stack_info = ai_suggest_framework(project_code, model)
    
    # print(f"\nDetected Tech Stack:")
    # print(f"Language: {stack_info['language']}")
    # print(f"Framework: {stack_info['framework']}")
    # print(f"Libraries: {', '.join(stack_info['libraries'])}")


    # prompt = (
    #     "You are a senior software engineer and technical writer.\n"
    #     "Given the following project source code snippets, generate a professional, comprehensive README file in Markdown format.\n"
    #     "The README should include:\n"
    #     "- Project title\n"
    #     "- Short description\n"
    #     "- Installation instructions\n"
    #     "- Usage examples\n"
    #     "- Features overview\n"
    #     "- File structure summary\n"
    #     "- Any important notes\n\n"
    #     "Avoid including raw code snippets. Write clearly and concisely.\n\n"
    #     "Project source code snippets:\n"
    #     f"{project_code}\n\n"
    #     "Generate the README now:\n"
    # )
    
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
