# geminitool/__init__.py

import argparse
import os
import google.generativeai as genai
from .generate_readme import generate_readme

def main():
    parser = argparse.ArgumentParser(prog="docufy", description="Generate a README using Gemini Pro")
    parser.add_argument("--path", required=True, help="Path to your project folder")
    parser.add_argument("--out", default="README.md", help="Output README file path")
    parser.add_argument("--apikey", help="Gemini API key (or set GEMINI_API_KEY)")
    parser.add_argument("--include", nargs="+", default=[".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json"], help="File extensions to include")
    parser.add_argument("--exclude", nargs="+", default=[], help="Files/folders to exclude")
    parser.add_argument("--model",type=str,default="gemini-2.0-flash", help="Name of the Gemini model to use (default: gemini-1.5-pro)")
    
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ Please provide Gemini API key via --apikey or GEMINI_API_KEY env var.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(args.model)
    generate_readme(args.path, model, args.out,include_exts=args.include,user_excludes=args.exclude)
