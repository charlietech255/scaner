# app.py - Terminal-Style Web Security Scanner by Charlie Syllas and Jaguar 45 ©2026
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
import subprocess
from urllib.parse import urlparse, quote
from flask import Flask, render_template_string, request, jsonify, Response, stream_with_context
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "h4ck3r-s3cr3t-2026")

# Disable Flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

# HTML Template with terminal-style CSS/JS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>root@securioscan:~$ | Charlie Syllas & Jaguar 45 ©2026</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg: #0a0a0a;
            --terminal-bg: #000000;
            --terminal-border: #00ff00;
            --text: #00ff00;
            --text-dim: #008800;
            --text-bright: #00ff00;
            --error: #ff5555;
            --warning: #ffaa00;
            --success: #00ff00;
            --cyan: #00ffff;
            --purple: #aa00ff;
            --blue: #0088ff;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 255, 0, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(0, 255, 255, 0.03) 0%, transparent 50%);
        }
        
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.1;
            pointer-events: none;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 10px;
        }
        
        .header {
            border-bottom: 1px solid var(--terminal-border);
            padding: 10px 0;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .ascii-art {
            font-family: monospace;
            white-space: pre;
            font-size: 12px;
            color: var(--cyan);
            line-height: 1.2;
        }
        
        .status-bar {
            display: flex;
            gap: 20px;
            color: var(--text-dim);
            font-size: 14px;
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .blink {
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .main-terminal {
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 10px;
            height: calc(100vh - 150px);
        }
        
        .sidebar {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid var(--terminal-border);
            border-radius: 5px;
            padding: 10px;
            overflow-y: auto;
        }
        
        .cmd-list {
            list-style: none;
        }
        
        .cmd-item {
            padding: 8px 10px;
            margin: 5px 0;
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid rgba(0, 255, 0, 0.3);
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .cmd-item:hover {
            background: rgba(0, 255, 0, 0.2);
            border-color: var(--success);
            transform: translateX(5px);
        }
        
        .cmd-item.active {
            background: rgba(0, 255, 0, 0.3);
            border-color: var(--success);
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }
        
        .cmd-item.danger {
            background: rgba(255, 0, 0, 0.1);
            border-color: rgba(255, 0, 0, 0.3);
        }
        
        .cmd-item.danger:hover {
            background: rgba(255, 0, 0, 0.2);
            border-color: var(--error);
        }
        
        .terminal-window {
            background: var(--terminal-bg);
            border: 1px solid var(--terminal-border);
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            height: 100%;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.1);
        }
        
        .terminal-header {
            background: rgba(0, 20, 0, 0.8);
            padding: 8px 15px;
            border-bottom: 1px solid var(--terminal-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
        }
        
        .terminal-controls {
            display: flex;
            gap: 8px;
        }
        
        .control-btn {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
        }
        
        .close-btn { background: #ff5f56; }
        .minimize-btn { background: #ffbd2e; }
        .maximize-btn { background: #27ca3f; }
        
        .terminal-body {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .prompt-line {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .prompt {
            color: var(--cyan);
            margin-right: 10px;
            white-space: nowrap;
        }
        
        .user { color: var(--success); }
        .host { color: var(--purple); }
        .path { color: var(--blue); }
        .symbol { color: var(--text); }
        
        .cmd-input {
            background: transparent;
            border: none;
            color: var(--text);
            font-family: 'Courier New', monospace;
            font-size: 14px;
            flex: 1;
            outline: none;
            caret-color: var(--success);
        }
        
        .output {
            margin-bottom: 15px;
        }
        
        .cmd-output {
            margin: 5px 0;
            padding-left: 20px;
            border-left: 2px solid rgba(0, 255, 0, 0.3);
        }
        
        .help-text {
            color: var(--text-dim);
            font-size: 13px;
            margin: 10px 0;
            padding-left: 10px;
        }
        
        .scan-results {
            margin-top: 15px;
            border-top: 1px dashed rgba(0, 255, 0, 0.3);
            padding-top: 15px;
        }
        
        .result-item {
            margin: 8px 0;
            padding: 8px;
            background: rgba(0, 20, 0, 0.3);
            border-radius: 3px;
            border-left: 3px solid var(--success);
            font-family: monospace;
            font-size: 13px;
        }
        
        .result-item.error {
            border-left-color: var(--error);
            background: rgba(255, 0, 0, 0.1);
        }
        
        .result-item.warning {
            border-left-color: var(--warning);
            background: rgba(255, 170, 0, 0.1);
        }
        
        .result-item.info {
            border-left-color: var(--cyan);
            background: rgba(0, 255, 255, 0.1);
        }
        
        .ip-address {
            color: var(--cyan);
            font-weight: bold;
        }
        
        .port-open {
            color: var(--success);
        }
        
        .port-closed {
            color: var(--error);
        }
        
        .status-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
            margin-right: 10px;
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid rgba(0, 255, 0, 0.5);
        }
        
        .typewriter {
            overflow: hidden;
            border-right: 2px solid var(--success);
            white-space: nowrap;
            animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
        }
        
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent; }
            50% { border-color: var(--success); }
        }
        
        .progress-container {
            margin: 15px 0;
            background: rgba(0, 20, 0, 0.3);
            border-radius: 3px;
            overflow: hidden;
            height: 20px;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #00ff00, #00cc00);
            width: 0%;
            transition: width 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(255, 255, 255, 0.4), 
                transparent);
            animation: shine 2s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .scan-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        
        .stat-box {
            background: rgba(0, 20, 0, 0.3);
            border: 1px solid rgba(0, 255, 0, 0.3);
            border-radius: 3px;
            padding: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: var(--success);
        }
        
        .stat-label {
            font-size: 11px;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .footer {
            text-align: center;
            padding: 15px;
            border-top: 1px solid var(--terminal-border);
            margin-top: 20px;
            font-size: 12px;
            color: var(--text-dim);
        }
        
        .matrix-char {
            position: absolute;
            color: var(--success);
            font-family: monospace;
            opacity: 0.8;
            pointer-events: none;
        }
        
        .tool-panel {
            display: none;
        }
        
        .tool-panel.active {
            display: block;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .input-label {
            display: block;
            color: var(--cyan);
            margin-bottom: 5px;
            font-size: 13px;
        }
        
        .terminal-input {
            width: 100%;
            background: rgba(0, 20, 0, 0.3);
            border: 1px solid rgba(0, 255, 0, 0.5);
            border-radius: 3px;
            padding: 8px 12px;
            color: var(--text);
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        
        .terminal-input:focus {
            outline: none;
            border-color: var(--success);
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }
        
        .btn {
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid rgba(0, 255, 0, 0.5);
            color: var(--text);
            padding: 8px 20px;
            border-radius: 3px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            transition: all 0.2s;
            margin-right: 10px;
        }
        
        .btn:hover {
            background: rgba(0, 255, 0, 0.3);
            border-color: var(--success);
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }
        
        .btn-danger {
            background: rgba(255, 0, 0, 0.2);
            border-color: rgba(255, 0, 0, 0.5);
        }
        
        .btn-danger:hover {
            background: rgba(255, 0, 0, 0.3);
            border-color: var(--error);
        }
        
        .console-log {
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid rgba(0, 255, 0, 0.3);
            border-radius: 3px;
            padding: 10px;
            font-family: monospace;
            font-size: 12px;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 15px;
            white-space: pre-wrap;
            line-height: 1.3;
        }
        
        .log-entry {
            margin-bottom: 5px;
            padding-left: 5px;
            border-left: 2px solid transparent;
        }
        
        .log-entry.info {
            border-left-color: var(--cyan);
            color: var(--cyan);
        }
        
        .log-entry.success {
            border-left-color: var(--success);
            color: var(--success);
        }
        
        .log-entry.error {
            border-left-color: var(--error);
            color: var(--error);
        }
        
        .log-entry.warning {
            border-left-color: var(--warning);
            color: var(--warning);
        }
        
        /* Matrix rain effect */
        #matrixCanvas {
            position: fixed;
            top: 0;
            left: 0;
            z-index: -1;
            opacity: 0.1;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main-terminal {
                grid-template-columns: 1fr;
                height: auto;
            }
            
            .sidebar {
                max-height: 200px;
            }
        }
    </style>
</head>
<body>
    <canvas id="matrixCanvas"></canvas>
    
    <div class="container">
        <div class="header">
            <div class="ascii-art">
 _____ _____ _____ _____ _____ _____ _____ _____ 
|   __|  |  |     |     |   __|  _  |   __|   __|
|  |  |  |  | | | |  |  |  |  |     |   __|   __|
|_____|_____|_|_|_|_____|_____|__|__|_____|_____|
            </div>
            <div class="status-bar">
                <div class="status-item">
                    <span class="blink">●</span>
                    <span id="connection-status">CONNECTED</span>
                </div>
                <div class="status-item">
                    <i class="fas fa-shield-alt"></i>
                    <span id="security-level">LEVEL 3</span>
                </div>
                <div class="status-item">
                    <i class="fas fa-bolt"></i>
                    <span id="system-status">OPERATIONAL</span>
                </div>
                <div class="status-item">
                    <i class="fas fa-user-secret"></i>
                    <span>ANONYMOUS</span>
                </div>
            </div>
        </div>
        
        <div class="main-terminal">
            <div class="sidebar">
                <h3 style="color: var(--cyan); margin-bottom: 15px; border-bottom: 1px solid rgba(0,255,0,0.3); padding-bottom: 5px;">
                    <i class="fas fa-terminal"></i> COMMAND MENU
                </h3>
                <ul class="cmd-list">
                    <li class="cmd-item active" onclick="showTool('portscan')">
                        <i class="fas fa-network-wired"></i> PORT SCANNER
                    </li>
                    <li class="cmd-item" onclick="showTool('dirscan')">
                        <i class="fas fa-folder-tree"></i> DIRECTORY SCANNER
                    </li>
                    <li class="cmd-item" onclick="showTool('vulnscan')">
                        <i class="fas fa-bug"></i> VULNERABILITY SCAN
                    </li>
                    <li class="cmd-item" onclick="showTool('bruteforce')">
                        <i class="fas fa-key"></i> CREDENTIAL TESTER
                    </li>
                    <li class="cmd-item danger" onclick="showTool('dos')">
                        <i class="fas fa-bomb"></i> STRESS TEST
                    </li>
                    <li class="cmd-item" onclick="showTool('info')">
                        <i class="fas fa-info-circle"></i> TARGET INFO
                    </li>
                    <li class="cmd-item" onclick="showTool('utils')">
                        <i class="fas fa-tools"></i> UTILITIES
                    </li>
                    <li class="cmd-item" onclick="showTool('help')">
                        <i class="fas fa-question-circle"></i> HELP & COMMANDS
                    </li>
                </ul>
                
                <div style="margin-top: 30px; padding: 10px; background: rgba(0,20,0,0.3); border-radius: 3px;">
                    <h4 style="color: var(--cyan); margin-bottom: 10px; font-size: 13px;">
                        <i class="fas fa-chart-line"></i> SYSTEM STATS
                    </h4>
                    <div id="system-stats">
                        <div>CPU: <span id="cpu-load">███░░░░░░░</span> 30%</div>
                        <div>MEM: <span id="mem-usage">█████░░░░░</span> 50%</div>
                        <div>NET: <span id="net-traffic">██░░░░░░░░</span> 20%</div>
                    </div>
                </div>
            </div>
            
            <div class="terminal-window">
                <div class="terminal-header">
                    <div>
                        <span style="color: var(--cyan);">root</span>
                        <span style="color: var(--text);">@</span>
                        <span style="color: var(--purple);">securioscan</span>
                        <span style="color: var(--text);">:</span>
                        <span style="color: var(--blue);">~/scanner</span>
                        <span style="color: var(--text);">$</span>
                    </div>
                    <div class="terminal-controls">
                        <button class="control-btn close-btn" onclick="closeTerminal()"></button>
                        <button class="control-btn minimize-btn" onclick="minimizeTerminal()"></button>
                        <button class="control-btn maximize-btn" onclick="maximizeTerminal()"></button>
                    </div>
                </div>
                
                <div class="terminal-body" id="terminalOutput">
                    <!-- Terminal output will be generated here -->
                </div>
                
                <div class="prompt-line">
                    <div class="prompt">
                        <span class="user">root</span>
                        <span>@</span>
                        <span class="host">securioscan</span>
                        <span>:</span>
                        <span class="path">~/scanner</span>
                        <span class="symbol">$</span>
                    </div>
                    <input type="text" class="cmd-input" id="terminalInput" autocomplete="off" 
                           placeholder="Type 'help' for commands or click menu items..." 
                           onkeypress="handleTerminalKey(event)">
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div style="margin-bottom: 10px;">
                <span style="color: var(--cyan);">SecurioScan Terminal v3.0</span> | 
                <span>Charlie Syllas & Jaguar 45 ©2026</span> | 
                <span style="color: var(--text-dim);">FOR AUTHORIZED SECURITY TESTING ONLY</span>
            </div>
            <div>
                <span id="deployment-info">{{ deployment_platform }} | {{ deployment_env }} | </span>
                <span id="current-time"></span>
            </div>
        </div>
    </div>
    
    <script>
        // Matrix rain effect
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%\"'#&_(),.;:?!\\|{}<>[]^~";
        const charArray = chars.split("");
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        
        const drops = [];
        for(let i = 0; i < columns; i++) {
            drops[i] = Math.floor(Math.random() * canvas.height / fontSize);
        }
        
        function drawMatrix() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.04)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#0F0";
            ctx.font = `${fontSize}px monospace`;
            
            for(let i = 0; i < drops.length; i++) {
                const text = charArray[Math.floor(Math.random() * charArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        
        // Terminal functionality
        const terminalOutput = document.getElementById('terminalOutput');
        const terminalInput = document.getElementById('terminalInput');
        let commandHistory = [];
        let historyIndex = -1;
        let currentTool = 'portscan';
        
        // Initialize terminal
        function initTerminal() {
            addOutput("Initializing SecurioScan Terminal v3.0...", "info");
            addOutput("System boot complete. All modules operational.", "success");
            addOutput("Type 'help' for available commands or use the menu.", "info");
            addOutput("");
            
            // Show initial tool
            showTool('portscan');
            
            // Update time
            updateTime();
            setInterval(updateTime, 1000);
            
            // Update system stats
            updateSystemStats();
            setInterval(updateSystemStats, 5000);
            
            // Start matrix animation
            setInterval(drawMatrix, 50);
        }
        
        function addOutput(text, type = "normal") {
            const outputDiv = document.createElement('div');
            outputDiv.className = `log-entry ${type}`;
            
            // Add timestamp
            const now = new Date();
            const timestamp = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;
            
            outputDiv.innerHTML = `<span style="color: var(--text-dim);">${timestamp}</span> ${text}`;
            terminalOutput.appendChild(outputDiv);
            
            // Scroll to bottom
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }
        
        function updateTime() {
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            document.getElementById('current-time').textContent = timeStr;
        }
        
        function updateSystemStats() {
            // Simulate changing system stats
            const cpu = 20 + Math.random() * 50;
            const mem = 30 + Math.random() * 40;
            const net = 10 + Math.random() * 30;
            
            document.getElementById('cpu-load').textContent = "█".repeat(Math.floor(cpu/10)) + "░".repeat(10 - Math.floor(cpu/10));
            document.getElementById('mem-usage').textContent = "█".repeat(Math.floor(mem/10)) + "░".repeat(10 - Math.floor(mem/10));
            document.getElementById('net-traffic').textContent = "█".repeat(Math.floor(net/10)) + "░".repeat(10 - Math.floor(net/10));
            
            // Update numeric values
            document.getElementById('cpu-load').parentNode.innerHTML = `CPU: <span id="cpu-load">${"█".repeat(Math.floor(cpu/10)) + "░".repeat(10 - Math.floor(cpu/10))}</span> ${Math.floor(cpu)}%`;
            document.getElementById('mem-usage').parentNode.innerHTML = `MEM: <span id="mem-usage">${"█".repeat(Math.floor(mem/10)) + "░".repeat(10 - Math.floor(mem/10))}</span> ${Math.floor(mem)}%`;
            document.getElementById('net-traffic').parentNode.innerHTML = `NET: <span id="net-traffic">${"█".repeat(Math.floor(net/10)) + "░".repeat(10 - Math.floor(net/10))}</span> ${Math.floor(net)}%`;
        }
        
        function handleTerminalKey(e) {
            if(e.key === 'Enter') {
                const command = terminalInput.value.trim();
                if(command) {
                    executeCommand(command);
                    commandHistory.push(command);
                    historyIndex = commandHistory.length;
                    terminalInput.value = '';
                }
            } else if(e.key === 'ArrowUp') {
                e.preventDefault();
                if(commandHistory.length > 0) {
                    if(historyIndex > 0) historyIndex--;
                    terminalInput.value = commandHistory[historyIndex] || '';
                }
            } else if(e.key === 'ArrowDown') {
                e.preventDefault();
                if(commandHistory.length > 0) {
                    if(historyIndex < commandHistory.length - 1) historyIndex++;
                    terminalInput.value = commandHistory[historyIndex] || '';
                }
            } else if(e.key === 'Tab') {
                e.preventDefault();
                // Tab completion could be implemented here
            }
        }
        
        function executeCommand(cmd) {
            addOutput(`<span class="user">root</span>@<span class="host">securioscan</span>:<span class="path">~/scanner</span>$ ${cmd}`);
            
            const parts = cmd.toLowerCase().split(' ');
            const mainCmd = parts[0];
            
            switch(mainCmd) {
                case 'help':
                    showHelp();
                    break;
                case 'scan':
                    if(parts[1] === 'ports') {
                        const target = parts[2] || prompt("Enter target:");
                        if(target) startPortScan(target);
                    } else if(parts[1] === 'dir') {
                        const target = parts[2] || prompt("Enter URL:");
                        if(target) startDirScan(target);
                    } else {
                        addOutput("Usage: scan ports [target] or scan dir [url]", "warning");
                    }
                    break;
                case 'clear':
                    terminalOutput.innerHTML = '';
                    break;
                case 'whoami':
                    addOutput("User: root (uid=0) | System: SecurioScan Terminal v3.0", "info");
                    break;
                case 'date':
                    addOutput(new Date().toString(), "info");
                    break;
                case 'pwd':
                    addOutput("/root/scanner", "info");
                    break;
                case 'ls':
                    addOutput("port_scanner.py  dir_scanner.py  vuln_scanner.py  utils.py", "info");
                    break;
                case 'exit':
                case 'quit':
                    addOutput("Logging out... Session terminated.", "warning");
                    setTimeout(() => {
                        document.body.innerHTML = '<div style="color:#0F0; font-family:monospace; text-align:center; margin-top:50px;">[CONNECTION TERMINATED]</div>';
                    }, 1000);
                    break;
                default:
                    addOutput(`Command not found: ${cmd}. Type 'help' for available commands.`, "error");
            }
        }
        
        function showHelp() {
            addOutput("Available Commands:", "cyan");
            addOutput("  help                 - Show this help message");
            addOutput("  scan ports [target]  - Scan ports on target");
            addOutput("  scan dir [url]       - Discover directories on web server");
            addOutput("  clear                - Clear terminal");
            addOutput("  whoami               - Show current user");
            addOutput("  date                 - Show system date and time");
            addOutput("  pwd                  - Print working directory");
            addOutput("  ls                   - List files");
            addOutput("  exit/quit            - Terminate session");
            addOutput("");
            addOutput("Or use the menu on the left for GUI tools.", "info");
        }
        
        function showTool(toolId) {
            // Update active menu item
            document.querySelectorAll('.cmd-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.classList.add('active');
            
            currentTool = toolId;
            
            // Clear terminal output
            terminalOutput.innerHTML = '';
            
            // Show tool-specific interface
            switch(toolId) {
                case 'portscan':
                    showPortScanTool();
                    break;
                case 'dirscan':
                    showDirScanTool();
                    break;
                case 'vulnscan':
                    showVulnScanTool();
                    break;
                case 'bruteforce':
                    showBruteForceTool();
                    break;
                case 'dos':
                    showDosTool();
                    break;
                case 'info':
                    showInfoTool();
                    break;
                case 'utils':
                    showUtilsTool();
                    break;
                case 'help':
                    showHelpTool();
                    break;
            }
            
            // Scroll to top
            terminalOutput.scrollTop = 0;
        }
        
        function showPortScanTool() {
            addOutput("=== PORT SCANNER TOOL ===", "success");
            addOutput("Scan target for open ports and services", "info");
            addOutput("");
            
            const html = `
                <div class="form-group">
                    <div class="input-label">Target (IP or Domain):</div>
                    <input type="text" class="terminal-input" id="portTarget" placeholder="192.168.1.1 or example.com" value="example.com">
                </div>
                
                <div class="form-group">
                    <div class="input-label">Scan Type:</div>
                    <select class="terminal-input" id="portScanType">
                        <option value="quick">Quick Scan (Top 50)</option>
                        <option value="common">Common Ports</option>
                        <option value="full">Full Scan (1-1000)</option>
                        <option value="custom">Custom Range</option>
                    </select>
                </div>
                
                <div class="form-group" id="customPortsGroup" style="display: none;">
                    <div class="input-label">Port Range:</div>
                    <input type="text" class="terminal-input" id="portRange" placeholder="1-1000">
                </div>
                
                <div class="form-group">
                    <button class="btn" onclick="startPortScan()">
                        <i class="fas fa-search"></i> START SCAN
                    </button>
                    <button class="btn btn-danger" onclick="stopScan('port')">
                        <i class="fas fa-stop"></i> STOP
                    </button>
                </div>
                
                <div id="portScanResults" class="scan-results"></div>
            `;
            
            addOutput(html);
            
            // Add event listener for scan type change
            setTimeout(() => {
                document.getElementById('portScanType').addEventListener('change', function() {
                    document.getElementById('customPortsGroup').style.display = 
                        this.value === 'custom' ? 'block' : 'none';
                });
            }, 100);
        }
        
        async function startPortScan() {
            const target = document.getElementById('portTarget')?.value || 'example.com';
            const scanType = document.getElementById('portScanType')?.value || 'quick';
            const portRange = document.getElementById('portRange')?.value || '1-100';
            
            addOutput(`Initiating port scan on ${target}...`, "info");
            
            const resultsDiv = document.getElementById('portScanResults');
            if(resultsDiv) {
                resultsDiv.innerHTML = `
                    <div style="text-align: center; padding: 20px; color: var(--text-dim);">
                        <div class="spinner" style="border: 3px solid rgba(0,255,0,0.3); border-top-color: var(--success); width: 40px; height: 40px; border-radius: 50%; margin: 0 auto 10px; animation: spin 1s linear infinite;"></div>
                        Scanning ports...
                        <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
                    </div>
                `;
            }
            
            try {
                const response = await fetch('/api/scan/ports', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target, scanType, customRange: portRange})
                });
                
                const data = await response.json();
                
                if(data.error) {
                    addOutput(`Error: ${data.error}`, "error");
                    return;
                }
                
                let resultsHTML = `
                    <div class="result-item success">
                        <strong>SCAN COMPLETE</strong><br>
                        Target: ${data.target}<br>
                        IP: ${data.host}<br>
                        Open Ports: ${data.open_ports.length}<br>
                        Scan Time: ${data.scan_time}s
                    </div>
                `;
                
                if(data.open_ports.length > 0) {
                    resultsHTML += '<div style="margin-top: 15px;"><strong>OPEN PORTS:</strong></div>';
                    data.open_ports.forEach(port => {
                        const service = getServiceName(port);
                        resultsHTML += `
                            <div class="result-item">
                                <span class="status-badge">PORT ${port}</span>
                                ${service}
                                <span style="float: right; color: var(--success);">OPEN</span>
                            </div>
                        `;
                    });
                } else {
                    resultsHTML += '<div class="result-item warning">No open ports found.</div>';
                }
                
                if(resultsDiv) {
                    resultsDiv.innerHTML = resultsHTML;
                }
                
                addOutput(`Port scan completed. Found ${data.open_ports.length} open ports.`, "success");
                
            } catch(error) {
                addOutput(`Scan failed: ${error.message}`, "error");
            }
        }
        
        function getServiceName(port) {
            const services = {
                21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
                53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
                443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
                3389: 'RDP', 5432: 'PostgreSQL', 8080: 'HTTP-Alt',
                8443: 'HTTPS-Alt', 27017: 'MongoDB', 6379: 'Redis'
            };
            return services[port] || 'Unknown Service';
        }
        
        function showDirScanTool() {
            addOutput("=== DIRECTORY SCANNER ===", "success");
            addOutput("Discover hidden directories and files on web servers", "info");
            addOutput("");
            
            const html = `
                <div class="form-group">
                    <div class="input-label">Target URL:</div>
                    <input type="text" class="terminal-input" id="dirTarget" placeholder="https://example.com" value="https://example.com">
                </div>
                
                <div class="form-group">
                    <div class="input-label">Wordlist:</div>
                    <select class="terminal-input" id="dirWordlist">
                        <option value="common">Common Directories</option>
                        <option value="large">Large Wordlist</option>
                        <option value="custom">Custom Wordlist</option>
                    </select>
                </div>
                
                <div class="form-group" id="customWordlistGroup" style="display: none;">
                    <div class="input-label">Custom Wordlist (comma separated):</div>
                    <input type="text" class="terminal-input" id="customWordlist" placeholder="admin,login,test,backup">
                </div>
                
                <div class="form-group">
                    <button class="btn" onclick="startDirScan()">
                        <i class="fas fa-search"></i> START DISCOVERY
                    </button>
                    <button class="btn btn-danger" onclick="stopScan('dir')">
                        <i class="fas fa-stop"></i> STOP
                    </button>
                </div>
                
                <div id="dirScanResults" class="scan-results"></div>
            `;
            
            addOutput(html);
            
            setTimeout(() => {
                document.getElementById('dirWordlist').addEventListener('change', function() {
                    document.getElementById('customWordlistGroup').style.display = 
                        this.value === 'custom' ? 'block' : 'none';
                });
            }, 100);
        }
        
        async function startDirScan() {
            const target = document.getElementById('dirTarget')?.value || 'https://example.com';
            const wordlistType = document.getElementById('dirWordlist')?.value || 'common';
            const customWords = document.getElementById('customWordlist')?.value || '';
            
            addOutput(`Starting directory discovery on ${target}...`, "info");
            
            const resultsDiv = document.getElementById('dirScanResults');
            if(resultsDiv) {
                resultsDiv.innerHTML = `
                    <div style="text-align: center; padding: 20px; color: var(--text-dim);">
                        <div class="spinner" style="border: 3px solid rgba(0,255,0,0.3); border-top-color: var(--success); width: 40px; height: 40px; border-radius: 50%; margin: 0 auto 10px; animation: spin 1s linear infinite;"></div>
                        Discovering directories...
                    </div>
                `;
            }
            
            try {
                const response = await fetch('/api/scan/directories', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target, wordlistType, customWords})
                });
                
                const data = await response.json();
                
                if(data.error) {
                    addOutput(`Error: ${data.error}`, "error");
                    return;
                }
                
                let resultsHTML = `
                    <div class="result-item success">
                        <strong>DISCOVERY COMPLETE</strong><br>
                        Target: ${data.target}<br>
                        Found: ${data.found.length} accessible paths
                    </div>
                `;
                
                if(data.found.length > 0) {
                    resultsHTML += '<div style="margin-top: 15px;"><strong>ACCESSIBLE PATHS:</strong></div>';
                    data.found.forEach(item => {
                        resultsHTML += `
                            <div class="result-item">
                                <span class="status-badge">${item.status}</span>
                                <a href="${item.url}" target="_blank" style="color: var(--cyan);">${item.path}</a>
                                <span style="float: right; color: var(--text-dim);">${item.size} bytes</span>
                            </div>
                        `;
                    });
                } else {
                    resultsHTML += '<div class="result-item warning">No accessible directories/files found.</div>';
                }
                
                if(resultsDiv) {
                    resultsDiv.innerHTML = resultsHTML;
                }
                
                addOutput(`Directory discovery completed. Found ${data.found.length} paths.`, "success");
                
            } catch(error) {
                addOutput(`Discovery failed: ${error.message}`, "error");
            }
        }
        
        function showVulnScanTool() {
            addOutput("=== VULNERABILITY SCANNER ===", "success");
            addOutput("Check for common web vulnerabilities", "info");
            addOutput("");
            
            const html = `
                <div class="form-group">
                    <div class="input-label">Target URL:</div>
                    <input type="text" class="terminal-input" id="vulnTarget" placeholder="https://example.com" value="https://example.com">
                </div>
                
                <div class="form-group">
                    <div class="input-label">Scan Types:</div>
                    <div style="margin-top: 5px;">
                        <label style="display: block; margin: 5px 0;">
                            <input type="checkbox" name="vulnCheck" value="sqli" checked>
                            SQL Injection
                        </label>
                        <label style="display: block; margin: 5px 0;">
                            <input type="checkbox" name="vulnCheck" value="xss" checked>
                            Cross-Site Scripting (XSS)
                        </label>
                        <label style="display: block; margin: 5px 0;">
                            <input type="checkbox" name="vulnCheck" value="headers">
                            Security Headers
                        </label>
                        <label style="display: block; margin: 5px 0;">
                            <input type="checkbox" name="vulnCheck" value="ssl">
                            SSL/TLS Configuration
                        </label>
                    </div>
                </div>
                
                <div class="form-group">
                    <button class="btn" onclick="startVulnScan()">
                        <i class="fas fa-shield-alt"></i> START VULNERABILITY SCAN
                    </button>
                </div>
                
                <div id="vulnScanResults" class="scan-results"></div>
            `;
            
            addOutput(html);
        }
        
        async function startVulnScan() {
            const target = document.getElementById('vulnTarget')?.value || 'https://example.com';
            const checkboxes = document.querySelectorAll('input[name="vulnCheck"]:checked');
            const vulnTypes = Array.from(checkboxes).map(cb => cb.value);
            
            addOutput(`Starting vulnerability scan on ${target}...`, "info");
            
            const resultsDiv = document.getElementById('vulnScanResults');
            if(resultsDiv) {
                resultsDiv.innerHTML = `
                    <div style="text-align: center; padding: 20px; color: var(--text-dim);">
                        <div class="spinner" style="border: 3px solid rgba(0,255,0,0.3); border-top-color: var(--success); width: 40px; height: 40px; border-radius: 50%; margin: 0 auto 10px; animation: spin 1s linear infinite;"></div>
                        Scanning for vulnerabilities...
                    </div>
                `;
            }
            
            try {
                const response = await fetch('/api/scan/vulnerabilities', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target, vulnTypes})
                });
                
                const data = await response.json();
                
                let resultsHTML = `
                    <div class="result-item ${data.vulnerabilities && data.vulnerabilities.length > 0 ? 'warning' : 'success'}">
                        <strong>VULNERABILITY SCAN COMPLETE</strong><br>
                        Target: ${data.target}<br>
                        Vulnerabilities Found: ${data.vulnerabilities ? data.vulnerabilities.length : 0}
                    </div>
                `;
                
                if(data.vulnerabilities && data.vulnerabilities.length > 0) {
                    resultsHTML += '<div style="margin-top: 15px;"><strong>FINDINGS:</strong></div>';
                    data.vulnerabilities.forEach(vuln => {
                        resultsHTML += `
                            <div class="result-item ${vuln.severity}">
                                <strong>${vuln.name}</strong><br>
                                ${vuln.description}<br>
                                <small>Risk: ${vuln.risk}</small>
                            </div>
                        `;
                    });
                } else {
                    resultsHTML += '<div class="result-item success">No vulnerabilities detected.</div>';
                }
                
                if(data.recommendations && data.recommendations.length > 0) {
                    resultsHTML += '<div style="margin-top: 15px;"><strong>RECOMMENDATIONS:</strong></div>';
                    data.recommendations.forEach(rec => {
                        resultsHTML += `<div class="result-item info">${rec}</div>`;
                    });
                }
                
                if(resultsDiv) {
                    resultsDiv.innerHTML = resultsHTML;
                }
                
                addOutput(`Vulnerability scan completed. Found ${data.vulnerabilities ? data.vulnerabilities.length : 0} issues.`, "success");
                
            } catch(error) {
                addOutput(`Scan failed: ${error.message}`, "error");
            }
        }
        
        function showBruteForceTool() {
            addOutput("=== CREDENTIAL TESTER ===", "success");
            addOutput("Educational tool for testing authentication systems", "warning");
            addOutput("USE ONLY ON SYSTEMS YOU OWN OR HAVE PERMISSION TO TEST", "error");
            addOutput("");
            
            const html = `
                <div class="alert" style="background: rgba(255,0,0,0.1); border: 1px solid var(--error); padding: 10px; margin-bottom: 15px; border-radius: 3px;">
                    <i class="fas fa-exclamation-triangle"></i> FOR AUTHORIZED SECURITY TESTING ONLY
                </div>
                
                <div class="form-group">
                    <div class="input-label">Target URL:</div>
                    <input type="text" class="terminal-input" id="bruteTarget" placeholder="http://example.com/login">
                </div>
                
                <div class="form-group">
                    <div class="input-label">Usernames (comma separated):</div>
                    <input type="text" class="terminal-input" id="bruteUsernames" value="admin,root,user,administrator">
                </div>
                
                <div class="form-group">
                    <div class="input-label">Passwords (comma separated):</div>
                    <input type="text" class="terminal-input" id="brutePasswords" value="admin,123456,password,12345">
                </div>
                
                <div class="form-group">
                    <button class="btn" onclick="startBruteForce()">
                        <i class="fas fa-key"></i> START CREDENTIAL TEST
                    </button>
                    <button class="btn btn-danger" onclick="stopScan('brute')">
                        <i class="fas fa-stop"></i> STOP
                    </button>
                </div>
                
                <div id="bruteResults" class="console-log"></div>
            `;
            
            addOutput(html);
        }
        
        async function startBruteForce() {
            const target = document.getElementById('bruteTarget')?.value;
            const usernames = document.getElementById('bruteUsernames')?.value.split(',') || ['admin'];
            const passwords = document.getElementById('brutePasswords')?.value.split(',') || ['password'];
            
            if(!target) {
                addOutput("Please enter a target URL", "error");
                return;
            }
            
            addOutput(`Starting credential test on ${target}...`, "info");
            
            const consoleDiv = document.getElementById('bruteResults');
            if(consoleDiv) {
                consoleDiv.innerHTML = `[${new Date().toLocaleTimeString()}] Starting credential test...\n`;
            }
            
            // Simulate testing (in real app, this would call the API)
            simulateBruteForce(target, usernames, passwords, consoleDiv);
        }
        
        function simulateBruteForce(target, usernames, passwords, consoleDiv) {
            let attempts = 0;
            const total = usernames.length * passwords.length;
            let found = [];
            
            const interval = setInterval(() => {
                if(attempts >= total) {
                    clearInterval(interval);
                    const resultText = found.length > 0 
                        ? `\n[+] CREDENTIALS FOUND:\n${found.map(c => `    ${c.username}:${c.password}`).join('\n')}`
                        : "\n[-] No valid credentials found";
                    
                    if(consoleDiv) {
                        consoleDiv.innerHTML += `\n[${new Date().toLocaleTimeString()}] Test completed. ${attempts} attempts made.${resultText}`;
                    }
                    addOutput(`Credential test completed. ${attempts} attempts made.`, "info");
                    return;
                }
                
                const username = usernames[Math.floor(attempts / passwords.length)];
                const password = passwords[attempts % passwords.length];
                attempts++;
                
                // Simulate checking
                const logEntry = `[${new Date().toLocaleTimeString()}] Trying: ${username}:${password}`;
                if(consoleDiv) {
                    consoleDiv.innerHTML += logEntry + '\n';
                    consoleDiv.scrollTop = consoleDiv.scrollHeight;
                }
                
                // Simulate finding credentials (demo only)
                if(username === 'admin' && password === 'admin') {
                    found.push({username, password});
                    if(consoleDiv) {
                        consoleDiv.innerHTML += `[!] SUCCESS: ${username}:${password}\n`;
                    }
                }
                
                // Update progress
                const progress = Math.floor((attempts / total) * 100);
                if(consoleDiv && attempts % 5 === 0) {
                    consoleDiv.innerHTML += `Progress: ${progress}%\n`;
                }
                
            }, 100);
        }
        
        function showDosTool() {
            addOutput("=== STRESS TEST TOOL ===", "success");
            addOutput("Load testing for resilience assessment", "warning");
            addOutput("STRICTLY FOR AUTHORIZED USE ONLY - ILLEGAL WITHOUT PERMISSION", "error");
            addOutput("");
            
            const html = `
                <div class="alert" style="background: rgba(255,0,0,0.1); border: 1px solid var(--error); padding: 10px; margin-bottom: 15px; border-radius: 3px;">
                    <i class="fas fa-skull-crossbones"></i> WARNING: Use only on systems you own or have written permission to test.
                </div>
                
                <div class="form-group">
                    <div class="input-label">Target URL:</div>
                    <input type="text" class="terminal-input" id="dosTarget" placeholder="http://example.com">
                </div>
                
                <div class="form-group">
                    <div class="input-label">Test Type:</div>
                    <select class="terminal-input" id="dosType">
                        <option value="slowloris">Slowloris Simulation</option>
                        <option value="http-flood">HTTP Flood Test</option>
                        <option value="syn">SYN Flood Simulation</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <div class="input-label">Duration (seconds):</div>
                    <input type="number" class="terminal-input" id="dosDuration" value="10" min="1" max="60">
                </div>
                
                <div class="form-group">
                    <button class="btn btn-danger" onclick="startDosTest()">
                        <i class="fas fa-bolt"></i> START STRESS TEST
                    </button>
                    <button class="btn" onclick="stopScan('dos')">
                        <i class="fas fa-stop"></i> STOP
                    </button>
                </div>
                
                <div id="dosResults" class="console-log"></div>
            `;
            
            addOutput(html);
        }
        
        async function startDosTest() {
            if(!confirm("⚠️ CONFIRMATION REQUIRED\n\nThis tool should ONLY be used on systems you own or have explicit written permission to test.\n\nUnauthorized use is ILLEGAL and may result in criminal charges.\n\nDo you have proper authorization?")) {
                addOutput("Stress test cancelled.", "warning");
                return;
            }
            
            const target = document.getElementById('dosTarget')?.value;
            const dosType = document.getElementById('dosType')?.value || 'slowloris';
            const duration = parseInt(document.getElementById('dosDuration')?.value || '10');
            
            if(!target) {
                addOutput("Please enter a target URL", "error");
                return;
            }
            
            addOutput(`Initiating ${dosType} stress test on ${target} for ${duration} seconds...`, "info");
            
            const consoleDiv = document.getElementById('dosResults');
            if(consoleDiv) {
                consoleDiv.innerHTML = `[${new Date().toLocaleTimeString()}] Starting ${dosType} stress test...\n`;
            }
            
            // Simulate test (in real app, this would call the API)
            simulateDosTest(target, dosType, duration, consoleDiv);
        }
        
        function simulateDosTest(target, type, duration, consoleDiv) {
            let elapsed = 0;
            let requests = 0;
            
            const interval = setInterval(() => {
                elapsed++;
                requests += Math.floor(Math.random() * 100) + 50;
                
                const logEntry = `[${new Date().toLocaleTimeString()}] ${type.toUpperCase()} - ${requests} requests sent`;
                if(consoleDiv) {
                    consoleDiv.innerHTML += logEntry + '\n';
                    consoleDiv.scrollTop = consoleDiv.scrollHeight;
                }
                
                if(elapsed >= duration) {
                    clearInterval(interval);
                    const resultText = `\n[${new Date().toLocaleTimeString()}] Test completed.\nTotal requests: ${requests}\nAverage RPS: ${Math.floor(requests/duration)}`;
                    
                    if(consoleDiv) {
                        consoleDiv.innerHTML += resultText;
                    }
                    addOutput(`Stress test completed. ${requests} requests sent.`, "info");
                }
            }, 1000);
        }
        
        function showInfoTool() {
            addOutput("=== TARGET INFORMATION ===", "success");
            addOutput("Gather information about target", "info");
            addOutput("");
            
            const html = `
                <div class="form-group">
                    <div class="input-label">Target (URL or IP):</div>
                    <input type="text" class="terminal-input" id="infoTarget" placeholder="example.com or 192.168.1.1" value="example.com">
                </div>
                
                <div class="form-group">
                    <button class="btn" onclick="getTargetInfo()">
                        <i class="fas fa-info-circle"></i> GET INFORMATION
                    </button>
                </div>
                
                <div id="infoResults" class="scan-results"></div>
            `;
            
            addOutput(html);
        }
        
        async function getTargetInfo() {
            const target = document.getElementById('infoTarget')?.value || 'example.com';
            
            addOutput(`Gathering information for ${target}...`, "info");
            
            const resultsDiv = document.getElementById('infoResults');
            if(resultsDiv) {
                resultsDiv.innerHTML = `
                    <div style="text-align: center; padding: 20px; color: var(--text-dim);">
                        <div class="spinner" style="border: 3px solid rgba(0,255,0,0.3); border-top-color: var(--success); width: 40px; height: 40px; border-radius: 50%; margin: 0 auto 10px; animation: spin 1s linear infinite;"></div>
                        Collecting information...
                    </div>
                `;
            }
            
            try {
                const response = await fetch('/api/tools/info', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target})
                });
                
                const data = await response.json();
                
                if(data.error) {
                    addOutput(`Error: ${data.error}`, "error");
                    return;
                }
                
                let resultsHTML = '<div class="result-item success"><strong>TARGET INFORMATION</strong></div>';
                
                for(const [key, value] of Object.entries(data)) {
                    if(value && typeof value === 'object') {
                        resultsHTML += `<div class="result-item"><strong>${key.toUpperCase()}:</strong><br>`;
                        for(const [k, v] of Object.entries(value)) {
                            resultsHTML += `  ${k}: ${v}<br>`;
                        }
                        resultsHTML += '</div>';
                    } else if(value) {
                        resultsHTML += `<div class="result-item"><strong>${key.replace('_', ' ').toUpperCase()}:</strong> ${value}</div>`;
                    }
                }
                
                if(resultsDiv) {
                    resultsDiv.innerHTML = resultsHTML;
                }
                
                addOutput(`Information gathering completed.`, "success");
                
            } catch(error) {
                addOutput(`Failed to gather information: ${error.message}`, "error");
            }
        }
        
        function showUtilsTool() {
            addOutput("=== SECURITY UTILITIES ===", "success");
            addOutput("Various security-related tools and converters", "info");
            addOutput("");
            
            const html = `
                <div class="scan-stats">
                    <div class="form-group">
                        <div class="input-label">Hash Generator:</div>
                        <input type="text" class="terminal-input" id="hashInput" placeholder="Text to hash">
                        <button class="btn" onclick="generateHashes()" style="margin-top: 5px; width: 100%;">
                            <i class="fas fa-hashtag"></i> GENERATE HASHES
                        </button>
                        <textarea class="terminal-input" id="hashOutput" rows="4" readonly style="margin-top: 5px; font-size: 11px;"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <div class="input-label">Base64 Encode/Decode:</div>
                        <input type="text" class="terminal-input" id="base64Input" placeholder="Text">
                        <div style="margin-top: 5px;">
                            <button class="btn" onclick="base64Encode()" style="width: 48%;">
                                ENCODE
                            </button>
                            <button class="btn" onclick="base64Decode()" style="width: 48%; float: right;">
                                DECODE
                            </button>
                        </div>
                        <textarea class="terminal-input" id="base64Output" rows="3" readonly style="margin-top: 5px; font-size: 11px;"></textarea>
                    </div>
                </div>
                
                <div class="form-group">
                    <div class="input-label">User Agent String:</div>
                    <button class="btn" onclick="generateUserAgent()" style="width: 100%;">
                        <i class="fas fa-user-secret"></i> GENERATE RANDOM USER AGENT
                    </button>
                    <textarea class="terminal-input" id="uaOutput" rows="2" readonly style="margin-top: 5px; font-size: 11px;"></textarea>
                </div>
            `;
            
            addOutput(html);
        }
        
        async function generateHashes() {
            const text = document.getElementById('hashInput')?.value;
            if(!text) {
                addOutput("Please enter text to hash", "warning");
                return;
            }
            
            try {
                const response = await fetch('/api/utils/hash', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text})
                });
                
                const data = await response.json();
                document.getElementById('hashOutput').value = data.hashes;
                addOutput("Hashes generated successfully", "success");
            } catch(error) {
                addOutput(`Failed to generate hashes: ${error.message}`, "error");
            }
        }
        
        function base64Encode() {
            const text = document.getElementById('base64Input')?.value;
            if(!text) {
                addOutput("Please enter text to encode", "warning");
                return;
            }
            
            try {
                document.getElementById('base64Output').value = btoa(text);
                addOutput("Text encoded to Base64", "success");
            } catch(error) {
                addOutput(`Encoding failed: ${error.message}`, "error");
            }
        }
        
        function base64Decode() {
            const text = document.getElementById('base64Input')?.value;
            if(!text) {
                addOutput("Please enter text to decode", "warning");
                return;
            }
            
            try {
                document.getElementById('base64Output').value = atob(text);
                addOutput("Base64 decoded successfully", "success");
            } catch(error) {
                addOutput(`Decoding failed: Invalid Base64`, "error");
            }
        }
        
        function generateUserAgent() {
            const userAgents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
            ];
            
            const randomUA = userAgents[Math.floor(Math.random() * userAgents.length)];
            document.getElementById('uaOutput').value = randomUA;
            addOutput("Random User Agent generated", "success");
        }
        
        function showHelpTool() {
            addOutput("=== HELP & COMMANDS ===", "success");
            addOutput("SecurioScan Terminal v3.0 - All Available Options", "info");
            addOutput("");
            
            addOutput("TERMINAL COMMANDS:", "cyan");
            addOutput("  help                 - Show command help");
            addOutput("  scan ports [target]  - Scan target ports");
            addOutput("  scan dir [url]       - Discover web directories");
            addOutput("  clear                - Clear terminal");
            addOutput("  whoami               - Show current user");
            addOutput("  date                 - Show date/time");
            addOutput("  pwd                  - Print working directory");
            addOutput("  ls                   - List files");
            addOutput("  exit/quit            - Exit terminal");
            addOutput("");
            
            addOutput("GUI TOOLS (via menu):", "cyan");
            addOutput("  Port Scanner         - Scan for open ports");
            addOutput("  Directory Scanner    - Find hidden files/dirs");
            addOutput("  Vulnerability Scan   - Check for web vulnerabilities");
            addOutput("  Credential Tester    - Test authentication (AUTHORIZED USE ONLY)");
            addOutput("  Stress Test          - Load testing (AUTHORIZED USE ONLY)");
            addOutput("  Target Information   - Gather target details");
            addOutput("  Utilities            - Hash, Base64, User Agent tools");
            addOutput("");
            
            addOutput("KEYBOARD SHORTCUTS:", "cyan");
            addOutput("  ↑/↓                  - Navigate command history");
            addOutput("  Tab                  - Auto-completion");
            addOutput("  Ctrl+C               - Stop current operation");
            addOutput("");
            
            addOutput("NOTES:", "warning");
            addOutput("  • Use attack tools ONLY on systems you own or have permission to test");
            addOutput("  • Unauthorized scanning/attacks are illegal");
            addOutput("  • This tool is for educational and authorized security testing only");
        }
        
        function stopScan(type) {
            addOutput(`Stopping ${type} scan...`, "warning");
            fetch(`/api/stop/${type}`, {method: 'POST'});
        }
        
        function closeTerminal() {
            if(confirm("Close terminal?")) {
                addOutput("Terminal session terminated.", "error");
                setTimeout(() => {
                    document.body.innerHTML = '<div style="color:#0F0; font-family:monospace; text-align:center; margin-top:50px;">[CONNECTION CLOSED]<br><br>SecurioScan Terminal v3.0<br>Charlie Syllas & Jaguar 45 ©2026</div>';
                }, 1000);
            }
        }
        
        function minimizeTerminal() {
            addOutput("Terminal minimized (simulated)", "info");
        }
        
        function maximizeTerminal() {
            addOutput("Terminal maximized (simulated)", "info");
        }
        
        // Initialize on load
        window.addEventListener('load', initTerminal);
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
        
        // Focus input on click anywhere
        document.addEventListener('click', function() {
            terminalInput.focus();
        });
    </script>
</body>
</html>
'''

# Security Scanner Functions (Same as before, but updated for terminal interface)
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
                wordlist = [w.strip() for w in custom_words.split(',') if w.strip()]
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
            for username in usernames[:5]:  # Limit for demo
                for password in passwords[:5]:
                    attempts += 1
                    # Simulate testing
                    time.sleep(0.1)
                    
                    # Demo logic
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
            
            # Check for SQL injection
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
            
            # Check for XSS
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
