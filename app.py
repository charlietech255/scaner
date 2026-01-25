"""
JAGUAR 45 CYBER KIT - SIMPLE UI
Fast, accurate, and easy-to-use cybersecurity tools
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
MAX_THREADS = 100  # Faster scanning
REQUEST_TIMEOUT = 5
USER_AGENT = "Jaguar45-Scanner/2.0"

# ========== SIMPLE HTML TEMPLATE ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jaguar 45 - Cyber Tools</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        body {
            background: #0a1929;
            color: #e6f1ff;
            min-height: 100vh;
            padding: 10px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 20px 0;
            margin-bottom: 20px;
            border-bottom: 2px solid #00d4aa;
        }
        
        .logo {
            font-size: 28px;
            font-weight: bold;
            color: #00d4aa;
            margin-bottom: 5px;
        }
        
        .subtitle {
            color: #8892b0;
            font-size: 14px;
        }
        
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .tool-card {
            background: #112240;
            border: 1px solid #233554;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }
        
        .tool-card:hover {
            background: #1a365d;
            border-color: #00d4aa;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 212, 170, 0.2);
        }
        
        .tool-card:active {
            transform: translateY(0);
        }
        
        .tool-icon {
            font-size: 24px;
            margin-bottom: 8px;
            color: #00d4aa;
        }
        
        .tool-name {
            font-size: 14px;
            font-weight: 500;
        }
        
        .input-section {
            background: #112240;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #233554;
        }
        
        .input-group {
            margin-bottom: 15px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 5px;
            color: #8892b0;
            font-size: 14px;
        }
        
        .input-group input,
        .input-group select {
            width: 100%;
            padding: 10px;
            background: #0a1929;
            border: 1px solid #233554;
            border-radius: 6px;
            color: #e6f1ff;
            font-size: 14px;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #00d4aa;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            flex: 1;
        }
        
        .btn-primary {
            background: #00d4aa;
            color: #0a1929;
        }
        
        .btn-primary:hover {
            background: #00b894;
        }
        
        .btn-secondary {
            background: #233554;
            color: #e6f1ff;
        }
        
        .btn-secondary:hover {
            background: #1a2c45;
        }
        
        .results-section {
            background: #112240;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #233554;
            min-height: 300px;
            max-height: 600px;
            overflow-y: auto;
        }
        
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #233554;
        }
        
        .results-title {
            font-size: 16px;
            font-weight: 500;
            color: #00d4aa;
        }
        
        .results-content {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .status-bar {
            margin-top: 20px;
            padding: 10px;
            background: #112240;
            border-radius: 6px;
            font-size: 12px;
            color: #8892b0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .success { color: #00d4aa; }
        .error { color: #ff6b6b; }
        .warning { color: #ffd93d; }
        .info { color: #4dabf7; }
        
        .result-item {
            padding: 8px;
            margin: 4px 0;
            background: #0a1929;
            border-radius: 4px;
            border-left: 3px solid #00d4aa;
        }
        
        .port-item {
            display: flex;
            justify-content: space-between;
            padding: 6px 8px;
            margin: 3px 0;
            background: #0a1929;
            border-radius: 4px;
            border-left: 3px solid #00d4aa;
        }
        
        .progress-bar {
            height: 4px;
            background: #233554;
            border-radius: 2px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: #00d4aa;
            width: 0%;
            transition: width 0.3s;
        }
        
        .quick-tools {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .quick-tool {
            padding: 8px 16px;
            background: #112240;
            border: 1px solid #233554;
            border-radius: 6px;
            color: #e6f1ff;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }
        
        .quick-tool:hover {
            background: #1a365d;
            border-color: #00d4aa;
        }
        
        @media (max-width: 768px) {
            .tools-grid {
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            }
            
            .button-group {
                flex-direction: column;
            }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.3s ease-out;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a1929;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #233554;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #1a2c45;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">JAGUAR 45</div>
            <div class="subtitle">Fast & Accurate Cyber Security Tools</div>
        </header>
        
        <div class="quick-tools">
            <div class="quick-tool" onclick="quickScan('port')">🔍 Quick Port Scan</div>
            <div class="quick-tool" onclick="quickScan('dir')">📁 Quick Dir Scan</div>
            <div class="quick-tool" onclick="quickScan('ssl')">🔐 SSL Check</div>
            <div class="quick-tool" onclick="quickScan('ip')">📍 IP Info</div>
            <div class="quick-tool" onclick="clearResults()">🗑️ Clear Results</div>
        </div>
        
        <div class="tools-grid">
            <div class="tool-card" onclick="selectTool(1)">
                <div class="tool-icon">🔌</div>
                <div class="tool-name">Port Scanner</div>
            </div>
            <div class="tool-card" onclick="selectTool(2)">
                <div class="tool-icon">📂</div>
                <div class="tool-name">Directory Scan</div>
            </div>
            <div class="tool-card" onclick="selectTool(3)">
                <div class="tool-icon">🌐</div>
                <div class="tool-name">Website Info</div>
            </div>
            <div class="tool-card" onclick="selectTool(4)">
                <div class="tool-icon">🔍</div>
                <div class="tool-name">WHOIS Lookup</div>
            </div>
            <div class="tool-card" onclick="selectTool(5)">
                <div class="tool-icon">🔐</div>
                <div class="tool-name">SSL Checker</div>
            </div>
            <div class="tool-card" onclick="selectTool(6)">
                <div class="tool-icon">⚡</div>
                <div class="tool-name">Speed Test</div>
            </div>
            <div class="tool-card" onclick="selectTool(7)">
                <div class="tool-icon">🛡️</div>
                <div class="tool-name">SQLi Test</div>
            </div>
            <div class="tool-card" onclick="selectTool(8)">
                <div class="tool-icon">🚫</div>
                <div class="tool-name">XSS Test</div>
            </div>
            <div class="tool-card" onclick="selectTool(9)">
                <div class="tool-icon">🎯</div>
                <div class="tool-name">Ping Test</div>
            </div>
            <div class="tool-card" onclick="selectTool(10)">
                <div class="tool-icon">📊</div>
                <div class="tool-name">IP Info</div>
            </div>
            <div class="tool-card" onclick="selectTool(11)">
                <div class="tool-icon">🔓</div>
                <div class="tool-name">Hash Cracker</div>
            </div>
            <div class="tool-card" onclick="selectTool(12)">
                <div class="tool-icon">📈</div>
                <div class="tool-name">Load Test</div>
            </div>
        </div>
        
        <div class="input-section">
            <div class="input-group">
                <label id="inputLabel">Enter Target:</label>
                <input type="text" id="targetInput" placeholder="example.com or 192.168.1.1">
            </div>
            
            <div class="input-group" id="extraInput" style="display: none;">
                <label id="extraLabel">Additional Info:</label>
                <input type="text" id="extraValue" placeholder="">
            </div>
            
            <div class="button-group">
                <button class="btn btn-primary" onclick="runScan()">Start Scan</button>
                <button class="btn btn-secondary" onclick="stopScan()">Stop</button>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" id="progressBar"></div>
            </div>
        </div>
        
        <div class="results-section">
            <div class="results-header">
                <div class="results-title">Scan Results</div>
                <div id="resultCount">0 items</div>
            </div>
            <div class="results-content" id="resultsContent">
                Ready to scan. Select a tool and enter target.
            </div>
        </div>
        
        <div class="status-bar">
            <div id="statusText">Status: Ready</div>
            <div id="scanTime">Time: --:--</div>
            <div id="toolName">Tool: None</div>
        </div>
    </div>

    <script>
        let currentTool = 0;
        let scanActive = false;
        let scanStartTime = null;
        let resultCount = 0;
        
        // Tool configurations
        const tools = {
            1: { name: 'Port Scanner', label: 'Target (IP/Domain):', extra: 'Ports (common/top100/1-1000):', extraValue: 'common' },
            2: { name: 'Directory Scanner', label: 'Website URL:', extra: 'Wordlist (optional):', extraValue: '' },
            3: { name: 'Website Info', label: 'Website URL:', extra: null },
            4: { name: 'WHOIS Lookup', label: 'Domain:', extra: null },
            5: { name: 'SSL Checker', label: 'Domain:', extra: null },
            6: { name: 'Speed Test', label: 'Website URL:', extra: null },
            7: { name: 'SQLi Test', label: 'URL with parameters:', extra: null },
            8: { name: 'XSS Test', label: 'Website URL:', extra: null },
            9: { name: 'Ping Test', label: 'Host/IP:', extra: 'Count (1-100):', extraValue: '5' },
            10: { name: 'IP Info', label: 'IP Address:', extra: null },
            11: { name: 'Hash Cracker', label: 'Hash to crack:', extra: 'Hash type (auto/MD5/SHA1):', extraValue: 'auto' },
            12: { name: 'Load Test', label: 'Your Server URL:', extra: 'Duration (seconds):', extraValue: '10' }
        };
        
        function selectTool(toolId) {
            currentTool = toolId;
            const tool = tools[toolId];
            
            // Update UI
            document.getElementById('inputLabel').textContent = tool.label;
            document.getElementById('toolName').textContent = `Tool: ${tool.name}`;
            
            // Show/hide extra input
            const extraInput = document.getElementById('extraInput');
            if (tool.extra) {
                extraInput.style.display = 'block';
                document.getElementById('extraLabel').textContent = tool.extra;
                document.getElementById('extraValue').value = tool.extraValue;
                document.getElementById('extraValue').placeholder = tool.extraValue;
            } else {
                extraInput.style.display = 'none';
            }
            
            // Clear results
            clearResults();
            
            // Update status
            updateStatus(`Selected: ${tool.name}`);
        }
        
        function quickScan(type) {
            let toolId;
            switch(type) {
                case 'port': toolId = 1; break;
                case 'dir': toolId = 2; break;
                case 'ssl': toolId = 5; break;
                case 'ip': toolId = 10; break;
            }
            selectTool(toolId);
            document.getElementById('targetInput').focus();
        }
        
        function runScan() {
            if (scanActive) return;
            
            const target = document.getElementById('targetInput').value.trim();
            if (!target) {
                updateStatus('Error: Please enter a target', 'error');
                return;
            }
            
            const extra = document.getElementById('extraValue').value;
            scanActive = true;
            scanStartTime = new Date();
            resultCount = 0;
            
            // Update UI
            updateStatus('Scanning...', 'info');
            document.getElementById('progressBar').style.width = '30%';
            clearResults();
            addResult('Starting scan...', 'info');
            
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
                    addResult(`Error: ${data.error}`, 'error');
                    updateStatus('Scan failed', 'error');
                } else {
                    displayResults(data.results);
                    updateStatus('Scan complete', 'success');
                    
                    // Update time
                    const endTime = new Date();
                    const duration = Math.round((endTime - scanStartTime) / 1000);
                    document.getElementById('scanTime').textContent = `Time: ${duration}s`;
                }
            })
            .catch(error => {
                scanActive = false;
                document.getElementById('progressBar').style.width = '0%';
                addResult(`Network error: ${error}`, 'error');
                updateStatus('Scan failed', 'error');
            });
        }
        
        function stopScan() {
            if (!scanActive) return;
            
            scanActive = false;
            document.getElementById('progressBar').style.width = '0%';
            addResult('Scan stopped by user', 'warning');
            updateStatus('Scan stopped', 'warning');
        }
        
        function displayResults(results) {
            const resultsDiv = document.getElementById('resultsContent');
            resultsDiv.innerHTML = '';
            
            if (Array.isArray(results)) {
                results.forEach(result => {
                    if (typeof result === 'object') {
                        // Table-like display for objects
                        const div = document.createElement('div');
                        div.className = 'result-item fade-in';
                        
                        let html = '';
                        for (const [key, value] of Object.entries(result)) {
                            html += `<div><strong>${key}:</strong> ${value}</div>`;
                        }
                        div.innerHTML = html;
                        resultsDiv.appendChild(div);
                    } else {
                        addResult(result, 'info');
                    }
                });
            } else if (typeof results === 'object') {
                // Single object result
                const div = document.createElement('div');
                div.className = 'result-item fade-in';
                
                let html = '';
                for (const [key, value] of Object.entries(results)) {
                    html += `<div><strong>${key}:</strong> ${value}</div>`;
                }
                div.innerHTML = html;
                resultsDiv.appendChild(div);
            } else {
                addResult(results, 'info');
            }
            
            updateResultCount();
        }
        
        function addResult(text, type = 'info') {
            resultCount++;
            const resultsDiv = document.getElementById('resultsContent');
            const div = document.createElement('div');
            div.className = `fade-in ${type}`;
            div.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
            resultsDiv.appendChild(div);
            resultsDiv.scrollTop = resultsDiv.scrollHeight;
            updateResultCount();
        }
        
        function clearResults() {
            resultCount = 0;
            document.getElementById('resultsContent').innerHTML = 'Results cleared.';
            document.getElementById('progressBar').style.width = '0%';
            document.getElementById('resultCount').textContent = '0 items';
            updateStatus('Ready', 'success');
        }
        
        function updateStatus(text, type = 'info') {
            document.getElementById('statusText').textContent = `Status: ${text}`;
            document.getElementById('statusText').className = type;
        }
        
        function updateResultCount() {
            document.getElementById('resultCount').textContent = `${resultCount} items`;
        }
        
        // Update time display
        function updateTime() {
            const now = new Date();
            const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            document.getElementById('scanTime').textContent = `Time: ${timeStr}`;
        }
        setInterval(updateTime, 1000);
        
        // Auto-select first tool on load
        window.onload = function() {
            selectTool(1);
            updateTime();
            
            // Add enter key support
            document.getElementById('targetInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') runScan();
            });
        };
    </script>
</body>
</html>'''

# ========== FAST SCANNING TOOLS ==========

class FastPortScanner:
    def __init__(self):
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 
                            445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 8888]
    
    def scan(self, target, port_range="common"):
        """Ultra-fast port scanning"""
        open_ports = []
        
        try:
            # Resolve target
            ip = socket.gethostbyname(target.split(':')[0]) if ':' not in target else target
            
            # Determine ports to scan
            if port_range == "common":
                ports = self.common_ports
            elif port_range == "top100":
                ports = list(range(1, 101))
            elif "-" in port_range:
                start, end = map(int, port_range.split("-"))
                ports = list(range(start, end + 1))
            else:
                ports = [int(p) for p in port_range.split(",") if p.isdigit()]
            
            # Fast threaded scan
            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        try:
                            sock.send(b'\r\n')
                            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()[:50]
                        except:
                            banner = ""
                        return port, banner
                    sock.close()
                except:
                    pass
                return None
            
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(check_port, port) for port in ports]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        port, banner = result
                        service = self.get_service_name(port)
                        open_ports.append({
                            "Port": port,
                            "Service": service,
                            "Status": "OPEN",
                            "Banner": banner or "No banner"
                        })
            
            return open_ports if open_ports else [{"Status": "No open ports found"}]
            
        except Exception as e:
            return [{"Error": str(e)}]
    
    def get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
            5900: "VNC", 8080: "HTTP Proxy", 8443: "HTTPS Alt", 8888: "HTTP Alt"
        }
        return services.get(port, "Unknown")

class FastDirectoryScanner:
    def __init__(self):
        self.common_paths = [
            "admin", "login", "dashboard", "wp-admin", "administrator",
            "api", "test", "backup", "config", ".env", ".git",
            "robots.txt", "sitemap.xml", "phpinfo.php", ".htaccess",
            "server-status", "wp-login.php", "admin.php", "cgi-bin",
            "debug", "dev", "staging", "old", "temp", "tmp"
        ]
    
    def scan(self, url):
        """Fast directory scanning"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            url = url.rstrip('/')
            
            # Fast parallel scanning
            def check_path(path):
                try:
                    test_url = f"{url}/{path}"
                    response = requests.head(test_url, timeout=2, verify=False, allow_redirects=True)
                    if response.status_code < 400:
                        # Get page title for GET requests that succeed
                        if response.status_code == 200:
                            try:
                                get_resp = requests.get(test_url, timeout=2, verify=False)
                                title_match = re.search(r'<title>(.*?)</title>', get_resp.text, re.IGNORECASE)
                                title = title_match.group(1)[:30] if title_match else "No title"
                            except:
                                title = "No title"
                        else:
                            title = "Redirect/Other"
                        
                        return {
                            "Path": path,
                            "URL": test_url,
                            "Status": response.status_code,
                            "Title": title
                        }
                except:
                    pass
                return None
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(check_path, path) for path in self.common_paths]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
            
            return results if results else [{"Status": "No accessible directories found"}]
            
        except Exception as e:
            return [{"Error": str(e)}]

class FastWebsiteInfo:
    def get_info(self, url):
        """Get comprehensive website information quickly"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            start_time = time.time()
            response = requests.get(url, timeout=5, verify=False)
            load_time = time.time() - start_time
            
            # Extract info
            headers = dict(response.headers)
            html = response.text
            
            # Detect CMS/Technology
            cms = self.detect_cms(html, headers)
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            title = title_match.group(1) if title_match else "No title"
            
            info = {
                "URL": url,
                "Status Code": response.status_code,
                "Load Time": f"{load_time:.2f}s",
                "Title": title[:100],
                "Server": headers.get('Server', 'Unknown'),
                "Content Type": headers.get('Content-Type', 'Unknown'),
                "Content Length": f"{len(response.content)} bytes",
                "CMS/Framework": cms,
                "IP Address": socket.gethostbyname(urlparse(url).hostname)
            }
            
            # Check security headers
            security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 
                              'X-XSS-Protection', 'Strict-Transport-Security']
            missing = [h for h in security_headers if h not in headers]
            if missing:
                info["Missing Security Headers"] = ", ".join(missing)
            
            return info
            
        except Exception as e:
            return {"Error": str(e)}
    
    def detect_cms(self, html, headers):
        """Detect CMS or framework"""
        indicators = {
            "WordPress": ["wp-content", "wp-includes", "wordpress"],
            "Joomla": ["joomla", "Joomla!", "media/system/js/"],
            "Drupal": ["Drupal", "drupal.js", "sites/all/"],
            "Magento": ["magento", "Mage.Cookies", "skin/frontend/"],
            "Laravel": ["laravel", "csrf-token", "mix-manifest.json"],
            "React": ["react", "React.createElement", "__NEXT_DATA__"],
            "Vue.js": ["vue", "Vue.config", "__vue__"],
            "Django": ["csrfmiddlewaretoken", "Django", "admin/js/"]
        }
        
        html_lower = html.lower()
        for cms, patterns in indicators.items():
            for pattern in patterns:
                if pattern.lower() in html_lower or pattern in str(headers):
                    return cms
        
        return "Unknown"

class FastHashCracker:
    def crack(self, hash_str, hash_type="auto"):
        """Fast hash cracking with common passwords"""
        common_passwords = [
            "password", "123456", "12345678", "qwerty", "abc123",
            "password1", "admin", "letmein", "welcome", "monkey",
            "dragon", "baseball", "football", "hello", "secret",
            "123123", "1234", "12345", "111111", "sunshine",
            "master", "login", "princess", "admin123", "passw0rd"
        ]
        
        try:
            # Auto-detect hash type
            if hash_type == "auto":
                if len(hash_str) == 32:
                    hash_type = "MD5"
                elif len(hash_str) == 40:
                    hash_type = "SHA1"
                elif len(hash_str) == 64:
                    hash_type = "SHA256"
                else:
                    hash_type = "MD5"  # Default
            
            # Try each password
            for password in common_passwords:
                hashed = None
                
                if hash_type.upper() == "MD5":
                    hashed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type.upper() == "SHA1":
                    hashed = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type.upper() == "SHA256":
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                
                if hashed and hashed.lower() == hash_str.lower():
                    return {
                        "Hash": hash_str,
                        "Type": hash_type,
                        "Status": "CRACKED",
                        "Password": password,
                        "Time": "Instant"
                    }
            
            return {
                "Hash": hash_str,
                "Type": hash_type,
                "Status": "NOT CRACKED",
                "Message": "Not in common password list"
            }
            
        except Exception as e:
            return {"Error": str(e)}

class FastNetworkTools:
    def ping(self, host, count=5):
        """Fast ping test"""
        try:
            ip = socket.gethostbyname(host)
            successes = 0
            times = []
            
            for i in range(int(count)):
                try:
                    start = time.time()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, 80))
                    elapsed = (time.time() - start) * 1000
                    
                    if result == 0:
                        successes += 1
                        times.append(elapsed)
                    sock.close()
                except:
                    pass
                
                if i < int(count) - 1:
                    time.sleep(0.1)
            
            if successes > 0:
                avg_time = sum(times) / len(times)
                return {
                    "Host": host,
                    "IP": ip,
                    "Status": "ONLINE",
                    "Packets Sent": count,
                    "Packets Received": successes,
                    "Success Rate": f"{(successes/int(count))*100:.1f}%",
                    "Average Time": f"{avg_time:.2f}ms",
                    "Min Time": f"{min(times):.2f}ms" if times else "N/A",
                    "Max Time": f"{max(times):.2f}ms" if times else "N/A"
                }
            else:
                return {
                    "Host": host,
                    "Status": "OFFLINE",
                    "Message": "No response received"
                }
            
        except Exception as e:
            return {"Error": str(e)}
    
    def ip_info(self, ip):
        """Fast IP information"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            info = {
                "IP Address": ip,
                "Type": "IPv4" if ip_obj.version == 4 else "IPv6",
                "Is Private": "Yes" if ip_obj.is_private else "No",
                "Is Loopback": "Yes" if ip_obj.is_loopback else "No"
            }
            
            # Try reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                info["Hostname"] = hostname
            except:
                info["Hostname"] = "Not found"
            
            # Quick geolocation
            try:
                response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    info["Country"] = data.get("country_name", "N/A")
                    info["City"] = data.get("city", "N/A")
                    info["ISP"] = data.get("org", "N/A")
            except:
                pass
            
            # Quick port check (top 5)
            common_ports = [80, 443, 22, 21, 25]
            open_ports = []
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    if sock.connect_ex((ip, port)) == 0:
                        open_ports.append(str(port))
                    sock.close()
                except:
                    pass
            
            if open_ports:
                info["Open Ports (common)"] = ", ".join(open_ports)
            
            return info
            
        except Exception as e:
            return {"Error": str(e)}

class FastSecurityScanner:
    def check_ssl(self, domain):
        """Fast SSL certificate check"""
        try:
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
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
            
            return {
                "Domain": domain,
                "Issuer": issuer.get('organizationName', 'Unknown'),
                "Expires": cert['notAfter'],
                "Days Left": days_left,
                "Status": "Valid" if days_left > 0 else "Expired",
                "Valid": "Yes" if days_left > 30 else "Warning" if days_left > 0 else "No"
            }
            
        except Exception as e:
            return {"Error": f"SSL check failed: {str(e)}"}
    
    def test_sqli(self, url):
        """Fast SQL injection test"""
        try:
            if not '?' in url:
                return {"Status": "No parameters to test"}
            
            test_payloads = ["'", "' OR '1'='1", "' OR '1'='1' --"]
            vulnerabilities = []
            
            for payload in test_payloads:
                try:
                    # Replace parameter values with payload
                    parsed = urlparse(url)
                    base = url.split('?')[0]
                    params = url.split('?')[1]
                    
                    # Test each parameter
                    for param in params.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            test_url = f"{base}?{key}={value}{payload}"
                            response = requests.get(test_url, timeout=2, verify=False)
                            
                            if any(word in response.text.lower() for word in ['sql', 'mysql', 'error', 'syntax']):
                                vulnerabilities.append(f"Parameter: {key}")
                                break
                    
                    if vulnerabilities:
                        break
                        
                except:
                    continue
            
            if vulnerabilities:
                return {
                    "Status": "VULNERABLE",
                    "Vulnerabilities": ", ".join(vulnerabilities),
                    "Risk": "High"
                }
            else:
                return {"Status": "No SQLi vulnerabilities detected"}
                
        except Exception as e:
            return {"Error": str(e)}
    
    def test_xss(self, url):
        """Fast XSS test"""
        try:
            test_payload = "<script>alert('XSS')</script>"
            
            # Check if URL has parameters
            if '?' in url:
                parsed = urlparse(url)
                base = url.split('?')[0]
                params = url.split('?')[1]
                
                for param in params.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        test_url = f"{base}?{key}={value}{test_payload}"
                        response = requests.get(test_url, timeout=2, verify=False)
                        
                        if test_payload in response.text:
                            return {
                                "Status": "VULNERABLE",
                                "Parameter": key,
                                "Risk": "Medium"
                            }
            
            return {"Status": "No XSS vulnerabilities detected"}
            
        except Exception as e:
            return {"Error": str(e)}

class FastLoadTester:
    def test(self, url, duration=10):
        """Fast load test for YOUR servers only"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            # Safety check
            if not any(allowed in url for allowed in ['localhost', '127.0.0.1', '192.168.', '10.', '172.']):
                return {
                    "Warning": "Load testing should only be performed on YOUR OWN servers.",
                    "Allowed": "Only localhost or private IP addresses",
                    "Your URL": url
                }
            
            requests_sent = 0
            errors = 0
            start_time = time.time()
            
            # Create session for connection reuse
            session = requests.Session()
            
            while time.time() - start_time < int(duration):
                try:
                    response = session.get(url, timeout=1, verify=False)
                    requests_sent += 1
                    time.sleep(0.01)  # Small delay
                except:
                    errors += 1
            
            elapsed = time.time() - start_time
            
            return {
                "Target": url,
                "Duration": f"{duration}s",
                "Requests Sent": requests_sent,
                "Errors": errors,
                "Requests/Second": f"{requests_sent/elapsed:.1f}",
                "Success Rate": f"{(requests_sent/(requests_sent+errors))*100:.1f}%" if requests_sent+errors > 0 else "0%"
            }
            
        except Exception as e:
            return {"Error": str(e)}

# ========== TOOL INSTANCES ==========
port_scanner = FastPortScanner()
dir_scanner = FastDirectoryScanner()
website_info = FastWebsiteInfo()
hash_cracker = FastHashCracker()
network_tools = FastNetworkTools()
security_scanner = FastSecurityScanner()
load_tester = FastLoadTester()

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
            results = port_scanner.scan(target, extra)
        
        # Tool 2: Directory Scanner
        elif tool_id == 2:
            results = dir_scanner.scan(target)
        
        # Tool 3: Website Info
        elif tool_id == 3:
            results = [website_info.get_info(target)]
        
        # Tool 4: WHOIS Lookup
        elif tool_id == 4:
            try:
                w = whois.whois(target)
                results = [{
                    "Domain": target,
                    "Registrar": w.registrar or "N/A",
                    "Created": str(w.creation_date) if w.creation_date else "N/A",
                    "Expires": str(w.expiration_date) if w.expiration_date else "N/A",
                    "Name Servers": ", ".join(w.name_servers)[:100] if w.name_servers else "N/A"
                }]
            except Exception as e:
                results = [{"Error": f"WHOIS failed: {str(e)}"}]
        
        # Tool 5: SSL Checker
        elif tool_id == 5:
            results = [security_scanner.check_ssl(target)]
        
        # Tool 6: Speed Test
        elif tool_id == 6:
            try:
                start = time.time()
                response = requests.get(target if target.startswith('http') else 'http://' + target, 
                                      timeout=5, verify=False)
                load_time = time.time() - start
                results = [{
                    "URL": target,
                    "Load Time": f"{load_time:.2f}s",
                    "Status": response.status_code,
                    "Size": f"{len(response.content)} bytes",
                    "Speed": f"{len(response.content)/load_time/1024:.1f} KB/s"
                }]
            except Exception as e:
                results = [{"Error": str(e)}]
        
        # Tool 7: SQLi Test
        elif tool_id == 7:
            results = [security_scanner.test_sqli(target)]
        
        # Tool 8: XSS Test
        elif tool_id == 8:
            results = [security_scanner.test_xss(target)]
        
        # Tool 9: Ping Test
        elif tool_id == 9:
            count = extra if extra and extra.isdigit() else "5"
            results = [network_tools.ping(target, count)]
        
        # Tool 10: IP Info
        elif tool_id == 10:
            results = [network_tools.ip_info(target)]
        
        # Tool 11: Hash Cracker
        elif tool_id == 11:
            hash_type = extra if extra else "auto"
            results = [hash_cracker.crack(target, hash_type)]
        
        # Tool 12: Load Test
        elif tool_id == 12:
            duration = extra if extra and extra.isdigit() else "10"
            results = [load_tester.test(target, duration)]
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Jaguar 45 Cyber Tools',
        'version': '2.0',
        'timestamp': datetime.now().isoformat()
    })

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                JAGUAR 45 - FAST CYBER TOOLS              ║
    ║                    Simple & Powerful                     ║
    ║                                                          ║
    ║    Server: http://localhost:{port}                        ║
    ║    Tools: 12 | Speed: Fast | Accuracy: High             ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
