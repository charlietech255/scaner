JAGUAR 45 Tool🚀

A powerful reconnaissance and vulnerability scanning tool developed by Charlie Syllas & Jaguar 45

---

📋 Overview

BlueGhost is an advanced network reconnaissance and vulnerability assessment framework designed for security professionals and penetration testers. Developed collaboratively by Charlie Syllas and Jaguar 45, this tool combines stealthy scanning techniques with comprehensive vulnerability detection to provide deep insights into target infrastructure.

⚠️ Legal Disclaimer: This tool is intended for authorized security testing and educational purposes only. Unauthorized scanning of networks or systems may violate laws and regulations. Always ensure you have explicit permission before testing.

---

✨ Key Features

Feature Description
🕵️ Stealth Scanning Evades basic IDS/IPS systems with configurable timing and randomization
🔍 Multi-Vector Recon Combines port scanning, service enumeration, and OS fingerprinting
🛡️ Vulnerability Detection Identifies CVE exposures and misconfigurations
📊 Smart Reporting Generates professional HTML, PDF, and JSON reports
⚡ Parallel Processing Multi-threaded architecture for high-speed scanning
🔄 API Integration Connects with Shodan, CVE databases, and exploit repositories

---

🛠️ Installation

Prerequisites

· Python 3.8+
· pip package manager
· Nmap (optional, for enhanced scanning)

Quick Install

```bash
# Clone the repository
git clone https://github.com/charliesyllas/blueghost.git
cd blueghost

# Install dependencies
pip install -r requirements.txt

# Install system-wide (optional)
sudo python setup.py install
```

Docker Installation

```bash
docker pull blueghost:latest
docker run -it blueghost --help
```

---

🚀 Usage

Basic Commands

```bash
# Quick scan
python blueghost.py -t 192.168.1.0/24

# Stealth mode scan
python blueghost.py -t example.com --stealth -p 1-1000

# Full vulnerability assessment
python blueghost.py -t target.com --full-scan --output report.html

# API intelligence gathering
python blueghost.py -t 8.8.8.8 --shodan-api YOUR_API_KEY
```

Advanced Options

```bash
python blueghost.py -t 10.0.0.1 \
  --ports 1-65535 \
  --threads 50 \
  --timeout 2 \
  --os-detect \
  --service-version \
  --vuln-scan \
  --output json \
  --verbose
```

Command Reference

Flag Description Default
-t, --target Target IP, range, or domain Required
-p, --ports Port range to scan 1-1000
--stealth Enable stealth scanning False
--threads Number of threads 25
--timeout Connection timeout (seconds) 3
--output Report format (html/pdf/json) html
--shodan-api Shodan API key None
--vuln-scan Enable vulnerability checks False
--full-scan Comprehensive scan mode False
-v, --verbose Verbose output False

---

📊 Output Examples

Console Output

```
[BLUEGHOST] Starting reconnaissance on target: 192.168.1.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[+] Host is up (0.042s latency)
[+] OS Detection: Linux 4.15 (92% confidence)
[+] Open Ports: 22, 80, 443, 3306, 8080

[!] Vulnerabilities Found:
    • CVE-2021-44228 - Apache Log4j2 (Critical)
    • CVE-2020-0601 - Windows CryptoAPI (High)
    • Misconfiguration: Default credentials detected

[✓] Scan completed in 2m 43s
[✓] Report saved to: scan_report_20240115.html
```

HTML Report Preview

· Executive summary with risk scores
· Interactive network topology maps
· Detailed vulnerability descriptions
· Remediation recommendations
· Export capabilities

---

🔧 Configuration

Create blueghost.conf for persistent settings:

```yaml
# BlueGhost Configuration File

scanning:
  threads: 50
  timeout: 3
  stealth_delay: 0.5
  randomize_ports: true

reporting:
  format: html
  include_remediation: true
  company_name: "Your Organization"

api:
  shodan_enabled: false
  cve_database: "https://cve.circl.lu"
  exploit_db: "/usr/share/exploitdb"

advanced:
  max_retries: 3
  packet_size: 1024
  custom_user_agent: "Mozilla/5.0 (BlueGhost/2.1)"
```

---

📁 Project Structure

```
blueghost/
├── blueghost.py              # Main entry point
├── core/
│   ├── scanner.py           # Port scanning engine
│   ├── detector.py          # OS & service detection
│   └── vuln_checker.py     # Vulnerability assessment
├── modules/
│   ├── shodan_lookup.py    # Shodan integration
│   ├── web_scanner.py      # Web app testing
│   └── exploit_matcher.py  # ExploitDB correlation
├── reports/
│   ├── html_generator.py   # HTML report builder
│   └── pdf_exporter.py     # PDF generation
├── utils/
│   ├── network.py          # Network utilities
│   └── validators.py       # Input validation
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

---

👨‍💻 Development

Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

Contributing Guidelines

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to branch (git push origin feature/amazing-feature)
5. Open a Pull Request

---

⚡ Performance

Scan Type Targets Ports Threads Duration
Quick 1 host 1000 25 ~30s
Stealth 1 host 1000 10 ~2m
Full 1 host 65535 50 ~8m
Network /24 1000 100 ~15m

---

🐛 Known Issues

· Windows compatibility requires Npcap/WinPcap
· Rate limiting may trigger on aggressive scans
· Some IPv6 implementations not fully supported
· Large networks (>/20) require extended timeouts

---

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

🙏 Acknowledgments

· Charlie Syllas - Lead Developer & Architecture
· Jaguar 45 - Core Engine & Vulnerability Research
· Open-source community for various libraries and tools

---

📬 Contact

· Charlie Syllas  - charliesyllas@gmail.com
· Jaguar 45 - 

Project Link: https://github.com/charlietech255/scaner

---

<div align="center">
  <sub>Built with ❤️ by Charlie Syllas & Jaguar 45</sub>
  <br>
  <sub>© 2026 JAGUAR 45 Tools. All rights reserved.</sub>
</div>
```
