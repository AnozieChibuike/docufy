# Docufy: AI-Powered README Generator

## Description

Docufy is a command-line tool that leverages the power of the Gemini Pro model to automatically generate comprehensive README files for your software projects. By analyzing your project's file structure and code, Docufy intelligently creates a well-structured README, including a project description, installation instructions, usage examples, features overview, and file structure summary.  It also supports excluding specific files and directories, and specifying file extensions to include.

## Installation

1.  **Install the package:**

    ```bash
    pip install docufy
    ```

    *Note: You might need to configure your `PYTHONPATH` if the script is not found after installation.*

2.  **Obtain a Gemini API Key:**
    *   Go to the [Google AI Studio](https://makersuite.google.com/) and create an API key.

3.  **Set the Gemini API Key:**

    You can set the API Key using the `--apikey` argument or let `docufy` prompt you for it. The API Key will be stored securely in a `.env` file.

## Usage

To generate a README file for your project, navigate to your project's root directory in the terminal and run:

```bash
docufy --path . --out README.md
```

*   `--path`: Specifies the path to your project directory. Defaults to the current directory (`.`).
*   `--out`: Specifies the output file name for the generated README. Defaults to `README.md`.
*   `--apikey`:  (Optional) Specifies your Gemini API key directly. If not provided, Docufy will prompt you for it and store it securely.
*   `--include`: (Optional) Specifies a list of file extensions to include for analysis. Defaults to a common set of code extensions (`.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`, `.json`).
*   `--exclude`: (Optional) Specifies a list of files or directories to exclude from analysis.  Supports glob patterns for more flexible exclusion rules.
*   `--model`: (Optional) Specifies the Gemini model to use. Defaults to `gemini-2.0-flash`.
*   `--delete-key`: (Optional) Deletes the stored Gemini API key from the .env file.

**Examples:**

*   Generate a README for the current directory:

    ```bash
    docufy --path .
    ```

*   Generate a README with a specific output file name:

    ```bash
    docufy --path . --out my_project_readme.md
    ```

*   Exclude specific files and directories:

    ```bash
    docufy --path . --exclude "node_modules/" "*.log" ".DS_Store"
    ```

*   Include only Python and JavaScript files:

    ```bash
    docufy --path . --include ".py" ".js"
    ```

*   Delete the stored API key:
    ```bash
    docufy --delete-key
    ```

## Features Overview

*   **Automated README Generation:**  Automatically creates a comprehensive README file based on your project's code.
*   **AI-Powered Analysis:**  Uses the Gemini Pro model to understand your project's purpose and functionality.
*   **Customizable:** Allows you to specify file extensions to include and files/directories to exclude.
*   **Secure API Key Storage:** Securely stores your Gemini API key in a `.env` file (if not provided directly).
*   **.readmeignore Support:**  Respects `.readmeignore` files for specifying files and directories to exclude from analysis, similar to `.gitignore`.
*   **Text File Detection:** Only includes text-based files for analysis to avoid processing binary files.

## File Structure

The `docufy` package has the following structure:

```
docufy/
├── __init__.py        # Package initialization and entry point
├── ai_analysis.py   # Contains AI analysis functions (e.g., language detection)
├── generate_readme.py  # Contains the main logic for generating the README
├── utils.py           # Utility functions (e.g., API key handling, file type checking)
└── .env               # (Optional) Stores the Gemini API key
```

## Important Notes

*   **API Key Security:** The Gemini API key is stored in a `.env` file.  Ensure this file is not committed to version control (add it to your `.gitignore`).
*   **Gemini Pro Usage:** Generating README files requires the Gemini Pro model, which may have usage limits or costs associated with it.  Refer to the Google AI Studio documentation for details.
*   **Context Size Limit:** The tool limits the total code size sent to the Gemini model to avoid exceeding context window limits. If your project is very large, not all code may be included in the analysis. Consider using `--include` and `--exclude` to narrow down the code processed.
*   **.readmeignore file:** You can create a `.readmeignore` file in your project root directory to specify files and directories that should be excluded from the README generation process. The format is the same as `.gitignore`.
*   The quality of the generated README depends on the clarity and structure of your source code.