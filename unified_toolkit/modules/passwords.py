"""modules/passwords.py — Password Attacks (15 options)"""
from modules.base import BaseModule

class PasswordsModule(BaseModule):
    NAME        = 'Password Attacks'
    ICON        = '🔑'
    COLOR       = 'magenta'
    DESCRIPTION = 'Hydra, John the Ripper, Hashcat, Medusa, Crunch'
    TOOLS       = ['hydra','john','hashcat','medusa','crunch']
    OPTIONS = [
        # ── Hydra ──
        {'name':'Hydra: SSH Brute Force',       'tool':'hydra',
         'cmd':'hydra -l {user} -P {wordlist} ssh://{target}',
         'params':['target','user','wordlist'],
         'hints':{'target':'Target IP','user':'Username or file (-L file.txt)','wordlist':'Path to password list'},
         'description':'Brute-force SSH login'},

        {'name':'Hydra: FTP Brute Force',       'tool':'hydra',
         'cmd':'hydra -l {user} -P {wordlist} ftp://{target}',
         'params':['target','user','wordlist'],
         'hints':{'target':'Target IP','user':'Username','wordlist':'Password list'},
         'description':'Brute-force FTP login'},

        {'name':'Hydra: HTTP POST Form',        'tool':'hydra',
         'cmd':'hydra -l {user} -P {wordlist} {target} http-post-form "{path}:{user_field}=^USER^&{pass_field}=^PASS^:{fail_str}"',
         'params':['target','user','wordlist','path','user_field','pass_field','fail_str'],
         'hints':{'target':'Target IP/domain','user':'Username','wordlist':'Password list',
                  'path':'/login.php','user_field':'username','pass_field':'password',
                  'fail_str':'Invalid credentials'},
         'description':'Brute-force HTTP login form'},

        {'name':'Hydra: RDP Brute Force',       'tool':'hydra',
         'cmd':'hydra -l {user} -P {wordlist} rdp://{target}',
         'params':['target','user','wordlist'],
         'hints':{'target':'Target IP','user':'Username','wordlist':'Password list'},
         'description':'Brute-force Remote Desktop (RDP)'},

        {'name':'Hydra: SMB Brute Force',       'tool':'hydra',
         'cmd':'hydra -l {user} -P {wordlist} smb://{target}',
         'params':['target','user','wordlist'],
         'hints':{'target':'Target IP','user':'Username','wordlist':'Password list'},
         'description':'Brute-force SMB/Windows login'},

        {'name':'Hydra: MySQL Brute Force',     'tool':'hydra',
         'cmd':'hydra -l {user} -P {wordlist} mysql://{target}',
         'params':['target','user','wordlist'],
         'hints':{'target':'Target IP','user':'root','wordlist':'Password list'},
         'description':'Brute-force MySQL database'},

        # ── John the Ripper ──
        {'name':'John: Crack Hash File',        'tool':'john',
         'cmd':'john {hashfile}',
         'params':['hashfile'],'hints':{'hashfile':'Path to hash file'},
         'description':'Crack hashes using john default rules'},

        {'name':'John: Wordlist Attack',        'tool':'john',
         'cmd':'john --wordlist={wordlist} {hashfile}',
         'params':['hashfile','wordlist'],
         'hints':{'hashfile':'Hash file path','wordlist':'Wordlist path'},
         'description':'Dictionary attack with custom wordlist'},

        {'name':'John: Show Cracked',           'tool':'john',
         'cmd':'john --show {hashfile}',
         'params':['hashfile'],'hints':{'hashfile':'Hash file path'},
         'description':'Display already-cracked passwords'},

        # ── Hashcat ──
        {'name':'Hashcat: Crack MD5',           'tool':'hashcat',
         'cmd':'hashcat -m 0 -a 0 {hashfile} {wordlist}',
         'params':['hashfile','wordlist'],
         'hints':{'hashfile':'Hash file','wordlist':'Wordlist path'},
         'description':'Dictionary attack on MD5 hashes'},

        {'name':'Hashcat: Crack SHA-256',       'tool':'hashcat',
         'cmd':'hashcat -m 1400 -a 0 {hashfile} {wordlist}',
         'params':['hashfile','wordlist'],
         'hints':{'hashfile':'Hash file','wordlist':'Wordlist path'},
         'description':'Dictionary attack on SHA-256 hashes'},

        {'name':'Hashcat: Crack NTLM',          'tool':'hashcat',
         'cmd':'hashcat -m 1000 -a 0 {hashfile} {wordlist}',
         'params':['hashfile','wordlist'],
         'hints':{'hashfile':'Hash file','wordlist':'Wordlist path'},
         'description':'Dictionary attack on NTLM (Windows) hashes'},

        # ── Medusa ──
        {'name':'Medusa: SSH Brute Force',      'tool':'medusa',
         'cmd':'medusa -h {target} -u {user} -P {wordlist} -M ssh',
         'params':['target','user','wordlist'],
         'hints':{'target':'Target IP','user':'Username','wordlist':'Password list'},
         'description':'Medusa parallel SSH brute-force'},

        # ── Crunch ──
        {'name':'Crunch: Generate Wordlist',    'tool':'crunch',
         'cmd':'crunch {min} {max} {charset} -o {output}',
         'params':['min','max','charset','output'],
         'hints':{'min':'Min length e.g. 6','max':'Max length e.g. 8',
                  'charset':'Characters e.g. abcdefghijklmnopqrstuvwxyz0123456789',
                  'output':'Output file e.g. wordlist.txt'},
         'description':'Generate custom wordlist'},

        {'name':'Custom Password Command',      'custom':True,'tool':'hydra',
         'description':'Enter any password attack command manually'},
    ]
