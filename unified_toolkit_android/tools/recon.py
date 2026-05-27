"""
Reconnaissance tools — pure Python (no nmap binary needed).
All heavy functions accept an optional progress_cb(line) for streaming output.
"""

import socket
import ssl
import re
import ipaddress
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# Port Scanner
# ─────────────────────────────────────────────────────────────

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306,
    3389, 5432, 5900, 6379, 8080, 8443, 8888, 9200, 27017
]


def port_scan(target: str, port_range: str = "common",
              timeout: float = 1.5, progress_cb=None) -> str:
    """
    Scan TCP ports on target.
    port_range: 'common' | '1-1024' | '1-65535' | '80,443,8080'
    """
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    emit(f"[*] Port scan started on {target}  [{datetime.now().strftime('%H:%M:%S')}]")

    # Resolve host
    try:
        ip = socket.gethostbyname(target)
        emit(f"[*] Resolved: {target} → {ip}")
    except socket.gaierror as e:
        emit(f"[!] Cannot resolve {target}: {e}")
        return "\n".join(lines)

    # Build port list
    if port_range == "common":
        ports = COMMON_PORTS
        emit(f"[*] Scanning {len(ports)} common ports ...")
    elif "," in port_range:
        ports = [int(p.strip()) for p in port_range.split(",") if p.strip().isdigit()]
    elif "-" in port_range:
        start, end = port_range.split("-", 1)
        ports = list(range(int(start), int(end) + 1))
        emit(f"[*] Scanning ports {start}-{end} ({len(ports)} total) ...")
    else:
        ports = [int(port_range)]

    open_ports = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                # Try banner grab
                svc = _service_name(port)
                banner = _quick_banner(ip, port, timeout=0.5)
                info = f"{svc}  {banner}" if banner else svc
                open_ports.append(port)
                line = f"  [OPEN]  {port:5d}/tcp   {info}"
                emit(line)
        except Exception:
            pass

    if not open_ports:
        emit("[*] No open ports found.")
    else:
        emit(f"\n[+] {len(open_ports)} open port(s) found.")

    emit(f"[*] Scan complete  [{datetime.now().strftime('%H:%M:%S')}]")
    return "\n".join(lines)


def _service_name(port: int) -> str:
    known = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
        6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
        8888: "HTTP-Alt", 9200: "Elasticsearch", 27017: "MongoDB",
    }
    return known.get(port, "unknown")


def _quick_banner(ip: str, port: int, timeout: float = 0.5) -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        if port in (80, 8080, 8888):
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(256).decode('utf-8', errors='ignore').strip()
        s.close()
        # Return only first line
        first = banner.split('\n')[0][:60]
        return first if first else ""
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────
# DNS Lookup
# ─────────────────────────────────────────────────────────────

def dns_lookup(domain: str, record_type: str = "A",
               progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    emit(f"[*] DNS lookup: {domain}  type={record_type}")

    try:
        if record_type == "A":
            infos = socket.getaddrinfo(domain, None, socket.AF_INET)
            ips = list({i[4][0] for i in infos})
            for ip in ips:
                emit(f"  A     {domain}  →  {ip}")

        elif record_type == "AAAA":
            infos = socket.getaddrinfo(domain, None, socket.AF_INET6)
            ips = list({i[4][0] for i in infos})
            for ip in ips:
                emit(f"  AAAA  {domain}  →  {ip}")

        elif record_type in ("MX", "NS", "TXT", "CNAME"):
            # Use raw DNS query via socket to 8.8.8.8
            result = _raw_dns_query(domain, record_type)
            emit(result)
        else:
            emit(f"[!] Unsupported record type: {record_type}")
    except Exception as e:
        emit(f"[!] Error: {e}")

    return "\n".join(lines)


def _raw_dns_query(domain: str, qtype: str) -> str:
    """Minimal DNS query to 8.8.8.8:53 — returns raw text."""
    TYPE_MAP = {"A": 1, "NS": 2, "CNAME": 5, "MX": 15, "TXT": 16, "AAAA": 28}
    qtype_id = TYPE_MAP.get(qtype, 1)

    # Build DNS query packet
    txid = b'\xaa\xbb'
    flags = b'\x01\x00'
    qdcount = b'\x00\x01'
    zeros = b'\x00\x00\x00\x00\x00\x00'
    question = _encode_dns_name(domain) + qtype_id.to_bytes(2, 'big') + b'\x00\x01'
    packet = txid + flags + qdcount + zeros + question

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        s.sendto(packet, ('8.8.8.8', 53))
        data, _ = s.recvfrom(512)
        s.close()
        return f"  [{qtype}] Query sent and response received ({len(data)} bytes)\n  (Use a full DNS library for parsed results)"
    except Exception as e:
        return f"  [!] DNS query failed: {e}"


def _encode_dns_name(domain: str) -> bytes:
    parts = domain.split('.')
    encoded = b''
    for part in parts:
        encoded += len(part).to_bytes(1, 'big') + part.encode()
    return encoded + b'\x00'


# ─────────────────────────────────────────────────────────────
# WHOIS Lookup
# ─────────────────────────────────────────────────────────────

def whois_lookup(domain: str, progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    # Strip protocol if present
    domain = re.sub(r'^https?://', '', domain).split('/')[0].strip()
    emit(f"[*] WHOIS lookup for: {domain}")

    # Determine TLD → WHOIS server
    tld = domain.rsplit('.', 1)[-1].lower() if '.' in domain else domain
    whois_servers = {
        'com': 'whois.verisign-grs.com',
        'net': 'whois.verisign-grs.com',
        'org': 'whois.pir.org',
        'io':  'whois.iana.org',
        'co':  'whois.iana.org',
        'uk':  'whois.nic.uk',
        'de':  'whois.denic.de',
        'ru':  'whois.tcinet.ru',
        'sa':  'whois.iana.org',
    }
    server = whois_servers.get(tld, 'whois.iana.org')
    emit(f"[*] Querying {server} ...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server, 43))
        s.sendall(f"{domain}\r\n".encode())
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()

        text = response.decode('utf-8', errors='ignore')
        for line in text.splitlines():
            line = line.rstrip()
            if line and not line.startswith('%') and not line.startswith('#'):
                emit(f"  {line}")
    except Exception as e:
        emit(f"[!] WHOIS failed: {e}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# SSL Certificate Check
# ─────────────────────────────────────────────────────────────

def ssl_check(host: str, port: int = 443, progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    emit(f"[*] SSL/TLS check for {host}:{port}")

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()

        emit(f"  Protocol  : {version}")
        emit(f"  Cipher    : {cipher[0]} ({cipher[2]} bits)")
        emit(f"  Subject   : {dict(x[0] for x in cert.get('subject', []))}")
        emit(f"  Issuer    : {dict(x[0] for x in cert.get('issuer', []))}")
        emit(f"  Valid From: {cert.get('notBefore', 'N/A')}")
        emit(f"  Valid To  : {cert.get('notAfter', 'N/A')}")
        sans = cert.get('subjectAltName', [])
        if sans:
            emit(f"  SANs      : {', '.join(v for _, v in sans[:8])}")
        emit("[+] Certificate is valid.")
    except ssl.SSLCertVerificationError as e:
        emit(f"[!] Certificate verification FAILED: {e}")
    except Exception as e:
        emit(f"[!] SSL check failed: {e}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Subdomain Enumeration
# ─────────────────────────────────────────────────────────────

SUBDOMAIN_WORDLIST = [
    'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
    'cpanel', 'whm', 'autodiscover', 'autoconfig', 'admin', 'portal', 'vpn',
    'remote', 'api', 'app', 'dev', 'staging', 'test', 'beta', 'secure',
    'login', 'cdn', 'static', 'img', 'images', 'media', 'blog', 'shop',
    'store', 'support', 'help', 'docs', 'status', 'dashboard', 'm', 'mobile',
]


def subdomain_enum(domain: str, extra_words: str = "",
                   progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    words = list(SUBDOMAIN_WORDLIST)
    if extra_words:
        words += [w.strip() for w in extra_words.split(',') if w.strip()]

    emit(f"[*] Subdomain enumeration for: {domain}")
    emit(f"[*] Testing {len(words)} subdomains ...")

    found = []
    for sub in words:
        fqdn = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            found.append((fqdn, ip))
            emit(f"  [FOUND]  {fqdn:40s}  →  {ip}")
        except socket.gaierror:
            pass

    emit(f"\n[+] {len(found)} subdomain(s) found out of {len(words)} tested.")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Banner Grabber
# ─────────────────────────────────────────────────────────────

def banner_grab(host: str, port: int = 80, progress_cb=None) -> str:
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    emit(f"[*] Banner grab: {host}:{port}")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(8)
        s.connect((socket.gethostbyname(host), int(port)))

        # Send appropriate probe
        if port in (80, 8080, 8888):
            probe = f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n".encode()
        elif port == 443:
            emit("[*] HTTPS — use SSL check instead for certificate info.")
            s.close()
            return "\n".join(lines)
        else:
            probe = b""

        if probe:
            s.sendall(probe)

        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()

        emit("[+] Banner received:")
        for line in banner.splitlines()[:20]:
            emit(f"  {line}")
    except ConnectionRefusedError:
        emit(f"[!] Connection refused on port {port}")
    except Exception as e:
        emit(f"[!] Error: {e}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Ping Sweep
# ─────────────────────────────────────────────────────────────

def ping_sweep(cidr: str, progress_cb=None) -> str:
    """Try TCP connect to port 80 for each host in CIDR."""
    lines = []

    def emit(line):
        lines.append(line)
        if progress_cb:
            progress_cb(line)

    emit(f"[*] Ping sweep (TCP/80) on: {cidr}")

    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        emit(f"[!] Invalid CIDR: {e}")
        return "\n".join(lines)

    hosts = list(network.hosts())
    if len(hosts) > 254:
        emit("[!] Range too large — limited to first 254 hosts.")
        hosts = hosts[:254]

    emit(f"[*] Testing {len(hosts)} hosts ...")
    alive = []
    for ip in hosts:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((str(ip), 80))
            s.close()
            if result in (0, 111):  # 0=open, 111=refused (host alive)
                alive.append(str(ip))
                emit(f"  [UP]  {ip}")
        except Exception:
            pass

    emit(f"\n[+] {len(alive)} host(s) responded.")
    return "\n".join(lines)
