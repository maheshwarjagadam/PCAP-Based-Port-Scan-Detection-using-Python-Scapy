# PCAP-Based-Port-Scan-Detection-using-Python-Scapy
Python-based PCAP analysis tool for detecting TCP SYN port scanning using Wireshark captures, Nmap-generated traffic, and Scapy-based detection logic.



## Overview
This project demonstrates detection of network reconnaissance activity (port scanning) by analyzing packet capture (PCAP) files.

Network traffic was generated using Nmap and captured using Wireshark. A Python-based detection engine was developed using Scapy to identify malicious behavior by analyzing TCP SYN packet patterns.

The project focuses on detecting large-scale port scanning activity and reducing false positives through packet-level filtering.

---

## Lab Setup

Attacker: Kali Linux (192.168.20.11)  
Target: Windows Machine (192.168.20.10)  
Network: Internal LABNET (private network)  
Capture Tool: Wireshark  
Analysis Tool: Python (Scapy)

---

## Attack Simulation

A full TCP SYN scan was performed against the target system:

nmap -sS -p- 192.168.20.10

This scan attempts connections across all 65,535 ports to identify open services and simulate reconnaissance behavior.

---

## Traffic Analysis

Captured traffic showed the following patterns:

- High volume of TCP SYN packets from a single source
- Sequential probing of multiple destination ports
- No completion of full TCP handshake for most ports

Wireshark filter used:

tcp.flags.syn == 1 and tcp.flags.ack == 0

This filter isolates SYN packets without ACK responses, which are typical indicators of port scanning activity.

---

## Detection Logic

A Python-based detection engine was built using Scapy to analyze the PCAP file.

Detection approach:

- Read PCAP file using Scapy
- Extract TCP packets with SYN flag
- Exclude SYN-ACK packets to avoid false positives
- Track unique destination ports per source IP
- Measure scan duration
- Trigger alert when a threshold of scanned ports is exceeded

Key logic:

- Only count pure SYN packets (flag = 0x02)
- If a source IP scans more than 50 ports, flag as suspicious

---

## Detection Output

The detection engine successfully identified the attacker:

[ALERT] Port Scan Detected from 192.168.20.11  
Target IP(s): 192.168.20.10  
Ports scanned: 65535  
Scan duration: 397.18 seconds  

---

## Screenshots

### 1. Nmap Attack Execution
![Nmap Scan](pcap-port-scan-detection/screenshots/1-nmap-full-syn-scan.png)

### 2. Wireshark Packet Capture
![Wireshark Capture](pcap-port-scan-detection/screenshots/2-wireshark-capture-running.png)

### 3. SYN Packet Pattern
![SYN Packets](pcap-port-scan-detection/screenshots/3-syn-packets-filter.png)

### 4. Attacker Traffic Isolation
![Filtered Traffic](pcap-port-scan-detection/screenshots/4-attacker-ip-filter.png)

### 5. Detection Engine Output
![Detection Output](pcap-port-scan-detection/screenshots/5-detection-output.png)

---

## Challenges Faced

1. Environment Setup Issues  
Initial attempts to install Scapy using pip failed due to Kali's externally managed Python environment. This was resolved by installing Scapy using the system package manager with appropriate permissions.

2. File Transfer Between Systems  
The PCAP file was captured on Windows and needed to be transferred to Kali for analysis. Drag-and-drop failed due to missing guest additions, requiring the use of shared folders.

3. Incorrect Packet Filtering  
Initial detection logic counted both SYN and SYN-ACK packets, leading to false positives where the target system was incorrectly flagged as an attacker.

4. Detection Logic Tuning  
The original logic did not consider TCP flag differences properly. This was fixed by filtering only pure SYN packets using exact flag matching.

5. Time-Based Detection Constraints  
Initial conditions using strict time thresholds caused detection to fail. The logic was adjusted to focus on port count while retaining duration as an informational metric.

---

## MITRE ATT&CK Mapping

Technique: T1046  
Name: Network Service Discovery  

The observed behavior aligns with reconnaissance activity where an attacker scans multiple ports to identify available services.

---

## Technologies Used

- Wireshark
- Nmap
- Python
- Scapy

---

## Key Takeaways

- Learned how to analyze raw PCAP data programmatically
- Built behavior-based detection instead of relying on tools alone
- Improved detection accuracy by eliminating false positives
- Understood TCP handshake behavior and its role in network attacks
- Mapped real network activity to MITRE ATT&CK techniques
