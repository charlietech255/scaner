"""
JAGUAR 45 - 10 REAL WORKING TOOLS
No placeholders, no simulations, all working
"""

import os
import sys
import json
import socket
import requests
import threading
import ipaddress
import time
import hashlib
import random
import string
import re
import ssl
import urllib3
import whois
import dns.resolver
from datetime import datetime
from urllib.parse import urlparse, parse_qs, quote
from concurrent.futures import ThreadPoolExecutor, as_completed

# Flask imports
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

# Disable warnings
import warnings
warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

# ========== CONFIGURATION ==========
MAX_THREADS = 100
REQUEST_TIMEOUT = 5

# ========== SIMPLE HTML TEMPLATE ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jaguar 45 - 10 Real Tools</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        
        body {
            background: #0a0a0a;
            color: #00ff00;
            min-height: 100vh;
            padding: 10px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            padding: 15px 0;
            margin-bottom: 15px;
            border-bottom: 1px solid #00aa00;
        }
        
        .title {
            color: #00ff00;
            font-size: 22px;
            font-weight: bold;
        }
        
        .subtitle {
            color: #008800;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .tool-btn {
            padding: 12px;
            background: #001100;
            border: 1px solid #003300;
            color: #00ff00;
            cursor: pointer;
            font-size: 14px;
            border-radius: 4px;
            transition: all 0.2s;
            text-align: left;
        }
        
        .tool-btn:hover {
            background: #002200;
            border-color: #00aa00;
        }
        
        .tool-btn.active {
            background: #003300;
            border-color: #00ff00;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }
        
        .tool-icon {
            font-size: 16px;
            margin-right: 8px;
        }
        
        .input-section {
            background: #001100;
            border: 1px solid #003300;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .input-row {
            margin-bottom: 10px;
        }
        
        .input-label {
            display: block;
            color: #00aa00;
            font-size: 13px;
            margin-bottom: 5px;
        }
        
        .input-field {
            width: 100%;
            padding: 10px;
            background: #000;
            border: 1px solid #005500;
            color: #00ff00;
            font-size: 14px;
            border-radius: 3px;
        }
        
        .input-field:focus {
            outline: none;
            border-color: #00ff00;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
        }
        
        .button-row {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        .action-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 3px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
            flex: 1;
        }
        
        .start-btn {
            background: #003300;
            color: #00ff00;
            border: 1px solid #00aa00;
        }
        
        .start-btn:hover {
            background: #004400;
            border-color: #00ff00;
        }
        
        .stop-btn {
            background: #330000;
            color: #ff0000;
            border: 1px solid #aa0000;
        }
        
        .stop-btn:hover {
            background: #440000;
            border-color: #ff0000;
        }
        
        .clear-btn {
            background: #111111;
            color: #888888;
            border: 1px solid #333333;
        }
        
        .clear-btn:hover {
            background: #222222;
            border-color: #666666;
        }
        
        .results-section {
            background: #000;
            border: 1px solid #003300;
            border-radius: 4px;
            padding: 15px;
            height: 500px;
            overflow-y: auto;
        }
        
        .results-header {
            color: #00aa00;
            font-size: 14px;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid #003300;
        }
        
        .results-content {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.4;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .status-bar {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: #001100;
            border: 1px solid #003300;
            border-radius: 4px;
            margin-top: 15px;
            font-size: 12px;
            color: #008800;
        }
        
        .green { color: #00ff00; }
        .red { color: #ff0000; }
        .yellow { color: #ffff00; }
        .cyan { color: #00ffff; }
        .magenta { color: #ff00ff; }
        .white { color: #ffffff; }
        .gray { color: #888888; }
        
        .output-line {
            margin-bottom: 2px;
        }
        
        .progress-bar {
            height: 4px;
            background: #001100;
            border-radius: 2px;
            margin-top: 10px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: #00aa00;
            width: 0%;
            transition: width 0.3s;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #001100;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #005500;
            border-radius: 4px;
        }
        
        @media (max-width: 768px) {
            .tools-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .button-row {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">JAGUAR 45 - 10 REAL WORKING TOOLS</div>
            <div class="subtitle">No placeholders, no simulations - All tools actually work</div>
        </div>
        
        <div class="tools-grid">
            <button class="tool-btn" onclick="selectTool(1)">
                <span class="tool-icon">🔌</span> Port Scanner
            </button>
            <button class="tool-btn" onclick="selectTool(2)">
                <span class="tool-icon">📁</span> Directory Scanner
            </button>
            <button class="tool-btn" onclick="selectTool(3)">
                <span class="tool-icon">🌐</span> Website Info
            </button>
            <button class="tool-btn" onclick="selectTool(4)">
                <span class="tool-icon">🔍</span> WHOIS Lookup
            </button>
            <button class="tool-btn" onclick="selectTool(5)">
                <span class="tool-icon">🔐</span> SSL Checker
            </button>
            <button class="tool-btn" onclick="selectTool(6)">
                <span class="tool-icon">💉</span> SQL Injection
            </button>
            <button class="tool-btn" onclick="selectTool(7)">
                <span class="tool-icon">🎯</span> XSS Scanner
            </button>
            <button class="tool-btn" onclick="selectTool(8)">
                <span class="tool-icon">🔓</span> Hash Cracker
            </button>
            <button class="tool-btn" onclick="selectTool(9)">
                <span class="tool-icon">📍</span> IP Information
            </button>
            <button class="tool-btn" onclick="selectTool(10)">
                <span class="tool-icon">⚡</span> Load Test
            </button>
        </div>
        
        <div class="input-section">
            <div class="input-row">
                <div class="input-label" id="mainLabel">Target:</div>
                <input type="text" class="input-field" id="targetInput" 
                       placeholder="example.com or 192.168.1.1" autocomplete="off">
            </div>
            
            <div class="input-row" id="extraRow" style="display: none;">
                <div class="input-label" id="extraLabel">Options:</div>
                <input type="text" class="input-field" id="extraInput" 
                       placeholder="" autocomplete="off">
            </div>
            
            <div class="button-row">
                <button class="action-btn start-btn" onclick="startScan()">▶ START SCAN</button>
                <button class="action-btn stop-btn" onclick="stopScan()">■ STOP</button>
                <button class="action-btn clear-btn" onclick="clearResults()">🗑 CLEAR</button>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="progressBar"></div>
            </div>
        </div>
        
        <div class="results-section">
            <div class="results-header" id="resultsHeader">Scan Results</div>
            <div class="results-content" id="resultsContent">
<span class="green">$ Jaguar 45 - 10 Real Working Tools</span>
<span class="cyan">$ All tools are actually functional</span>
<span class="gray">$ No placeholders, no simulations</span>
<span class="white">$ Select a tool and enter target</span>
            </div>
        </div>
        
        <div class="status-bar">
            <div id="statusText">STATUS: READY</div>
            <div id="toolName">TOOL: PORT SCANNER</div>
            <div id="timeDisplay">TIME: --:--:--</div>
        </div>
    </div>

    <script>
        let currentTool = 1;
        let scanActive = false;
        let scanStartTime = null;
        
        const tools = {
            1: { name: 'Port Scanner', label: 'Target (IP/Domain):', 
                 extra: true, extraLabel: 'Port Range:', extraPlaceholder: 'common / top100 / 1-1000' },
            2: { name: 'Directory Scanner', label: 'Website URL:', 
                 extra: false },
            3: { name: 'Website Info', label: 'Website URL:', 
                 extra: false },
            4: { name: 'WHOIS Lookup', label: 'Domain:', 
                 extra: false },
            5: { name: 'SSL Checker', label: 'Domain:', 
                 extra: false },
            6: { name: 'SQL Injection', label: 'URL with parameters:', 
                 extra: false },
            7: { name: 'XSS Scanner', label: 'Website URL:', 
                 extra: false },
            8: { name: 'Hash Cracker', label: 'Hash:', 
                 extra: true, extraLabel: 'Hash Type:', extraPlaceholder: 'md5 / sha1 / sha256' },
            9: { name: 'IP Information', label: 'IP Address:', 
                 extra: false },
            10: { name: 'Load Test', label: 'Target URL:', 
                  extra: true, extraLabel: 'Duration (seconds):', extraPlaceholder: '10' }
        };
        
        function selectTool(toolId) {
            currentTool = toolId;
            const tool = tools[toolId];
            
            document.getElementById('mainLabel').textContent = tool.label;
            document.getElementById('toolName').textContent = `TOOL: ${tool.name}`;
            document.getElementById('resultsHeader').textContent = `${tool.name} - Ready`;
            
            const extraRow = document.getElementById('extraRow');
            if (tool.extra) {
                extraRow.style.display = 'block';
                document.getElementById('extraLabel').textContent = tool.extraLabel;
                document.getElementById('extraInput').placeholder = tool.extraPlaceholder;
            } else {
                extraRow.style.display = 'none';
            }
            
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            clearResults();
            addOutput(`$ Tool selected: ${tool.name}`, 'green');
            updateStatus('READY');
        }
        
        function startScan() {
            if (scanActive) {
                addOutput('$ Scan already in progress', 'yellow');
                return;
            }
            
            const target = document.getElementById('targetInput').value.trim();
            if (!target) {
                addOutput('ERROR: Please enter a target', 'red');
                return;
            }
            
            const extra = document.getElementById('extraInput').value.trim();
            scanActive = true;
            scanStartTime = new Date();
            
            updateStatus('SCANNING...');
            document.getElementById('progressBar').style.width = '30%';
            addOutput(`$ Starting ${tools[currentTool].name}...`, 'cyan');
            addOutput(`$ Target: ${target}`, 'white');
            if (extra) addOutput(`$ Options: ${extra}`, 'gray');
            addOutput('='.repeat(60), 'gray');
            
            const data = {
                tool: currentTool,
                target: target,
                extra: extra
            };
            
            fetch('/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                scanActive = false;
                document.getElementById('progressBar').style.width = '100%';
                
                if (data.error) {
                    addOutput(`ERROR: ${data.error}`, 'red');
                    updateStatus('FAILED');
                } else {
                    displayResults(data.results);
                    updateStatus('COMPLETE');
                    
                    const endTime = new Date();
                    const duration = ((endTime - scanStartTime) / 1000).toFixed(2);
                    addOutput('='.repeat(60), 'gray');
                    addOutput(`$ Scan completed in ${duration}s`, 'green');
                }
                
                setTimeout(() => {
                    document.getElementById('progressBar').style.width = '0%';
                }, 1000);
            })
            .catch(error => {
                scanActive = false;
                document.getElementById('progressBar').style.width = '0%';
                addOutput(`NETWORK ERROR: ${error}`, 'red');
                updateStatus('ERROR');
            });
        }
        
        function stopScan() {
            if (!scanActive) return;
            
            scanActive = false;
            document.getElementById('progressBar').style.width = '0%';
            addOutput('$ Scan stopped by user', 'yellow');
            updateStatus('STOPPED');
        }
        
        function displayResults(results) {
            if (!results || results.length === 0) {
                addOutput('No results found', 'yellow');
                return;
            }
            
            if (Array.isArray(results)) {
                results.forEach(item => {
                    if (typeof item === 'object') {
                        for (const [key, value] of Object.entries(item)) {
                            const color = getColor(key, value);
                            addOutput(`${key}: ${value}`, color);
                        }
                        addOutput('', 'gray');
                    } else {
                        const color = getColor('', item);
                        addOutput(item, color);
                    }
                });
            } else if (typeof results === 'object') {
                for (const [key, value] of Object.entries(results)) {
                    const color = getColor(key, value);
                    addOutput(`${key}: ${value}`, color);
                }
            } else {
                addOutput(results, 'white');
            }
        }
        
        function getColor(key, value) {
            const keyLower = String(key).toLowerCase();
            const valueLower = String(value).toLowerCase();
            
            if (keyLower.includes('error') || valueLower.includes('error')) return 'red';
            if (keyLower.includes('success') || valueLower.includes('success')) return 'green';
            if (keyLower.includes('warning') || valueLower.includes('warning')) return 'yellow';
            if (keyLower.includes('open') || valueLower.includes('open')) return 'green';
            if (keyLower.includes('vulnerable') || valueLower.includes('vulnerable')) return 'red';
            if (keyLower.includes('port') || valueLower.includes('port')) return 'cyan';
            if (keyLower.includes('time') || valueLower.includes('time')) return 'magenta';
            if (keyLower.includes('hash') || valueLower.includes('hash')) return 'magenta';
            
            return 'white';
        }
        
        function addOutput(text, colorClass = 'white') {
            const resultsDiv = document.getElementById('resultsContent');
            const line = document.createElement('div');
            line.className = `output-line ${colorClass}`;
            line.textContent = text;
            resultsDiv.appendChild(line);
            resultsDiv.scrollTop = resultsDiv.scrollHeight;
        }
        
        function clearResults() {
            document.getElementById('resultsContent').innerHTML = '';
            document.getElementById('progressBar').style.width = '0%';
            addOutput('$ Results cleared', 'gray');
            addOutput('$ System ready', 'green');
            updateStatus('READY');
        }
        
        function updateStatus(text) {
            document.getElementById('statusText').textContent = `STATUS: ${text}`;
        }
        
        function updateTime() {
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            document.getElementById('timeDisplay').textContent = `TIME: ${timeStr}`;
        }
        setInterval(updateTime, 1000);
        
        window.onload = function() {
            selectTool(1);
            updateTime();
            
            document.getElementById('targetInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') startScan();
            });
            document.getElementById('extraInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') startScan();
            });
        };
    </script>
</body>
</html>'''

# ========== REAL WORKING TOOLS ==========

class RealPortScanner:
    """Actually scans ports - no simulation"""
    
    def scan(self, target, port_range="common"):
        results = []
        
        try:
            # Remove http:// if present
            target = target.replace('http://', '').replace('https://', '').split('/')[0]
            
            # Get IP
            try:
                ip = socket.gethostbyname(target)
            except:
                ip = target
            
            results.append(f"Target: {target}")
            results.append(f"IP: {ip}")
            
            # Determine ports
            if port_range == "common":
                ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 
                        3306, 3389, 5432, 5900, 8080, 8443, 8888]
            elif port_range == "top100":
                ports = list(range(1, 101))
            elif "-" in port_range:
                start, end = map(int, port_range.split("-"))
                ports = list(range(start, end + 1))
            else:
                ports = [int(p) for p in port_range.split(",") if p.isdigit()]
            
            results.append(f"Scanning {len(ports)} ports...")
            results.append("=" * 60)
            
            open_ports = []
            
            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        return port, True
                    sock.close()
                except:
                    pass
                return port, False
            
            # Threaded scan
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(check_port, port) for port in ports]
                for future in as_completed(futures):
                    port, is_open = future.result()
                    if is_open:
                        open_ports.append(port)
                        service = self.get_service(port)
                        results.append(f"PORT {port:<6} OPEN   {service}")
            
            results.append("=" * 60)
            results.append(f"Found {len(open_ports)} open ports")
            if open_ports:
                results.append(f"Open ports: {sorted(open_ports)}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def get_service(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP Proxy", 8443: "HTTPS Alt"
        }
        return services.get(port, "Unknown")

class RealDirectoryScanner:
    """Actually scans for directories - no simulation"""
    
    def __init__(self):
        self.common_paths = [
            "admin", "administrator", "login", "dashboard", "wp-admin",
            "wp-login.php", "admin.php", "backend", "cgi-bin", "api",
            "test", "backup", "config", "config.php", ".env", ".git",
            "robots.txt", "sitemap.xml", "phpinfo.php", ".htaccess",
            "server-status", "logs", "error_log", "upload", "uploads"
        ]
    
    def scan(self, url):
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            base_url = url.rstrip('/')
            results.append(f"Scanning: {url}")
            results.append(f"Checking {len(self.common_paths)} common paths")
            results.append("=" * 60)
            
            found = 0
            
            def check_path(path):
                try:
                    test_url = f"{base_url}/{path}"
                    response = requests.head(test_url, timeout=2, verify=False, allow_redirects=True)
                    if response.status_code < 400:
                        # Get more info
                        get_response = requests.get(test_url, timeout=3, verify=False)
                        size = len(get_response.content)
                        return path, response.status_code, size, True
                except:
                    pass
                return path, 0, 0, False
            
            # Threaded scanning
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(check_path, path) for path in self.common_paths]
                for future in as_completed(futures):
                    path, status, size, found_flag = future.result()
                    if found_flag:
                        found += 1
                        results.append(f"[{status}] {base_url}/{path}")
                        results.append(f"     Size: {size} bytes")
            
            results.append("=" * 60)
            results.append(f"Found {found} accessible paths")
            
            if found == 0:
                results.append("Tip: Try with different protocols (http/https)")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

class RealWebsiteInfo:
    """Actually gets website info - no simulation"""
    
    def get_info(self, url):
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            start_time = time.time()
            response = requests.get(url, timeout=5, verify=False)
            load_time = time.time() - start_time
            
            results.append(f"URL: {url}")
            results.append(f"Status Code: {response.status_code}")
            results.append(f"Load Time: {load_time:.2f}s")
            results.append(f"Content Size: {len(response.content)} bytes")
            results.append(f"Server: {response.headers.get('Server', 'Unknown')}")
            results.append(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            
            # Get IP
            try:
                hostname = urlparse(url).hostname
                ip = socket.gethostbyname(hostname)
                results.append(f"IP Address: {ip}")
            except:
                results.append(f"IP Address: Could not resolve")
            
            # Check headers
            security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 
                              'X-XSS-Protection', 'Strict-Transport-Security']
            missing = []
            for header in security_headers:
                if header not in response.headers:
                    missing.append(header)
            
            if missing:
                results.append(f"Missing Security Headers: {', '.join(missing)}")
            
            # Try to get page title
            title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
            if title_match:
                results.append(f"Page Title: {title_match.group(1)[:100]}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

class RealWHOISLookup:
    """Actually does WHOIS lookup - no simulation"""
    
    def lookup(self, domain):
        results = []
        
        try:
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
            w = whois.whois(domain)
            
            results.append(f"Domain: {domain}")
            
            if w.registrar:
                results.append(f"Registrar: {w.registrar}")
            
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    results.append(f"Created: {w.creation_date[0]}")
                else:
                    results.append(f"Created: {w.creation_date}")
            
            if w.expiration_date:
                if isinstance(w.expiration_date, list):
                    results.append(f"Expires: {w.expiration_date[0]}")
                else:
                    results.append(f"Expires: {w.expiration_date}")
            
            if w.name_servers:
                servers = ', '.join(w.name_servers[:3])
                if len(w.name_servers) > 3:
                    servers += f" (+{len(w.name_servers)-3} more)"
                results.append(f"Name Servers: {servers}")
            
            if w.status:
                if isinstance(w.status, list):
                    results.append(f"Status: {', '.join(w.status[:3])}")
                else:
                    results.append(f"Status: {w.status}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

class RealSSLChecker:
    """Actually checks SSL certificate - no simulation"""
    
    def check(self, domain):
        results = []
        
        try:
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
            results.append(f"Domain: {domain}")
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            # Parse dates
            from datetime import datetime
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_left = (not_after - datetime.now()).days
            
            # Get issuer
            issuer = dict(x[0] for x in cert['issuer'])
            
            results.append(f"Issuer: {issuer.get('organizationName', 'Unknown')}")
            results.append(f"Valid From: {cert['notBefore']}")
            results.append(f"Valid Until: {cert['notAfter']}")
            results.append(f"Days Left: {days_left}")
            
            if days_left > 30:
                results.append(f"Status: VALID (Expires in {days_left} days)")
            elif days_left > 0:
                results.append(f"Status: WARNING (Expires in {days_left} days)")
            else:
                results.append(f"Status: EXPIRED")
            
            return results
            
        except Exception as e:
            return [f"ERROR: SSL check failed: {str(e)}"]

class RealSQLInjection:
    """Actually tests for SQL injection - no simulation"""
    
    def test(self, url):
        results = []
        
        try:
            if '?' not in url:
                return ["ERROR: URL must have parameters (e.g., ?id=1)"]
            
            results.append(f"Testing: {url}")
            results.append("=" * 60)
            
            # Basic SQLi payloads
            payloads = ["'", "' OR '1'='1", "' OR '1'='1' --", "' UNION SELECT NULL--"]
            
            parsed = urlparse(url)
            base = url.split('?')[0]
            params = url.split('?')[1]
            
            vulnerable = False
            
            for param in params.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    
                    for payload in payloads:
                        try:
                            test_url = f"{base}?{key}={value}{payload}"
                            response = requests.get(test_url, timeout=3, verify=False)
                            
                            # Check for SQL errors
                            if any(word in response.text.lower() for word in ['sql', 'mysql', 'error', 'syntax']):
                                vulnerable = True
                                results.append(f"VULNERABLE: Parameter '{key}'")
                                results.append(f"Payload: {payload}")
                                break
                        except:
                            continue
                    
                    if vulnerable:
                        break
            
            if vulnerable:
                results.append("")
                results.append("EXPLOITATION:")
                results.append(f"Try: sqlmap -u \"{url}\" --batch")
                results.append(f"Or manually test with UNION queries")
            else:
                results.append("No SQL injection vulnerabilities detected")
                results.append("")
                results.append("TRY THESE PAYLOADS MANUALLY:")
                results.append("' UNION SELECT 1,2,3--")
                results.append("admin' OR '1'='1")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

class RealXSSScanner:
    """Actually tests for XSS - no simulation"""
    
    def scan(self, url):
        results = []
        
        try:
            results.append(f"Testing: {url}")
            results.append("=" * 60)
            
            payload = "<script>alert('xss')</script>"
            
            if '?' in url:
                # Test parameters
                base = url.split('?')[0]
                params = url.split('?')[1]
                
                for param in params.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        test_url = f"{base}?{key}={value}{payload}"
                        response = requests.get(test_url, timeout=3, verify=False)
                        
                        if payload in response.text:
                            results.append(f"VULNERABLE: Parameter '{key}'")
                            results.append("Type: Reflected XSS")
                            results.append("")
                            results.append("EXPLOITATION:")
                            results.append(f"Attack URL: {test_url}")
                            return results
            
            # Test without parameters
            test_url = f"{url}?test={payload}"
            response = requests.get(test_url, timeout=3, verify=False)
            
            if payload in response.text:
                results.append(f"VULNERABLE: Reflected XSS")
                results.append(f"Attack URL: {test_url}")
            else:
                results.append("No XSS vulnerabilities detected")
                results.append("")
                results.append("TRY THESE PAYLOADS MANUALLY:")
                results.append("<script>alert(1)</script>")
                results.append("\" onmouseover=\"alert(1)")
                results.append("<img src=x onerror=alert(1)>")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

class RealHashCracker:
    """Actually cracks hashes - no simulation"""
    
    def crack(self, hash_str, hash_type="auto"):
        results = []
        
        try:
            results.append(f"Hash: {hash_str}")
            
            # Auto-detect
            if hash_type == "auto":
                if len(hash_str) == 32:
                    hash_type = "MD5"
                elif len(hash_str) == 40:
                    hash_type = "SHA1"
                elif len(hash_str) == 64:
                    hash_type = "SHA256"
                else:
                    hash_type = "Unknown"
            
            results.append(f"Type: {hash_type}")
            results.append("=" * 60)
            
            # Common passwords to try
            common_passwords = [
                "password", "123456", "12345678", "qwerty", "abc123",
                "password1", "admin", "letmein", "welcome", "monkey",
                "dragon", "baseball", "football", "hello", "secret"
            ]
            
            found = False
            
            for password in common_passwords:
                hashed = None
                
                if hash_type.upper() == "MD5":
                    hashed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type.upper() == "SHA1":
                    hashed = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type.upper() == "SHA256":
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                
                if hashed and hashed.lower() == hash_str.lower():
                    results.append(f"CRACKED!")
                    results.append(f"Password: {password}")
                    results.append(f"Hash: {hashed}")
                    found = True
                    break
            
            if not found:
                results.append("Not found in common passwords")
                results.append("")
                results.append("TRY THESE MANUALLY:")
                results.append("Password: 123456")
                results.append("Password: admin")
                results.append("Password: password")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

class RealIPInfo:
    """Actually gets IP information - no simulation"""
    
    def info(self, ip):
        results = []
        
        try:
            # Validate IP
            ip_obj = ipaddress.ip_address(ip)
            
            results.append(f"IP Address: {ip}")
            results.append(f"IP Version: IPv{ip_obj.version}")
            results.append(f"Private: {'Yes' if ip_obj.is_private else 'No'}")
            results.append(f"Loopback: {'Yes' if ip_obj.is_loopback else 'No'}")
            
            # Reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                results.append(f"Hostname: {hostname}")
            except:
                results.append(f"Hostname: Not found")
            
            # Quick geolocation
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        results.append(f"Country: {data.get('country', 'N/A')}")
                        results.append(f"City: {data.get('city', 'N/A')}")
                        results.append(f"ISP: {data.get('isp', 'N/A')}")
            except:
                pass
            
            # Check common ports
            common_ports = [21, 22, 80, 443, 3389]
            open_ports = []
            
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    if sock.connect_ex((ip, port)) == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
            
            if open_ports:
                results.append(f"Open Ports (common): {', '.join(map(str, open_ports))}")
            
            return results
            
        except ValueError:
            return ["ERROR: Invalid IP address"]
        except Exception as e:
            return [f"ERROR: {str(e)}"]

class RealLoadTest:
    """Actually does load testing - no simulation"""
    
    def test(self, url, duration=10):
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            duration = int(duration) if str(duration).isdigit() else 10
            if duration > 30:
                duration = 30
            
            results.append(f"Target: {url}")
            results.append(f"Duration: {duration}s")
            results.append("Starting load test...")
            results.append("=" * 60)
            
            requests_sent = 0
            errors = 0
            start_time = time.time()
            
            session = requests.Session()
            
            while time.time() - start_time < duration:
                try:
                    session.get(url, timeout=2, verify=False)
                    requests_sent += 1
                    time.sleep(0.01)
                except:
                    errors += 1
            
            elapsed = time.time() - start_time
            
            results.append(f"Requests Sent: {requests_sent}")
            results.append(f"Errors: {errors}")
            results.append(f"Actual Time: {elapsed:.2f}s")
            results.append(f"Requests/Second: {requests_sent/elapsed:.1f}")
            
            if errors == 0:
                results.append(f"Success Rate: 100%")
            else:
                success_rate = (requests_sent/(requests_sent+errors))*100
                results.append(f"Success Rate: {success_rate:.1f}%")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

# ========== TOOL INSTANCES ==========
port_scanner = RealPortScanner()
dir_scanner = RealDirectoryScanner()
website_info = RealWebsiteInfo()
whois_lookup = RealWHOISLookup()
ssl_checker = RealSSLChecker()
sqli_tester = RealSQLInjection()
xss_scanner = RealXSSScanner()
hash_cracker = RealHashCracker()
ip_info = RealIPInfo()
load_tester = RealLoadTest()

# ========== FLASK ROUTES ==========
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.get_json()
        tool_id = int(data.get('tool', 1))
        target = data.get('target', '').strip()
        extra = data.get('extra', '').strip()
        
        if not target:
            return jsonify({'error': 'Target required'})
        
        results = []
        
        # Tool 1: Port Scanner
        if tool_id == 1:
            results = port_scanner.scan(target, extra if extra else "common")
        
        # Tool 2: Directory Scanner
        elif tool_id == 2:
            results = dir_scanner.scan(target)
        
        # Tool 3: Website Info
        elif tool_id == 3:
            results = website_info.get_info(target)
        
        # Tool 4: WHOIS Lookup
        elif tool_id == 4:
            results = whois_lookup.lookup(target)
        
        # Tool 5: SSL Checker
        elif tool_id == 5:
            results = ssl_checker.check(target)
        
        # Tool 6: SQL Injection
        elif tool_id == 6:
            results = sqli_tester.test(target)
        
        # Tool 7: XSS Scanner
        elif tool_id == 7:
            results = xss_scanner.scan(target)
        
        # Tool 8: Hash Cracker
        elif tool_id == 8:
            results = hash_cracker.crack(target, extra if extra else "auto")
        
        # Tool 9: IP Information
        elif tool_id == 9:
            results = ip_info.info(target)
        
        # Tool 10: Load Test
        elif tool_id == 10:
            results = load_tester.test(target, extra if extra else "10")
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Jaguar 45 - 10 Real Tools',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║            JAGUAR 45 - 10 REAL WORKING TOOLS             ║
    ║               No placeholders, no simulations            ║
    ║                                                          ║
    ║         Server: http://localhost:{port:<15}               ║
    ║         All 10 tools actually work                       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
