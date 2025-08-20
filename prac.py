import dns
import dns.resolver
import socket

result = socket.gethostbyaddr('13.203.125.58')

print(result)

result1 = dns.resolver.resolve('mail.google.com', 'A')

print(result1)