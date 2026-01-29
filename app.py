"""
JAGUAR 45 CYBER KIT - 30 REAL TOOLS
All tools work in real-time, no simulations
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
import subprocess
import uuid
import base64
import hashlib
import hmac
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, quote, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import HTTPConnection, HTTPSConnection
import mimetypes

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
MAX_THREADS = 200
REQUEST_TIMEOUT = 3
USER_AGENT = "Jaguar45-Scanner/3.0"
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "admin", "letmein", "welcome", "monkey",
    "dragon", "baseball", "football", "hello", "secret",
    "123123", "1234", "12345", "111111", "sunshine",
    "master", "login", "princess", "admin123", "passw0rd",
    "shadow", "ashley", "michael", "jordan", "superman",
    "harley", "thomas", "robert", "hunter", "buster",
    "soccer", "tigger", "batman", "test", "pass",
    "killer", "hockey", "george", "charlie", "andrew",
    "michelle", "love", "jessica", "pepper", "daniel"
]

# ========== HTML TEMPLATE (SAME AS BEFORE) ==========
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
            <div class="subtitle">30 Real Tools • No Simulations • Fast Results</div>
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
            <button class="tool-btn" onclick="selectTool(13)">🌍 Subdomain</button>
            <button class="tool-btn" onclick="selectTool(14)">📡 DNS Records</button>
            <button class="tool-btn" onclick="selectTool(15)">🛡️ Headers Check</button>
            <button class="tool-btn" onclick="selectTool(16)">📤 Upload Test</button>
            <button class="tool-btn" onclick="selectTool(17)">🔄 CORS Test</button>
            <button class="tool-btn" onclick="selectTool(18)">🎯 CRLF Test</button>
            <button class="tool-btn" onclick="selectTool(19)">↪️ Redirect Test</button>
            <button class="tool-btn" onclick="selectTool(20)">🏗️ CMS Detect</button>
            <button class="tool-btn" onclick="selectTool(21)">🔗 SSRF Test</button>
            <button class="tool-btn" onclick="selectTool(22)">📧 Email Verify</button>
            <button class="tool-btn" onclick="selectTool(23)">🔐 JWT Test</button>
            <button class="tool-btn" onclick="selectTool(24)">📊 HTTP Methods</button>
            <button class="tool-btn" onclick="selectTool(25)">📜 Backup Find</button>
            <button class="tool-btn" onclick="selectTool(26)">💾 Git Exposed</button>
            <button class="tool-btn" onclick="selectTool(27)">📝 Robots Check</button>
            <button class="tool-btn" onclick="selectTool(28)">🔍 Shodan Lookup</button>
            <button class="tool-btn" onclick="selectTool(29)">🛡️ Firewall Test</button>
            <button class="tool-btn" onclick="selectTool(30)">🌐 Cloudflare Check</button>
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
$ 30 real working tools available
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
                 extra: true, extraLabel: 'Duration (sec):', extraPlaceholder: '10' },
            13: { name: 'Subdomain Scan', label: 'Domain:', 
                 extra: false },
            14: { name: 'DNS Records', label: 'Domain:', 
                 extra: false },
            15: { name: 'Headers Check', label: 'Website URL:', 
                 extra: false },
            16: { name: 'Upload Test', label: 'Upload URL:', 
                 extra: true, extraLabel: 'File name:', extraPlaceholder: 'test.php' },
            17: { name: 'CORS Test', label: 'API URL:', 
                 extra: false },
            18: { name: 'CRLF Test', label: 'Website URL:', 
                 extra: false },
            19: { name: 'Redirect Test', label: 'URL with redirect:', 
                 extra: false },
            20: { name: 'CMS Detect', label: 'Website URL:', 
                 extra: false },
            21: { name: 'SSRF Test', label: 'Your Server URL:', 
                 extra: true, extraLabel: 'Test URL:', extraPlaceholder: 'http://localhost' },
            22: { name: 'Email Verify', label: 'Email address:', 
                 extra: false },
            23: { name: 'JWT Test', label: 'JWT Token:', 
                 extra: true, extraLabel: 'Secret key:', extraPlaceholder: 'optional' },
            24: { name: 'HTTP Methods', label: 'Website URL:', 
                 extra: false },
            25: { name: 'Backup Find', label: 'Website URL:', 
                 extra: false },
            26: { name: 'Git Exposed', label: 'Website URL:', 
                 extra: false },
            27: { name: 'Robots Check', label: 'Website URL:', 
                 extra: false },
            28: { name: 'Shodan Lookup', label: 'IP or Domain:', 
                 extra: false },
            29: { name: 'Firewall Test', label: 'Website URL:', 
                 extra: false },
            30: { name: 'Cloudflare Check', label: 'Website URL:', 
                 extra: false }
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
            addOutput('$ Jaguar 45 Cyber Scanner v3.0', 'cyan');
            addOutput('$ 30 real working tools loaded', 'green');
            addOutput('$ Select tool and enter target', 'gray');
        };
    </script>
</body>
</html>'''

# ========== REAL WORKING TOOLS ==========

class RealWorkingTools:
    def __init__(self):
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                            993, 995, 3306, 3389, 5432, 5900, 8080, 8443, 8888]
        self.common_subdomains = [
            "www", "mail", "ftp", "smtp", "pop", "imap", "webmail",
            "admin", "blog", "dev", "test", "staging", "api",
            "secure", "vpn", "portal", "download", "cdn", "static",
            "shop", "store", "forum", "support", "help", "docs"
        ]
    
    # ========== EXISTING TOOLS ==========
    
    def port_scan(self, target, port_range="common"):
        results = []
        open_count = 0
        
        try:
            ip = socket.gethostbyname(target.split(':')[0]) if ':' not in target else target
            
            if port_range == "common":
                ports = self.common_ports
            elif port_range == "top100":
                ports = list(range(1, 101))
            elif "-" in port_range:
                start, end = map(int, port_range.split("-"))
                ports = list(range(start, end + 1))
                if len(ports) > 1000:
                    ports = ports[:1000]
            else:
                ports = [int(p) for p in port_range.split(",") if p.isdigit()][:100]
            
            results.append(f"Scanning {target} ({ip})")
            results.append(f"Ports to scan: {len(ports)}")
            results.append("=" * 50)
            
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
    
    def dir_scan(self, url):
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
                "server-status", "wp-login.php", "admin.php", "cgi-bin",
                "upload", "uploads", "images", "files", "download"
            ]
            
            results.append(f"Scanning: {url}")
            results.append(f"Checking {len(paths)} paths")
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
            
            # Get IP
            try:
                hostname = urlparse(url).hostname
                ip = socket.gethostbyname(hostname)
                results.append(f"IP Address:     {ip}")
            except:
                results.append(f"IP Address:     Could not resolve")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ssl_check(self, domain):
        results = []
        
        try:
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
            results.append(f"Domain:         {domain}")
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            from datetime import datetime
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_left = (not_after - datetime.now()).days
            
            issuer = dict(x[0] for x in cert['issuer'])
            
            results.append(f"Issuer:         {issuer.get('organizationName', 'Unknown')}")
            results.append(f"Valid Until:    {cert['notAfter']}")
            results.append(f"Days Left:      {days_left}")
            
            if days_left > 30:
                results.append(f"Status:         VALID ({days_left} days)")
            elif days_left > 0:
                results.append(f"Status:         WARNING ({days_left} days)")
            else:
                results.append(f"Status:         EXPIRED")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def whois_lookup(self, domain):
        results = []
        
        try:
            w = whois.whois(domain)
            
            results.append(f"Domain:         {domain}")
            results.append(f"Registrar:      {w.registrar or 'Unknown'}")
            
            if w.creation_date:
                results.append(f"Created:        {w.creation_date}")
            
            if w.expiration_date:
                results.append(f"Expires:        {w.expiration_date}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def speed_test(self, url):
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"Testing:        {url}")
            
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
            avg_speed = (sum(sizes) / sum(times)) / 1024
            
            results.append(f"Load Time:      {avg_time:.2f}s (avg)")
            results.append(f"Speed:          {avg_speed:.1f} KB/s")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def sqli_test(self, url):
        results = []
        
        try:
            if '?' not in url:
                return ["ERROR: URL must have parameters"]
            
            results.append(f"Testing:        {url}")
            
            test_payloads = ["'", "' OR '1'='1", "' OR '1'='1' --"]
            vulnerable = False
            
            for payload in test_payloads:
                try:
                    parsed = urlparse(url)
                    base = url.split('?')[0]
                    params = url.split('?')[1]
                    
                    for param in params.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            test_url = f"{base}?{key}={value}{payload}"
                            response = requests.get(test_url, timeout=2, verify=False)
                            
                            if any(word in response.text.lower() for word in ['sql', 'mysql', 'error', 'syntax']):
                                vulnerable = True
                                results.append(f"VULNERABLE:     Parameter '{key}'")
                                break
                    
                    if vulnerable:
                        break
                        
                except:
                    continue
            
            if not vulnerable:
                results.append(f"Result:         No SQLi detected")
            else:
                results.append(f"Risk Level:     HIGH")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def xss_test(self, url):
        results = []
        
        try:
            results.append(f"Testing:        {url}")
            
            payload = "<script>alert('xss')</script>"
            
            if '?' in url:
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
            
            test_url = f"{url}?test={payload}"
            response = requests.get(test_url, timeout=2, verify=False)
            
            if payload in response.text:
                results.append(f"VULNERABLE:     Reflected XSS")
            else:
                results.append(f"Result:         No XSS detected")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ping_test(self, host, count="5"):
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
                        results.append(f"Reply: {elapsed:.1f}ms")
                    else:
                        results.append(f"Timeout")
                    
                except:
                    results.append(f"Failed")
                
                if i < count - 1:
                    time.sleep(0.5)
            
            results.append("-" * 50)
            results.append(f"Packets:        {count} sent, {successes} received")
            
            if successes > 0:
                avg_time = sum(times) / len(times)
                results.append(f"Average:        {avg_time:.1f}ms")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ip_info(self, ip):
        results = []
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            results.append(f"IP Address:     {ip}")
            results.append(f"IP Version:     IPv{ip_obj.version}")
            results.append(f"Private:        {'Yes' if ip_obj.is_private else 'No'}")
            
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                results.append(f"Hostname:       {hostname}")
            except:
                results.append(f"Hostname:       Not found")
            
            return results
            
        except ValueError:
            return ["ERROR: Invalid IP address"]
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def hash_crack(self, hash_str, hash_type="auto"):
        results = []
        
        try:
            results.append(f"Hash:           {hash_str}")
            
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
            
            found = False
            for pwd in COMMON_PASSWORDS:
                hashed = None
                
                if hash_type.upper() == "MD5":
                    hashed = hashlib.md5(pwd.encode()).hexdigest()
                elif hash_type.upper() == "SHA1":
                    hashed = hashlib.sha1(pwd.encode()).hexdigest()
                elif hash_type.upper() == "SHA256":
                    hashed = hashlib.sha256(pwd.encode()).hexdigest()
                
                if hashed and hashed.lower() == hash_str.lower():
                    results.append(f"CRACKED:        {pwd}")
                    results.append(f"Status:         Success!")
                    found = True
                    break
            
            if not found:
                results.append(f"Result:         Not in common list")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def load_test(self, url, duration="10"):
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            # Safety check
            parsed = urlparse(url)
            hostname = parsed.hostname
            
            if not any(x in hostname for x in ['localhost', '127.0.0.1', '192.168.', '10.', '172.']):
                results.append("WARNING: Only test YOUR servers")
                results.append(f"Target: {url}")
                return results
            
            duration = int(duration) if duration.isdigit() else 10
            if duration > 30:
                duration = 30
            
            results.append(f"Target:         {url}")
            results.append(f"Duration:       {duration}s")
            
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
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    # ========== NEW TOOLS ==========
    
    def subdomain_scan(self, domain):
        """Find subdomains"""
        results = []
        
        try:
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
            results.append(f"Domain:         {domain}")
            results.append(f"Checking {len(self.common_subdomains)} subdomains")
            results.append("=" * 50)
            
            found = 0
            
            def check_subdomain(sub):
                try:
                    test_domain = f"{sub}.{domain}"
                    ip = socket.gethostbyname(test_domain)
                    return sub, ip, True
                except:
                    return sub, None, False
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(check_subdomain, sub) for sub in self.common_subdomains]
                for future in as_completed(futures):
                    sub, ip, found_flag = future.result()
                    if found_flag:
                        found += 1
                        results.append(f"FOUND   {sub}.{domain:<20} [{ip}]")
            
            results.append("=" * 50)
            results.append(f"Found {found} subdomains")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def dns_records(self, domain):
        """Get DNS records"""
        results = []
        
        try:
            domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
            
            results.append(f"Domain:         {domain}")
            results.append("=" * 50)
            
            # A records
            try:
                answers = dns.resolver.resolve(domain, 'A')
                for rdata in answers:
                    results.append(f"A Record:       {rdata.address}")
            except:
                pass
            
            # MX records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    results.append(f"MX Record:      {rdata.exchange} (pri:{rdata.preference})")
            except:
                pass
            
            # TXT records
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    for txt in rdata.strings:
                        results.append(f"TXT Record:     {txt.decode()[:50]}")
            except:
                pass
            
            # NS records
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                for rdata in answers:
                    results.append(f"NS Record:      {rdata.target}")
            except:
                pass
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def headers_check(self, url):
        """Check security headers"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            response = requests.get(url, timeout=5, verify=False)
            
            results.append(f"URL:            {url}")
            results.append(f"Status:         {response.status_code}")
            results.append("=" * 50)
            
            security_headers = {
                'X-Frame-Options': 'Prevents clickjacking',
                'X-Content-Type-Options': 'Prevents MIME sniffing',
                'X-XSS-Protection': 'XSS protection',
                'Strict-Transport-Security': 'Enforces HTTPS',
                'Content-Security-Policy': 'Prevents XSS/injection',
                'Referrer-Policy': 'Controls referrer info'
            }
            
            for header, description in security_headers.items():
                if header in response.headers:
                    results.append(f"✓ {header:<25} {response.headers[header][:50]}")
                else:
                    results.append(f"✗ {header:<25} MISSING")
            
            results.append("=" * 50)
            
            # Check cookies
            if 'Set-Cookie' in response.headers:
                cookie = response.headers['Set-Cookie']
                if 'HttpOnly' in cookie:
                    results.append(f"✓ Cookies:       HttpOnly flag present")
                else:
                    results.append(f"✗ Cookies:       HttpOnly flag missing")
                
                if 'Secure' in cookie:
                    results.append(f"✓ Cookies:       Secure flag present")
                else:
                    results.append(f"✗ Cookies:       Secure flag missing")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def upload_test(self, url, filename="test.php"):
        """Test file upload vulnerability"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"Testing:        {url}")
            results.append(f"File:           {filename}")
            results.append("=" * 50)
            
            # Try simple POST with file
            files = {'file': (filename, b'<?php echo "test"; ?>', 'application/x-php')}
            
            try:
                response = requests.post(url, files=files, timeout=5, verify=False)
                results.append(f"Status:         {response.status_code}")
                
                if response.status_code in [200, 201, 301, 302]:
                    results.append(f"Result:         Upload endpoint may be accessible")
                    
                    # Check if file was uploaded
                    upload_url = f"{url.rstrip('/')}/uploads/{filename}"
                    check_response = requests.head(upload_url, timeout=3, verify=False)
                    
                    if check_response.status_code == 200:
                        results.append(f"WARNING:        File may be accessible at {upload_url}")
                    else:
                        results.append(f"Info:           Uploaded file not directly accessible")
                else:
                    results.append(f"Result:         Upload not successful")
            
            except Exception as e:
                results.append(f"Error:          {str(e)}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def cors_test(self, url):
        """Test CORS misconfiguration"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"Testing:        {url}")
            results.append("=" * 50)
            
            # Test with Origin header
            headers = {
                'Origin': 'https://evil.com',
                'User-Agent': USER_AGENT
            }
            
            response = requests.get(url, headers=headers, timeout=5, verify=False)
            
            # Check CORS headers
            if 'Access-Control-Allow-Origin' in response.headers:
                origin = response.headers['Access-Control-Allow-Origin']
                results.append(f"CORS Header:    {origin}")
                
                if origin == '*':
                    results.append(f"VULNERABLE:     CORS misconfigured (wildcard)")
                    results.append(f"Risk:           HIGH - Any domain can access")
                elif 'evil.com' in origin:
                    results.append(f"VULNERABLE:     CORS reflects origin")
                    results.append(f"Risk:           MEDIUM")
                else:
                    results.append(f"Secure:         CORS properly configured")
            else:
                results.append(f"No CORS headers detected")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def crlf_test(self, url):
        """Test CRLF injection"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"Testing:        {url}")
            results.append("=" * 50)
            
            # Test CRLF injection
            test_url = f"{url}?test=%0d%0aX-Injected-Header: test"
            response = requests.get(test_url, timeout=5, verify=False)
            
            # Check if header was injected
            headers_str = str(response.headers).lower()
            
            if 'x-injected-header' in headers_str:
                results.append(f"VULNERABLE:     CRLF injection possible")
                results.append(f"Risk:           MEDIUM - Header injection")
            else:
                results.append(f"Secure:         No CRLF injection detected")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def redirect_test(self, url):
        """Test open redirect vulnerability"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"Testing:        {url}")
            results.append("=" * 50)
            
            # Common redirect parameters
            redirect_params = ['url', 'redirect', 'next', 'return', 'r', 'u']
            
            # Check if URL has parameters
            parsed = urlparse(url)
            if parsed.query:
                params = parse_qs(parsed.query)
                
                for param in redirect_params:
                    if param in params:
                        results.append(f"Found param:    {param}")
                        
                        # Test with external URL
                        test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{param}=https://evil.com"
                        response = requests.get(test_url, timeout=5, verify=False, allow_redirects=False)
                        
                        if response.status_code in [301, 302, 303, 307, 308]:
                            location = response.headers.get('Location', '')
                            if 'evil.com' in location:
                                results.append(f"VULNERABLE:     Open redirect via {param}")
                                results.append(f"Risk:           MEDIUM")
                                break
            
            if len(results) <= 2:  # Only header lines
                results.append(f"No redirect parameters found")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def cms_detect(self, url):
        """Detect CMS/Framework"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            response = requests.get(url, timeout=5, verify=False)
            
            results.append(f"URL:            {url}")
            results.append(f"Status:         {response.status_code}")
            results.append("=" * 50)
            
            html = response.text.lower()
            headers = str(response.headers).lower()
            
            cms_indicators = {
                'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
                'Joomla': ['joomla', 'media/system/js/', 'joomla.css'],
                'Drupal': ['drupal', 'sites/all/', 'drupal.js'],
                'Magento': ['magento', 'skin/frontend/', 'mage/cookies'],
                'Laravel': ['laravel', 'csrf-token', 'mix-manifest.json'],
                'React': ['react', 'react-dom', '__next_data__'],
                'Vue.js': ['vue', 'vue.js', '__vue__'],
                'Django': ['django', 'csrfmiddlewaretoken', 'admin/js/']
            }
            
            detected = []
            
            for cms, indicators in cms_indicators.items():
                for indicator in indicators:
                    if indicator in html or indicator in headers:
                        detected.append(cms)
                        break
            
            if detected:
                results.append(f"Detected:       {', '.join(set(detected))}")
            else:
                results.append(f"Detected:       Unknown/Static")
            
            # Check version if possible
            if 'WordPress' in detected:
                version_url = f"{url.rstrip('/')}/readme.html"
                try:
                    version_resp = requests.get(version_url, timeout=3, verify=False)
                    if 'wordpress' in version_resp.text.lower():
                        version_match = re.search(r'version\s*(\d+\.\d+(\.\d+)?)', version_resp.text, re.IGNORECASE)
                        if version_match:
                            results.append(f"Version:        {version_match.group(1)}")
                except:
                    pass
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ssrf_test(self, url, test_url="http://localhost"):
        """Test SSRF vulnerability"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"Testing:        {url}")
            results.append(f"Test URL:       {test_url}")
            results.append("=" * 50)
            
            # Common SSRF parameters
            ssrf_params = ['url', 'file', 'path', 'load', 'src', 'document']
            
            parsed = urlparse(url)
            if parsed.query:
                params = parse_qs(parsed.query)
                
                for param in ssrf_params:
                    if param in params:
                        results.append(f"Found param:    {param}")
                        
                        # Test with localhost URL
                        test_param = f"{param}={test_url}"
                        test_full_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{test_param}"
                        
                        try:
                            response = requests.get(test_full_url, timeout=5, verify=False)
                            
                            # Check if localhost content appears
                            if 'localhost' in response.text or '127.0.0.1' in response.text:
                                results.append(f"VULNERABLE:     SSRF via {param}")
                                results.append(f"Risk:           HIGH")
                            else:
                                results.append(f"Tested:         No SSRF detected")
                        except:
                            results.append(f"Error:          Request failed")
            
            if len(results) <= 2:
                results.append(f"No SSRF parameters found")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def email_verify(self, email):
        """Verify email address"""
        results = []
        
        try:
            results.append(f"Email:          {email}")
            results.append("=" * 50)
            
            # Basic format check
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                results.append(f"Format:         INVALID")
                return results
            
            results.append(f"Format:         VALID")
            
            # Extract domain
            domain = email.split('@')[1]
            
            # Check MX records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                mx_servers = [str(rdata.exchange) for rdata in answers]
                results.append(f"MX Records:     {', '.join(mx_servers[:2])}")
            except:
                results.append(f"MX Records:     NOT FOUND (domain may not exist)")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def jwt_test(self, token, secret=""):
        """Test JWT token"""
        results = []
        
        try:
            results.append(f"Token:          {token[:50]}...")
            results.append("=" * 50)
            
            # Split JWT
            parts = token.split('.')
            
            if len(parts) != 3:
                results.append(f"Format:         INVALID (not a JWT)")
                return results
            
            results.append(f"Format:         VALID JWT")
            
            # Decode header
            try:
                header = json.loads(base64.urlsafe_b64decode(parts[0] + '==').decode())
                results.append(f"Algorithm:      {header.get('alg', 'unknown')}")
                results.append(f"Type:           {header.get('typ', 'JWT')}")
            except:
                results.append(f"Header:         Could not decode")
            
            # Decode payload
            try:
                payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==').decode())
                
                # Check expiration
                if 'exp' in payload:
                    exp_time = datetime.fromtimestamp(payload['exp'])
                    now = datetime.now()
                    if exp_time > now:
                        results.append(f"Expires:        {exp_time} (VALID)")
                    else:
                        results.append(f"Expires:        {exp_time} (EXPIRED)")
                
                # Check issued at
                if 'iat' in payload:
                    iat_time = datetime.fromtimestamp(payload['iat'])
                    results.append(f"Issued At:      {iat_time}")
                
                # Show some claims
                for key in ['sub', 'iss', 'aud', 'email', 'name']:
                    if key in payload:
                        results.append(f"{key.upper():<15} {str(payload[key])[:50]}")
            
            except:
                results.append(f"Payload:        Could not decode")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def http_methods(self, url):
        """Test HTTP methods"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"URL:            {url}")
            results.append("=" * 50)
            
            methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE']
            
            for method in methods:
                try:
                    response = requests.request(method, url, timeout=3, verify=False)
                    results.append(f"{method:<10}     {response.status_code}")
                except Exception as e:
                    results.append(f"{method:<10}     ERROR")
            
            results.append("=" * 50)
            results.append(f"DANGEROUS:      DELETE, PUT, TRACE (if enabled)")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def backup_find(self, url):
        """Find backup files"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            base_url = url.rstrip('/')
            
            backup_files = [
                "backup.zip", "backup.tar", "backup.tar.gz", "backup.sql",
                "backup.db", "backup.rar", "database.zip", "database.sql",
                "dump.sql", "dump.zip", "www.zip", "site.tar.gz",
                "config.bak", "config.old", "config.backup",
                ".bak", ".old", ".backup", ".orig"
            ]
            
            results.append(f"URL:            {url}")
            results.append(f"Checking {len(backup_files)} backup files")
            results.append("=" * 50)
            
            found = 0
            
            def check_file(filename):
                try:
                    test_url = f"{base_url}/{filename}"
                    response = requests.head(test_url, timeout=2, verify=False)
                    if response.status_code == 200:
                        return filename, response.status_code, True
                except:
                    pass
                return filename, 0, False
            
            with ThreadPoolExecutor(max_workers=30) as executor:
                futures = [executor.submit(check_file, f) for f in backup_files]
                for future in as_completed(futures):
                    filename, status, found_flag = future.result()
                    if found_flag:
                        found += 1
                        results.append(f"FOUND   {filename:<20} [{status}]")
            
            results.append("=" * 50)
            results.append(f"Found {found} backup files")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def git_exposed(self, url):
        """Check for exposed .git directory"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            base_url = url.rstrip('/')
            
            git_files = [
                ".git/HEAD",
                ".git/config",
                ".git/description",
                ".git/index",
                ".git/logs/HEAD"
            ]
            
            results.append(f"URL:            {url}")
            results.append(f"Checking for exposed .git")
            results.append("=" * 50)
            
            found = False
            
            for git_file in git_files:
                try:
                    test_url = f"{base_url}/{git_file}"
                    response = requests.get(test_url, timeout=2, verify=False)
                    
                    if response.status_code == 200:
                        found = True
                        if git_file == ".git/HEAD":
                            content = response.text[:100]
                            results.append(f"EXPOSED:        {git_file}")
                            results.append(f"Content:        {content}")
                        else:
                            results.append(f"EXPOSED:        {git_file}")
                except:
                    continue
            
            if not found:
                results.append(f"Secure:         No .git exposure detected")
            else:
                results.append(f"WARNING:        Source code may be exposed")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def robots_check(self, url):
        """Check robots.txt"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            robots_url = f"{url.rstrip('/')}/robots.txt"
            
            results.append(f"URL:            {robots_url}")
            results.append("=" * 50)
            
            try:
                response = requests.get(robots_url, timeout=3, verify=False)
                
                if response.status_code == 200:
                    content = response.text
                    results.append(f"Status:         FOUND (200)")
                    results.append("=" * 50)
                    
                    # Parse robots.txt
                    lines = content.split('\n')
                    for line in lines[:20]:  # Show first 20 lines
                        line = line.strip()
                        if line and not line.startswith('#'):
                            results.append(f"{line}")
                    
                    # Check for sensitive paths
                    sensitive = ['admin', 'config', 'backup', 'database', 'sql', '.git', '.env']
                    for path in sensitive:
                        if path in content.lower():
                            results.append(f"WARNING:        '{path}' found in robots.txt")
                
                else:
                    results.append(f"Status:         NOT FOUND ({response.status_code})")
            
            except:
                results.append(f"Error:          Could not fetch robots.txt")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def shodan_lookup(self, query):
        """Shodan-like lookup using public APIs"""
        results = []
        
        try:
            results.append(f"Query:          {query}")
            results.append("=" * 50)
            
            # Try ip-api.com for IP info
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', query):
                try:
                    response = requests.get(f"http://ip-api.com/json/{query}", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('status') == 'success':
                            results.append(f"Country:        {data.get('country', 'N/A')}")
                            results.append(f"City:           {data.get('city', 'N/A')}")
                            results.append(f"ISP:            {data.get('isp', 'N/A')}")
                            results.append(f"Org:            {data.get('org', 'N/A')}")
                            results.append(f"AS:             {data.get('as', 'N/A')}")
                        else:
                            results.append(f"Info:           No data from API")
                except:
                    results.append(f"API Error:      Could not fetch data")
            
            # For domains, get IP and basic info
            else:
                try:
                    ip = socket.gethostbyname(query)
                    results.append(f"IP Address:     {ip}")
                    
                    # Quick port scan (top 5)
                    common_ports = [80, 443, 22, 21, 25]
                    open_ports = []
                    
                    for port in common_ports:
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(1)
                            if sock.connect_ex((ip, port)) == 0:
                                open_ports.append(str(port))
                            sock.close()
                        except:
                            pass
                    
                    if open_ports:
                        results.append(f"Open Ports:     {', '.join(open_ports)}")
                    else:
                        results.append(f"Open Ports:     None (common ports)")
                
                except:
                    results.append(f"Error:          Could not resolve domain")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def firewall_test(self, url):
        """Test for WAF/firewall"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"URL:            {url}")
            results.append("=" * 50)
            
            # Test with SQL injection payload
            test_url = f"{url}?id=' OR '1'='1"
            
            try:
                response = requests.get(test_url, timeout=5, verify=False)
                
                # Check for WAF indicators
                waf_indicators = [
                    ('cloudflare', 'Cloudflare'),
                    ('akamai', 'Akamai'),
                    ('imperva', 'Imperva'),
                    ('fortinet', 'Fortinet'),
                    ('f5', 'F5 BIG-IP'),
                    ('barracuda', 'Barracuda'),
                    ('sucuri', 'Sucuri'),
                    ('incapsula', 'Incapsula')
                ]
                
                headers = str(response.headers).lower()
                body = response.text.lower()
                
                detected = False
                
                for indicator, name in waf_indicators:
                    if indicator in headers or indicator in body:
                        results.append(f"WAF Detected:  {name}")
                        detected = True
                
                if not detected:
                    # Check for common WAF response codes
                    if response.status_code in [403, 406, 419, 500, 501, 503]:
                        results.append(f"Possible WAF:   Status {response.status_code}")
                    else:
                        results.append(f"WAF:            Not detected")
                
                # Check for captcha
                if 'captcha' in body or 'recaptcha' in body:
                    results.append(f"Captcha:        Present")
            
            except Exception as e:
                results.append(f"Error:          {str(e)}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def cloudflare_check(self, url):
        """Check if site uses Cloudflare"""
        results = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            results.append(f"URL:            {url}")
            results.append("=" * 50)
            
            try:
                response = requests.get(url, timeout=5, verify=False)
                headers = str(response.headers).lower()
                
                # Check Cloudflare headers
                cf_headers = ['cf-ray', 'cf-cache-status', 'cloudflare', 'cf-request-id']
                
                cf_detected = False
                for header in cf_headers:
                    if header in headers:
                        cf_detected = True
                        break
                
                # Check for Cloudflare in response
                if cf_detected or 'cloudflare' in response.text.lower():
                    results.append(f"Cloudflare:     DETECTED")
                    
                    # Get origin IP if possible
                    try:
                        # Use DNS history (simplified)
                        domain = urlparse(url).hostname
                        
                        # Check common subdomains that might bypass CF
                        bypass_domains = [
                            f"direct.{domain}",
                            f"origin.{domain}",
                            f"cpanel.{domain}",
                            f"mail.{domain}",
                            f"ftp.{domain}"
                        ]
                        
                        for bypass in bypass_domains:
                            try:
                                ip = socket.gethostbyname(bypass)
                                results.append(f"Possible Origin: {bypass} -> {ip}")
                            except:
                                pass
                    
                    except:
                        pass
                
                else:
                    results.append(f"Cloudflare:     NOT DETECTED")
                
                # Check if under attack mode
                if 'cf-please-wait' in headers or 'checking your browser' in response.text.lower():
                    results.append(f"Under Attack:   ENABLED")
            
            except Exception as e:
                results.append(f"Error:          {str(e)}")
            
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

# ========== TOOL INSTANCE ==========
tools = RealWorkingTools()

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
        
        # Map tool IDs to methods
        tool_map = {
            1: tools.port_scan,
            2: tools.dir_scan,
            3: tools.website_info,
            4: tools.whois_lookup,
            5: tools.ssl_check,
            6: tools.speed_test,
            7: tools.sqli_test,
            8: tools.xss_test,
            9: tools.ping_test,
            10: tools.ip_info,
            11: tools.hash_crack,
            12: tools.load_test,
            13: tools.subdomain_scan,
            14: tools.dns_records,
            15: tools.headers_check,
            16: tools.upload_test,
            17: tools.cors_test,
            18: tools.crlf_test,
            19: tools.redirect_test,
            20: tools.cms_detect,
            21: tools.ssrf_test,
            22: tools.email_verify,
            23: tools.jwt_test,
            24: tools.http_methods,
            25: tools.backup_find,
            26: tools.git_exposed,
            27: tools.robots_check,
            28: tools.shodan_lookup,
            29: tools.firewall_test,
            30: tools.cloudflare_check
        }
        
        if tool_id in tool_map:
            if tool_id in [11, 16, 21, 23]:  # Tools that need extra param
                results = tool_map[tool_id](target, extra)
            elif tool_id in [1, 9, 12]:  # Tools that can use extra param
                results = tool_map[tool_id](target, extra if extra else "")
            else:
                results = tool_map[tool_id](target)
        else:
            return jsonify({'error': 'Invalid tool ID'})
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Jaguar 45 Cyber Tools',
        'version': '3.0',
        'tools': 30,
        'timestamp': datetime.now().isoformat()
    })

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║           JAGUAR 45 - 30 REAL WORKING TOOLS              ║
    ║                No Simulations • All Real                 ║
    ║                                                          ║
    ║         Server: http://localhost:{port:<15}               ║
    ║         Tools: 30 • Threads: 200 • All Functional       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
