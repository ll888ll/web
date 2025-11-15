#!/usr/bin/env python3
import os, sys, time, csv, ipaddress, subprocess

CONF = os.environ.get('CONF', '/etc/cicf/env')
env = {}
if os.path.exists(CONF):
    with open(CONF) as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k,v = line.split('=',1)
                env[k.strip()] = v.strip()

PCAP_DIR = env.get('PCAP_DIR','/var/log/cicf/pcap')
ALERT_DIR = env.get('ALERT_DIR','/var/log/cicf/alerts')
ALLOWED_DNS = [x.strip() for x in env.get('ALLOWED_DNS','').split(',') if x.strip()]
TIME_WIN = int(env.get('DNS_TIME_WINDOW_S','5'))
LOW_TTL = int(env.get('DNS_LOW_TTL','60'))

os.makedirs(ALERT_DIR, exist_ok=True)
alert_log = os.path.join(ALERT_DIR,'dnsmon.log')

def log_alert(kind, msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {kind}: {msg}\n"
    sys.stdout.write(line)
    sys.stdout.flush()
    with open(alert_log,'a') as f:
        f.write(line)

def have_tshark():
    try:
        subprocess.run(['tshark','-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

FIELDS = ['frame.time_epoch','ip.src','ip.dst','udp.srcport','udp.dstport','dns.flags.response','dns.id','dns.qry.name','dns.a','dns.resp.ttl']

def parse_pcap_with_tshark(pcap):
    cmd = ['tshark','-r', pcap, '-Y','dns','-T','fields']
    for f in FIELDS:
        cmd += ['-e', f]
    cmd += ['-E','separator=,','-E','header=y']
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        log_alert('ERROR', f'tshark fallo con {pcap}: rc={out.returncode}')
        return []
    lines = out.stdout.strip().splitlines()
    if not lines:
        return []
    rdr = csv.DictReader(lines)
    return list(rdr)

def is_private(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return False

def analyze(records):
    # Track queries by (client, server, qname, id) with time
    queries = {}
    answers_by_name = {}
    alerts = []
    for r in records:
        try:
            t = float(r.get('frame.time_epoch') or 0)
            src = r.get('ip.src') or ''
            dst = r.get('ip.dst') or ''
            sport = r.get('udp.srcport') or r.get('tcp.srcport') or ''
            dport = r.get('udp.dstport') or r.get('tcp.dstport') or ''
            flag = r.get('dns.flags.response') or ''
            is_resp = (flag in ('1','True','true','TRUE'))
            dnsid = r.get('dns.id') or ''
            qname = (r.get('dns.qry.name') or '').lower()
            ans = r.get('dns.a') or ''
            ttl = int(r.get('dns.resp.ttl') or 0)
        except Exception:
            continue
        if not qname:
            continue
        key = (src, dst, qname, dnsid)
        if not is_resp:
            queries[key] = t
            continue
        # is response
        # Checks
        if ALLOWED_DNS and src not in ALLOWED_DNS:
            alerts.append(('UNAUTH_SRC', f'resp from {src} for {qname} (id {dnsid})'))
        # match by reverse direction
        qkey = (dst, src, qname, dnsid)
        t_q = queries.get(qkey)
        if t_q is None or (t - t_q) > TIME_WIN:
            alerts.append(('TXID_MISS', f'resp {src}->{dst} id {dnsid} for {qname} without timely query'))
        if ans:
            # multiple answers inconsistency
            prev = answers_by_name.get(qname)
            if prev and ans not in prev['ips']:
                alerts.append(('MULTI_ANS', f'{qname} answers changed {prev["ips"]} -> {ans} src {src}'))
                prev['ips'].add(ans)
            else:
                answers_by_name[qname] = {'t': t, 'ips': set([ans])}
            if is_private(ans):
                alerts.append(('PRIVATE_IP', f'{qname} -> {ans} (private) src {src}'))
            if ttl and ttl < LOW_TTL:
                alerts.append(('LOW_TTL', f'{qname} ttl {ttl} from {src}'))
    return alerts

def main():
    # Modo de una sola pasada si se indica
    pcap_once = None
    if len(sys.argv) > 1:
        pcap_once = sys.argv[1]
    if not pcap_once:
        pcap_once = os.environ.get('PCAP_ONCE')
    if pcap_once:
        if not have_tshark():
            log_alert('ERROR','tshark no disponible; no puedo analizar')
            return 1
        recs = parse_pcap_with_tshark(pcap_once)
        alerts = analyze(recs)
        for k,msg in alerts:
            log_alert(k, f'{os.path.basename(pcap_once)}: {msg}')
        return 0

    seen = set()
    if not have_tshark():
        log_alert('WARN','tshark no disponible; dnsmon inactivo')
        while True:
            time.sleep(60)
    while True:
        for name in sorted(os.listdir(PCAP_DIR)):
            if not name.endswith('.pcap'):
                continue
            p = os.path.join(PCAP_DIR, name)
            if p in seen:
                continue
            seen.add(p)
            recs = parse_pcap_with_tshark(p)
            alerts = analyze(recs)
            for k,msg in alerts:
                log_alert(k, f'{os.path.basename(p)}: {msg}')
        time.sleep(5)

if __name__ == '__main__':
    main()
