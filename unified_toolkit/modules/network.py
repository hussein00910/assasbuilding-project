"""modules/network.py — Network Tools (12 options)"""
from modules.base import BaseModule

class NetworkModule(BaseModule):
    NAME        = 'Network Tools'
    ICON        = '🔌'
    COLOR       = 'white'
    DESCRIPTION = 'Netcat, Tcpdump, Tshark, Ettercap, Arpspoof, Hping3'
    TOOLS       = ['nc','tcpdump','tshark','ettercap','arpspoof','hping3']
    OPTIONS = [
        # ── Netcat ──
        {'name':'Netcat: Listen (Bind Shell)',   'tool':'nc',
         'cmd':'nc -lvnp {port}',
         'params':['port'],'hints':{'port':'Port to listen on e.g. 4444'},
         'description':'Start a TCP listener (catch reverse shells)'},

        {'name':'Netcat: Connect to Host',      'tool':'nc',
         'cmd':'nc {host} {port}',
         'params':['host','port'],
         'hints':{'host':'Target IP','port':'Port number'},
         'description':'Connect to a remote host/port'},

        {'name':'Netcat: Port Scan',            'tool':'nc',
         'cmd':'nc -zv {host} {start}-{end}',
         'params':['host','start','end'],
         'hints':{'host':'Target IP','start':'Start port','end':'End port'},
         'description':'Quick TCP port scan with netcat'},

        {'name':'Netcat: File Transfer (send)','tool':'nc',
         'cmd':'nc -w 3 {host} {port} < {file}',
         'params':['host','port','file'],
         'hints':{'host':'Receiver IP','port':'Port','file':'File path to send'},
         'description':'Send a file to a netcat listener'},

        # ── Tcpdump ──
        {'name':'Tcpdump: Capture All Traffic', 'tool':'tcpdump',
         'cmd':'tcpdump -i {iface} -v',
         'params':['iface'],'hints':{'iface':'Interface e.g. eth0'},
         'requires_root':True,
         'description':'Live capture all traffic on an interface'},

        {'name':'Tcpdump: Capture Host Traffic','tool':'tcpdump',
         'cmd':'tcpdump -i {iface} host {host} -v',
         'params':['iface','host'],
         'hints':{'iface':'Interface','host':'Target IP'},
         'requires_root':True,
         'description':'Capture traffic to/from a specific host'},

        {'name':'Tcpdump: Save to PCAP',        'tool':'tcpdump',
         'cmd':'tcpdump -i {iface} -w {file}.pcap -c {count}',
         'params':['iface','file','count'],
         'hints':{'iface':'Interface','file':'Output filename','count':'Packet count'},
         'requires_root':True,
         'description':'Save captured packets to a .pcap file'},

        # ── Tshark ──
        {'name':'Tshark: Capture Live',         'tool':'tshark',
         'cmd':'tshark -i {iface}',
         'params':['iface'],'hints':{'iface':'Interface e.g. eth0'},
         'requires_root':True,
         'description':'Wireshark CLI live capture'},

        {'name':'Tshark: Analyze PCAP',         'tool':'tshark',
         'cmd':'tshark -r {file} -V | head -200',
         'params':['file'],'hints':{'file':'Path to .pcap file'},
         'description':'Read and analyze a PCAP capture file'},

        # ── MITM ──
        {'name':'Ettercap: ARP Poison MITM',    'tool':'ettercap',
         'cmd':'ettercap -T -q -i {iface} -M arp:remote /{target1}// /{target2}//',
         'params':['iface','target1','target2'],
         'hints':{'iface':'Interface','target1':'Victim IP','target2':'Gateway IP'},
         'requires_root':True,
         'description':'Man-in-the-middle via ARP poisoning'},

        {'name':'Arpspoof: Poison Gateway',     'tool':'arpspoof',
         'cmd':'arpspoof -i {iface} -t {victim} {gateway}',
         'params':['iface','victim','gateway'],
         'hints':{'iface':'Interface','victim':'Victim IP','gateway':'Gateway IP'},
         'requires_root':True,
         'description':'Redirect victim traffic through attacker'},

        {'name':'Custom Network Command',       'custom':True,'tool':'nc',
         'description':'Enter any network command manually'},
    ]
