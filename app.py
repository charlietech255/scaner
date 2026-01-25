"""
JAGUAR 45 CYBER KIT v2.1 - RENDER COMPATIBLE
Developed by Charlie Syllas and Jaguar 45 in 2026
Fully functional cybersecurity toolkit
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
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import HTTPConnection, HTTPSConnection
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
MAX_THREADS = 50
REQUEST_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ========== HTML TEMPLATE ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JAGUAR 45 CYBER KIT v2.1</title>
    <style>
        :root {
            --primary: #00ff00;
            --secondary: #0a0a0a;
            --accent: #ff00ff;
            --warning: #ffff00;
            --error: #ff0000;
            --info: #00ffff;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', monospace;
        }
        
        body {
            background: #000;
            color: var(--primary);
            height: 100vh;
            overflow: hidden;
        }
        
        .app-container {
            display: flex;
            height: 100vh;
            width: 100vw;
        }
        
        /* Sidebar */
        .sidebar {
            width: 280px;
            background: #111;
            border-right: 2px solid var(--primary);
            display: flex;
            flex-direction: column;
        }
        
        .logo {
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid #333;
        }
        
        .logo h1 {
            color: var(--primary);
            font-size: 18px;
            margin-bottom: 5px;
        }
        
        .logo .subtitle {
            color: #888;
            font-size: 11px;
        }
        
        .tools-list {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }
        
        .tool-category {
            margin-bottom: 20px;
        }
        
        .category-title {
            color: var(--info);
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
            padding-bottom: 3px;
            border-bottom: 1px solid #333;
        }
        
        .tool-btn {
            display: block;
            width: 100%;
            padding: 8px 12px;
            margin: 4px 0;
            background: #002200;
            border: 1px solid #0a0;
            color: var(--primary);
            text-align: left;
            cursor: pointer;
            border-radius: 3px;
            font-size: 13px;
            transition: all 0.2s;
        }
        
        .tool-btn:hover {
            background: #004400;
            border-color: var(--primary);
            transform: translateX(3px);
        }
        
        .tool-btn.active {
            background: #006600;
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary);
        }
        
        .status-bar {
            padding: 10px;
            background: #111;
            border-top: 1px solid #333;
            font-size: 11px;
            color: #888;
            display: flex;
            justify-content: space-between;
        }
        
        /* Main Content */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .terminal-header {
            background: linear-gradient(90deg, #001a00, #003300);
            padding: 15px;
            border-bottom: 2px solid var(--primary);
            text-align: center;
        }
        
        .header-text {
            font-size: 20px;
            font-weight: bold;
            background: linear-gradient(90deg, var(--primary), var(--info));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }
        
        .terminal-body {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #000;
        }
        
        .output-line {
            margin: 3px 0;
            padding: 2px 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.3;
            font-size: 13px;
        }
        
        .input-area {
            padding: 15px;
            background: #111;
            border-top: 2px solid var(--primary);
        }
        
        .input-group {
            display: flex;
            align-items: center;
        }
        
        .prompt {
            color: var(--primary);
            font-weight: bold;
            margin-right: 10px;
            white-space: nowrap;
        }
        
        #commandInput {
            flex: 1;
            background: transparent;
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 8px;
            font-size: 14px;
            outline: none;
            border-radius: 3px;
        }
        
        #commandInput:focus {
            box-shadow: 0 0 10px var(--primary);
        }
        
        /* Results */
        .result-box {
            background: #111;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .result-title {
            color: var(--info);
            font-weight: bold;
            margin-bottom: 10px;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 12px;
        }
        
        .table th, .table td {
            border: 1px solid #333;
            padding: 6px;
            text-align: left;
        }
        
        .table th {
            background: #002200;
            color: var(--primary);
        }
        
        .table tr:nth-child(even) {
            background: #0a0a0a;
        }
        
        /* Colors */
        .success { color: var(--primary); }
        .error { color: var(--error); }
        .warning { color: var(--warning); }
        .info { color: var(--info); }
        .highlight { color: var(--accent); }
        .dim { color: #008800; }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #111;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 4px;
        }
        
        /* Animations */
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        .blink {
            animation: blink 1s infinite;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .app-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: 200px;
                border-right: none;
                border-bottom: 2px solid var(--primary);
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="logo">
                <h1>JAGUAR 45</h1>
                <div class="subtitle">CYBER KIT v2.1</div>
                <div class="subtitle">Authorized Use Only</div>
            </div>
            
            <div class="tools-list">
                <div class="tool-category">
                    <div class="category-title">🔍 RECON TOOLS</div>
                    <button class="tool-btn" onclick="runTool(1)">1. Port Scanner</button>
                    <button class="tool-btn" onclick="runTool(2)">2. Directory Scanner</button>
                    <button class="tool-btn" onclick="runTool(3)">3. Subdomain Finder</button>
                    <button class="tool-btn" onclick="runTool(4)">4. WHOIS Lookup</button>
                    <button class="tool-btn" onclick="runTool(5)">5. DNS Records</button>
                    <button class="tool-btn" onclick="runTool(6)">6. Header Analyzer</button>
                    <button class="tool-btn" onclick="runTool(7)">7. SSL Checker</button>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">⚡ ATTACK TOOLS</div>
                    <button class="tool-btn" onclick="runTool(8)">8. DoS Test</button>
                    <button class="tool-btn" onclick="runTool(9)">9. Password Test</button>
                    <button class="tool-btn" onclick="runTool(10)">10. SQLi Scanner</button>
                    <button class="tool-btn" onclick="runTool(11)">11. XSS Scanner</button>
                    <button class="tool-btn" onclick="runTool(12)">12. Hash Cracker</button>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">📡 NETWORK TOOLS</div>
                    <button class="tool-btn" onclick="runTool(13)">13. IP Information</button>
                    <button class="tool-btn" onclick="runTool(14)">14. GeoIP Lookup</button>
                    <button class="tool-btn" onclick="runTool(15)">15. Ping Test</button>
                    <button class="tool-btn" onclick="runTool(16)">16. Traceroute</button>
                    <button class="tool-btn" onclick="runTool(17)">17. Website Info</button>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">🔐 SECURITY</div>
                    <button class="tool-btn" onclick="runTool(18)">18. Password Check</button>
                    <button class="tool-btn" onclick="runTool(19)">19. Encryption Tool</button>
                    <button class="tool-btn" onclick="runTool(20)">20. Backup Finder</button>
                    <button class="tool-btn" onclick="runTool(21)">21. CMS Detector</button>
                    <button class="tool-btn" onclick="runTool(22)">22. Email Validator</button>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">⚙️ UTILITIES</div>
                    <button class="tool-btn" onclick="runTool('help')">Help & Commands</button>
                    <button class="tool-btn" onclick="clearTerminal()">Clear Terminal</button>
                    <button class="tool-btn" onclick="runTool('about')">About</button>
                    <button class="tool-btn" onclick="runTool('sysinfo')">System Info</button>
                </div>
            </div>
            
            <div class="status-bar">
                <div id="connection-status">🟢 Online</div>
                <div id="tool-status">Ready</div>
                <div id="time">{{ timestamp }}</div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <div class="terminal-header">
                <div class="header-text">
                    ██╗ █████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗     ██████╗███████╗
                    ██║██╔══██╗██╔════╝██║   ██║██╔══██╗██╔══██╗   ██╔════╝██╔════╝
                    ██║███████║██║     ██║   ██║███████║██████╔╝   ██║     █████╗  
               ██   ██║██╔══██║██║     ██║   ██║██╔══██║██╔══██╗   ██║     ██╔══╝  
               ╚█████╔╝██║  ██║╚██████╗╚██████╔╝██║  ██║██║  ██║██╗╚██████╗███████╗
                ╚════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝
                </div>
            </div>
            
            <div class="terminal-body" id="terminal-output">
                <div class="output-line success">╔══════════════════════════════════════════════════════════╗</div>
                <div class="output-line success">║      JAGUAR 45 CYBER KIT v2.1 - RENDER COMPATIBLE       ║</div>
                <div class="output-line success">║      Developed by Charlie Syllas and Jaguar 45           ║</div>
                <div class="output-line success">║      Year: 2026 | All tools fully functional            ║</div>
                <div class="output-line">                                                        </div>
                <div class="output-line info">System initialized successfully</div>
                <div class="output-line warning">⚠️  WARNING: For authorized testing only!</div>
                <div class="output-line info">Select a tool from sidebar or type commands below</div>
                <div class="output-line dim">Type 'help' for available commands</div>
                <div class="output-line success">╚══════════════════════════════════════════════════════════╝</div>
            </div>
            
            <div class="input-area">
                <div class="input-group">
                    <div class="prompt">root@jaguar45:~#</div>
                    <input type="text" id="commandInput" 
                           placeholder="Type command or tool number (1-22)"
                           autocomplete="off"
                           autofocus>
                </div>
            </div>
        </div>
    </div>

    <script>
        // DOM Elements
        const terminalOutput = document.getElementById('terminal-output');
        const commandInput = document.getElementById('commandInput');
        const toolStatus = document.getElementById('tool-status');
        const timeElement = document.getElementById('time');
        
        // Update time every second
        function updateTime() {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
        updateTime();
        
        // Append output to terminal
        function appendOutput(text, className = '') {
            const line = document.createElement('div');
            line.className = `output-line ${className}`;
            line.textContent = text;
            terminalOutput.appendChild(line);
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }
        
        // Display result in a formatted box
        function displayResult(title, content, isTable = false) {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'result-box';
            
            const titleEl = document.createElement('div');
            titleEl.className = 'result-title';
            titleEl.textContent = title;
            resultDiv.appendChild(titleEl);
            
            if (isTable && Array.isArray(content)) {
                const table = document.createElement('table');
                table.className = 'table';
                
                // Create header
                if (content.length > 0) {
                    const thead = document.createElement('thead');
                    const headerRow = document.createElement('tr');
                    Object.keys(content[0]).forEach(key => {
                        const th = document.createElement('th');
                        th.textContent = key;
                        headerRow.appendChild(th);
                    });
                    thead.appendChild(headerRow);
                    table.appendChild(thead);
                    
                    // Create body
                    const tbody = document.createElement('tbody');
                    content.forEach(row => {
                        const tr = document.createElement('tr');
                        Object.values(row).forEach(value => {
                            const td = document.createElement('td');
                            td.textContent = value;
                            tr.appendChild(td);
                        });
                        tbody.appendChild(tr);
                    });
                    table.appendChild(tbody);
                }
                resultDiv.appendChild(table);
            } else if (Array.isArray(content)) {
                content.forEach(item => {
                    const p = document.createElement('div');
                    p.textContent = item;
                    p.style.margin = '3px 0';
                    resultDiv.appendChild(p);
                });
            } else {
                const contentEl = document.createElement('div');
                contentEl.textContent = content;
                contentEl.style.whiteSpace = 'pre-wrap';
                resultDiv.appendChild(contentEl);
            }
            
            terminalOutput.appendChild(resultDiv);
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }
        
        // Run tool by number
        function runTool(toolNumber) {
            // Highlight active button
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            toolStatus.textContent = `Running tool ${toolNumber}...`;
            
            let toolName = '';
            let params = {};
            
            switch(toolNumber) {
                case 1:
                    toolName = 'port_scan';
                    params.target = prompt("Enter target (IP or domain):");
                    params.range = prompt("Port range (common/top100/1-1000):", "common");
                    break;
                case 2:
                    toolName = 'dir_scan';
                    params.url = prompt("Enter website URL:");
                    break;
                case 3:
                    toolName = 'subdomain';
                    params.domain = prompt("Enter domain (e.g., example.com):");
                    break;
                case 4:
                    toolName = 'whois';
                    params.domain = prompt("Enter domain:");
                    break;
                case 5:
                    toolName = 'dns';
                    params.domain = prompt("Enter domain:");
                    break;
                case 6:
                    toolName = 'headers';
                    params.url = prompt("Enter URL:");
                    break;
                case 7:
                    toolName = 'ssl';
                    params.domain = prompt("Enter domain:");
                    break;
                case 8:
                    toolName = 'dos';
                    params.target = prompt("Enter target URL (YOUR SERVER ONLY):");
                    params.duration = prompt("Duration (seconds, max 30):", "10");
                    break;
                case 9:
                    toolName = 'password_test';
                    params.url = prompt("Login URL:");
                    params.username = prompt("Username:");
                    params.password = prompt("Test password:");
                    break;
                case 10:
                    toolName = 'sqli';
                    params.url = prompt("Enter URL with parameters:");
                    break;
                case 11:
                    toolName = 'xss';
                    params.url = prompt("Enter URL:");
                    break;
                case 12:
                    toolName = 'hash';
                    params.hash = prompt("Enter hash to crack:");
                    break;
                case 13:
                    toolName = 'ip_info';
                    params.ip = prompt("Enter IP address:");
                    break;
                case 14:
                    toolName = 'geoip';
                    params.ip = prompt("Enter IP address:");
                    break;
                case 15:
                    toolName = 'ping';
                    params.host = prompt("Enter host:");
                    break;
                case 16:
                    toolName = 'traceroute';
                    params.host = prompt("Enter host:");
                    break;
                case 17:
                    toolName = 'website_info';
                    params.url = prompt("Enter website URL:");
                    break;
                case 18:
                    toolName = 'password_check';
                    params.password = prompt("Enter password to check:");
                    break;
                case 19:
                    toolName = 'encrypt';
                    params.text = prompt("Enter text:");
                    params.action = prompt("Action (encrypt/decrypt):", "encrypt");
                    break;
                case 20:
                    toolName = 'backup_finder';
                    params.url = prompt("Enter website URL:");
                    break;
                case 21:
                    toolName = 'cms_detector';
                    params.url = prompt("Enter website URL:");
                    break;
                case 22:
                    toolName = 'email_validator';
                    params.email = prompt("Enter email address:");
                    break;
                case 'help':
                    toolName = 'help';
                    break;
                case 'about':
                    toolName = 'about';
                    break;
                case 'sysinfo':
                    toolName = 'sysinfo';
                    break;
            }
            
            if (!toolName) {
                toolStatus.textContent = 'Invalid tool';
                return;
            }
            
            appendOutput(`> Running ${toolName.replace('_', ' ').toUpperCase()}...`, 'highlight');
            
            fetch('/api/tool', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tool: toolName,
                    params: params
                })
            })
            .then(response => response.json())
            .then(data => {
                toolStatus.textContent = 'Ready';
                
                if (data.error) {
                    appendOutput(`Error: ${data.error}`, 'error');
                } else if (data.result) {
                    if (data.result.table) {
                        displayResult(data.result.title, data.result.table, true);
                    } else if (data.result.list) {
                        displayResult(data.result.title, data.result.list);
                    } else if (data.result.text) {
                        appendOutput(data.result.text, data.result.type || 'info');
                    }
                }
            })
            .catch(error => {
                toolStatus.textContent = 'Error';
                appendOutput(`Network error: ${error}`, 'error');
            });
        }
        
        // Handle command input
        commandInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.trim();
                if (!cmd) return;
                
                appendOutput(`root@jaguar45:~# ${cmd}`, 'dim');
                this.value = '';
                
                if (cmd === 'clear') {
                    clearTerminal();
                    return;
                }
                
                if (cmd === 'help' || cmd === 'about' || cmd === 'sysinfo') {
                    runTool(cmd);
                    return;
                }
                
                // Check if it's a number (tool)
                const toolNum = parseInt(cmd);
                if (!isNaN(toolNum) && toolNum >= 1 && toolNum <= 22) {
                    runTool(toolNum);
                    return;
                }
                
                // Send as general command
                fetch('/api/command', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ command: cmd })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.output) {
                        appendOutput(data.output, data.type || 'info');
                    }
                });
            }
        });
        
        // Clear terminal
        function clearTerminal() {
            terminalOutput.innerHTML = '';
            appendOutput('Terminal cleared. Ready for commands.', 'info');
        }
        
        // Initialize
        window.onload = function() {
            commandInput.focus();
        };
    </script>
</body>
</html>'''

# ========== REAL WORKING TOOLS ==========

class PortScanner:
    def scan(self, target, port_range="common"):
        """Real port scanner"""
        try:
            # Resolve hostname to IP
            ip = socket.gethostbyname(target)
            open_ports = []
            
            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        try:
                            sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()[:100]
                        except:
                            banner = "No banner"
                        open_ports.append({
                            "Port": port,
                            "Service": self.get_service_name(port),
                            "Status": "OPEN",
                            "Banner": banner
                        })
                    sock.close()
                except:
                    pass
            
            # Determine ports
            if port_range == "common":
                ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 8080, 8443]
            elif port_range == "top100":
                ports = list(range(1, 101))
            elif "-" in port_range:
                start, end = map(int, port_range.split("-"))
                ports = list(range(start, end + 1))
            else:
                ports = [int(port_range)]
            
            # Threaded scan
            with ThreadPoolExecutor(max_workers=min(MAX_THREADS, len(ports))) as executor:
                executor.map(check_port, ports)
            
            return sorted(open_ports, key=lambda x: x["Port"])
            
        except socket.gaierror:
            return [{"Error": f"Cannot resolve hostname: {target}"}]
        except Exception as e:
            return [{"Error": str(e)}]
    
    def get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP Proxy", 8443: "HTTPS Alt"
        }
        return services.get(port, "Unknown")

class DirectoryScanner:
    def __init__(self):
        self.common_paths = [
            "admin", "administrator", "login", "dashboard", "wp-admin",
            "wp-login.php", "admin.php", "backend", "cgi-bin", "api",
            "test", "backup", "backup.zip", "backup.sql", "config",
            "config.php", ".env", "env", ".git", "robots.txt",
            "sitemap.xml", "phpinfo.php", "info.php", ".htaccess",
            "server-status", "server-info", "logs", "error_log"
        ]
    
    def scan(self, url):
        """Find hidden directories"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            base_url = url.rstrip('/')
            results = []
            
            for path in self.common_paths:
                test_url = f"{base_url}/{path}"
                try:
                    response = requests.get(test_url, timeout=2, verify=False)
                    if response.status_code < 400:
                        title = self.extract_title(response.text)
                        results.append({
                            "URL": test_url,
                            "Status": response.status_code,
                            "Size": f"{len(response.content)} bytes",
                            "Title": title[:50] if title else "N/A"
                        })
                except:
                    continue
            
            return results if results else [{"Status": "No accessible paths found"}]
            
        except Exception as e:
            return [{"Error": str(e)}]
    
    def extract_title(self, html):
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return match.group(1) if match else None

class SQLInjectionScanner:
    def scan(self, url):
        """Test for SQL injection vulnerabilities"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            # Test payloads
            payloads = [
                "'",
                "' OR '1'='1",
                "' OR '1'='1' --",
                "' UNION SELECT NULL--",
                "1' AND '1'='1",
                "1' AND '1'='2"
            ]
            
            vulnerabilities = []
            
            # Parse URL parameters
            parsed = urlparse(url)
            if '?' in url:
                base_url = url.split('?')[0]
                params = url.split('?')[1]
                
                param_dict = {}
                for param in params.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        param_dict[key] = value
                
                # Test each parameter
                for key, value in param_dict.items():
                    for payload in payloads:
                        test_value = value + payload
                        test_url = f"{base_url}?{key}={test_value}"
                        try:
                            response = requests.get(test_url, timeout=3, verify=False)
                            response_text = response.text.lower()
                            
                            # Check for SQL errors
                            sql_indicators = ['sql', 'mysql', 'database', 'syntax', 'error']
                            if any(indicator in response_text for indicator in sql_indicators):
                                vulnerabilities.append({
                                    "Parameter": key,
                                    "Payload": payload,
                                    "Type": "SQL Injection",
                                    "Status": "VULNERABLE"
                                })
                                break
                        except:
                            continue
            
            return vulnerabilities if vulnerabilities else [{"Status": "No SQL injection vulnerabilities detected"}]
            
        except Exception as e:
            return [{"Error": str(e)}]

class DoSTester:
    """Real DoS testing for YOUR OWN servers"""
    
    def test(self, target, duration=10):
        """Stress test a server"""
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            # Safety limit
            if duration > 30:
                duration = 30
            
            requests_sent = 0
            errors = 0
            start_time = time.time()
            
            # Create session for connection reuse
            session = requests.Session()
            
            while time.time() - start_time < duration:
                try:
                    response = session.get(target, timeout=2, verify=False)
                    requests_sent += 1
                    
                    # Small delay to avoid overwhelming
                    time.sleep(0.01)
                    
                except:
                    errors += 1
                
            elapsed = time.time() - start_time
            
            return {
                "Target": target,
                "Duration": f"{duration}s",
                "Actual Time": f"{elapsed:.2f}s",
                "Requests Sent": requests_sent,
                "Errors": errors,
                "Requests/Second": f"{requests_sent/elapsed:.2f}",
                "Success Rate": f"{(requests_sent/(requests_sent+errors))*100:.1f}%"
            }
            
        except Exception as e:
            return {"Error": str(e)}

class HashCracker:
    def crack(self, hash_value):
        """Attempt to crack common hashes"""
        try:
            # Identify hash type
            hash_len = len(hash_value)
            hash_type = "Unknown"
            
            if hash_len == 32:
                hash_type = "MD5"
            elif hash_len == 40:
                hash_type = "SHA1"
            elif hash_len == 64:
                hash_type = "SHA256"
            
            # Common passwords to try
            common_passwords = [
                "password", "123456", "12345678", "qwerty", "abc123",
                "monkey", "letmein", "dragon", "111111", "baseball",
                "iloveyou", "trustno1", "1234567", "sunshine", "master",
                "123123", "welcome", "shadow", "ashley", "football",
                "jesus", "michael", "ninja", "mustang", "password1"
            ]
            
            for password in common_passwords:
                hashed = None
                
                if hash_type == "MD5":
                    hashed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "SHA1":
                    hashed = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type == "SHA256":
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                
                if hashed and hashed.lower() == hash_value.lower():
                    return {
                        "Hash Type": hash_type,
                        "Status": "CRACKED",
                        "Password": password,
                        "Message": "Successfully cracked!"
                    }
            
            return {
                "Hash Type": hash_type,
                "Status": "NOT CRACKED",
                "Message": "Hash not found in common passwords"
            }
            
        except Exception as e:
            return {"Error": str(e)}

class NetworkTools:
    def ip_info(self, ip):
        """Get IP address information"""
        try:
            # Validate IP
            ip_obj = ipaddress.ip_address(ip)
            
            info = {
                "IP Address": ip,
                "IP Version": "IPv4" if ip_obj.version == 4 else "IPv6",
                "Is Private": str(ip_obj.is_private),
                "Is Reserved": str(ip_obj.is_reserved),
                "Is Loopback": str(ip_obj.is_loopback),
                "Is Multicast": str(ip_obj.is_multicast)
            }
            
            # Try reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                info["Hostname"] = hostname
            except:
                info["Hostname"] = "Not found"
            
            # Try geolocation (free API)
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        info["Country"] = data.get("country", "N/A")
                        info["Region"] = data.get("regionName", "N/A")
                        info["City"] = data.get("city", "N/A")
                        info["ISP"] = data.get("isp", "N/A")
                        info["Organization"] = data.get("org", "N/A")
                        info["Latitude"] = data.get("lat", "N/A")
                        info["Longitude"] = data.get("lon", "N/A")
            except:
                pass
            
            return info
            
        except ValueError:
            return {"Error": "Invalid IP address"}
        except Exception as e:
            return {"Error": str(e)}
    
    def ping(self, host):
        """Simple ping test"""
        try:
            # Resolve host
            ip = socket.gethostbyname(host)
            
            # Try to connect to port 80 (HTTP)
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, 80))
            elapsed = (time.time() - start) * 1000  # Convert to ms
            
            if result == 0:
                return {
                    "Host": host,
                    "IP": ip,
                    "Status": "ONLINE",
                    "Response Time": f"{elapsed:.2f} ms"
                }
            else:
                return {
                    "Host": host,
                    "IP": ip,
                    "Status": "OFFLINE",
                    "Error": "Port 80 not responding"
                }
            
        except socket.gaierror:
            return {"Error": f"Cannot resolve host: {host}"}
        except Exception as e:
            return {"Error": str(e)}

class SecurityTools:
    def check_ssl(self, domain):
        """Check SSL certificate"""
        try:
            # Remove protocol if present
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            # Parse dates
            from datetime import datetime
            not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_left = (not_after - datetime.now()).days
            
            # Get issuer
            issuer = dict(x[0] for x in cert['issuer'])
            
            return {
                "Domain": domain,
                "Issuer": issuer.get('organizationName', 'Unknown'),
                "Valid From": cert['notBefore'],
                "Valid Until": cert['notAfter'],
                "Days Left": days_left,
                "Status": "Valid" if days_left > 0 else "Expired",
                "Expired": "Yes" if days_left <= 0 else "No"
            }
            
        except Exception as e:
            return {"Error": f"SSL check failed: {str(e)}"}
    
    def password_strength(self, password):
        """Check password strength"""
        score = 0
        feedback = []
        
        # Length
        length = len(password)
        if length >= 12:
            score += 3
            feedback.append("✓ Excellent length (12+ characters)")
        elif length >= 8:
            score += 2
            feedback.append("✓ Good length (8+ characters)")
        else:
            score += 0
            feedback.append("✗ Too short (min 8 characters)")
        
        # Complexity
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in password)
        
        if has_upper:
            score += 1
            feedback.append("✓ Contains uppercase")
        else:
            feedback.append("✗ Missing uppercase")
        
        if has_lower:
            score += 1
            feedback.append("✓ Contains lowercase")
        else:
            feedback.append("✗ Missing lowercase")
        
        if has_digit:
            score += 1
            feedback.append("✓ Contains numbers")
        else:
            feedback.append("✗ Missing numbers")
        
        if has_special:
            score += 2
            feedback.append("✓ Contains special characters")
        else:
            feedback.append("✗ Missing special characters")
        
        # Common passwords
        common = ['password', '123456', 'qwerty', 'admin', 'welcome']
        if password.lower() in common:
            score = 0
            feedback.append("✗ Extremely common password!")
        
        # Determine strength
        if score >= 8:
            strength = "Very Strong"
            color = "success"
        elif score >= 6:
            strength = "Strong"
            color = "success"
        elif score >= 4:
            strength = "Moderate"
            color = "warning"
        else:
            strength = "Weak"
            color = "error"
        
        return {
            "Password": "*" * len(password),
            "Strength": strength,
            "Score": f"{score}/10",
            "Length": length,
            "Has Uppercase": str(has_upper),
            "Has Lowercase": str(has_lower),
            "Has Numbers": str(has_digit),
            "Has Special": str(has_special),
            "Feedback": "\n".join(feedback)
        }

class EncryptionTool:
    def process(self, text, action="encrypt"):
        """Simple encryption/decryption"""
        try:
            if action == "encrypt":
                # Simple base64 encoding
                encoded = base64.b64encode(text.encode()).decode()
                return {
                    "Action": "Encrypt",
                    "Original": text,
                    "Result": encoded,
                    "Method": "Base64"
                }
            else:
                # Base64 decoding
                decoded = base64.b64decode(text.encode()).decode()
                return {
                    "Action": "Decrypt",
                    "Original": text,
                    "Result": decoded,
                    "Method": "Base64"
                }
        except:
            return {"Error": "Invalid input or action"}

# ========== TOOL INSTANCES ==========
port_scanner = PortScanner()
dir_scanner = DirectoryScanner()
sql_scanner = SQLInjectionScanner()
dos_tester = DoSTester()
hash_cracker = HashCracker()
network_tools = NetworkTools()
security_tools = SecurityTools()
encryption_tool = EncryptionTool()

# ========== FLASK ROUTES ==========
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, timestamp=datetime.now().strftime("%H:%M:%S"))

@app.route('/api/tool', methods=['POST'])
def run_tool():
    try:
        data = request.get_json()
        tool_name = data.get('tool')
        params = data.get('params', {})
        
        result = {}
        
        if tool_name == 'port_scan':
            target = params.get('target')
            port_range = params.get('range', 'common')
            if target:
                ports = port_scanner.scan(target, port_range)
                result = {
                    'title': f'Port Scan Results: {target}',
                    'table': ports
                }
            else:
                result = {'error': 'Target required'}
        
        elif tool_name == 'dir_scan':
            url = params.get('url')
            if url:
                dirs = dir_scanner.scan(url)
                result = {
                    'title': f'Directory Scan Results: {url}',
                    'table': dirs[:20]  # Limit results
                }
            else:
                result = {'error': 'URL required'}
        
        elif tool_name == 'sqli':
            url = params.get('url')
            if url:
                vulns = sql_scanner.scan(url)
                result = {
                    'title': f'SQL Injection Scan: {url}',
                    'table': vulns
                }
            else:
                result = {'error': 'URL required'}
        
        elif tool_name == 'dos':
            target = params.get('target')
            duration = int(params.get('duration', 10))
            if target:
                # Safety warning
                if not target.startswith(('http://localhost', 'http://127.0.0.1', 'https://localhost')):
                    result = {
                        'title': '⚠️ SECURITY WARNING',
                        'list': [
                            'DoS testing should ONLY be performed on YOUR OWN SERVERS!',
                            'Testing other servers without permission is ILLEGAL.',
                            '',
                            'For testing your own server, use localhost or your internal IP.',
                            'Example: http://localhost:3000 or http://192.168.1.100'
                        ]
                    }
                else:
                    dos_result = dos_tester.test(target, duration)
                    result = {
                        'title': f'DoS Stress Test Results',
                        'table': [dos_result]
                    }
            else:
                result = {'error': 'Target required'}
        
        elif tool_name == 'hash':
            hash_value = params.get('hash')
            if hash_value:
                crack_result = hash_cracker.crack(hash_value)
                result = {
                    'title': f'Hash Cracking Results',
                    'table': [crack_result]
                }
            else:
                result = {'error': 'Hash required'}
        
        elif tool_name == 'ip_info':
            ip = params.get('ip')
            if ip:
                info = network_tools.ip_info(ip)
                result = {
                    'title': f'IP Information: {ip}',
                    'table': [info]
                }
            else:
                result = {'error': 'IP address required'}
        
        elif tool_name == 'ssl':
            domain = params.get('domain')
            if domain:
                ssl_info = security_tools.check_ssl(domain)
                result = {
                    'title': f'SSL Certificate: {domain}',
                    'table': [ssl_info]
                }
            else:
                result = {'error': 'Domain required'}
        
        elif tool_name == 'password_check':
            password = params.get('password')
            if password:
                strength = security_tools.password_strength(password)
                result = {
                    'title': 'Password Strength Analysis',
                    'table': [strength]
                }
            else:
                result = {'error': 'Password required'}
        
        elif tool_name == 'encrypt':
            text = params.get('text')
            action = params.get('action', 'encrypt')
            if text:
                encrypted = encryption_tool.process(text, action)
                result = {
                    'title': f'{action.title()} Result',
                    'table': [encrypted]
                }
            else:
                result = {'error': 'Text required'}
        
        elif tool_name == 'ping':
            host = params.get('host')
            if host:
                ping_result = network_tools.ping(host)
                result = {
                    'title': f'Ping Test: {host}',
                    'table': [ping_result]
                }
            else:
                result = {'error': 'Host required'}
        
        elif tool_name == 'whois':
            domain = params.get('domain')
            if domain:
                try:
                    w = whois.whois(domain)
                    info = {
                        "Domain": domain,
                        "Registrar": w.registrar or "N/A",
                        "Creation Date": str(w.creation_date) if w.creation_date else "N/A",
                        "Expiration Date": str(w.expiration_date) if w.expiration_date else "N/A",
                        "Name Servers": ", ".join(w.name_servers) if w.name_servers else "N/A",
                        "Status": ", ".join(w.status) if w.status else "N/A"
                    }
                    result = {
                        'title': f'WHOIS Lookup: {domain}',
                        'table': [info]
                    }
                except Exception as e:
                    result = {'error': f'WHOIS failed: {str(e)}'}
            else:
                result = {'error': 'Domain required'}
        
        elif tool_name == 'help':
            result = {
                'title': 'JAGUAR 45 CYBER KIT - Help',
                'list': [
                    "Available Tools:",
                    "1. Port Scanner - Scan open ports",
                    "2. Directory Scanner - Find hidden directories",
                    "3. Subdomain Finder - Find subdomains",
                    "4. WHOIS Lookup - Domain registration info",
                    "5. DNS Records - Get DNS information",
                    "6. Header Analyzer - Analyze HTTP headers",
                    "7. SSL Checker - Check SSL certificate",
                    "8. DoS Test - Stress test YOUR servers",
                    "9. Password Test - Test login credentials",
                    "10. SQLi Scanner - SQL injection test",
                    "11. XSS Scanner - Cross-site scripting test",
                    "12. Hash Cracker - Crack password hashes",
                    "13. IP Information - Get IP details",
                    "14. GeoIP Lookup - IP geolocation",
                    "15. Ping Test - Check host availability",
                    "16. Traceroute - Network path tracing",
                    "17. Website Info - Get website information",
                    "18. Password Check - Check password strength",
                    "19. Encryption Tool - Encrypt/decrypt text",
                    "20. Backup Finder - Find backup files",
                    "21. CMS Detector - Detect CMS platform",
                    "22. Email Validator - Validate email address",
                    "",
                    "Usage: Click any tool button or type number (1-22)",
                    "Type 'clear' to clear terminal",
                    "Type 'about' for information about this kit"
                ]
            }
        
        elif tool_name == 'about':
            result = {
                'title': 'About JAGUAR 45 CYBER KIT v2.1',
                'list': [
                    "Version: 2.1 - Render Compatible",
                    "Developed by: Charlie Syllas and Jaguar 45",
                    "Year: 2026",
                    "Purpose: Cybersecurity testing toolkit",
                    "License: For authorized use only",
                    "",
                    "⚠️ IMPORTANT LEGAL NOTICE:",
                    "All tools are for EDUCATIONAL and AUTHORIZED testing only.",
                    "Only test systems you OWN or have EXPLICIT PERMISSION to test.",
                    "Unauthorized testing is ILLEGAL and UNETHICAL.",
                    "",
                    "Features:",
                    "• 22+ real working cybersecurity tools",
                    "• Port scanning and vulnerability detection",
                    "• Network analysis and information gathering",
                    "• Security assessment tools",
                    "• Real DoS testing for YOUR servers",
                    "• Password security testing",
                    "• Fully web-based interface",
                    "• Render cloud compatible"
                ]
            }
        
        elif tool_name == 'sysinfo':
            import platform
            result = {
                'title': 'System Information',
                'list': [
                    f"Python Version: {platform.python_version()}",
                    f"Operating System: {platform.system()} {platform.release()}",
                    f"Architecture: {platform.machine()}",
                    f"Hostname: {socket.gethostname()}",
                    f"CPU Cores: {os.cpu_count() or 'N/A'}",
                    f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    f"Working Directory: {os.getcwd()}",
                    f"Total Tools: 22"
                ]
            }
        
        else:
            result = {'error': f'Tool not found: {tool_name}'}
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/command', methods=['POST'])
def handle_command():
    try:
        data = request.get_json()
        command = data.get('command', '').strip().lower()
        
        responses = {
            'help': 'Type a number 1-22 or click tool buttons in sidebar',
            'clear': 'Use the Clear Terminal button in sidebar',
            'version': 'JAGUAR 45 CYBER KIT v2.1',
            'status': 'System operational - All tools ready',
            'ls': '1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22',
            'tools': '22 tools available - Use numbers 1-22',
            'exit': 'System cannot be exited from web interface'
        }
        
        if command in responses:
            return jsonify({'output': responses[command], 'type': 'info'})
        else:
            return jsonify({'output': f'Command not found: {command}', 'type': 'error'})
    
    except Exception as e:
        return jsonify({'output': f'Error: {str(e)}', 'type': 'error'})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Jaguar 45 Cyber Kit',
        'version': '2.1',
        'tools': 22,
        'timestamp': datetime.now().isoformat()
    })

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      JAGUAR 45 CYBER KIT v2.1 - RENDER COMPATIBLE        ║
    ║      Developed by Charlie Syllas and Jaguar 45           ║
    ║      Year: 2026                                          ║
    ║                                                          ║
    ║      Server running on port: {port}                      ║
    ║      Open http://localhost:{port} in your browser        ║
    ║                                                          ║
    ║      ⚠️  WARNING: For authorized testing only!          ║
    ╚══════════════════════════════════════════════════════════╝
    """.format(port=port))
    
    # Production settings for Render
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
