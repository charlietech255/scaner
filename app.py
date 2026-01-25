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
                <d
