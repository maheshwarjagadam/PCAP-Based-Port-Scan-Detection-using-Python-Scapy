from scapy.all import rdpcap, TCP, IP
from collections import defaultdict

packets = rdpcap("port-scan.pcap")
scan_data = defaultdict(list)
for pkt in packets:
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        tcp_flags = int(pkt[TCP].flags)
        # Only count pure SYN packets, not SYN-ACK
        if tcp_flags == 0x02:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            dst_port = pkt[TCP].dport
            pkt_time = float(pkt.time)
            scan_data[src_ip].append((pkt_time, dst_ip, dst_port))

print("DEBUG START")
for src_ip, entries in scan_data.items():
    print(f"{src_ip} -> {len(entries)} pure SYN packets captured")

print("\n--- Detection Results ---")
for src_ip, entries in scan_data.items():
    ports = set()
    times = []
    destinations = set()
    for pkt_time, dst_ip, dst_port in entries:
        ports.add(dst_port)
        times.append(pkt_time)
        destinations.add(dst_ip)
    duration = max(times) - min(times) if times else 0
    if len(ports) > 50:
        print(f"[ALERT] Port Scan Detected from {src_ip}")
        print(f"Target IP(s): {', '.join(destinations)}")
        print(f"Ports scanned: {len(ports)}")
        print(f"Scan duration: {duration:.2f} seconds")
        print("-" * 40)
