import socket


def get_ip() -> str:
    """Gets the IP Address of the computer.

    Returns:
        The IP Address of the computer.

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        ip = s.getsockname()[0]
    except (TimeoutError, InterruptedError):
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip
