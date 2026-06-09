"""
Network utility tools — pure Python.
Traceroute (TTL probes), IP geolocation, network info.
"""

import socket
import time

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False


def traceroute(host: str, max_hops: int = 20, timeout: float = 2.0,
               progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    emit(f"[*] Traceroute to {host} (max {max_hops} hops)")
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror as e:
        emit(f"[!] Cannot resolve {host}: {e}")
        return "\n".join(lines)

    emit(f"[*] Destination IP: {dest_addr}")
    emit("")
    port = 33434

    for ttl in range(1, int(max_hops) + 1):
        recv_sock = send_sock = None
        try:
            recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            recv_sock.settimeout(timeout)
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            start = time.time()
            send_sock.sendto(b"", (dest_addr, port))
            try:
                data, addr = recv_sock.recvfrom(512)
                rtt = (time.time() - start) * 1000
                hop_ip = addr[0]
                try:
                    hop_host = socket.gethostbyaddr(hop_ip)[0]
                except Exception:
                    hop_host = hop_ip
                line = f"  {ttl:2d}  {hop_ip:16s}  {hop_host[:30]:30s}  {rtt:.1f} ms"
                emit(line)
                if hop_ip == dest_addr:
                    emit(f"\n[+] Reached destination in {ttl} hops.")
                    break
            except socket.timeout:
                emit(f"  {ttl:2d}  *  (timeout)")
        except PermissionError:
            emit("[!] Raw socket requires root/admin privileges.")
            break
        except Exception as e:
            emit(f"  {ttl:2d}  [error: {e}]")
        finally:
            if recv_sock: recv_sock.close()
            if send_sock: send_sock.close()

    return "\n".join(lines)


def ip_geolocate(ip: str, progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    ip = ip.strip()
    try:
        resolved = socket.gethostbyname(ip)
        if resolved != ip:
            emit(f"[*] Resolved {ip} -> {resolved}")
            ip = resolved
    except Exception:
        pass

    emit(f"[*] IP Geolocation for: {ip}")
    if not REQUESTS_OK:
        emit("[!] requests not available.")
        return "\n".join(lines)

    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        data = r.json()
        fields = [
            ('IP',        data.get('ip')),
            ('Country',   data.get('country_name')),
            ('City',      data.get('city')),
            ('Region',    data.get('region')),
            ('Latitude',  data.get('latitude')),
            ('Longitude', data.get('longitude')),
            ('ISP / Org', data.get('org')),
            ('ASN',       data.get('asn')),
            ('Timezone',  data.get('timezone')),
        ]
        for label, value in fields:
            if value:
                emit(f"  {label:12s}: {value}")
    except Exception as e:
        emit(f"[!] Geolocation error: {e}")
        try:
            r2 = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            d = r2.json()
            if d.get('status') == 'success':
                emit(f"  Country : {d.get('country')}")
                emit(f"  City    : {d.get('city')}")
                emit(f"  ISP     : {d.get('isp')}")
        except Exception as e2:
            emit(f"[!] Fallback failed: {e2}")

    return "\n".join(lines)


def network_info(progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    emit("[*] Local Network Information")
    emit("")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        emit(f"  Hostname : {hostname}")
        emit(f"  Local IP : {local_ip}")
    except Exception as e:
        emit(f"  [!] {e}")

    if REQUESTS_OK:
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=8)
            public_ip = r.json().get('ip', 'N/A')
            emit(f"  Public IP: {public_ip}")
        except Exception:
            emit(f"  Public IP: (could not fetch)")

    return "\n".join(lines)


def tcp_connect(host: str, port: int = 80, message: str = "",
                progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    emit(f"[*] TCP connect to {host}:{port}")
    try:
        ip = socket.gethostbyname(host)
        emit(f"[*] Resolved: {ip}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        start = time.time()
        s.connect((ip, int(port)))
        rtt = (time.time() - start) * 1000
        emit(f"[+] Connected! RTT: {rtt:.1f} ms")
        if message:
            s.sendall((message + '\n').encode())
            emit(f"[*] Sent: {message}")
            response = s.recv(4096).decode('utf-8', errors='ignore')
            emit(f"[*] Response:\n{response}")
        s.close()
    except ConnectionRefusedError:
        emit(f"[!] Connection refused on port {port}")
    except socket.timeout:
        emit("[!] Connection timed out")
    except Exception as e:
        emit(f"[!] Error: {e}")

    return "\n".join(lines)
