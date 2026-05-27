"""core/checker.py — Detect which security tools are installed."""
import shutil

# Master list of all tools the toolkit can use
ALL_TOOLS: dict[str, str] = {
    # Recon
    'nmap':          'Network / Port scanner',
    'whois':         'Domain WHOIS lookup',
    'host':          'DNS query tool',
    'dig':           'DNS lookup utility',
    'dnsrecon':      'DNS reconnaissance',
    'subfinder':     'Subdomain discovery',
    'amass':         'OSINT subdomain enum',
    'theHarvester':  'Email & domain harvesting',
    # Scanning
    'nikto':         'Web server vulnerability scanner',
    'wapiti':        'Web application auditor',
    # Exploitation
    'msfconsole':    'Metasploit Framework console',
    'msfvenom':      'Metasploit payload generator',
    'sqlmap':        'SQL injection automation',
    'searchsploit':  'Exploit-DB offline search',
    # Passwords
    'hydra':         'Online password brute-forcer',
    'john':          'Offline hash cracker (John the Ripper)',
    'hashcat':       'GPU-accelerated hash cracker',
    'medusa':        'Parallel login brute-forcer',
    'crunch':        'Wordlist generator',
    # Web
    'gobuster':      'Directory / DNS brute-forcer',
    'dirb':          'Web directory brute-forcer',
    'wfuzz':         'Web fuzzer',
    'curl':          'HTTP request tool',
    'wget':          'File downloader',
    # Phishing
    'zphisher':      'Phishing page toolkit',
    'setoolkit':     'Social Engineering Toolkit',
    # Wireless
    'airmon-ng':     'Wireless monitor mode manager',
    'airodump-ng':   'Wireless packet capture',
    'aireplay-ng':   'Wireless packet injector',
    'aircrack-ng':   'WEP/WPA cracker',
    'wifite':        'Automated wireless auditor',
    'reaver':        'WPS brute-force tool',
    # Network
    'nc':            'Netcat — network Swiss army knife',
    'tcpdump':       'Packet capture',
    'tshark':        'Wireshark CLI analyzer',
    'ettercap':      'MITM attack suite',
    'arpspoof':      'ARP spoofing tool',
    'hping3':        'Custom TCP/IP packet crafting',
    # Forensics
    'binwalk':       'Firmware analysis & extraction',
    'strings':       'Extract printable strings',
    'steghide':      'Steganography tool',
    'exiftool':      'Metadata reader/writer',
    'volatility':    'Memory forensics framework',
    'foremost':      'File carving tool',
}


def check_tool(name: str) -> bool:
    """Return True if *name* is on PATH."""
    return shutil.which(name) is not None


def check_all() -> dict[str, bool]:
    """Return availability dict for every known tool."""
    return {name: check_tool(name) for name in ALL_TOOLS}


def get_description(name: str) -> str:
    return ALL_TOOLS.get(name, '')
