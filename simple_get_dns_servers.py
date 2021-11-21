# https://docs.microsoft.com/en-us/windows/win32/api/windns/nf-windns-dnsqueryconfig
import ctypes
import socket
import struct

INITIAL_BUFFER_LEN = 4096  # should be plenty big enough


# https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
ERROR_SUCCESS = 0
ERROR_MORE_DATA = 234

# https://docs.microsoft.com/en-us/windows/win32/api/windns/ne-windns-dns_config_type
DNS_CONFIG_DNS_SERVER_LIST = 6


def get_dns_servers():
    buffer_len = ctypes.c_ulong(INITIAL_BUFFER_LEN)
    buffer = ctypes.create_string_buffer(buffer_len.value)
    result = ctypes.windll.dnsapi.DnsQueryConfig(
        DNS_CONFIG_DNS_SERVER_LIST,
        0,
        None,
        None,
        ctypes.byref(buffer),
        ctypes.byref(buffer_len)
    )

    # NOTE while we are unlikely to be told that 4096 wasn't a big enough buffer,
    # if it were, this code will allocate the # of bytes the API tells us we need
    if result == ERROR_MORE_DATA:
        # buffer_len now contains how many bytes we actually need
        buffer = ctypes.create_string_buffer(buffer_len.value)
        result = ctypes.windll.dnsapi.DnsQueryConfig(
            DNS_CONFIG_DNS_SERVER_LIST,
            0,
            None,
            None,
            ctypes.byref(buffer),
            ctypes.byref(buffer_len)
        )

    iplist = []

    if result == ERROR_SUCCESS:
        # NOTE buffer is a `struct IP4_ARRAY``
        #  which is a Count (of IP addresses) followed by 4 * Count bytes
        # see https://docs.microsoft.com/en-us/windows/win32/api/windns/ns-windns-ip4_array
        ipcount = struct.unpack('I', buffer[0: 4])[0]
        iplist = [socket.inet_ntoa(buffer[i: i + 4]) for i in range(4, ipcount * 4 + 4, 4)]

    return iplist


def main():
    print(get_dns_servers())


if __name__ == "__main__":
    main()
