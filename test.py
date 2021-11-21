import dns.resolver

dns_resolver = dns.resolver.Resolver()

print(f"{dns_resolver.domain=}")
print(f"{dns_resolver.nameservers=}")
print(f"{dns_resolver.search=}")
