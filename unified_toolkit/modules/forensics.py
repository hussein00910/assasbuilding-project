"""modules/forensics.py — Digital Forensics (10 options)"""
from modules.base import BaseModule

class ForensicsModule(BaseModule):
    NAME        = 'Digital Forensics'
    ICON        = '🔬'
    COLOR       = 'purple'
    DESCRIPTION = 'Binwalk, Strings, Steghide, Exiftool, Volatility'
    TOOLS       = ['binwalk','strings','steghide','exiftool','volatility']
    OPTIONS = [
        # ── Binwalk ──
        {'name':'Binwalk: Analyze File',        'tool':'binwalk',
         'cmd':'binwalk {file}',
         'params':['file'],'hints':{'file':'Target file path'},
         'description':'Identify embedded files and data in binary'},

        {'name':'Binwalk: Extract All',         'tool':'binwalk',
         'cmd':'binwalk -e {file}',
         'params':['file'],'hints':{'file':'Target file path'},
         'description':'Extract all embedded files automatically'},

        {'name':'Binwalk: Entropy Analysis',    'tool':'binwalk',
         'cmd':'binwalk -E {file}',
         'params':['file'],'hints':{'file':'Target file path'},
         'description':'Show entropy graph (high = compressed/encrypted)'},

        # ── Strings ──
        {'name':'Strings: Extract All',         'tool':'strings',
         'cmd':'strings {file}',
         'params':['file'],'hints':{'file':'Target file path'},
         'description':'Extract all printable strings from binary'},

        {'name':'Strings: Search Pattern',      'tool':'strings',
         'cmd':'strings {file} | grep -i "{pattern}"',
         'params':['file','pattern'],
         'hints':{'file':'File path','pattern':'Search pattern e.g. password'},
         'description':'Extract and filter strings by keyword'},

        # ── Steghide ──
        {'name':'Steghide: Extract Hidden',     'tool':'steghide',
         'cmd':'steghide extract -sf {file}',
         'params':['file'],'hints':{'file':'Image/audio file path'},
         'description':'Extract hidden data from image/audio file'},

        {'name':'Steghide: Embed File',         'tool':'steghide',
         'cmd':'steghide embed -cf {cover} -ef {secret}',
         'params':['cover','secret'],
         'hints':{'cover':'Cover file (image/audio)','secret':'File to hide'},
         'description':'Hide a file inside an image/audio carrier'},

        # ── Exiftool ──
        {'name':'Exiftool: Read Metadata',      'tool':'exiftool',
         'cmd':'exiftool {file}',
         'params':['file'],'hints':{'file':'Target file path'},
         'description':'Read all metadata from any file type'},

        # ── Volatility ──
        {'name':'Volatility: Image Info',       'tool':'volatility',
         'cmd':'volatility -f {dump} imageinfo',
         'params':['dump'],'hints':{'dump':'Memory dump file path'},
         'description':'Identify OS and profile of a memory dump'},

        {'name':'Volatility: Process List',     'tool':'volatility',
         'cmd':'volatility -f {dump} --profile={profile} pslist',
         'params':['dump','profile'],
         'hints':{'dump':'Memory dump path','profile':'Profile e.g. Win7SP1x64'},
         'description':'List running processes from memory dump'},
    ]
