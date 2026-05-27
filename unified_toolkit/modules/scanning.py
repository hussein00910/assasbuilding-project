"""modules/scanning.py — Vulnerability Scanning (10 options)"""
from modules.base import BaseModule

class ScanningModule(BaseModule):
    NAME        = 'Vulnerability Scanning'
    ICON        = '🛡️'
    COLOR       = 'yellow'
    DESCRIPTION = 'Find vulnerabilities using nmap NSE, nikto, wapiti'
    TOOLS       = ['nmap','nikto','wapiti']
    OPTIONS = [
        {'name':'Default NSE Scripts',          'tool':'nmap',
         'cmd':'nmap -sC {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'description':'Run nmap default script set'},

        {'name':'Vulnerability Scripts',        'tool':'nmap',
         'cmd':'nmap --script vuln {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'description':'Run all vulnerability-detection NSE scripts',
         'requires_root':True},

        {'name':'Auth Scripts',                 'tool':'nmap',
         'cmd':'nmap --script auth {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'description':'Check for default / weak credentials'},

        {'name':'Discovery Scripts',            'tool':'nmap',
         'cmd':'nmap --script discovery {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'description':'Service and host discovery scripts'},

        {'name':'Safe Scripts + Version',       'tool':'nmap',
         'cmd':'nmap -sV --script safe {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'description':'Comprehensive but non-intrusive scan'},

        {'name':'SMB Vulnerabilities',          'tool':'nmap',
         'cmd':'nmap --script smb-vuln* -p 445 {target}',
         'params':['target'],'hints':{'target':'Target IP'},
         'description':'Check for EternalBlue, MS17-010, etc.',
         'requires_root':True},

        {'name':'HTTP Vulnerabilities',         'tool':'nmap',
         'cmd':'nmap --script http-vuln* -p 80,443 {target}',
         'params':['target'],'hints':{'target':'Target IP / hostname'},
         'description':'Web-related vulnerability scripts'},

        {'name':'Nikto Web Server Scan',        'tool':'nikto',
         'cmd':'nikto -h {url}',
         'params':['url'],'hints':{'url':'Target URL e.g. http://site.com'},
         'description':'Comprehensive web server vulnerability scan'},

        {'name':'Nikto with SSL',               'tool':'nikto',
         'cmd':'nikto -h {url} -ssl',
         'params':['url'],'hints':{'url':'Target URL'},
         'description':'Nikto scan forcing SSL/TLS'},

        {'name':'Wapiti Web Audit',             'tool':'wapiti',
         'cmd':'wapiti -u {url}',
         'params':['url'],'hints':{'url':'Target URL'},
         'description':'Full web application vulnerability audit'},
    ]
