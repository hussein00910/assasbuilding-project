"""
Category and option definitions.
Each category has a list of OPTIONS that map to pure Python tool functions.
"""

from tools.recon import (
    port_scan, dns_lookup, whois_lookup, ssl_check,
    subdomain_enum, banner_grab, ping_sweep,
)
from tools.web_tools import (
    http_headers, dir_bruteforce, sql_test,
    tech_detect, crawl_links, xss_test,
)
from tools.password_tools import (
    ssh_brute, ftp_brute, hash_identify, hash_generate,
)
from tools.network_tools import (
    traceroute, ip_geolocate, network_info, tcp_connect,
)


# ──────────────────────────────────────────────────────────────
# Option schema:
# {
#   "name":        display name
#   "icon":        emoji
#   "description": short description
#   "func":        Python function to call
#   "params": [
#     {"key": str, "label": str, "hint": str, "default": str}
#   ]
# }
# ──────────────────────────────────────────────────────────────

CATEGORIES = [
    {
        "id":    "recon",
        "name":  "Recon & Info",
        "icon":  "🔍",
        "color": "cyan",
        "desc":  "Information gathering and reconnaissance",
        "options": [
            {
                "name": "Quick Port Scan",
                "icon": "🚪",
                "description": "Scan 20 most common ports",
                "func": port_scan,
                "params": [
                    {"key": "target",     "label": "Target Host/IP",
                     "hint": "e.g. 192.168.1.1 or example.com",
                     "default": ""},
                    {"key": "port_range", "label": "Port Range",
                     "hint": "common | 1-1024 | 80,443,8080",
                     "default": "common"},
                ],
            },
            {
                "name": "Full Port Scan",
                "icon": "🔓",
                "description": "Scan all 65535 TCP ports",
                "func": port_scan,
                "params": [
                    {"key": "target",     "label": "Target Host/IP",
                     "hint": "e.g. 192.168.1.1",
                     "default": ""},
                    {"key": "port_range", "label": "Port Range",
                     "hint": "1-65535",
                     "default": "1-65535"},
                ],
            },
            {
                "name": "DNS Lookup (A)",
                "icon": "🌐",
                "description": "Resolve domain to IP address",
                "func": dns_lookup,
                "params": [
                    {"key": "domain",      "label": "Domain",
                     "hint": "example.com",
                     "default": ""},
                    {"key": "record_type", "label": "Record Type",
                     "hint": "A | AAAA | MX | NS | TXT",
                     "default": "A"},
                ],
            },
            {
                "name": "WHOIS Lookup",
                "icon": "📋",
                "description": "Domain registration information",
                "func": whois_lookup,
                "params": [
                    {"key": "domain", "label": "Domain",
                     "hint": "example.com",
                     "default": ""},
                ],
            },
            {
                "name": "SSL Certificate",
                "icon": "🔒",
                "description": "Check SSL/TLS certificate details",
                "func": ssl_check,
                "params": [
                    {"key": "host", "label": "Host",
                     "hint": "example.com",
                     "default": ""},
                    {"key": "port", "label": "Port",
                     "hint": "443",
                     "default": "443"},
                ],
            },
            {
                "name": "Subdomain Enum",
                "icon": "🗺️",
                "description": "Find subdomains by brute force",
                "func": subdomain_enum,
                "params": [
                    {"key": "domain",      "label": "Domain",
                     "hint": "example.com",
                     "default": ""},
                    {"key": "extra_words", "label": "Extra subdomains (optional)",
                     "hint": "intranet,vpn2,erp",
                     "default": ""},
                ],
            },
            {
                "name": "Banner Grab",
                "icon": "📡",
                "description": "Grab service banner from port",
                "func": banner_grab,
                "params": [
                    {"key": "host", "label": "Host",
                     "hint": "example.com",
                     "default": ""},
                    {"key": "port", "label": "Port",
                     "hint": "80",
                     "default": "80"},
                ],
            },
            {
                "name": "Ping Sweep",
                "icon": "📶",
                "description": "Find live hosts in a network range",
                "func": ping_sweep,
                "params": [
                    {"key": "cidr", "label": "CIDR Range",
                     "hint": "192.168.1.0/24",
                     "default": "192.168.1.0/24"},
                ],
            },
        ],
    },

    {
        "id":    "web",
        "name":  "Web App",
        "icon":  "🌐",
        "color": "green",
        "desc":  "Web application scanning and testing",
        "options": [
            {
                "name": "HTTP Headers",
                "icon": "📝",
                "description": "Analyze HTTP response headers + security",
                "func": http_headers,
                "params": [
                    {"key": "url", "label": "URL",
                     "hint": "https://example.com",
                     "default": ""},
                ],
            },
            {
                "name": "Directory Bruteforce",
                "icon": "📂",
                "description": "Find hidden directories and files",
                "func": dir_bruteforce,
                "params": [
                    {"key": "url",         "label": "Base URL",
                     "hint": "https://example.com",
                     "default": ""},
                    {"key": "extra_paths", "label": "Extra paths (optional)",
                     "hint": "upload,shell,cmd",
                     "default": ""},
                ],
            },
            {
                "name": "SQL Injection Test",
                "icon": "💉",
                "description": "Test URL parameter for SQLi",
                "func": sql_test,
                "params": [
                    {"key": "url",   "label": "URL",
                     "hint": "https://example.com/page",
                     "default": ""},
                    {"key": "param", "label": "Parameter",
                     "hint": "id",
                     "default": "id"},
                ],
            },
            {
                "name": "XSS Test",
                "icon": "⚡",
                "description": "Test for reflected XSS vulnerabilities",
                "func": xss_test,
                "params": [
                    {"key": "url",   "label": "URL",
                     "hint": "https://example.com/search",
                     "default": ""},
                    {"key": "param", "label": "Parameter",
                     "hint": "q",
                     "default": "q"},
                ],
            },
            {
                "name": "Tech Detection",
                "icon": "🔧",
                "description": "Identify CMS, frameworks, server software",
                "func": tech_detect,
                "params": [
                    {"key": "url", "label": "URL",
                     "hint": "https://example.com",
                     "default": ""},
                ],
            },
            {
                "name": "Link Crawler",
                "icon": "🕷️",
                "description": "Extract all links from a webpage",
                "func": crawl_links,
                "params": [
                    {"key": "url", "label": "URL",
                     "hint": "https://example.com",
                     "default": ""},
                ],
            },
        ],
    },

    {
        "id":    "passwords",
        "name":  "Passwords",
        "icon":  "🔑",
        "color": "purple",
        "desc":  "Password attacks and hash cracking",
        "options": [
            {
                "name": "SSH Brute Force",
                "icon": "🔐",
                "description": "Try common passwords against SSH",
                "func": ssh_brute,
                "params": [
                    {"key": "host",      "label": "SSH Host",
                     "hint": "192.168.1.1",
                     "default": ""},
                    {"key": "username",  "label": "Username",
                     "hint": "root",
                     "default": "root"},
                    {"key": "passwords", "label": "Passwords (comma-separated, optional)",
                     "hint": "pass1,pass2,pass3",
                     "default": ""},
                    {"key": "port",      "label": "Port",
                     "hint": "22",
                     "default": "22"},
                ],
            },
            {
                "name": "FTP Brute Force",
                "icon": "📤",
                "description": "Try common passwords against FTP",
                "func": ftp_brute,
                "params": [
                    {"key": "host",      "label": "FTP Host",
                     "hint": "192.168.1.1",
                     "default": ""},
                    {"key": "username",  "label": "Username",
                     "hint": "anonymous",
                     "default": "anonymous"},
                    {"key": "passwords", "label": "Passwords (optional)",
                     "hint": "pass1,pass2",
                     "default": ""},
                ],
            },
            {
                "name": "Hash Identify",
                "icon": "🔢",
                "description": "Identify hash type (MD5, SHA1, bcrypt...)",
                "func": hash_identify,
                "params": [
                    {"key": "hash_str", "label": "Hash string",
                     "hint": "5f4dcc3b5aa765d61d8327deb882cf99",
                     "default": ""},
                ],
            },
            {
                "name": "Hash Generate",
                "icon": "🔣",
                "description": "Generate MD5/SHA1/SHA256 hash of text",
                "func": hash_generate,
                "params": [
                    {"key": "text",      "label": "Text to hash",
                     "hint": "password123",
                     "default": ""},
                    {"key": "algorithm", "label": "Algorithm",
                     "hint": "all | md5 | sha1 | sha256 | sha512",
                     "default": "all"},
                ],
            },
        ],
    },

    {
        "id":    "network",
        "name":  "Network",
        "icon":  "🌐",
        "color": "teal",
        "desc":  "Network diagnostics and tools",
        "options": [
            {
                "name": "IP Geolocation",
                "icon": "📍",
                "description": "Get location info for an IP address",
                "func": ip_geolocate,
                "params": [
                    {"key": "ip", "label": "IP Address or Domain",
                     "hint": "8.8.8.8 or example.com",
                     "default": ""},
                ],
            },
            {
                "name": "Traceroute",
                "icon": "🛤️",
                "description": "Trace network path to destination",
                "func": traceroute,
                "params": [
                    {"key": "host",     "label": "Target Host",
                     "hint": "google.com",
                     "default": ""},
                    {"key": "max_hops", "label": "Max Hops",
                     "hint": "20",
                     "default": "20"},
                ],
            },
            {
                "name": "Network Info",
                "icon": "📊",
                "description": "Show local network and public IP info",
                "func": network_info,
                "params": [],
            },
            {
                "name": "TCP Connect",
                "icon": "🔌",
                "description": "Connect to TCP port and optionally send data",
                "func": tcp_connect,
                "params": [
                    {"key": "host",    "label": "Host",
                     "hint": "example.com",
                     "default": ""},
                    {"key": "port",    "label": "Port",
                     "hint": "80",
                     "default": "80"},
                    {"key": "message", "label": "Message to send (optional)",
                     "hint": "HELLO",
                     "default": ""},
                ],
            },
        ],
    },
]


def get_category(cat_id: str) -> dict:
    for cat in CATEGORIES:
        if cat['id'] == cat_id:
            return cat
    return {}
