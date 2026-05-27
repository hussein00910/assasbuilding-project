"""ai/agent.py — Claude AI Agent with multi-step ReAct analysis."""
import json
try:
    import requests as _req
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'
ANTHROPIC_VER = '2023-06-01'

# ── System Prompts ─────────────────────────────────────────────────────────────────
SYS_RECON = """
You are RedAmon, an expert AI penetration tester.
You analyze reconnaissance scan results for a given target.
Your task:
1. Identify OPEN PORTS and their risk (exposed services, version disclosure)
2. Identify MISSING SECURITY HEADERS and classify severity
3. Identify TECHNOLOGY STACK and known CVEs for detected versions
4. Identify EXPOSED PATHS that may lead to vulnerabilities
5. Identify SSL/TLS weaknesses

For each finding output exactly:
SEVERITY: [CRITICAL|HIGH|MEDIUM|LOW|INFO]
TITLE: <one-line title>
DETAIL: <2-3 sentence explanation>
---

Finish with a RISK LEVEL line: RISK: [CRITICAL|HIGH|MEDIUM|LOW]
"""

SYS_REPORT = """
You are RedAmon, an expert AI penetration tester writing a professional pentest report.
Structure your report with these exact sections:

## Executive Summary
## Risk Level: [CRITICAL/HIGH/MEDIUM/LOW]
## Attack Surface
## Vulnerabilities Found
## Exploitation Potential
## Recommendations
## Next Steps

Be concise, technical, and actionable. Format in Markdown.
"""

SYS_CHAT = """
You are RedAmon, an expert AI penetration tester.
You are discussing scan results for a specific target.
Answer the user's questions with technical accuracy.
If asked about exploitation, provide general educational guidance only.
Always remind the user to only test authorized systems.
"""


# ── Core API call ─────────────────────────────────────────────────────────────────
def _call(api_key, model, system, messages, max_tokens=4096):
    """Direct Anthropic API call via requests."""
    if not HAS_REQUESTS:
        return '[ERROR] requests library not installed.'
    if not api_key or api_key == 'YOUR_API_KEY':
        return '[ERROR] No Claude API key set. Go to Settings and add your key.'
    try:
        resp = _req.post(
            ANTHROPIC_URL,
            headers={
                'x-api-key': api_key,
                'anthropic-version': ANTHROPIC_VER,
                'content-type': 'application/json',
            },
            json={
                'model': model,
                'max_tokens': max_tokens,
                'system': system,
                'messages': messages,
            },
            timeout=90,
        )
        if resp.status_code == 200:
            return resp.json()['content'][0]['text']
        elif resp.status_code == 401:
            return '[ERROR] Invalid API key. Check Settings.'
        elif resp.status_code == 429:
            return '[ERROR] Rate limit hit. Wait a moment and retry.'
        else:
            return f'[ERROR] API {resp.status_code}: {resp.text[:200]}'
    except Exception as e:
        return f'[ERROR] Network error: {e}'


# ── Public Agent Functions ─────────────────────────────────────────────────────────
def analyze_scan(api_key, model, target, raw_results):
    """
    Step 1: Analyze raw scan output and extract structured findings.
    Returns the AI's finding analysis as a string.
    """
    prompt = (
        f'Target: {target}\n\n'
        f'Scan Results:\n{raw_results[:12000]}'
    )
    return _call(api_key, model, SYS_RECON,
                 [{'role': 'user', 'content': prompt}])


def generate_report(api_key, model, target, findings_text, raw_summary):
    """
    Step 2: Generate a full pentest report from findings.
    """
    prompt = (
        f'Target: {target}\n\n'
        f'Findings:\n{findings_text}\n\n'
        f'Raw scan summary:\n{raw_summary[:4000]}'
    )
    return _call(api_key, model, SYS_REPORT,
                 [{'role': 'user', 'content': prompt}],
                 max_tokens=6000)


def parse_findings(analysis_text):
    """
    Parse the structured finding blocks from analyze_scan() output.
    Returns list of dicts: {severity, title, detail}
    """
    findings = []
    blocks = analysis_text.split('---')
    for block in blocks:
        block = block.strip()
        if not block: continue
        sev = title = detail = ''
        for line in block.splitlines():
            if line.startswith('SEVERITY:'):
                sev = line.split(':', 1)[1].strip()
            elif line.startswith('TITLE:'):
                title = line.split(':', 1)[1].strip()
            elif line.startswith('DETAIL:'):
                detail = line.split(':', 1)[1].strip()
        if title:
            findings.append({
                'severity': sev or 'INFO',
                'title':    title,
                'detail':   detail,
            })
    return findings


def extract_risk(analysis_text):
    """Extract the overall RISK level from the analysis."""
    for line in analysis_text.splitlines():
        if line.strip().startswith('RISK:'):
            return line.split(':', 1)[1].strip()
    return 'Unknown'


def chat(api_key, model, history, user_msg, target, context):
    """
    Interactive chat with context about a specific scan.
    history: list of {role, content} dicts (conversation so far)
    Returns assistant reply string.
    """
    sys_with_ctx = (
        f'{SYS_CHAT}\n\n'
        f'Current target: {target}\n'
        f'Scan context:\n{context[:3000]}'
    )
    messages = list(history) + [{'role': 'user', 'content': user_msg}]
    return _call(api_key, model, sys_with_ctx, messages, max_tokens=2048)
