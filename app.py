# app.py - Working Terminal Security Scanner
import os
import socket
import time
import json
import requests
import hashlib
from flask import Flask, render_template_string, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

# Simple HTML with terminal style
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal Scanner</title>
    <style>
        body {
            background: #000;
            color: #0f0;
            font-family: monospace;
            margin: 0;
            padding: 20px;
            overflow-x: hidden;
        }
        
        .terminal {
            max-width: 1000px;
            margin: 0 auto;
            border: 1px solid #0f0;
            padding: 20px;
            border-radius: 5px;
            background: #111;
        }
        
        .header {
            text-align: center;
            border-bottom: 1px solid #0f0;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        .output {
            min-height: 400px;
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            background: #000;
            border: 1px solid #333;
            margin-bottom: 10px;
        }
        
        .prompt {
            display: flex;
            align-items: center;
        }
        
        .prompt-text {
            color: #0ff;
            margin-right: 10px;
        }
        
        input {
            background: transparent;
            border: none;
            color: #0f0;
            font-family: monospace;
            font-size: 16px;
            width: 100%;
            outline: none;
        }
        
        .command {
            color: #0ff;
        }
        
        .result {
            margin: 5px 0;
            padding-left: 10px;
        }
        
        .error { color: #f00; }
        .success { color: #0f0; }
        .warning { color: #ff0; }
        .info { color: #0ff; }
        
        .menu {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .menu-btn {
            background: #222;
            color: #0f0;
            border: 1px solid #0f0;
            padding: 10px;
            cursor: pointer;
            font-family: monospace;
            text-align: left;
        }
        
        .menu-btn:hover {
            background: #333;
        }
        
        .scanning {
            color: #0f0;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="header">
            <h1>🔒 TERMINAL SECURITY SCANNER</h1>
            <p>Type "help" for commands or click menu buttons</p>
        </div>
        
        <div class="menu">
            <button class="menu-btn" onclick="runCommand('scan ports')">📡 Port Scan</button>
            <button class="menu-btn" onclick="runCommand('scan dir')">📁 Directory Scan</button>
            <button class="menu-btn" onclick="runCommand('vuln scan')">🛡️ Vuln Scan</button>
            <button class="menu-btn" onclick="runCommand('info')">ℹ️ Target Info</button>
            <button class="menu-btn" onclick="runCommand('utils')">🛠️ Utilities</button>
            <button class="menu-btn" onclick="runCommand('clear')">🗑️ Clear</button>
        </div>
        
        <div class="output" id="output"></div>
        
        <div class="prompt">
            <span class="prompt-text">root@scanner:~$</span>
            <input type="text" id="commandInput" autocomplete="off" 
                   placeholder="Type command here..." 
                   onkeypress="if(event.key === 'Enter') executeCommand()">
        </div>
    </div>
    
    <script>
        const output = document.getElementById('output');
        const input = document.getElementById('commandInput');
        let commandHistory = [];
        let historyIndex = -1;
        
        function addOutput(text, className = '') {
            const div = document.createElement('div');
            div.className = className + ' result';
            div.innerHTML = text;
            output.appendChild(div);
            output.scrollTop = output.scrollHeight;
        }
        
        function runCommand(cmd) {
            input.value = cmd;
            executeCommand();
        }
        
        function executeCommand() {
            const cmd = input.value.trim();
            if (!cmd) return;
            
            // Add to history
            commandHistory.push(cmd);
            historyIndex = commandHistory.length;
            
            // Show command
            addOutput(`<span class="command">root@scanner:~$ ${cmd}</span>`);
            
            // Process command
            const parts = cmd.toLowerCase().split(' ');
            const action = parts[0];
            
            switch(action) {
                case 'help':
                    showHelp();
                    break;
                case 'scan':
                    if (parts[1] === 'ports') {
                        startPortScan(parts[2]);
                    } else if (parts[1] === 'dir') {
                        startDirScan(parts[2]);
                    } else {
                        addOutput('Usage: scan ports [target] or scan dir [url]', 'warning');
                    }
                    break;
                case 'vuln':
                    startVulnScan(parts[2]);
                    break;
                case 'info':
                    getTargetInfo(parts[1]);
                    break;
                case 'utils':
                    showUtils();
                    break;
                case 'clear':
                    output.innerHTML = '';
                    break;
                default:
                    addOutput(`Command not found: ${cmd}. Type "help" for commands.`, 'error');
            }
            
            input.value = '';
            input.focus();
        }
        
        function showHelp() {
            addOutput('<strong>Available Commands:</strong>', 'info');
            addOutput('help                 - Show this help', 'info');
            addOutput('scan ports [target]  - Scan ports (e.g., scan ports example.com)', 'info');
            addOutput('scan dir [url]       - Scan directories (e.g., scan dir http://example.com)', 'info');
            addOutput('vuln scan [url]      - Vulnerability scan', 'info');
            addOutput('info [target]        - Get target information', 'info');
            addOutput('utils                - Show utilities', 'info');
            addOutput('clear                - Clear terminal', 'info');
        }
        
        async function startPortScan(target = null) {
            if (!target) {
                target = prompt('Enter target (IP or domain):', 'example.com');
                if (!target) return;
            }
            
            addOutput(`Starting port scan on ${target}...`, 'scanning');
            
            try {
                const response = await fetch('/scan/ports', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: target})
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addOutput(`Error: ${data.error}`, 'error');
                    return;
                }
                
                addOutput(`Scan completed in ${data.scan_time}s`, 'success');
                addOutput(`Target: ${data.target} (${data.host})`, 'info');
                addOutput(`Open ports: ${data.open_ports.length}`, 'info');
                
                if (data.open_ports.length > 0) {
                    data.open_ports.forEach(port => {
                        addOutput(`  Port ${port} - ${getServiceName(port)}`, 'success');
                    });
                } else {
                    addOutput('No open ports found', 'warning');
                }
                
            } catch (error) {
                addOutput(`Scan failed: ${error.message}`, 'error');
            }
        }
        
        function getServiceName(port) {
            const services = {
                21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
                53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
                443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
                3389: 'RDP', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt'
            };
            return services[port] || 'Unknown';
        }
        
        async function startDirScan(url = null) {
            if (!url) {
                url = prompt('Enter URL:', 'http://example.com');
                if (!url) return;
            }
            
            addOutput(`Starting directory scan on ${url}...`, 'scanning');
            
            try {
                const response = await fetch('/scan/dir', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addOutput(`Error: ${data.error}`, 'error');
                    return;
                }
                
                addOutput(`Scan completed. Found ${data.found.length} paths`, 'success');
                
                if (data.found.length > 0) {
                    data.found.forEach(item => {
                        addOutput(`  ${item.path} (${item.status}) - ${item.url}`, 'success');
                    });
                } else {
                    addOutput('No accessible paths found', 'warning');
                }
                
            } catch (error) {
                addOutput(`Scan failed: ${error.message}`, 'error');
            }
        }
        
        async function startVulnScan(url = null) {
            if (!url) {
                url = prompt('Enter URL:', 'http://example.com');
                if (!url) return;
            }
            
            addOutput(`Starting vulnerability scan on ${url}...`, 'scanning');
            
            try {
                const response = await fetch('/scan/vuln', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addOutput(`Error: ${data.error}`, 'error');
                    return;
                }
                
                addOutput(`Vulnerability scan completed`, 'success');
                addOutput(`Vulnerabilities found: ${data.vulnerabilities.length}`, 'info');
                
                if (data.vulnerabilities.length > 0) {
                    data.vulnerabilities.forEach(vuln => {
                        addOutput(`  ${vuln.name} - ${vuln.risk} risk`, 'warning');
                    });
                } else {
                    addOutput('No vulnerabilities found', 'success');
                }
                
            } catch (error) {
                addOutput(`Scan failed: ${error.message}`, 'error');
            }
        }
        
        async function getTargetInfo(target = null) {
            if (!target) {
                target = prompt('Enter target:', 'example.com');
                if (!target) return;
            }
            
            addOutput(`Getting information for ${target}...`, 'scanning');
            
            try {
                const response = await fetch('/info', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: target})
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addOutput(`Error: ${data.error}`, 'error');
                    return;
                }
                
                addOutput(`Target information:`, 'success');
                for (const [key, value] of Object.entries(data)) {
                    if (value) {
                        addOutput(`  ${key}: ${value}`, 'info');
                    }
                }
                
            } catch (error) {
                addOutput(`Failed: ${error.message}`, 'error');
            }
        }
        
        function showUtils() {
            addOutput('<strong>Security Utilities:</strong>', 'info');
            addOutput('Hash Generator:', 'info');
            const text = prompt('Enter text to hash:', 'password123');
            if (text) {
                const md5 = CryptoJS.MD5(text).toString();
                const sha1 = CryptoJS.SHA1(text).toString();
                const sha256 = CryptoJS.SHA256(text).toString();
                
                addOutput(`  MD5: ${md5}`, 'info');
                addOutput(`  SHA1: ${sha1}`, 'info');
                addOutput(`  SHA256: ${sha256}`, 'info');
            }
        }
        
        // Handle keyboard shortcuts
        input.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (historyIndex > 0) {
                    historyIndex--;
                    input.value = commandHistory[historyIndex] || '';
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (historyIndex < commandHistory.length - 1) {
                    historyIndex++;
                    input.value = commandHistory[historyIndex] || '';
                } else {
                    historyIndex = commandHistory.length;
                    input.value = '';
                }
            }
        });
        
        // Initialize
        window.onload = function() {
            addOutput('Terminal Security Scanner v1.0', 'success');
            addOutput('Type "help" for available commands', 'info');
            addOutput('');
            input.focus();
        };
    </script>
    
    <!-- Include CryptoJS for hashing -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
</body>
</html>
'''

class Scanner:
    @staticmethod
    def scan_ports(target):
        try:
            open_ports = []
            start_time = time.time()
            
            # Resolve hostname
            try:
                host = socket.gethostbyname(target)
            except:
                host = target
            
            # Scan common ports
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                    993, 995, 3306, 3389, 5900, 8080, 8443]
            
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    if result == 0:
                        open_ports.append(port)
                except:
                    pass
            
            scan_time = round(time.time() - start_time, 2)
            return {
                "target": target,
                "host": host,
                "open_ports": open_ports,
                "scan_time": scan_time
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def scan_directories(url):
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            found = []
            paths = [
                "admin", "login", "dashboard", "panel", "wp-admin",
                "administrator", "api", "test", "backup", "config",
                "data", "db", "secret", "private", "cgi-bin",
                "robots.txt", ".git", ".env", "config.php"
            ]
            
            for path in paths:
                try:
                    test_url = f"{url.rstrip('/')}/{path}"
                    response = requests.get(test_url, timeout=2, verify=False)
                    if response.status_code < 400:
                        found.append({
                            "path": path,
                            "url": test_url,
                            "status": response.status_code
                        })
                except:
                    pass
            
            return {"url": url, "found": found}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def scan_vulnerabilities(url):
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            vulnerabilities = []
            
            # Check for common issues
            try:
                response = requests.get(url, timeout=5, verify=False)
                headers = response.headers
                
                # Check security headers
                security_headers = ["X-Frame-Options", "X-Content-Type-Options", 
                                  "X-XSS-Protection", "Content-Security-Policy"]
                
                for header in security_headers:
                    if header not in headers:
                        vulnerabilities.append({
                            "name": f"Missing {header}",
                            "risk": "Medium",
                            "description": f"Security header {header} is not set"
                        })
                
                # Check for common files
                common_files = ["robots.txt", ".env", "config.php", "wp-config.php"]
                for file in common_files:
                    try:
                        test_url = f"{url.rstrip('/')}/{file}"
                        resp = requests.get(test_url, timeout=2, verify=False)
                        if resp.status_code == 200:
                            vulnerabilities.append({
                                "name": f"Exposed {file}",
                                "risk": "High",
                                "description": f"Sensitive file {file} is publicly accessible"
                            })
                    except:
                        pass
                        
            except:
                vulnerabilities.append({
                    "name": "Connection failed",
                    "risk": "Info",
                    "description": "Could not connect to target"
                })
            
            return {"url": url, "vulnerabilities": vulnerabilities}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_info(target):
        try:
            info = {}
            
            # Get IP address
            try:
                ip = socket.gethostbyname(target)
                info["ip_address"] = ip
            except:
                info["ip_address"] = "Unknown"
            
            # Try to get HTTP info
            for protocol in ['https://', 'http://']:
                try:
                    url = protocol + target
                    response = requests.get(url, timeout=5, verify=False)
                    info["url"] = url
                    info["status"] = response.status_code
                    info["server"] = response.headers.get('Server', 'Not specified')
                    info["content_type"] = response.headers.get('Content-Type', 'Not specified')
                    break
                except:
                    continue
            
            return info
        except Exception as e:
            return {"error": str(e)}

# Flask routes
@app.route('/')
def index():
    return HTML

@app.route('/scan/ports', methods=['POST'])
def port_scan():
    data = request.json
    result = Scanner.scan_ports(data.get('target', ''))
    return jsonify(result)

@app.route('/scan/dir', methods=['POST'])
def dir_scan():
    data = request.json
    result = Scanner.scan_directories(data.get('url', ''))
    return jsonify(result)

@app.route('/scan/vuln', methods=['POST'])
def vuln_scan():
    data = request.json
    result = Scanner.scan_vulnerabilities(data.get('url', ''))
    return jsonify(result)

@app.route('/info', methods=['POST'])
def target_info():
    data = request.json
    result = Scanner.get_info(data.get('target', ''))
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
