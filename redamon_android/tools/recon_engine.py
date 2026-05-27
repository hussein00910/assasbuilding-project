"""tools/recon_engine.py
Nine pure-Python reconnaissance modules.
Every public method is a generator that yields str lines.
"""
import socket, ssl, threading, re, time
from queue import Queue
from urllib.parse import urljoin, urlparse

try:
    import requests
    requests.packages.urllib3.disable_warnings()
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Common ports with service names
COMMON_PORTS = {
    21:'FTP', 22:'SSH', 23:'Telnet', 25:'SMTP', 53:'DNS',
    80:'HTTP', 110:'POP3', 143:'IMAP', 443:'HTTPS', 445:'SMB',
    1433:'MSSQL', 1521:'Oracle', 3306:'MySQL', 3389:'RDP',
    5432:'PostgreSQL', 5900:'VNC', 6379:'Redis', 8080:'HTTP-Alt',
    8443:'HTTPS-Alt', 8888:'Jupyter', 9200:'Elasticsearch',
    27017:'MongoDB', 6443:'K8s-API', 2375:'Docker',
}

DIR_WORDLIST = [
    'admin','login','dashboard','wp-admin','phpmyadmin','config',
    'backup','test','api','v1','v2','upload','uploads','images',
    'static','media','files','data','db','database','user','users',
    'panel','cp','manager','administrator','index','app','robots.txt',
    'sitemap.xml','.env','.git','README.md','server-status',
    'phpinfo.php','wp-login.php','xmlrpc.php','.htaccess',
    'web.config','swagger.json','api-docs','graphql',
]

SUBDOMAINS = [
    'www','mail','remote','blog','webmail','server','ns1','ns2',
    'smtp','secure','vpn','m','shop','ftp','admin','portal','api',
    'dev','staging','test','app','cdn','static','media','img',
    'assets','docs','help','support','status','monitor','git',
    'jenkins','ci','jira','confluence','wiki','forum','login',
]

TECH_SIGNATURES = {
    'WordPress':   ['wp-content','wp-includes','WordPress'],
    'Joomla':      ['Joomla!', '/components/com_'],
    'Drupal':      ['Drupal.settings','/sites/default/files'],
    'Laravel':     ['laravel_session','Laravel'],
    'Django':      ['csrfmiddlewaretoken', 'django'],
    'React':       ['react.development','__reactFiber'],
    'Angular':     ['ng-version','angular.min.js'],
    'Vue.js':      ['vue.min.js','__vue__'],
    'jQuery':      ['jquery.min.js','jquery-'],
    'Bootstrap':   ['bootstrap.min.css','bootstrap.bundle'],
    'Apache':      ['Apache/', 'Server: Apache'],
    'Nginx':       ['nginx/', 'Server: nginx'],
    'IIS':         ['Server: Microsoft-IIS'],
    'PHP':         ['X-Powered-By: PHP','PHPSESSID'],
    'ASP.NET':     ['X-AspNet-Version','ASP.NET'],
    'Node.js':     ['X-Powered-By: Express'],
    'Cloudflare':  ['cf-ray', 'cloudflare'],
}


# ── 1. Port Scanner ─────────────────────────────────────────────────────────────
def port_scan(host, start=1, end=1024, timeout=0.5):
    yield f'[PORT SCAN] {host}  {start}-{end}\n'
    q = Queue()

    def _check(p):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                if s.connect_ex((host, p)) == 0:
                    svc = COMMON_PORTS.get(p, 'Unknown')
                    banner = ''
                    try:
                        s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                        banner = s.recv(64).decode(errors='ignore').split('\n')[0]
                    except:
                        pass
                    q.put((p, svc, banner.strip()))
        except:
            pass

    threads = []
    for port in range(start, end + 1):
        t = threading.Thread(target=_check, args=(port,), daemon=True)
        threads.append(t); t.start()
        if len(threads) >= 100:
            for th in threads: th.join()
            threads = []
    for th in threads: th.join()

    results = sorted(q.queue)
    if not results:
        yield '[!] No open ports found.\n'
    else:
        yield f'PORT       SERVICE      BANNER\n{"─"*55}\n'
        for port, svc, banner in results:
            b = (banner[:28] + '…') if len(banner) > 28 else banner
            yield f'{port:<10} {svc:<12} {b}\n'
    yield f'\n[✓] Done — {len(results)} open port(s)\n'


# ── 2. Subdomain Enumeration ─────────────────────────────────────────────────
def subdomain_enum(domain):
    yield f'[SUBDOMAIN] Enumerating: {domain}\n'
    found = []
    q = Queue()

    def _check(sub):
        fqdn = f'{sub}.{domain}'
        try:
            ip = socket.gethostbyname(fqdn)
            q.put((fqdn, ip))
        except:
            pass

    threads = [threading.Thread(target=_check, args=(s,), daemon=True)
               for s in SUBDOMAINS]
    for t in threads: t.start()
    for t in threads: t.join()

    while not q.empty():
        found.append(q.get())
    found.sort()

    if not found:
        yield '[!] No subdomains found.\n'
    else:
        yield f'SUBDOMAIN{" "*30} IP\n{"─"*55}\n'
        for fqdn, ip in found:
            yield f'{fqdn:<38} {ip}\n'
    yield f'\n[✓] Done — {len(found)} subdomain(s)\n'


# ── 3. DNS Lookup ───────────────────────────────────────────────────────────────
def dns_lookup(target):
    yield f'[DNS] Lookup: {target}\n\n'
    # A record
    try:
        ips = socket.getaddrinfo(target, None)
        seen = set()
        for r in ips:
            ip = r[4][0]
            if ip not in seen:
                seen.add(ip)
                yield f'  A/AAAA  {ip}\n'
    except Exception as e:
        yield f'  [!] A record: {e}\n'
    # Reverse DNS
    try:
        ip = socket.gethostbyname(target)
        host = socket.gethostbyaddr(ip)[0]
        yield f'  PTR     {host}\n'
    except:
        pass
    # MX (manual)
    try:
        import subprocess
        result = subprocess.run(['nslookup', '-type=MX', target],
                                capture_output=True, text=True, timeout=5)
        for line in result.stdout.splitlines():
            if 'mail exchanger' in line.lower() or 'MX' in line:
                yield f'  MX      {line.strip()}\n'
    except:
        pass
    yield f'\n[✓] DNS lookup complete\n'


# ── 4. SSL / TLS Analysis ─────────────────────────────────────────────────────
def ssl_check(host, port=443):
    yield f'[SSL] Checking {host}:{port}\n\n'
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(10)
            s.connect((host, port))
            cert = s.getpeercert()
            ver  = s.version()

        yield f'  Protocol   : {ver}\n'
        subject = dict(x[0] for x in cert.get('subject', []))
        issuer  = dict(x[0] for x in cert.get('issuer',  []))
        yield f'  Subject CN : {subject.get("commonName","?") }\n'
        yield f'  Issuer     : {issuer.get("organizationName","?")}\n'
        yield f'  Not Before : {cert.get("notBefore","?")}\n'
        yield f'  Not After  : {cert.get("notAfter","?")}\n'
        sans = [v for _, v in cert.get('subjectAltName', [])]
        if sans:
            yield f'  SANs       : {" , ".join(sans[:6])}\n'

        # Weak protocol check
        if ver in ('TLSv1', 'TLSv1.1', 'SSLv2', 'SSLv3'):
            yield f'  [HIGH] Weak protocol: {ver}\n'
        else:
            yield f'  [✓] Protocol OK: {ver}\n'
    except ssl.SSLCertVerificationError as e:
        yield f'  [HIGH] Certificate validation failed: {e}\n'
    except Exception as e:
        yield f'  [!] Could not connect: {e}\n'
    yield f'\n[✓] SSL check complete\n'


# ── 5. HTTP Header Analysis ────────────────────────────────────────────────────
def header_analysis(url):
    if not HAS_REQUESTS:
        yield '[!] requests library not available.\n'; return
    yield f'[HEADERS] {url}\n\n'
    try:
        r = requests.get(url, timeout=10, verify=False, allow_redirects=True)
        yield f'  Status   : {r.status_code}\n'
        yield f'  Final URL: {r.url}\n\n'
        yield '  ── All Headers ──\n'
        for k, v in r.headers.items():
            yield f'  {k}: {v}\n'
        SEC = {
            'Strict-Transport-Security': 'HIGH',
            'Content-Security-Policy':   'HIGH',
            'X-Frame-Options':           'MEDIUM',
            'X-Content-Type-Options':    'MEDIUM',
            'X-XSS-Protection':          'LOW',
            'Referrer-Policy':           'LOW',
            'Permissions-Policy':        'LOW',
        }
        yield '\n  ── Security Headers ──\n'
        for h, sev in SEC.items():
            if h in r.headers:
                yield f'  [✓] {h}\n'
            else:
                yield f'  [{sev}] MISSING: {h}\n'
        server  = r.headers.get('Server', 'Hidden')
        powered = r.headers.get('X-Powered-By', 'Hidden')
        yield f'\n  Server    : {server}\n'
        yield f'  Powered-By: {powered}\n'
    except Exception as e:
        yield f'  [!] Error: {e}\n'
    yield f'\n[✓] Header analysis complete\n'


# ── 6. Technology Fingerprinting ───────────────────────────────────────────────
def tech_detect(url):
    if not HAS_REQUESTS:
        yield '[!] requests library not available.\n'; return
    yield f'[TECH] Fingerprinting: {url}\n\n'
    try:
        r = requests.get(url, timeout=10, verify=False)
        body    = r.text
        headers = str(r.headers)
        combined = body + headers
        detected = []
        for tech, sigs in TECH_SIGNATURES.items():
            if any(s.lower() in combined.lower() for s in sigs):
                detected.append(tech)
        if detected:
            for t in detected:
                yield f'  [✓] {t}\n'
        else:
            yield '  [!] No known technologies detected.\n'
        cookies = list(r.cookies.keys())
        if cookies:
            yield f'\n  Cookies: {", ".join(cookies)}\n'
    except Exception as e:
        yield f'  [!] Error: {e}\n'
    yield f'\n[✓] Tech detection complete\n'


# ── 7. Directory Brute-Force ─────────────────────────────────────────────────────
def dir_bruteforce(url, wordlist=None):
    if not HAS_REQUESTS:
        yield '[!] requests library not available.\n'; return
    words = wordlist or DIR_WORDLIST
    if not url.endswith('/'): url += '/'
    yield f'[DIRB] {url}  ({len(words)} paths)\n\n'
    found = 0
    STATUS_OK = {200, 201, 301, 302, 403, 401}
    for path in words:
        try:
            r = requests.get(url + path, timeout=6, verify=False,
                             allow_redirects=False)
            if r.status_code in STATUS_OK:
                code = r.status_code
                size = len(r.content)
                mark = {'200':'[OK]','403':'[FORBIDDEN]','401':'[AUTH]',
                        '301':'[REDIR]','302':'[REDIR]'}.get(str(code), f'[{code}]')
                yield f'  {mark:<12} /{path:<30} {size}B\n'
                found += 1
        except requests.exceptions.ConnectionError:
            yield f'[!] Cannot connect to {url}\n'; return
        except:
            pass
    yield f'\n[✓] Done — {found} path(s) found\n'


# ── 8. WHOIS Lookup ────────────────────────────────────────────────────────────────
def whois_lookup(domain):
    yield f'[WHOIS] {domain}\n\n'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect(('whois.iana.org', 43))
            s.send(f'{domain}\r\n'.encode())
            raw = b''
            while True:
                chunk = s.recv(4096)
                if not chunk: break
                raw += chunk
        text = raw.decode(errors='ignore')
        # Extract key fields
        for line in text.splitlines():
            l = line.lower()
            if any(k in l for k in ('registrar','created','expir','name server',
                                    'registrant','status','updated','country')):
                yield f'  {line.strip()}\n'
    except Exception as e:
        yield f'  [!] WHOIS error: {e}\n'
    yield f'\n[✓] WHOIS complete\n'


# ── 9. Web Crawler ─────────────────────────────────────────────────────────────────
def web_crawl(url, max_pages=20):
    if not HAS_REQUESTS:
        yield '[!] requests library not available.\n'; return
    yield f'[CRAWL] {url}  (max {max_pages} pages)\n\n'
    visited, queue_, found_forms, found_params = set(), [url], [], set()
    base = urlparse(url).netloc

    while queue_ and len(visited) < max_pages:
        current = queue_.pop(0)
        if current in visited: continue
        visited.add(current)
        try:
            r = requests.get(current, timeout=8, verify=False,
                             allow_redirects=True)
            yield f'  [{r.status_code}] {current}\n'
            body = r.text
            # Find links
            links = re.findall(r'href=["\']([^"\']+)["\']', body)
            for lnk in links:
                full = urljoin(current, lnk)
                if urlparse(full).netloc == base and full not in visited:
                    queue_.append(full)
            # Find forms
            forms = re.findall(r'<form[^>]*action=["\']([^"\']*)["\']', body, re.I)
            for f in forms:
                if f not in found_forms:
                    found_forms.append(urljoin(current, f))
                    yield f'  [FORM] {urljoin(current, f)}\n'
            # Find URL params
            params = re.findall(r'[?&]([a-zA-Z_][\w]*)', current)
            for p in params:
                if p not in found_params:
                    found_params.add(p)
                    yield f'  [PARAM] {p}\n'
        except:
            pass
    yield f'\n[✓] Crawl done: {len(visited)} pages, {len(found_forms)} forms, {len(found_params)} params\n'
