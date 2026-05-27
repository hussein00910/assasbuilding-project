"""modules/web.py — Web Application Testing (14 options)"""
from modules.base import BaseModule

class WebModule(BaseModule):
    NAME        = 'Web Application'
    ICON        = '🌐'
    COLOR       = 'blue'
    DESCRIPTION = 'Gobuster, Dirb, SQLMap, Wfuzz, Nikto, Curl'
    TOOLS       = ['gobuster','dirb','sqlmap','wfuzz','nikto','curl']
    OPTIONS = [
        # ── Gobuster ──
        {'name':'Gobuster: Directory Mode',     'tool':'gobuster',
         'cmd':'gobuster dir -u {url} -w {wordlist}',
         'params':['url','wordlist'],
         'hints':{'url':'Target URL','wordlist':'Wordlist e.g. /usr/share/wordlists/dirb/common.txt'},
         'description':'Brute-force directories and files'},

        {'name':'Gobuster: DNS Subdomain',      'tool':'gobuster',
         'cmd':'gobuster dns -d {domain} -w {wordlist}',
         'params':['domain','wordlist'],
         'hints':{'domain':'Target domain','wordlist':'Subdomain wordlist'},
         'description':'Brute-force subdomains via DNS'},

        {'name':'Gobuster: Virtual Hosts',      'tool':'gobuster',
         'cmd':'gobuster vhost -u {url} -w {wordlist}',
         'params':['url','wordlist'],
         'hints':{'url':'Base URL','wordlist':'Vhost wordlist'},
         'description':'Enumerate virtual hosts'},

        # ── Dirb ──
        {'name':'Dirb: Default Wordlist',       'tool':'dirb',
         'cmd':'dirb {url}',
         'params':['url'],'hints':{'url':'Target URL'},
         'description':'Directory brute-force with built-in wordlist'},

        {'name':'Dirb: Custom Wordlist',        'tool':'dirb',
         'cmd':'dirb {url} {wordlist}',
         'params':['url','wordlist'],
         'hints':{'url':'Target URL','wordlist':'Wordlist path'},
         'description':'Directory brute-force with custom wordlist'},

        # ── SQLMap ──
        {'name':'SQLMap: Test URL',             'tool':'sqlmap',
         'cmd':'sqlmap -u "{url}" --batch --level 3',
         'params':['url'],'hints':{'url':'URL with parameter e.g. http://site.com/?id=1'},
         'description':'Thorough SQL injection test'},

        {'name':'SQLMap: Crawl & Test',         'tool':'sqlmap',
         'cmd':'sqlmap -u "{url}" --batch --crawl=3',
         'params':['url'],'hints':{'url':'Base URL of web app'},
         'description':'Crawl site and test all found parameters'},

        # ── Wfuzz ──
        {'name':'Wfuzz: Directory Fuzzing',     'tool':'wfuzz',
         'cmd':'wfuzz -c -z file,{wordlist} --hc 404 {url}/FUZZ',
         'params':['url','wordlist'],
         'hints':{'url':'Base URL','wordlist':'Wordlist path'},
         'description':'Fuzz directories hiding 404 responses'},

        {'name':'Wfuzz: Parameter Fuzzing',     'tool':'wfuzz',
         'cmd':'wfuzz -c -z file,{wordlist} --hc 404 "{url}?FUZZ=test"',
         'params':['url','wordlist'],
         'hints':{'url':'Base URL','wordlist':'Parameter names wordlist'},
         'description':'Discover hidden GET parameters'},

        # ── Nikto ──
        {'name':'Nikto: Full Web Scan',         'tool':'nikto',
         'cmd':'nikto -h {url} -C all',
         'params':['url'],'hints':{'url':'Target URL'},
         'description':'Full Nikto scan with all CGI checks'},

        # ── Curl ──
        {'name':'Curl: GET Request + Headers',  'tool':'curl',
         'cmd':'curl -v -A "Mozilla/5.0" {url}',
         'params':['url'],'hints':{'url':'Target URL'},
         'description':'Verbose GET request showing all headers'},

        {'name':'Curl: POST Request',           'tool':'curl',
         'cmd':'curl -X POST -d "{data}" {url}',
         'params':['url','data'],
         'hints':{'url':'Target URL','data':'POST data e.g. user=admin&pass=1234'},
         'description':'Send a POST request with custom data'},

        {'name':'Curl: Check Security Headers', 'tool':'curl',
         'cmd':'curl -I -s {url} | grep -iE "strict|content-security|x-frame|x-xss|x-content"',
         'params':['url'],'hints':{'url':'Target URL'},
         'description':'Quickly check for security response headers'},

        {'name':'Custom Web Command',           'custom':True,'tool':'gobuster',
         'description':'Enter any web testing command manually'},
    ]
