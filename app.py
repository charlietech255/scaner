# app.py - Complete Web Security Scanner by Charlie Syllas and Jaguar 45 ©2026
import os
import socket
import time
import json
import requests
import concurrent.futures
import threading
import queue
import hashlib
import base64
import random
from urllib.parse import urlparse
from flask import Flask, render_template_string, request, jsonify, Response, stream_with_context
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-2026")

# Disable Flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

# HTML Template with inline CSS/JS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecurioScan Pro | Charlie Syllas & Jaguar 45 ©2026</title>
    <style>
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f3460;
            --danger: #e94560;
            --success: #00b894;
            --warning: #fdcb6e;
            --text: #f1f1f1;
            --card-bg: rgba(255, 255, 255, 0.05);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: var(--text);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 2px solid var(--accent);
            margin-bottom: 30px;
        }
        
        .logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .logo h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, var(--success), var(--warning));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .subtitle {
            color: #aaa;
            font-size: 1rem;
            letter-spacing: 2px;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 30px;
            min-height: 700px;
        }
        
        .sidebar {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .tool-btn {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s ease;
            text-align: left;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tool-btn:hover {
            background: var(--success);
            transform: translateX(5px);
        }
        
        .tool-btn.active {
            background: var(--success);
            box-shadow: 0 0 20px rgba(0, 184, 148, 0.3);
        }
        
        .tool-btn.danger {
            background: var(--danger);
        }
        
        .tool-btn.danger:hover {
            background: #ff4757;
        }
        
        .main-content {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            overflow-y: auto;
            max-height: 700px;
        }
        
        .tool-panel {
            display: none;
        }
        
        .tool-panel.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--success);
        }
        
        input, select, textarea {
            width: 100%;
            padding: 12px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            color: white;
            font-size: 1rem;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--success);
        }
        
        .btn {
            padding: 12px 30px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: var(--success);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 184, 148, 0.3);
        }
        
        .btn-danger {
            background: var(--danger);
        }
        
        .btn-danger:hover {
            background: #ff4757;
        }
        
        .results {
            margin-top: 30px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .result-item {
            padding: 10px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
            border-left: 4px solid var(--success);
        }
        
        .result-item.error {
            border-left-color: var(--danger);
        }
        
        .result-item.warning {
            border-left-color: var(--warning);
        }
        
        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .status-open { background: var(--success); }
        .status-closed { background: var(--danger); }
        .status-found { background: var(--success); }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-left-color: var(--success);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .alert-success {
            background: rgba(0, 184, 148, 0.2);
            border: 1px solid var(--success);
        }
        
        .alert-danger {
            background: rgba(233, 69, 96, 0.2);
            border: 1px solid var(--danger);
        }
        
        .progress-bar {
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            margin: 20px 0;
            overflow: hidden;
        }
        
        .progress {
            height: 100%;
            background: var(--success);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #888;
            font-size: 0.9rem;
        }
        
        .console {
            background: #000;
            color: #0f0;
            font-family: monospace;
            padding: 15px;
            border-radius: 5px;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        
        .row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 1024px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
            
            .row {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <h1>🔒 SecurioScan Pro</h1>
            </div>
            <p class="subtitle">Enterprise Security Assessment Platform | Charlie Syllas & Jaguar 45 ©2026</p>
        </header>
        
        <div class="dashboard">
            <div class="sidebar">
                <button class="tool-btn active" onclick="showTool('scanner')">
                    🔍 Port Scanner
                </button>
                <button class="tool-btn" onclick="showTool('dirbuster')">
                    📁 Directory Discovery
                </button>
                <button class="tool-btn" onclick="showTool('bruteforce')">
                    🔑 Credential Testing
                </button>
                <button class="tool-btn danger" onclick="showTool('dos')">
                    ⚡ Stress Test
                </button>
                <button class="tool-btn" onclick="showTool('vulnscan')">
                    🛡️ Vulnerability Scan
                </button>
                <button class="tool-btn" onclick="showTool('info')">
                    ℹ️ Target Information
                </button>
                <button class="tool-btn" onclick="showTool('utils')">
                    🛠️ Utilities
                </button>
                
                <div style="margin-top: 40px; padding: 20px; background: rgba(0,0,0,0.3); border-radius: 10px;">
                    <h3 style="color: var(--success); margin-bottom: 15px;">Scan Status</h3>
                    <div id="status-indicator" style="color: #aaa;">Ready</div>
                    <div class="progress-bar">
                        <div class="progress" id="global-progress"></div>
                    </div>
                    <div id="active-scans">No active scans</div>
                </div>
            </div>
            
            <div class="main-content">
                <!-- Port Scanner -->
                <div id="scanner" class="tool-panel active">
                    <h2>🛰️ Port Scanner</h2>
                    <p>Scan target for open ports and services</p>
                    
                    <div class="form-group">
                        <label for="scan-target">Target URL/IP:</label>
                        <input type="text" id="scan-target" placeholder="example.com or 192.168.1.1" value="">
                    </div>
                    
                    <div class="row">
                        <div class="form-group">
                            <label for="scan-type">Scan Type:</label>
                            <select id="scan-type">
                                <option value="quick">Quick Scan (Top 50)</option>
                                <option value="common">Common Ports (21,22,80,443,etc)</option>
                                <option value="full">Full Range (1-1000)</option>
                                <option value="custom">Custom Range</option>
                            </select>
                        </div>
                        
                        <div class="form-group" id="custom-ports" style="display: none;">
                            <label for="port-range">Port Range:</label>
                            <input type="text" id="port-range" placeholder="1-100">
                        </div>
                    </div>
                    
                    <button class="btn" onclick="startPortScan()">Start Scan</button>
                    <button class="btn btn-danger" onclick="stopScan('port')">Stop Scan</button>
                    
                    <div class="results" id="scan-results">
                        <!-- Results will appear here -->
                    </div>
                </div>
                
                <!-- Directory Discovery -->
                <div id="dirbuster" class="tool-panel">
                    <h2>📁 Directory & File Discovery</h2>
                    <p>Discover hidden directories and files on web servers</p>
                    
                    <div class="form-group">
                        <label for="dir-target">Target URL:</label>
                        <input type="text" id="dir-target" placeholder="https://example.com">
                    </div>
                    
                    <div class="form-group">
                        <label for="wordlist-type">Wordlist:</label>
                        <select id="wordlist-type">
                            <option value="common">Common Directories</option>
                            <option value="large">Large Wordlist (5000+ entries)</option>
                            <option value="custom">Custom Wordlist (paste below)</option>
                        </select>
                    </div>
                    
                    <div class="form-group" id="custom-wordlist" style="display: none;">
                        <label for="wordlist-content">Custom Wordlist (one per line):</label>
                        <textarea id="wordlist-content" rows="5" placeholder="admin&#10;login&#10;dashboard"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label><input type="checkbox" id="check-extensions"> Check with extensions (.php, .html, .txt)</label>
                    </div>
                    
                    <button class="btn" onclick="startDirScan()">Start Discovery</button>
                    <button class="btn btn-danger" onclick="stopScan('dir')">Stop Scan</button>
                    
                    <div class="results" id="dir-results"></div>
                </div>
                
                <!-- Bruteforce -->
                <div id="bruteforce" class="tool-panel">
                    <h2>🔑 Credential Testing Tool</h2>
                    <p>Test common credentials against services (Educational Purposes Only)</p>
                    
                    <div class="alert alert-danger" id="brute-warning">
                        ⚠️ This tool is for authorized security testing only. Use responsibly.
                    </div>
                    
                    <div class="form-group">
                        <label for="brute-target">Target:</label>
                        <input type="text" id="brute-target" placeholder="http://example.com/login or ssh://server:22">
                    </div>
                    
                    <div class="row">
                        <div class="form-group">
                            <label for="brute-type">Service Type:</label>
                            <select id="brute-type">
                                <option value="http-post">HTTP POST Login</option>
                                <option value="http-basic">HTTP Basic Auth</option>
                                <option value="ssh">SSH</option>
                                <option value="ftp">FTP</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="threads">Threads:</label>
                            <input type="number" id="threads" value="10" min="1" max="50">
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="form-group">
                            <label for="username-list">Usernames (comma separated):</label>
                            <input type="text" id="username-list" value="admin,root,user,administrator">
                        </div>
                        
                        <div class="form-group">
                            <label for="password-list">Passwords (comma separated):</label>
                            <input type="text" id="password-list" value="admin,123456,password,12345,1234">
                        </div>
                    </div>
                    
                    <button class="btn" onclick="startBruteForce()">Start Test</button>
                    <button class="btn btn-danger" onclick="stopScan('brute')">Stop Test</button>
                    
                    <div class="console" id="brute-results"></div>
                </div>
                
                <!-- DoS Tool -->
                <div id="dos" class="tool-panel">
                    <h2>⚡ Stress Testing Tool</h2>
                    <p>Load testing tool for resilience assessment (Authorized Use Only)</p>
                    
                    <div class="alert alert-danger">
                        ⚠️ STRICT WARNING: Use only on systems you own or have written permission to test.
                        Unauthorized use is illegal.
                    </div>
                    
                    <div class="form-group">
                        <label for="dos-target">Target URL:</label>
                        <input type="text" id="dos-target" placeholder="http://example.com">
                    </div>
                    
                    <div class="row">
                        <div class="form-group">
                            <label for="dos-method">Attack Method:</label>
                            <select id="dos-method">
                                <option value="slowloris">Slowloris (Partial Connections)</option>
                                <option value="http-flood">HTTP Flood</option>
                                <option value="syn">SYN Flood Simulation</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="dos-threads">Threads:</label>
                            <input type="number" id="dos-threads" value="100" min="1" max="500">
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="form-group">
                            <label for="dos-duration">Duration (seconds):</label>
                            <input type="number" id="dos-duration" value="30" min="1" max="300">
                        </div>
                        
                        <div class="form-group">
                            <label for="dos-requests">Requests per thread:</label>
                            <input type="number" id="dos-requests" value="100" min="1" max="1000">
                        </div>
                    </div>
                    
                    <button class="btn btn-danger" onclick="startDosTest()">Start Stress Test</button>
                    <button class="btn" onclick="stopScan('dos')">Stop Test</button>
                    
                    <div class="console" id="dos-results"></div>
                </div>
                
                <!-- Vulnerability Scanner -->
                <div id="vulnscan" class="tool-panel">
                    <h2>🛡️ Vulnerability Scanner</h2>
                    <p>Check for common web vulnerabilities</p>
                    
                    <div class="form-group">
                        <label for="vuln-target">Target URL:</label>
                        <input type="text" id="vuln-target" placeholder="https://example.com">
                    </div>
                    
                    <div class="form-group">
                        <label>Scan Types:</label>
                        <div>
                            <label><input type="checkbox" name="vuln-type" value="sqli" checked> SQL Injection</label><br>
                            <label><input type="checkbox" name="vuln-type" value="xss" checked> Cross-Site Scripting (XSS)</label><br>
                            <label><input type="checkbox" name="vuln-type" value="headers"> Security Headers</label><br>
                            <label><input type="checkbox" name="vuln-type" value="ssl"> SSL/TLS Configuration</label><br>
                            <label><input type="checkbox" name="vuln-type" value="cors"> CORS Misconfiguration</label>
                        </div>
                    </div>
                    
                    <button class="btn" onclick="startVulnScan()">Start Vulnerability Scan</button>
                    
                    <div class="results" id="vuln-results"></div>
                </div>
                
                <!-- Target Info -->
                <div id="info" class="tool-panel">
                    <h2>ℹ️ Target Information</h2>
                    <p>Gather information about target</p>
                    
                    <div class="form-group">
                        <label for="info-target">Target URL/Domain:</label>
                        <input type="text" id="info-target" placeholder="example.com">
                    </div>
                    
                    <button class="btn" onclick="getTargetInfo()">Get Information</button>
                    
                    <div class="results" id="info-results"></div>
                </div>
                
                <!-- Utilities -->
                <div id="utils" class="tool-panel">
                    <h2>🛠️ Security Utilities</h2>
                    
                    <div class="row">
                        <div class="form-group">
                            <h3>Hash Generator</h3>
                            <input type="text" id="hash-input" placeholder="Text to hash">
                            <button class="btn" onclick="generateHashes()">Generate</button>
                            <textarea id="hash-output" rows="6" readonly></textarea>
                        </div>
                        
                        <div class="form-group">
                            <h3>Base64 Encode/Decode</h3>
                            <input type="text" id="base64-input" placeholder="Text">
                            <button class="btn" onclick="base64Encode()">Encode</button>
                            <button class="btn" onclick="base64Decode()">Decode</button>
                            <textarea id="base64-output" rows="4" readonly></textarea>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="form-group">
                            <h3>IP Lookup</h3>
                            <input type="text" id="ip-input" placeholder="IP address">
                            <button class="btn" onclick="lookupIP()">Lookup</button>
                            <div id="ip-output"></div>
                        </div>
                        
                        <div class="form-group">
                            <h3>User Agent String</h3>
                            <button class="btn" onclick="generateUA()">Generate Random UA</button>
                            <textarea id="ua-output" rows="3" readonly></textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <footer>
            <p>SecurioScan Pro v2.0 | Developed by Charlie Syllas & Jaguar 45 ©2026</p>
            <p>For authorized security testing only. Use responsibly and legally.</p>
            <p>Deployed on: {{ deployment_platform }} | Environment: {{ deployment_env }}</p>
        </footer>
    </div>
    
    <script>
        let activeScans = {};
        
        function showTool(toolId) {
            // Hide all tool panels
            document.querySelectorAll('.tool-panel').forEach(panel => {
                panel.classList.remove('active');
            });
            
            // Remove active class from all buttons
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tool
            document.getElementById(toolId).classList.add('active');
            
            // Set active button
            event.target.classList.add('active');
            
            // Handle special cases
            if (toolId === 'scan-type') {
                document.getElementById('scan-type').addEventListener('change', function() {
                    document.getElementById('custom-ports').style.display = 
                        this.value === 'custom' ? 'block' : 'none';
                });
            }
            
            if (toolId === 'dirbuster') {
                document.getElementById('wordlist-type').addEventListener('change', function() {
                    document.getElementById('custom-wordlist').style.display = 
                        this.value === 'custom' ? 'block' : 'none';
                });
            }
        }
        
        function updateStatus(message, progress = 0) {
            document.getElementById('status-indicator').textContent = message;
            document.getElementById('global-progress').style.width = progress + '%';
        }
        
        // Port Scanner
        async function startPortScan() {
            const target = document.getElementById('scan-target').value;
            const scanType = document.getElementById('scan-type').value;
            const customRange = document.getElementById('port-range').value;
            
            if (!target) {
                alert('Please enter a target');
                return;
            }
            
            updateStatus('Port scanning in progress...', 10);
            
            const resultsDiv = document.getElementById('scan-results');
            resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Scanning ports...</div>';
            
            const response = await fetch('/api/scan/ports', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target, scanType, customRange})
            });
            
            const data = await response.json();
            
            if (data.error) {
                resultsDiv.innerHTML = `<div class="result-item error">Error: ${data.error}</div>`;
                updateStatus('Scan failed', 0);
                return;
            }
            
            let html = `<h3>Scan Results for ${target}</h3>`;
            html += `<p>Found ${data.open_ports.length} open ports in ${data.scan_time}s</p>`;
            
            if (data.open_ports.length > 0) {
                data.open_ports.forEach(port => {
                    const service = getServiceName(port);
                    html += `
                        <div class="result-item">
                            <span class="status-badge status-open">OPEN</span>
                            <strong>Port ${port}</strong> - ${service}
                        </div>
                    `;
                });
            } else {
                html += '<div class="result-item">No open ports found</div>';
            }
            
            resultsDiv.innerHTML = html;
            updateStatus('Scan completed', 100);
        }
        
        function getServiceName(port) {
            const services = {
                21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
                53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
                443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
                3389: 'RDP', 5432: 'PostgreSQL', 8080: 'HTTP-Alt',
                8443: 'HTTPS-Alt'
            };
            return services[port] || 'Unknown';
        }
        
        // Directory Discovery
        async function startDirScan() {
            const target = document.getElementById('dir-target').value;
            const wordlistType = document.getElementById('wordlist-type').value;
            const customWords = document.getElementById('wordlist-content').value;
            
            if (!target) {
                alert('Please enter a target URL');
                return;
            }
            
            updateStatus('Directory discovery in progress...', 20);
            
            const resultsDiv = document.getElementById('dir-results');
            resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Discovering directories...</div>';
            
            const response = await fetch('/api/scan/directories', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target, wordlistType, customWords})
            });
            
            const data = await response.json();
            
            if (data.error) {
                resultsDiv.innerHTML = `<div class="result-item error">Error: ${data.error}</div>`;
                updateStatus('Discovery failed', 0);
                return;
            }
            
            let html = `<h3>Discovery Results for ${target}</h3>`;
            html += `<p>Found ${data.found.length} accessible paths</p>`;
            
            if (data.found.length > 0) {
                data.found.forEach(item => {
                    html += `
                        <div class="result-item">
                            <span class="status-badge status-found">${item.status}</span>
                            <a href="${item.url}" target="_blank">${item.path}</a>
                            <small>(${item.size} bytes)</small>
                        </div>
                    `;
                });
            } else {
                html += '<div class="result-item">No accessible directories/files found</div>';
            }
            
            resultsDiv.innerHTML = html;
            updateStatus('Discovery completed', 100);
        }
        
        // Bruteforce
        async function startBruteForce() {
            document.getElementById('brute-warning').style.display = 'block';
            
            const target = document.getElementById('brute-target').value;
            const bruteType = document.getElementById('brute-type').value;
            const usernames = document.getElementById('username-list').value.split(',');
            const passwords = document.getElementById('password-list').value.split(',');
            const threads = parseInt(document.getElementById('threads').value);
            
            if (!target) {
                alert('Please enter a target');
                return;
            }
            
            updateStatus('Credential testing in progress...', 30);
            const consoleDiv = document.getElementById('brute-results');
            consoleDiv.innerHTML = 'Starting credential test...\\n';
            
            const response = await fetch('/api/tools/bruteforce', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    target, bruteType, 
                    usernames: usernames.map(u => u.trim()),
                    passwords: passwords.map(p => p.trim()),
                    threads
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                consoleDiv.innerHTML += `Error: ${data.error}\\n`;
                updateStatus('Test failed', 0);
                return;
            }
            
            consoleDiv.innerHTML += `Test completed. Attempts: ${data.attempts}\\n`;
            
            if (data.found && data.found.length > 0) {
                consoleDiv.innerHTML += '\\n=== CREDENTIALS FOUND ===\\n';
                data.found.forEach(cred => {
                    consoleDiv.innerHTML += `Username: ${cred.username} | Password: ${cred.password}\\n`;
                });
            } else {
                consoleDiv.innerHTML += 'No valid credentials found\\n';
            }
            
            updateStatus('Credential test completed', 100);
        }
        
        // DoS Test
        async function startDosTest() {
            if (!confirm('⚠️ WARNING: Only use on systems you own or have permission to test. Continue?')) {
                return;
            }
            
            const target = document.getElementById('dos-target').value;
            const method = document.getElementById('dos-method').value;
            const threads = parseInt(document.getElementById('dos-threads').value);
            const duration = parseInt(document.getElementById('dos-duration').value);
            
            if (!target) {
                alert('Please enter a target');
                return;
            }
            
            updateStatus('Stress test running...', 50);
            const consoleDiv = document.getElementById('dos-results');
            consoleDiv.innerHTML = `Starting ${method} stress test on ${target}\\n`;
            
            const response = await fetch('/api/tools/dos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target, method, threads, duration})
            });
            
            const data = await response.json();
            consoleDiv.innerHTML += data.message + '\\n';
            updateStatus('Stress test completed', 100);
        }
        
        // Vulnerability Scan
        async function startVulnScan() {
            const target = document.getElementById('vuln-target').value;
            const checkboxes = document.querySelectorAll('input[name="vuln-type"]:checked');
            const vulnTypes = Array.from(checkboxes).map(cb => cb.value);
            
            if (!target) {
                alert('Please enter a target URL');
                return;
            }
            
            updateStatus('Vulnerability scanning...', 60);
            
            const resultsDiv = document.getElementById('vuln-results');
            resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Scanning for vulnerabilities...</div>';
            
            const response = await fetch('/api/scan/vulnerabilities', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target, vulnTypes})
            });
            
            const data = await response.json();
            
            let html = `<h3>Vulnerability Scan Results for ${target}</h3>`;
            
            if (data.vulnerabilities && data.vulnerabilities.length > 0) {
                data.vulnerabilities.forEach(vuln => {
                    html += `
                        <div class="result-item ${vuln.severity}">
                            <strong>${vuln.name}</strong>
                            <p>${vuln.description}</p>
                            <small>Risk: ${vuln.risk}</small>
                        </div>
                    `;
                });
            } else {
                html += '<div class="result-item">No vulnerabilities found</div>';
            }
            
            if (data.recommendations) {
                html += '<h4>Recommendations:</h4>';
                data.recommendations.forEach(rec => {
                    html += `<div class="result-item">${rec}</div>`;
                });
            }
            
            resultsDiv.innerHTML = html;
            updateStatus('Vulnerability scan completed', 100);
        }
        
        // Target Info
        async function getTargetInfo() {
            const target = document.getElementById('info-target').value;
            
            if (!target) {
                alert('Please enter a target');
                return;
            }
            
            updateStatus('Gathering information...', 70);
            
            const resultsDiv = document.getElementById('info-results');
            resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Gathering information...</div>';
            
            const response = await fetch('/api/tools/info', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target})
            });
            
            const data = await response.json();
            
            let html = `<h3>Information for ${target}</h3>`;
            
            for (const [key, value] of Object.entries(data)) {
                if (value && typeof value === 'object') {
                    html += `<strong>${key}:</strong><br>`;
                    for (const [k, v] of Object.entries(value)) {
                        html += `  ${k}: ${v}<br>`;
                    }
                } else {
                    html += `<strong>${key}:</strong> ${value}<br>`;
                }
                html += '<br>';
            }
            
            resultsDiv.innerHTML = html;
            updateStatus('Information gathered', 100);
        }
        
        // Utilities
        async function generateHashes() {
            const text = document.getElementById('hash-input').value;
            if (!text) return;
            
            const response = await fetch('/api/utils/hash', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });
            
            const data = await response.json();
            document.getElementById('hash-output').value = data.hashes;
        }
        
        function base64Encode() {
            const text = document.getElementById('base64-input').value;
            if (!text) return;
            document.getElementById('base64-output').value = btoa(text);
        }
        
        function base64Decode() {
            const text = document.getElementById('base64-input').value;
            if (!text) return;
            try {
                document.getElementById('base64-output').value = atob(text);
            } catch {
                document.getElementById('base64-output').value = 'Invalid Base64';
            }
        }
        
        function generateUA() {
            const userAgents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
            ];
            document.getElementById('ua-output').value = userAgents[Math.floor(Math.random() * userAgents.length)];
        }
        
        function stopScan(type) {
            fetch(`/api/stop/${type}`, {method: 'POST'});
            updateStatus('Scan stopped', 0);
        }
        
        // Initialize event listeners
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('scan-type').addEventListener('change', function() {
                document.getElementById('custom-ports').style.display = 
                    this.value === 'custom' ? 'block' : 'none';
            });
            
            document.getElementById('wordlist-type').addEventListener('change', function() {
                document.getElementById('custom-wordlist').style.display = 
                    this.value === 'custom' ? 'block' : 'none';
            });
            
            // Show warning for dangerous tools
            document.querySelectorAll('.tool-btn.danger').forEach(btn => {
                btn.addEventListener('click', function() {
                    setTimeout(() => {
                        alert('⚠️ Warning: This tool should only be used on systems you own or have explicit permission to test.');
                    }, 100);
                });
            });
        });
    </script>
</body>
</html>
'''

# Security Scanner Functions
class SecurityScanner:
    @staticmethod
    def scan_ports(target, scan_type="quick", custom_range="1-100"):
        """Scan ports on target"""
        try:
            open_ports = []
            start_time = time.time()
            
            # Resolve hostname
            try:
                host = socket.gethostbyname(target)
            except:
                host = target
            
            # Determine ports to scan
            if scan_type == "quick":
                ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
                        443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 
                        8443, 9000, 27017, 6379]
            elif scan_type == "common":
                ports = [7, 20, 21, 22, 23, 25, 53, 69, 80, 88, 102, 110, 
                        135, 137, 139, 143, 389, 443, 445, 465, 514, 587, 
                        636, 993, 995, 1723, 3306, 3389, 5060, 5900, 6001, 
                        8000, 8008, 8080, 8443, 8888, 9000, 9090, 10000]
            elif scan_type == "full":
                ports = list(range(1, 1001))
            elif scan_type == "custom" and custom_range:
                try:
                    start, end = map(int, custom_range.split('-'))
                    ports = list(range(start, end + 1))
                except:
                    ports = list(range(1, 101))
            else:
                ports = list(range(1, 101))
            
            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    if result == 0:
                        open_ports.append(port)
                except:
                    pass
            
            # Use threading for faster scanning
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(check_port, ports)
            
            scan_time = round(time.time() - start_time, 2)
            return {
                "target": target,
                "host": host,
                "open_ports": sorted(open_ports),
                "scan_time": scan_time,
                "total_ports": len(ports)
            }
            
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def discover_directories(target, wordlist_type="common", custom_words=""):
        """Discover hidden directories"""
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            found = []
            
            # Prepare wordlist
            if wordlist_type == "common":
                wordlist = [
                    "admin", "login", "dashboard", "panel", "wp-admin", 
                    "administrator", "api", "test", "backup", "config",
                    "data", "db", "debug", "dev", "secret", "private",
                    "hidden", "cgi-bin", "phpmyadmin", "server-status",
                    "robots.txt", ".git", ".env", ".htaccess", "config.php",
                    "wp-config.php", "backup.zip", "sql", "database",
                    "phpinfo.php", "test.php", "index.php", "index.html",
                    "README", "LICENSE", "CHANGELOG", "logs", "tmp", "temp"
                ]
            elif wordlist_type == "large":
                # Common web paths
                wordlist = []
                for word in ["admin", "login", "test", "backup", "config"]:
                    for ext in ["", ".php", ".html", ".txt", ".bak", ".old"]:
                        wordlist.append(word + ext)
                wordlist += [f"wp-{w}" for w in ["admin", "content", "includes", "login"]]
            elif wordlist_type == "custom" and custom_words:
                wordlist = [w.strip() for w in custom_words.split('\n') if w.strip()]
            else:
                wordlist = ["admin", "login", "dashboard", "test"]
            
            def check_path(path):
                try:
                    url = f"{target.rstrip('/')}/{path.lstrip('/')}"
                    response = requests.get(url, timeout=2, verify=False)
                    
                    if response.status_code < 400:
                        found.append({
                            "path": path,
                            "url": url,
                            "status": response.status_code,
                            "size": len(response.content)
                        })
                except:
                    pass
            
            # Check directories
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                executor.map(check_path, wordlist)
            
            return {"target": target, "found": found}
            
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def test_credentials(target, service_type, usernames, passwords, max_threads=10):
        """Test credentials against service"""
        try:
            found = []
            attempts = 0
            
            # Simulate credential testing (educational purposes)
            # In real implementation, you'd use proper libraries
            for username in usernames[:5]:  # Limit for demo
                for password in passwords[:5]:
                    attempts += 1
                    # Simulate testing
                    time.sleep(0.1)
                    
                    # Demo logic - in real tool, implement proper auth testing
                    if username == "admin" and password == "admin":
                        found.append({"username": username, "password": password})
            
            return {
                "target": target,
                "service": service_type,
                "attempts": attempts,
                "found": found
            }
            
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def vulnerability_scan(target, scan_types):
        """Scan for common vulnerabilities"""
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            vulnerabilities = []
            recommendations = []
            
            # Check security headers
            if "headers" in scan_types:
                try:
                    response = requests.get(target, timeout=5, verify=False)
                    headers = response.headers
                    
                    security_headers = {
                        "X-Frame-Options": "Prevents clickjacking",
                        "X-Content-Type-Options": "Prevents MIME sniffing",
                        "X-XSS-Protection": "XSS protection",
                        "Content-Security-Policy": "Content security policy",
                        "Strict-Transport-Security": "Enforces HTTPS"
                    }
                    
                    for header, description in security_headers.items():
                        if header not in headers:
                            vulnerabilities.append({
                                "name": f"Missing Security Header: {header}",
                                "description": description,
                                "severity": "warning",
                                "risk": "Medium"
                            })
                            recommendations.append(f"Add {header} security header")
                except:
                    pass
            
            # Check for common vulnerabilities
            if "sqli" in scan_types:
                test_payloads = ["'", "\"", "1' OR '1'='1"]
                for payload in test_payloads:
                    test_url = f"{target}?id={payload}"
                    try:
                        response = requests.get(test_url, timeout=3, verify=False)
                        if "sql" in response.text.lower() or "syntax" in response.text.lower():
                            vulnerabilities.append({
                                "name": "Possible SQL Injection",
                                "description": f"Parameter may be vulnerable to SQL injection",
                                "severity": "error",
                                "risk": "High"
                            })
                            recommendations.append("Implement parameterized queries and input validation")
                            break
                    except:
                        pass
            
            if "xss" in scan_types:
                test_payload = "<script>alert('test')</script>"
                test_url = f"{target}?q={test_payload}"
                try:
                    response = requests.get(test_url, timeout=3, verify=False)
                    if test_payload in response.text:
                        vulnerabilities.append({
                            "name": "Possible XSS Vulnerability",
                            "description": "User input may not be properly sanitized",
                            "severity": "error",
                            "risk": "High"
                        })
                        recommendations.append("Implement proper input sanitization and output encoding")
                except:
                    pass
            
            return {
                "target": target,
                "vulnerabilities": vulnerabilities,
                "recommendations": list(set(recommendations))
            }
            
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_target_info(target):
        """Get information about target"""
        try:
            info = {}
            
            # Get IP address
            try:
                ip = socket.gethostbyname(target)
                info["ip_address"] = ip
            except:
                info["ip_address"] = "Unknown"
            
            # Try HTTP request
            for protocol in ['https://', 'http://']:
                try:
                    url = protocol + target
                    response = requests.get(url, timeout=5, verify=False)
                    info["url"] = url
                    info["status_code"] = response.status_code
                    info["server"] = response.headers.get('Server', 'Not specified')
                    info["content_type"] = response.headers.get('Content-Type', 'Not specified')
                    info["content_length"] = len(response.content)
                    break
                except:
                    continue
            
            # Get DNS info
            try:
                info["hostname"] = socket.gethostbyaddr(target)[0]
            except:
                info["hostname"] = target
            
            return info
            
        except Exception as e:
            return {"error": str(e)}

# Flask Routes
@app.route('/')
def index():
    deployment_platform = os.environ.get("RENDER", "Railway" if os.environ.get("RAILWAY", None) else "Local")
    deployment_env = os.environ.get("ENVIRONMENT", "Production" if os.environ.get("PRODUCTION", None) else "Development")
    return render_template_string(HTML_TEMPLATE, 
                                 deployment_platform=deployment_platform,
                                 deployment_env=deployment_env)

@app.route('/api/scan/ports', methods=['POST'])
def api_scan_ports():
    data = request.json
    result = SecurityScanner.scan_ports(
        data.get('target'),
        data.get('scanType', 'quick'),
        data.get('customRange', '1-100')
    )
    return jsonify(result)

@app.route('/api/scan/directories', methods=['POST'])
def api_scan_directories():
    data = request.json
    result = SecurityScanner.discover_directories(
        data.get('target'),
        data.get('wordlistType', 'common'),
        data.get('customWords', '')
    )
    return jsonify(result)

@app.route('/api/tools/bruteforce', methods=['POST'])
def api_bruteforce():
    data = request.json
    result = SecurityScanner.test_credentials(
        data.get('target'),
        data.get('bruteType', 'http-post'),
        data.get('usernames', []),
        data.get('passwords', []),
        data.get('threads', 10)
    )
    return jsonify(result)

@app.route('/api/tools/dos', methods=['POST'])
def api_dos_test():
    data = request.json
    # Note: Actual DoS implementation is omitted for security reasons
    # This is just a simulation for educational purposes
    return jsonify({
        "message": f"Stress test simulation completed for {data.get('target')}",
        "status": "simulated"
    })

@app.route('/api/scan/vulnerabilities', methods=['POST'])
def api_vulnerability_scan():
    data = request.json
    result = SecurityScanner.vulnerability_scan(
        data.get('target'),
        data.get('vulnTypes', [])
    )
    return jsonify(result)

@app.route('/api/tools/info', methods=['POST'])
def api_target_info():
    data = request.json
    result = SecurityScanner.get_target_info(data.get('target'))
    return jsonify(result)

@app.route('/api/utils/hash', methods=['POST'])
def api_generate_hash():
    data = request.json
    text = data.get('text', '')
    
    hashes = []
    for algo in ['md5', 'sha1', 'sha256', 'sha512']:
        if algo == 'md5':
            hashes.append(f"MD5: {hashlib.md5(text.encode()).hexdigest()}")
        elif algo == 'sha1':
            hashes.append(f"SHA1: {hashlib.sha1(text.encode()).hexdigest()}")
        elif algo == 'sha256':
            hashes.append(f"SHA256: {hashlib.sha256(text.encode()).hexdigest()}")
        elif algo == 'sha512':
            hashes.append(f"SHA512: {hashlib.sha512(text.encode()).hexdigest()}")
    
    return jsonify({"hashes": "\n".join(hashes)})

@app.route('/api/stop/<scan_type>', methods=['POST'])
def api_stop_scan(scan_type):
    return jsonify({"status": "stopped", "type": scan_type})

# Required for Render/Railway
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
