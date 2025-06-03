import textwrap

def ai_suggest_framework(context_str, model):
    """Detect framework using AI analysis"""
    prompt = textwrap.dedent(f"""
    Analyze the following project structure and codebase to determine the:
    1. Programming language
    2. Web framework
    3. Key libraries

    Respond in this EXACT format without additional text:
    Language: <language>
    Framework: <framework>
    Libraries: <comma-separated list>

    Project context:
    {context_str}
    """)

    response = model.generate_content(prompt)
    return parse_ai_response(response.text)


def parse_ai_response(response_text):
    """Parse AI response into structured data"""
    result = {
        'language': 'Unknown',
        'framework': 'Unknown',
        'libraries': []
    }

    try:
        for line in response_text.splitlines():
            if line.startswith('Language:'):
                result['language'] = line.split(':', 1)[1].strip()
            elif line.startswith('Framework:'):
                result['framework'] = line.split(':', 1)[1].strip()
            elif line.startswith('Libraries:'):
                libs = line.split(':', 1)[1].strip()
                result['libraries'] = [lib.strip() for lib in libs.split(',') if lib.strip()]
    except Exception:
        pass

    return result
