"""modules/recon.py — Information Gathering & Reconnaissance (18 options)"""
from modules.base import BaseModule

class ReconModule(BaseModule):
    NAME        = 'Information Gathering'
    ICON        = '🔍'
    COLOR       = 'cyan'
    DESCRIPTION = 'Recon, port scanning, DNS, OSINT, subdomain discovery'
    TOOLS       = ['nmap','whois','host','dig','dnsrecon','subfinder','amass','theHarvester']
    OPTIONS = [
        # ── NMAP ──
        {'name':'Quick Scan (top 100 ports)',   'tool':'nmap',
         'description':'Fast scan of most common ports',
         'cmd':'nmap -F {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'}},

        {'name':'Full Port Scan (1-65535)',      'tool':'nmap',
         'description':'Scan every TCP port',
         'cmd':'nmap -p- {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'}},

        {'name':'Service & Version Detection',  'tool':'nmap',
         'description':'Identify running services and their versions',
         'cmd':'nmap -sV {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'}},

        {'name':'OS Detection',                 'tool':'nmap',
         'description':'Attempt to fingerprint the remote OS',
         'cmd':'nmap -O {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'requires_root':True},

        {'name':'Aggressive Scan (-A)',          'tool':'nmap',
         'description':'OS + version + scripts + traceroute',
         'cmd':'nmap -A {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'requires_root':True},

        {'name':'Stealth SYN Scan',             'tool':'nmap',
         'description':'Half-open TCP scan (less detectable)',
         'cmd':'nmap -sS {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'requires_root':True},

        {'name':'UDP Scan',                     'tool':'nmap',
         'description':'Scan top UDP ports',
         'cmd':'nmap -sU --top-ports 200 {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'requires_root':True},

        {'name':'Ping Sweep (host discovery)',  'tool':'nmap',
         'description':'Find live hosts in a subnet',
         'cmd':'nmap -sn {range}',
         'params':['range'],'hints':{'range':'CIDR range e.g. 192.168.1.0/24'}},

        # ── WHOIS / DNS ──
        {'name':'WHOIS Lookup',                 'tool':'whois',
         'description':'Domain registration information',
         'cmd':'whois {domain}',
         'params':['domain'],'hints':{'domain':'Domain name e.g. example.com'}},

        {'name':'DNS A Record',                 'tool':'host',
         'description':'Resolve hostname to IPv4',
         'cmd':'host -t A {domain}',
         'params':['domain'],'hints':{'domain':'Domain name'}},

        {'name':'DNS MX Record',                'tool':'host',
         'description':'Mail exchanger records',
         'cmd':'host -t MX {domain}',
         'params':['domain'],'hints':{'domain':'Domain name'}},

        {'name':'DNS TXT Record',               'tool':'host',
         'description':'TXT records (SPF, DKIM, etc.)',
         'cmd':'host -t TXT {domain}',
         'params':['domain'],'hints':{'domain':'Domain name'}},

        {'name':'Full DNS Recon',               'tool':'dnsrecon',
         'description':'Comprehensive DNS enumeration',
         'cmd':'dnsrecon -d {domain}',
         'params':['domain'],'hints':{'domain':'Target domain'}},

        {'name':'Zone Transfer Attempt',        'tool':'dig',
         'description':'Try AXFR zone transfer (misconfigured DNS)',
         'cmd':'dig axfr {domain} @{nameserver}',
         'params':['domain','nameserver'],
         'hints':{'domain':'Domain','nameserver':'NS server IP'}},

        # ── SUBDOMAIN / OSINT ──
        {'name':'Subdomain Enumeration',        'tool':'subfinder',
         'description':'Passive subdomain discovery',
         'cmd':'subfinder -d {domain}',
         'params':['domain'],'hints':{'domain':'Target domain'}},

        {'name':'OSINT Subdomain (amass)',       'tool':'amass',
         'description':'Deep OSINT-based subdomain enum',
         'cmd':'amass enum -d {domain}',
         'params':['domain'],'hints':{'domain':'Target domain'}},

        {'name':'Email & Domain Harvesting',    'tool':'theHarvester',
         'description':'Harvest emails, subdomains, IPs from public sources',
         'cmd':'theHarvester -d {domain} -b all',
         'params':['domain'],'hints':{'domain':'Target domain'}},

        {'name':'Custom nmap Command',
         'tool':'nmap','custom':True,
         'description':'Enter any nmap command manually'},
    ]
