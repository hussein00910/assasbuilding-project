"""modules/phishing.py — Social Engineering & Phishing (6 options)"""
from modules.base import BaseModule

class PhishingModule(BaseModule):
    NAME        = 'Phishing / Social Engineering'
    ICON        = '🎣'
    COLOR       = 'orange3'
    DESCRIPTION = 'Zphisher, SET, phishing page hosting'
    TOOLS       = ['zphisher','setoolkit']
    OPTIONS = [
        {'name':'Launch Zphisher',              'tool':'zphisher',
         'cmd':'zphisher',
         'params':[],'interactive':True,
         'description':'Start zphisher — phishing page generator with tunneling'},

        {'name':'Launch SET (Setoolkit)',        'tool':'setoolkit',
         'cmd':'setoolkit',
         'params':[],'interactive':True,
         'requires_root':True,
         'description':'Social Engineering Toolkit — full attack suite'},

        {'name':'Clone Website (curl)',          'tool':'curl',
         'cmd':'curl -s {url} -o index.html && echo "Saved to index.html"',
         'params':['url'],'hints':{'url':'URL to clone'},
         'description':'Download a web page to use as phishing template'},

        {'name':'Start Python HTTP Server',     'tool':'python3',
         'cmd':'python3 -m http.server {port}',
         'params':['port'],'hints':{'port':'Port number e.g. 8080'},
         'description':'Serve current directory over HTTP (host phishing pages)'},

        {'name':'Generate Evil QR Code (qrencode)','tool':'qrencode',
         'cmd':'qrencode -o qr.png "{url}" && echo "QR saved to qr.png"',
         'params':['url'],'hints':{'url':'Malicious URL'},
         'description':'Create a QR code pointing to your phishing URL'},

        {'name':'Custom Phishing Command',      'custom':True,'tool':'setoolkit',
         'description':'Enter any social engineering command manually'},
    ]
