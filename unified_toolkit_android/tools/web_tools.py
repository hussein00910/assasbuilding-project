"""
Web application security tools — pure Python using requests + re.
"""

import re
import socket
import ssl

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Android; SecurityToolkit) AppleWebKit/537.36',
}

TIMEOUT = 10


def _get(url, **kwargs):
    if not REQUESTS_OK:
        raise RuntimeError("requests library not available")
    return requests.get(url, headers=HEADERS, timeout=TIMEOUT,
                        verify=False, allow_redirects=True, **kwargs)


def _ensure_scheme(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url


# ─────────────────────────────────────────────────────────────
# HTTP Headers Analysis
# ─────────────────────────────────────────────────────────────

SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'Content-Security-Policy',
    'X-Frame-Options',
    'X-Content-Type-Options',
    'X-XSS-Protection',
    'Referrer-Policy',
    'Permissions-Policy',
    'Access-Control-Allow-Origin',
]


def http_headers(url: str, progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    url = _ensure_scheme(url)
    emit(f"[*] Checking HTTP headers: {url}")

    try:
        r = _get(url)
        emit(f"  Status Code : {r.status_code} {r.reason}")
        emit(f"  Final URL   : {r.url}")
        emit("")
        emit("  ── All Response Headers ──")
        for k, v in r.headers.items():
            emit(f"  {k:35s}: {v}")

        emit("")
        emit("  ── Security Headers Analysis ──")
        for sh in SECURITY_HEADERS:
            if sh in r.headers:
                emit(f"  [✓] {sh}")
            else:
                emit(f"  [✗] MISSING: {sh}")
    except Exception as e:
        emit(f"[!] Error: {e}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Directory / Path Bruteforce
# ─────────────────────────────────────────────────────────────

DIR_WORDLIST = [
    'admin', 'login', 'dashboard', 'api', 'v1', 'v2', 'backup', 'config',
    'uploads', 'images', 'static', 'assets', 'js', 'css', 'wp-admin',
    'wp-login.php', '.git', '.env', 'robots.txt', 'sitemap.xml',
    'phpinfo.php', 'info.php', 'test', 'debug', 'console', 'phpmyadmin',
    'database', 'db', 'sql', 'data', 'logs', 'log', 'error', 'errors',
    'tmp', 'temp', 'cache', 'cgi-bin', 'bin', 'shell', 'cmd', 'exec',
    'old', 'bak', 'backup.zip', 'backup.tar.gz', 'README', 'README.md',
    'CHANGELOG', 'LICENSE', 'Makefile', 'package.json', 'composer.json',
    'swagger', 'swagger-ui', 'api-docs', 'docs', 'documentation',
]


def dir_bruteforce(url: str, extra_paths: str = "",
                   progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    url = _ensure_scheme(url).rstrip('/')
    words = list(DIR_WORDLIST)
    if extra_paths:
        words += [p.strip() for p in extra_paths.split(',') if p.strip()]

    emit(f"[*] Directory bruteforce: {url}")
    emit(f"[*] Testing {len(words)} paths ...")
    found = []

    for path in words:
        target = f"{url}/{path}"
        try:
            r = _get(target)
            code = r.status_code
            if code in (200, 201, 204, 301, 302, 401, 403):
                label = {200: "OK", 201: "CREATED", 204: "NO CONTENT",
                         301: "REDIRECT", 302: "REDIRECT",
                         401: "AUTH REQUIRED", 403: "FORBIDDEN"}.get(code, str(code))
                line = f"  [{code}] {label:15s} {target}"
                found.append(line)
                emit(line)
        except Exception:
            pass

    emit(f"\n[+] {len(found)} path(s) found.")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# SQL Injection Tester
# ─────────────────────────────────────────────────────────────

SQL_PAYLOADS = [
    "'", '"', "' OR '1'='1", "' OR 1=1--", "'; DROP TABLE users--",
    "1' AND '1'='1", "1 UNION SELECT NULL--",
    "' OR SLEEP(3)--", "' AND 1=1--", "' AND 1=2--",
]

SQL_ERRORS = [
    'sql syntax', 'mysql_fetch', 'odbc', 'jdbc', 'oracle', 'sqlite',
    'syntax error', 'unexpected token', 'pg_query', 'database error',
    'ORA-', 'Microsoft OLE DB', 'SQLSTATE',
]


def sql_test(url: str, param: str = "id", progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    url = _ensure_scheme(url)
    emit(f"[*] SQL injection test: {url}")
    emit(f"[*] Parameter: {param}")
    emit(f"[*] Testing {len(SQL_PAYLOADS)} payloads ...")

    vulns_found = 0
    for payload in SQL_PAYLOADS:
        try:
            # Append payload to URL param
            test_url = f"{url}?{param}={requests.utils.quote(payload)}"
            r = _get(test_url)
            body = r.text.lower()
            for err in SQL_ERRORS:
                if err in body:
                    emit(f"  [VULN!] Error detected with payload: {payload!r}")
                    emit(f"         SQL error signature: '{err}'")
                    vulns_found += 1
                    break
        except Exception as e:
            emit(f"  [!] Request failed for {payload!r}: {e}")

    if vulns_found:
        emit(f"\n[!!!] {vulns_found} potential SQL injection point(s) found!")
    else:
        emit("\n[*] No obvious SQL injection errors detected.")
        emit("    (Manual testing recommended — blind SQLi may not show errors)")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Technology Detection
# ─────────────────────────────────────────────────────────────

TECH_SIGNATURES = {
    'WordPress':    [r'wp-content', r'wp-includes', r'WordPress'],
    'Joomla':       [r'Joomla!', r'/components/com_'],
    'Drupal':       [r'Drupal', r'/sites/default/'],
    'Django':       [r'csrfmiddlewaretoken', r'__admin'],
    'Laravel':      [r'laravel', r'XSRF-TOKEN'],
    'React':        [r'react-dom', r'__REACT'],
    'Angular':      [r'ng-version', r'angular'],
    'Vue.js':       [r'vue\.js', r'__vue__'],
    'jQuery':       [r'jquery', r'jQuery'],
    'Bootstrap':    [r'bootstrap', r'Bootstrap'],
    'PHP':          [r'\.php', r'X-Powered-By: PHP'],
    'ASP.NET':      [r'ASP\.NET', r'__VIEWSTATE', r'aspx'],
    'Node.js':      [r'X-Powered-By: Express', r'node\.js'],
    'Apache':       [r'Apache/', r'Server: Apache'],
    'Nginx':        [r'nginx', r'Server: nginx'],
    'CloudFlare':   [r'cloudflare', r'cf-ray'],
    'AWS':          [r'amazonaws', r'X-Amzn'],
}


def tech_detect(url: str, progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    url = _ensure_scheme(url)
    emit(f"[*] Technology detection: {url}")

    try:
        r = _get(url)
        body = r.text
        headers_str = str(r.headers)
        combined = body + headers_str

        emit(f"  Status : {r.status_code}")
        emit(f"  Server : {r.headers.get('Server', 'N/A')}")
        emit(f"  X-Powered-By: {r.headers.get('X-Powered-By', 'N/A')}")
        emit("")
        emit("  ── Detected Technologies ──")

        detected = []
        for tech, patterns in TECH_SIGNATURES.items():
            for pat in patterns:
                if re.search(pat, combined, re.IGNORECASE):
                    detected.append(tech)
                    emit(f"  [+] {tech}")
                    break

        if not detected:
            emit("  (No known technologies detected)")

        # Cookies
        if r.cookies:
            emit("")
            emit("  ── Cookies ──")
            for c in r.cookies:
                emit(f"  {c.name} = {c.value[:40]}")

    except Exception as e:
        emit(f"[!] Error: {e}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Link Crawler
# ─────────────────────────────────────────────────────────────

def crawl_links(url: str, depth: int = 1, progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    url = _ensure_scheme(url)
    emit(f"[*] Crawling links on: {url}")

    try:
        r = _get(url)
        links = re.findall(r'href=["\']([\'"]+)["\']', r.text, re.IGNORECASE)

        # Normalise
        from urllib.parse import urljoin, urlparse
        base = urlparse(url)
        all_links = set()
        internal = []
        external = []

        for link in links:
            full = urljoin(url, link)
            parsed = urlparse(full)
            if parsed.scheme in ('http', 'https') and full not in all_links:
                all_links.add(full)
                if parsed.netloc == base.netloc:
                    internal.append(full)
                else:
                    external.append(full)

        emit(f"\n  ── Internal Links ({len(internal)}) ──")
        for l in internal[:40]:
            emit(f"  {l}")

        emit(f"\n  ── External Links ({len(external)}) ──")
        for l in external[:20]:
            emit(f"  {l}")

        emit(f"\n[+] Total: {len(all_links)} unique links found.")
    except Exception as e:
        emit(f"[!] Error: {e}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# XSS Detection
# ─────────────────────────────────────────────────────────────

XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '"><script>alert(1)</script>',
    "'><script>alert(1)</script>",
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    'javascript:alert(1)',
    '<body onload=alert(1)>',
]


def xss_test(url: str, param: str = "q", progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    url = _ensure_scheme(url)
    emit(f"[*] XSS test: {url}  param={param}")

    vulns = 0
    for payload in XSS_PAYLOADS:
        try:
            test_url = f"{url}?{param}={requests.utils.quote(payload)}"
            r = _get(test_url)
            if payload in r.text or payload.lower() in r.text.lower():
                emit(f"  [REFLECTED!] Payload reflected: {payload[:50]}")
                vulns += 1
        except Exception:
            pass

    if vulns:
        emit(f"\n[!!!] {vulns} reflected XSS candidate(s) found!")
    else:
        emit("\n[*] No reflected XSS detected. (DOM-based XSS requires browser)")

    return "\n".join(lines)
