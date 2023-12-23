"""A test client for the network_tcp module."""

import socket


class NetworkTCPTestClient:
    """A test client for the network_tcp module."""

    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.conn: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))

    def send(self, data: bytes) -> None:
        """Send data to the server."""
        self.conn.send(data)

    def recv(self, size: int, timeout: int = 5) -> bytes:
        """Receive data from the server."""
        self.conn.settimeout(timeout)
        return self.conn.recv(size)

    def close(self) -> None:
        """Close the connection."""
        self.conn.close()
