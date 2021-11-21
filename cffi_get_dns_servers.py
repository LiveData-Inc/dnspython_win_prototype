# https://docs.microsoft.com/en-us/windows/win32/iphlp/retrieving-information-using-getnetworkparams

import cffi

ffi = cffi.FFI()

ffi.set_unicode(True)

Iphlpapi = ffi.dlopen("Iphlpapi.dll")

ERROR_BUFFER_OVERFLOW = 111

ffi.cdef("""
#define MAX_HOSTNAME_LEN 128
#define MAX_DOMAIN_NAME_LEN 128
#define MAX_SCOPE_ID_LEN 256

typedef struct {
  char String[16];
} IP_ADDRESS_STRING, *PIP_ADDRESS_STRING, IP_MASK_STRING, *PIP_MASK_STRING;

typedef struct _IP_ADDR_STRING {
  // NOTE: cffi didn't like `struct _IP_ADDR_STRING *Next;`
  void                   *Next;
  IP_ADDRESS_STRING      IpAddress;
  IP_MASK_STRING         IpMask;
  DWORD                  Context;
} IP_ADDR_STRING, *PIP_ADDR_STRING;

typedef struct {
  char            HostName[MAX_HOSTNAME_LEN + 4];
  char            DomainName[MAX_DOMAIN_NAME_LEN + 4];
  PIP_ADDR_STRING CurrentDnsServer;
  IP_ADDR_STRING  DnsServerList;
  UINT            NodeType;
  char            ScopeId[MAX_SCOPE_ID_LEN + 4];
  UINT            EnableRouting;
  UINT            EnableProxy;
  UINT            EnableDns;
} FIXED_INFO, *PFIXED_INFO;

DWORD GetNetworkParams(
  PFIXED_INFO pFixedInfo,
  PULONG      pOutBufLen
);

""")


def get_dns_servers():
    pFixedInfo = ffi.new("PFIXED_INFO")
    pOutBufLen = ffi.new("unsigned long *")
    pOutBufLen[0] = ffi.sizeof("FIXED_INFO")

    result = Iphlpapi.GetNetworkParams(pFixedInfo, pOutBufLen)

    # NOTE: this error is ok; it means we need to supply a bigger buffer,
    # and this error indicates that we must check updated value at pOutBufLen
    # for the required size buffer we need to supply
    if result == ERROR_BUFFER_OVERFLOW:
        bigger_FixedInfo = ffi.new("BYTE[]", pOutBufLen[0])
        pFixedInfo = ffi.cast("PFIXED_INFO", bigger_FixedInfo)
        result = Iphlpapi.GetNetworkParams(pFixedInfo, pOutBufLen)

    host_name = None
    domain_name = None
    dns_servers = []
    if result == 0:
        dns_servers.append(ffi.string(pFixedInfo.DnsServerList.IpAddress.String, 16).decode())

        # NOTE this cast is due to cffi issue noted above
        pIPAddr = ffi.cast("PIP_ADDR_STRING", pFixedInfo.DnsServerList.Next)
        while pIPAddr:
            dns_servers.append(ffi.string(pIPAddr.IpAddress.String, 16).decode())
            pIPAddr = pIPAddr.Next

        host_name = ffi.string(pFixedInfo.HostName).decode()
        domain_name = ffi.string(pFixedInfo.DomainName).decode()

    return host_name, domain_name, dns_servers


def main():
    print(get_dns_servers())


if __name__ == "__main__":
    main()
