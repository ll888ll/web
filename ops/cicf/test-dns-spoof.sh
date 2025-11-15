#!/usr/bin/env bash
set -euo pipefail

CONF=${CONF:-ops/cicf/env}
# shellcheck disable=SC1090
. "$CONF"

OUT_DIR=${PCAP_DIR:-/var/log/cicf/pcap}
mkdir -p "$OUT_DIR"
PCAP="$OUT_DIR/dns-spoof-test.pcap"

if command -v python3 >/dev/null 2>&1; then
  python3 - "$PCAP" <<'PY'
from scapy.all import *
import sys
pcap = sys.argv[1]
client='192.0.2.10'
legit='8.8.8.8'
spoof='10.1.2.3'
qname='example.com.'
txid=0x1234

pkts=[]
q=IP(src=client,dst=legit)/UDP(sport=53000,dport=53)/DNS(rd=1,id=txid,qd=DNSQR(qname=qname,qtype='A'))
pkts.append(q)
# Spoofed response from unauthorized server
spr=IP(src=spoof,dst=client)/UDP(sport=53,dport=53000)/DNS(id=txid,qr=1,aa=1,qd=DNSQR(qname=qname),an=DNSRR(rrname=qname,type='A',ttl=10,rdata='1.2.3.4'))
pkts.append(spr)
# Legitimate response
leg=IP(src=legit,dst=client)/UDP(sport=53,dport=53000)/DNS(id=txid,qr=1,aa=1,qd=DNSQR(qname=qname),an=DNSRR(rrname=qname,type='A',ttl=300,rdata='93.184.216.34'))
pkts.append(leg)
wrpcap(pcap, pkts)
print(pcap)
PY
else
  echo "[test] Python3 no disponible; instala scapy para generar PCAP de prueba" >&2
  exit 1
fi

echo "[test] Analizando PCAP de prueba con dnsmon (una pasada)"
CONF=/etc/cicf/env /usr/local/bin/python3 /usr/local/bin/cicf-dnsmon.py "$PCAP" || true

echo "[test] Listo: $PCAP"

