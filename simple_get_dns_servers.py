import ctypes
from ctypes.wintypes import DWORD
import socket
import struct

ERROR_SUCCESS = 0


def get_dns_servers():
    DNS_CONFIG_DNS_SERVER_LIST = 6

    buffer = ctypes.create_string_buffer(2048)
    result = ctypes.windll.dnsapi.DnsQueryConfig(
        DNS_CONFIG_DNS_SERVER_LIST,
        0,
        None,
        None,
        ctypes.byref(buffer),
        ctypes.byref(DWORD(len(buffer)))
    )

    iplist = []

    if result == ERROR_SUCCESS:
        ipcount = struct.unpack('I', buffer[0:4])[0]
        iplist = [socket.inet_ntoa(buffer[i:i+4]) for i in range(4, ipcount*4+4, 4)]

    return iplist


def main():
    print(get_dns_servers())

if __name__ == "__main__":
    main()
