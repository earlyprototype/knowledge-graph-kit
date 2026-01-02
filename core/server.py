"""
Simple HTTP server for viewing knowledge graph
Serves static files and provides API endpoints
"""

import http.server
import socketserver
from pathlib import Path
import json
import webbrowser
from threading import Timer
from functools import partial


class GraphHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with CORS enabled"""
    
    def end_headers(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


def start_server(port: int = 8000, directory: str = ".", open_browser: bool = True):
    """
    Start HTTP server for viewing knowledge graph
    
    Args:
        port: Port number (default 8000)
        directory: Directory to serve (default current)
        open_browser: Whether to open browser automatically
    """
    path = Path(directory).resolve()
    
    # Create server with the directory argument
    handler = partial(GraphHTTPHandler, directory=str(path))
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}/viewer.html"
            print(f"📊 Knowledge Graph Server")
            print(f"=" * 50)
            print(f"Server running at: http://localhost:{port}")
            print(f"Viewer URL: {url}")
            print(f"Serving files from: {path}")
            print(f"\nPress Ctrl+C to stop")
            print(f"=" * 50)
            
            # Open browser after short delay
            if open_browser:
                Timer(1.0, lambda: webbrowser.open(url)).start()
            
            httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"Try: python server.py --port {port + 1}")
        else:
            raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Start knowledge graph server')
    parser.add_argument('--port', type=int, default=8000, help='Port number')
    parser.add_argument('--directory', type=str, default=".", help='Directory to serve')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t open browser')
    
    args = parser.parse_args()
    
    start_server(args.port, args.directory, not args.no_browser)
