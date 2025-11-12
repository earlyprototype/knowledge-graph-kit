"""
Dual Server for Knowledge Graph Viewer with Gemini Chat

Launches two servers:
1. HTTP Server (port 8000) - Serves the knowledge graph viewer and static files
2. Flask API Server (port 8001) - Handles Gemini chat API requests

Usage:
    python start_server.py

Then open: http://localhost:8000/@Research/knowledge_graph/knowledge_graph_viewer.html
Press Ctrl+C to stop both servers.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import subprocess
from pathlib import Path

PORT = 8000
API_PORT = 8001

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to add CORS headers"""
    
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Suppress log messages or customize them
        print(f"[Server] {format % args}")

def check_gemini_config():
    """Check if Gemini configuration exists."""
    config_file = Path(__file__).parent / "gemini_config.json"
    template_file = Path(__file__).parent / "gemini_config.template.json"
    
    if not config_file.exists():
        print("\n⚠️  WARNING: Gemini configuration not found!")
        print(f"   File: {config_file}")
        print(f"\n   To enable chat functionality:")
        print(f"   1. Copy: {template_file}")
        print(f"   2. Rename to: gemini_config.json")
        print(f"   3. Add your Gemini API key from: https://makersuite.google.com/app/apikey")
        print(f"\n   Chat features will be disabled without configuration.\n")
        return False
    
    return True


def start_api_server():
    """Start the Flask API server in a subprocess."""
    api_script = Path(__file__).parent / "gemini_api_server.py"
    
    if not api_script.exists():
        print(f"\n✗ API server script not found: {api_script}")
        print("   Chat features will not be available.\n")
        return None
    
    try:
        # Start API server as subprocess
        process = subprocess.Popen(
            [sys.executable, str(api_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Wait a moment for server to start
        import time
        time.sleep(1)
        
        if process.poll() is None:
            print(f"✓ Gemini Chat API server started on port {API_PORT}")
            return process
        else:
            print(f"✗ API server failed to start")
            return None
            
    except Exception as e:
        print(f"✗ Failed to start API server: {e}")
        return None


def main():
    # Change to AI/_Research directory so we can serve @Research, .lia folders, etc.
    server_dir = Path(__file__).parent.parent.parent
    os.chdir(server_dir)
    
    print("=" * 60)
    print("Knowledge Graph Viewer with Gemini Chat")
    print("=" * 60)
    print(f"\nServer directory: {os.getcwd()}")
    
    # Check Gemini configuration
    gemini_configured = check_gemini_config()
    
    # Start API server
    api_process = None
    if gemini_configured:
        print(f"\nStarting Gemini Chat API server on port {API_PORT}...")
        api_process = start_api_server()
    
    # Start HTTP server
    print(f"\nStarting HTTP server on port {PORT}...")
    Handler = MyHTTPRequestHandler
    
    print(f"\n📊 Open in browser: http://localhost:{PORT}/@Research/knowledge_graph/knowledge_graph_viewer.html")
    print("\n✨ Features enabled:")
    print("   • Markdown paper summaries")
    print("   • Interactive knowledge graph")
    print("   • No CORS restrictions")
    
    if api_process:
        print("   • Gemini Chat AI assistant")
    else:
        print("   • Chat features disabled (see warnings above)")
    
    print("\n⚠️  Press Ctrl+C to stop both servers\n")
    print("=" * 60 + "\n")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        # Open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}/@Research/knowledge_graph/knowledge_graph_viewer.html')
            print("✓ Browser opened automatically\n")
        except:
            print("⚠️  Could not open browser automatically\n")
            print(f"Please open: http://localhost:{PORT}/@Research/knowledge_graph/knowledge_graph_viewer.html\n")
        
        print("Servers running... (Ctrl+C to stop)\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print("Stopping servers...")
            print("=" * 60)
            
            # Stop API server if running
            if api_process:
                print("Stopping API server...")
                api_process.terminate()
                try:
                    api_process.wait(timeout=3)
                    print("✓ API server stopped")
                except:
                    api_process.kill()
                    print("✓ API server force stopped")
            
            print("✓ HTTP server stopped")
            print("=" * 60)
            return

if __name__ == "__main__":
    main()

