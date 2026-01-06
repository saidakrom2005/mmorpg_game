import socket
import msgpack
from _thread import *
import sys

server = "192.168.100.112"
port = 5050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(f"Failed to bind to {server}:{port} -> {e}")
    # try to bind to all interfaces as a fallback
    try:
        s.bind(("0.0.0.0", port))
        server = "0.0.0.0"
        print(f"Falling back to 0.0.0.0:{port}")
    except socket.error as e2:
        print(f"Failed to bind fallback interface: {e2}")
        s.close()
        sys.exit(1)

try:
    s.listen(2)
except OSError as e:
    print(f"Listen failed: {e}")
    s.close()
    sys.exit(1)

print("Waiting for a connection, Server Started")

# store simple player state dicts instead of complex objects
players = [
    {'x': 1210, 'y': 1210},
    {'x': 1200, 'y': 1200}
]

def threaded_client(conn, player):
    # send initial state for this player
    try:
        conn.send(msgpack.packb(players[player], use_bin_type=True))
    except Exception:
        pass

    reply = None
    while True:
        try:
            raw = conn.recv(2048)
            if not raw:
                print('Disconnected (no data)')
                break

            data = msgpack.unpackb(raw, raw=False)
            players[player] = data

            if player == 1:
                reply = players[0]
            else:
                reply = players[1]

            print("Received:", data)
            print("Sending:", reply)

            conn.sendall(msgpack.packb(reply, use_bin_type=True))
        except Exception:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1