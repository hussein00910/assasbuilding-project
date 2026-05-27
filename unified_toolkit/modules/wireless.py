"""modules/wireless.py — Wireless Attacks (10 options)"""
from modules.base import BaseModule

class WirelessModule(BaseModule):
    NAME        = 'Wireless Attacks'
    ICON        = '📡'
    COLOR       = 'green'
    DESCRIPTION = 'Aircrack-ng suite, Wifite, Reaver WPS'
    TOOLS       = ['airmon-ng','airodump-ng','aireplay-ng','aircrack-ng','wifite','reaver']
    OPTIONS = [
        {'name':'List Wireless Interfaces',     'tool':'airmon-ng',
         'cmd':'airmon-ng',
         'params':[],'requires_root':True,
         'description':'Show available wireless network interfaces'},

        {'name':'Start Monitor Mode',           'tool':'airmon-ng',
         'cmd':'airmon-ng start {iface}',
         'params':['iface'],'hints':{'iface':'Interface e.g. wlan0'},
         'requires_root':True,
         'description':'Put wireless card into monitor mode'},

        {'name':'Stop Monitor Mode',            'tool':'airmon-ng',
         'cmd':'airmon-ng stop {iface}',
         'params':['iface'],'hints':{'iface':'Monitor interface e.g. wlan0mon'},
         'requires_root':True,
         'description':'Stop monitor mode and restore interface'},

        {'name':'Scan Nearby Networks',         'tool':'airodump-ng',
         'cmd':'airodump-ng {iface}',
         'params':['iface'],'hints':{'iface':'Monitor interface e.g. wlan0mon'},
         'requires_root':True,
         'description':'Capture and display all nearby WiFi networks'},

        {'name':'Capture WPA Handshake',        'tool':'airodump-ng',
         'cmd':'airodump-ng --bssid {bssid} -c {channel} -w handshake {iface}',
         'params':['bssid','channel','iface'],
         'hints':{'bssid':'Target AP MAC','channel':'AP channel','iface':'Monitor interface'},
         'requires_root':True,
         'description':'Capture WPA/WPA2 4-way handshake'},

        {'name':'Deauth Attack',                'tool':'aireplay-ng',
         'cmd':'aireplay-ng --deauth {count} -a {bssid} {iface}',
         'params':['count','bssid','iface'],
         'hints':{'count':'Packets e.g. 10','bssid':'Target AP MAC','iface':'Monitor interface'},
         'requires_root':True,
         'description':'Send deauthentication frames to disconnect clients'},

        {'name':'Crack WPA Handshake',          'tool':'aircrack-ng',
         'cmd':'aircrack-ng -w {wordlist} {capfile}',
         'params':['capfile','wordlist'],
         'hints':{'capfile':'Capture file .cap','wordlist':'Wordlist path'},
         'description':'Dictionary attack on captured WPA handshake'},

        {'name':'Crack WEP Key',                'tool':'aircrack-ng',
         'cmd':'aircrack-ng {capfile}',
         'params':['capfile'],'hints':{'capfile':'Capture file .cap/.ivs'},
         'description':'Statistical WEP key recovery'},

        {'name':'Wifite: Auto Attack All',      'tool':'wifite',
         'cmd':'wifite',
         'params':[],'interactive':True,'requires_root':True,
         'description':'Automated attack on all detected networks'},

        {'name':'Reaver: WPS Brute Force',      'tool':'reaver',
         'cmd':'reaver -i {iface} -b {bssid} -vv',
         'params':['iface','bssid'],
         'hints':{'iface':'Monitor interface','bssid':'Target AP MAC'},
         'requires_root':True,
         'description':'Brute-force WPS PIN to recover WPA passphrase'},
    ]
