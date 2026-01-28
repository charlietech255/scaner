"""
JAGUAR 45 CYBER KIT - TERMINAL STYLE
Fast, accurate, and clean terminal-style results
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
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import base64

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
REQUEST_TIMEOUT = 3
USER_AGENT = "Jaguar45-Scanner/2.0"
SCAN_TIMEOUT = 30  # Max scan time

# ========== CLEAN TERMINAL HTML TEMPLATE ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jaguar 45 - Cyber Scanner</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', monospace;
        }
        
        body {
            background: #0a0a0a;
            color: #00ff00;
            min-height: 100vh;
            padding: 10px;
        }
        
        .header {
            text-align: center;
            padding: 10px 0;
            margin-bottom: 10px;
            border-bottom: 1px solid #00aa00;
        }
        
        .title {
            color: #00ff00;
            font-size: 18px;
            font-weight: bold;
        }
        
        .subtitle {
            color: #008800;
            font-size: 12px;
            margin-top: 3px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .tools-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 10px;
            padding: 8px;
            background: #001100;
            border: 1px solid #003300;
            border-radius: 3px;
        }
        
        .tool-btn {
            padding: 6px 12px;
            background: #002200;
            border: 1px solid #005500;
            color: #00ff00;
            cursor: pointer;
            font-size: 12px;
            border-radius: 2px;
            transition: all 0.2s;
        }
        
        .tool-btn:hover {
            background: #003300;
            border-color: #00aa00;
        }
        
        .tool-btn.active {
            background: #004400;
            border-color: #00ff00;
            box-shadow: 0 0 5px #00ff00;
        }
        
        .input-area {
            background: #001100;
            border: 1px solid #003300;
            border-radius: 3px;
            padding: 10px;
            margin-bottom: 10px;
        }
        
        .input-row {
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
            align-items: center;
        }
        
        .input-label {
            color: #00aa00;
            font-size: 13px;
            min-width: 150px;
        }
        
        .input-field {
            flex: 1;
            padding: 8px;
            background: #000;
            border: 1px solid #005500;
            color: #00ff00;
            font-size: 13px;
            border-radius: 2px;
        }
        
        .input-field:focus {
            outline: none;
            border-color: #00ff00;
            box-shadow: 0 0 5px #00ff00;
        }
        
        .button-row {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .action-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 2px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .scan-btn {
            background: #003300;
            color: #00ff00;
            border: 1px solid #00aa00;
        }
        
        .scan-btn:hover {
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
        
        .results-area {
            background: #000;
            border: 1px solid #003300;
            border-radius: 3px;
            padding: 10px;
            margin-bottom: 10px;
            height: 500px;
            overflow-y: auto;
        }
        
        .results-header {
            color: #00aa00;
            font-size: 13px;
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
            padding: 8px;
            background: #001100;
            border: 1px solid #003300;
            border-radius: 3px;
            font-size: 12px;
            color: #008800;
        }
        
        /* Color Classes */
        .green { color: #00ff00; }
        .cyan { color: #00ffff; }
        .yellow { color: #ffff00; }
        .red { color: #ff0000; }
        .magenta { color: #ff00ff; }
        .blue { color: #0088ff; }
        .white { color: #ffffff; }
        .gray { color: #888888; }
        
        /* Terminal Output Styles */
        .output-line {
            margin-bottom: 2px;
            padding-left: 2px;
        }
        
        .port-open {
            color: #00ff00;
            background: #002200;
            padding: 1px 5px;
            margin: 1px 0;
        }
        
        .port-closed {
            color: #888888;
            padding: 1px 5px;
            margin: 1px 0;
        }
        
        .success {
            color: #00ff00;
        }
        
        .error {
            color: #ff0000;
        }
        
        .warning {
            color: #ffff00;
        }
        
        .info {
            color: #00ffff;
        }
        
        .highlight {
            color: #ff00ff;
        }
        
        /* Progress Bar */
        .progress-container {
            height: 4px;
            background: #001100;
            border-radius: 2px;
            margin-top: 8px;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background: #00aa00;
            width: 0%;
            transition: width 0.3s;
        }
        
        /* Scrollbar */
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
        
        ::-webkit-scrollbar-thumb:hover {
            background: #00aa00;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .tools-bar {
                justify-content: center;
            }
            
            .input-row {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .input-label {
                min-width: auto;
            }
            
            .results-area {
                height: 400px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">JAGUAR 45 CYBER SCANNER</div>
            <div class="subtitle">Fast • Accurate • Terminal-Style Results</div>
        </div>
        
        <div class="tools-bar">
            <button class="tool-btn" onclick="selectTool(1)">🔌 Port Scan</button>
            <button class="tool-btn" onclick="selectTool(2)">📁 Dir Scan</button>
            <button class="tool-btn" onclick="selectTool(3)">🌐 Website Info</button>
            <button class="tool-btn" onclick="selectTool(4)">🔍 WHOIS</button>
            <button class="tool-btn" onclick="selectTool(5)">🔐 SSL Check</button>
            <button class="tool-btn" onclick="selectTool(6)">⚡ Speed Test</button>
            <button class="tool-btn" onclick="selectTool(7)">🛡️ SQLi Test</button>
            <button class="tool-btn" onclick="selectTool(8)">🚫 XSS Test</button>
            <button class="tool-btn" onclick="selectTool(9)">🎯 Ping Test</button>
            <button class="tool-btn" onclick="selectTool(10)">📍 IP Info</button>
            <button class="tool-btn" onclick="selectTool(11)">🔓 Hash Crack</button>
            <button class="tool-btn" onclick="selectTool(12)">📈 Load Test</button>
        </div>
        
        <div class="input-area">
            <div class="input-row">
                <div class="input-label" id="mainLabel">Target:</div>
                <input type="text" class="input-field" id="targetInput" 
                       placeholder="example.com or 192.168.1.1" autocomplete="off">
            </div>
            
            <div class="input-row" id="extraRow" style="display: none;">
                <div class="input-label" id="extraLabel">Port Range:</div>
                <input type="text" class="input-field" id="extraInput" 
                       placeholder="common / top100 / 1-1000" autocomplete="off">
            </div>
            
            <div class="button-row">
                <button class="action-btn scan-btn" onclick="startScan()">▶ START SCAN</button>
                <button class="action-btn stop-btn" onclick="stopScan()">■ STOP</button>
                <button class="action-btn clear-btn" onclick="clearResults()">🗑 CLEAR</button>
            </div>
            
            <div class="progress-container">
                <div class="progress-bar" id="progressBar"></div>
            </div>
        </div>
        
        <div class="results-area">
            <div class="results-header" id="resultsHeader">
                Scan Results • Ready
            </div>
            <div class="results-content" id="resultsContent">
$ System Ready
$ Select tool and enter target
$ Type 'help' for quick reference
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
        
        // Tool configurations
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
            6: { name: 'Speed Test', label: 'Website URL:', 
                 extra: false },
            7: { name: 'SQLi Test', label: 'URL with parameters:', 
                 extra: false },
            8: { name: 'XSS Test', label: 'Website URL:', 
                 extra: false },
            9: { name: 'Ping Test', label: 'Host/IP:', 
                 extra: true, extraLabel: 'Count:', extraPlaceholder: '5' },
            10: { name: 'IP Info', label: 'IP Address:', 
                 extra: false },
            11: { name: 'Hash Cracker', label: 'Hash to crack:', 
                 extra: true, extraLabel: 'Hash Type:', extraPlaceholder: 'auto / md5 / sha1 / sha256' },
            12: { name: 'Load Test', label: 'Your Server URL:', 
                 extra: true, extraLabel: 'Duration (sec):', extraPlaceholder: '10' }
        };
        
        function selectTool(toolId) {
            currentTool = toolId;
            const tool = tools[toolId];
            
            // Update UI
            document.getElementById('mainLabel').textContent = tool.label;
            document.getElementById('toolName').textContent = `TOOL: ${tool.name.toUpperCase()}`;
            document.getElementById('resultsHeader').textContent = `${tool.name} • Ready`;
            
            // Update extra input
            const extraRow = document.getElementById('extraRow');
            if (tool.extra) {
                extraRow.style.display = 'flex';
                document.getElementById('extraLabel').textContent = tool.extraLabel;
                document.getElementById('extraInput').placeholder = tool.extraPlaceholder;
            } else {
                extraRow.style.display = 'none';
            }
            
            // Update active button
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Clear results
            clearResults();
            addOutput(`$ Tool selected: ${tool.name}`, 'green');
            updateStatus('READY');
        }
        
        function startScan() {
            if (scanActive) return;
            
            const target = document.getElementById('targetInput').value.trim();
            if (!target) {
                addOutput('ERROR: Please enter a target', 'red');
                return;
            }
            
            const extra = document.getElementById('extraInput').value.trim();
            scanActive = true;
            scanStartTime = new Date();
            
            // Update UI
            updateStatus('SCANNING...');
            document.getElementById('progressBar').style.width = '30%';
            addOutput(`$ Starting ${tools[currentTool].name}...`, 'cyan');
            addOutput(`$ Target: ${target}`, 'gray');
            if (extra) addOutput(`$ Options: ${extra}`, 'gray');
            addOutput('', 'white');
            
            // Prepare data
            const data = {
                tool: currentTool,
                target: target,
                extra: extra
            };
            
            // Start scan
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
                    
                    // Update time
                    const endTime = new Date();
                    const duration = ((endTime - scanStartTime) / 1000).toFixed(2);
                    addOutput(`$ Scan completed in ${duration}s`, 'green');
                }
                
                // Reset progress bar after delay
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
            
            // Handle array of objects
            if (Array.isArray(results)) {
                results.forEach(item => {
                    if (typeof item === 'object') {
                        // Display object properties
                        for (const [key, value] of Object.entries(item)) {
                            if (value && typeof value === 'string') {
                                const color = getColorForKey(key, value);
                                addOutput(`${key.padEnd(20)}: ${value}`, color);
                            }
                        }
                        addOutput('', 'white'); // Empty line
                    } else {
                        // Plain string result
                        addOutput(item, 'white');
                    }
                });
            } 
            // Handle single object
            else if (typeof results === 'object') {
                for (const [key, value] of Object.entries(results)) {
                    if (value && typeof value === 'string') {
                        const color = getColorForKey(key, value);
                        addOutput(`${key.padEnd(20)}: ${value}`, color);
                    }
                }
            }
            // Handle plain text
            else {
                addOutput(results, 'white');
            }
        }
        
        function getColorForKey(key, value) {
            const keyLower = key.toLowerCase();
            const valueLower = value.toLowerCase();
            
            if (keyLower.includes('error') || valueLower.includes('error')) return 'red';
            if (keyLower.includes('success') || valueLower.includes('success')) return 'green';
            if (keyLower.includes('warning') || valueLower.includes('warning')) return 'yellow';
            if (keyLower.includes('open') || keyLower.includes('port')) return 'green';
            if (keyLower.includes('closed') || keyLower.includes('filtered')) return 'gray';
            if (keyLower.includes('vulnerable') || keyLower.includes('risk')) return 'red';
            if (keyLower.includes('status') || keyLower.includes('code')) return 'cyan';
            if (keyLower.includes('time') || keyLower.includes('duration')) return 'blue';
            if (keyLower.includes('size') || keyLower.includes('length')) return 'magenta';
            
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
        
        // Update time display
        function updateTime() {
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            document.getElementById('timeDisplay').textContent = `TIME: ${timeStr}`;
        }
        setInterval(updateTime, 1000);
        
        // Auto-select first tool on load
        window.onload = function() {
            selectTool(1);
            updateTime();
            
            // Add enter key support
            document.getElementById('targetInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') startScan();
            });
            document.getElementById('extraInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') startScan();
            });
            
            // Initial message
            addOutput('$ Jaguar 45 Cyber Scanner v2.0', 'cyan');
            addOutput('$ Ready for scanning', 'green');
            addOutput('$ Select tool and enter target', 'gray');
        };
    </script>
</body>
</html>'''

# ========== ULTRA-FAST SCANNING TOOLS ==========

class UltraFastScanner:
    def __init__(self):
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                            993, 995, 3306, 3389, 5432, 5900, 8080, 8443, 8888]
        
    def port_scan(self, target, port_range="common"):
        """Ultra-fast threaded port scanner"""
        results = []
        open_count = 0
        
        try:
            # Resolve target
            ip = socket.gethostbyname(target.split(':')[0]) if ':' not in target else target
            
            # Determine ports
            if port_range == "common":
                ports = self.common_ports
            elif port_range == "top100":
                ports = list(range(1, 101))
            elif "-" in port_range:
                start, end = map(int, port_range.split("-"))
                ports = list(range(start, end + 1))
                if len(ports) > 1000:
                    ports = ports[:1000]  # Limit
            else:
                ports = [int(p) for p in port_range.split(",") if p.isdigit()][:100]
            
            total_ports = len(ports)
            results.append(f"Scanning {target} ({ip})")
            results.append(f"Ports to scan: {total_ports}")
            results.append("=" * 50)
            
            # Fast scan with threads
            open_ports = []
            
            def scan_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.3)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    if result == 0:
                        return port, True
                except:
                    pass
                return port, False
            
            with ThreadPoolExecutor(max_workers=200) as executor:
                futures = {executor.submit(scan_port, port): port for port in ports}
                for future in as_completed(futures):
                    port, is_open = future.result()
                    if is_open:
                        open_ports.append(port)
                        service = self.get_service(port)
                        results.append(f"PORT {port:<6} OPEN   {service}")
                        open_count += 1
            
            results.append("=" * 50)
            results.append(f"Scan completed: {open_count} open ports found")
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
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt"
        }
        return services.get(port, "Unknown")
    
    def dir_scan(self, url):
        """Fast directory scanning"""
        results = []
        found = 0
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            base_url = url.rstrip('/')
            paths = [
                "admin", "login", "dashboard", "wp-admin", "administrator",
                "api", "test", "backup", "config", ".env", ".git",
                "robots.txt", "sitemap.xml", "phpinfo.php", ".htaccess",
                "server-status", "wp-login.php", "admin.php", "cgi-bin"
            ]
            
            results.append(f"Scanning: {url}")
            results.append(f"Checking {len(paths)} common paths")
            results.append("=" * 50)
            
            def check_path(path):
                try:
                    test_url = f"{base_url}/{path}"
                    response = requests.head(test_url, timeout=1, verify=False, allow_redirects=True)
                    if response.status_code < 400:
                        return path, response.status_code, True
                except:
                    pass
                return path, 0, False
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(check_path, path) for path in paths]
                for future in as_completed(futures):
                    path, status, found_flag = future.result()
                    if found_flag:
                        found += 1
                        results.append(f"FOUND   {path:<20} [{status}]")
            
            results.append("=" * 50)
            results.append(f"Found {found} accessible paths")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def website_info(self, url):
        """Get website information"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            start = time.time()
            response = requests.get(url, timeout=5, verify=False)
            load_time = time.time() - start
            
            results.append(f"URL:            {url}")
            results.append(f"Status:         {response.status_code}")
            results.append(f"Load Time:      {load_time:.2f}s")
            results.append(f"Content Size:   {len(response.content)} bytes")
            results.append(f"Server:         {response.headers.get('Server', 'Unknown')}")
            results.append(f"Content-Type:   {response.headers.get('Content-Type', 'Unknown')}")
            
            # Get IP
            try:
                hostname = urlparse(url).hostname
                ip = socket.gethostbyname(hostname)
                results.append(f"IP Address:     {ip}")
            except:
                results.append(f"IP Address:     Could not resolve")
            
            # Check security headers
            sec_headers = ['X-Frame-Options', 'X-Content-Type-Options', 
                         'X-XSS-Protection', 'Strict-Transport-Security']
            missing = []
            for header in sec_headers:
                if header not in response.headers:
                    missing.append(header)
            
            if missing:
                results.append(f"Missing Sec:    {', '.join(missing)}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ssl_check(self, domain):
        """Check SSL certificate"""
        results = []
        
        try:
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
            results.append(f"Domain:         {domain}")
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            # Parse dates
            from datetime import datetime
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_left = (not_after - datetime.now()).days
            
            # Get issuer
            issuer = dict(x[0] for x in cert['issuer'])
            
            results.append(f"Issuer:         {issuer.get('organizationName', 'Unknown')}")
            results.append(f"Valid From:     {cert['notBefore']}")
            results.append(f"Valid Until:    {cert['notAfter']}")
            results.append(f"Days Left:      {days_left}")
            
            if days_left > 30:
                results.append(f"Status:         VALID (Expires in {days_left} days)")
            elif days_left > 0:
                results.append(f"Status:         WARNING (Expires in {days_left} days)")
            else:
                results.append(f"Status:         EXPIRED")
            
            return results
            
        except Exception as e:
            return [f"ERROR: SSL check failed: {str(e)}"]
    
    def whois_lookup(self, domain):
        """WHOIS lookup"""
        results = []
        
        try:
            w = whois.whois(domain)
            
            results.append(f"Domain:         {domain}")
            results.append(f"Registrar:      {w.registrar or 'Unknown'}")
            
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    results.append(f"Created:        {w.creation_date[0]}")
                else:
                    results.append(f"Created:        {w.creation_date}")
            
            if w.expiration_date:
                if isinstance(w.expiration_date, list):
                    results.append(f"Expires:        {w.expiration_date[0]}")
                else:
                    results.append(f"Expires:        {w.expiration_date}")
            
            if w.name_servers:
                servers = ', '.join(w.name_servers[:3])
                if len(w.name_servers) > 3:
                    servers += f" (+{len(w.name_servers)-3} more)"
                results.append(f"Name Servers:   {servers}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def speed_test(self, url):
        """Website speed test"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"Testing:        {url}")
            
            # Test multiple times for average
            times = []
            sizes = []
            
            for i in range(3):
                start = time.time()
                response = requests.get(url, timeout=5, verify=False)
                end = time.time()
                
                times.append(end - start)
                sizes.append(len(response.content))
                
                if i == 0:
                    results.append(f"Status:         {response.status_code}")
                    results.append(f"Size:           {len(response.content)} bytes")
            
            avg_time = sum(times) / len(times)
            avg_speed = (sum(sizes) / sum(times)) / 1024  # KB/s
            
            results.append(f"Load Time:      {avg_time:.2f}s (average)")
            results.append(f"Speed:          {avg_speed:.1f} KB/s")
            
            if avg_time < 1:
                results.append(f"Rating:         FAST")
            elif avg_time < 3:
                results.append(f"Rating:         AVERAGE")
            else:
                results.append(f"Rating:         SLOW")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def sqli_test(self, url):
        """SQL injection test"""
        results = []
        
        try:
            if '?' not in url:
                return ["ERROR: URL must have parameters (e.g., ?id=1)"]
            
            results.append(f"Testing:        {url}")
            results.append(f"Method:         GET parameters")
            
            test_payloads = ["'", "' OR '1'='1", "' OR '1'='1' --"]
            vulnerable = False
            
            for payload in test_payloads:
                try:
                    # Test each parameter
                    parsed = urlparse(url)
                    base = url.split('?')[0]
                    params = url.split('?')[1]
                    
                    for param in params.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            test_url = f"{base}?{key}={value}{payload}"
                            response = requests.get(test_url, timeout=2, verify=False)
                            
                            # Check for SQL errors
                            if any(word in response.text.lower() for word in ['sql', 'mysql', 'error', 'syntax']):
                                vulnerable = True
                                results.append(f"VULNERABLE:     Parameter '{key}' with payload '{payload}'")
                                break
                    
                    if vulnerable:
                        break
                        
                except:
                    continue
            
            if not vulnerable:
                results.append(f"Result:         No SQLi vulnerabilities detected")
            else:
                results.append(f"Risk Level:     HIGH")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def xss_test(self, url):
        """XSS test"""
        results = []
        
        try:
            results.append(f"Testing:        {url}")
            
            payload = "<script>alert('xss')</script>"
            
            if '?' in url:
                # Test parameters
                base = url.split('?')[0]
                params = url.split('?')[1]
                
                for param in params.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        test_url = f"{base}?{key}={value}{payload}"
                        response = requests.get(test_url, timeout=2, verify=False)
                        
                        if payload in response.text:
                            results.append(f"VULNERABLE:     Parameter '{key}'")
                            results.append(f"Risk Level:     MEDIUM")
                            return results
            
            # Test form if no parameters
            test_url = f"{url}?test={payload}"
            response = requests.get(test_url, timeout=2, verify=False)
            
            if payload in response.text:
                results.append(f"VULNERABLE:     Reflected XSS detected")
                results.append(f"Risk Level:     MEDIUM")
            else:
                results.append(f"Result:         No XSS vulnerabilities detected")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ping_test(self, host, count="5"):
        """Ping test"""
        results = []
        
        try:
            ip = socket.gethostbyname(host)
            count = int(count) if count.isdigit() else 5
            
            results.append(f"Host:           {host}")
            results.append(f"IP:             {ip}")
            results.append(f"Ping Count:     {count}")
            results.append("-" * 50)
            
            successes = 0
            times = []
            
            for i in range(count):
                try:
                    start = time.time()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, 80))
                    elapsed = (time.time() - start) * 1000
                    sock.close()
                    
                    if result == 0:
                        successes += 1
                        times.append(elapsed)
                        results.append(f"Reply from {ip}: time={elapsed:.1f}ms")
                    else:
                        results.append(f"Request timed out")
                    
                except:
                    results.append(f"Request failed")
                
                if i < count - 1:
                    time.sleep(0.5)
            
            results.append("-" * 50)
            results.append(f"Packets:        Sent = {count}, Received = {successes}, Lost = {count - successes}")
            
            if successes > 0:
                avg_time = sum(times) / len(times)
                results.append(f"Approximate round trip times in ms:")
                results.append(f"Minimum = {min(times):.1f}ms, Maximum = {max(times):.1f}ms, Average = {avg_time:.1f}ms")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ip_info(self, ip):
        """IP information"""
        results = []
        
        try:
            # Validate IP
            ip_obj = ipaddress.ip_address(ip)
            
            results.append(f"IP Address:     {ip}")
            results.append(f"IP Version:     IPv{ip_obj.version}")
            results.append(f"Private:        {'Yes' if ip_obj.is_private else 'No'}")
            results.append(f"Loopback:       {'Yes' if ip_obj.is_loopback else 'No'}")
            results.append(f"Multicast:      {'Yes' if ip_obj.is_multicast else 'No'}")
            
            # Reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                results.append(f"Hostname:       {hostname}")
            except:
                results.append(f"Hostname:       Not found")
            
            # Quick geolocation
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        results.append(f"Country:        {data.get('country', 'N/A')}")
                        results.append(f"Region:         {data.get('regionName', 'N/A')}")
                        results.append(f"City:           {data.get('city', 'N/A')}")
                        results.append(f"ISP:            {data.get('isp', 'N/A')}")
            except:
                pass
            
            return results
            
        except ValueError:
            return ["ERROR: Invalid IP address"]
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def hash_crack(self, hash_str, hash_type="auto"):
        """Hash cracking"""
        results = []
        
        try:
            results.append(f"Hash:           {hash_str}")
            
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
            
            results.append(f"Type:           {hash_type}")
            
            # Common passwords
            common = [
                "password", "123456", "12345678", "qwerty", "abc123",
                "password1", "admin", "letmein", "welcome", "monkey"
            ]
            
            found = False
            for pwd in common:
                hashed = None
                
                if hash_type.upper() == "MD5":
                    hashed = hashlib.md5(pwd.encode()).hexdigest()
                elif hash_type.upper() == "SHA1":
                    hashed = hashlib.sha1(pwd.encode()).hexdigest()
                elif hash_type.upper() == "SHA256":
                    hashed = hashlib.sha256(pwd.encode()).hexdigest()
                
                if hashed and hashed.lower() == hash_str.lower():
                    results.append(f"CRACKED:        {pwd}")
                    results.append(f"Status:         Successfully cracked!")
                    found = True
                    break
            
            if not found:
                results.append(f"Result:         Not found in common passwords")
                results.append(f"Try:            More extensive wordlist")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def load_test(self, url, duration="10"):
        """Load test for YOUR servers"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            # Safety warning for non-local servers
            parsed = urlparse(url)
            hostname = parsed.hostname
            
            if not any(x in hostname for x in ['localhost', '127.0.0.1', '192.168.', '10.', '172.']):
                results.append("WARNING: Load testing should only be performed on")
                results.append("         YOUR OWN servers (localhost or private IPs)")
                results.append(f"Your target: {url}")
                return results
            
            duration = int(duration) if duration.isdigit() else 10
            if duration > 30:
                duration = 30
            
            results.append(f"Target:         {url}")
            results.append(f"Duration:       {duration}s")
            results.append("Starting load test...")
            
            requests_sent = 0
            errors = 0
            start_time = time.time()
            
            session = requests.Session()
            
            while time.time() - start_time < duration:
                try:
                    session.get(url, timeout=1, verify=False)
                    requests_sent += 1
                    time.sleep(0.01)
                except:
                    errors += 1
            
            elapsed = time.time() - start_time
            
            results.append(f"Requests:       {requests_sent}")
            results.append(f"Errors:         {errors}")
            results.append(f"Req/Sec:        {requests_sent/elapsed:.1f}")
            
            if errors == 0:
                results.append(f"Status:         All requests successful")
            else:
                success_rate = (requests_sent/(requests_sent+errors))*100
                results.append(f"Success Rate:   {success_rate:.1f}%")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]

# ========== SCANNER INSTANCE ==========
scanner = UltraFastScanner()

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
        
        # Tool 1: Port Scan
        if tool_id == 1:
            results = scanner.port_scan(target, extra if extra else "common")
        
        # Tool 2: Directory Scan
        elif tool_id == 2:
            results = scanner.dir_scan(target)
        
        # Tool 3: Website Info
        elif tool_id == 3:
            results = scanner.website_info(target)
        
        # Tool 4: WHOIS Lookup
        elif tool_id == 4:
            results = scanner.whois_lookup(target)
        
        # Tool 5: SSL Check
        elif tool_id == 5:
            results = scanner.ssl_check(target)
        
        # Tool 6: Speed Test
        elif tool_id == 6:
            results = scanner.speed_test(target)
        
        # Tool 7: SQLi Test
        elif tool_id == 7:
            results = scanner.sqli_test(target)
        
        # Tool 8: XSS Test
        elif tool_id == 8:
            results = scanner.xss_test(target)
        
        # Tool 9: Ping Test
        elif tool_id == 9:
            results = scanner.ping_test(target, extra if extra else "5")
        
        # Tool 10: IP Info
        elif tool_id == 10:
            results = scanner.ip_info(target)
        
        # Tool 11: Hash Crack
        elif tool_id == 11:
            results = scanner.hash_crack(target, extra if extra else "auto")
        
        # Tool 12: Load Test
        elif tool_id == 12:
            results = scanner.load_test(target, extra if extra else "10")
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Jaguar 45 Cyber Scanner',
        'version': '2.0',
        'uptime': 'running',
        'timestamp': datetime.now().isoformat()
    })

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║           JAGUAR 45 - TERMINAL-STYLE SCANNER             ║
    ║                 Clean • Fast • Accurate                  ║
    ║                                                          ║
    ║         Server: http://localhost:{port:<15}               ║
    ║         Tools: 12 • Threads: 200 • Timeout: 3s          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
