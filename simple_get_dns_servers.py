# https://docs.microsoft.com/en-us/windows/win32/api/windns/nf-windns-dnsqueryconfig
import ctypes
from ctypes.wintypes import DWORD
import socket
import struct


# https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
ERROR_SUCCESS = 0

# https://docs.microsoft.com/en-us/windows/win32/api/windns/ne-windns-dns_config_type
DNS_CONFIG_DNS_SERVER_LIST = 6


def get_dns_servers():
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
