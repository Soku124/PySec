from scapy.all import *

ports = [25,80,53,443,445,8080,8443]

def SynScan(host):
    ans, unans = sr(IP(dst=host)/TCP(sport=5555,dport=ports,flags="S"),timeout=2,verbose=0)
    print(f"Open ports at : {host}")
    for (s,r,) in ans:
        if s[TCP].dport == r[TCP].sport:
            print(s[TCP].dport)


def DNSScan(host):
    ans, unans = sr(IP(dst=host)/UDP(sport=5555,dport=53)/DNS(rd=1,qd=DNSQR(qname="google.com")),timeout=2,verbose=0)
    if ans:
        print(f"DNS Server at {host}")

host = "192.168.0.1"

SynScan(host)
DNSScan(host)
