from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
from arbit import check_sports  # Import the check_sports function from arbit.py

# Function to start a simple HTTP server to bind the app to a port
def start_http_server():
    port = 8000  # You can change this to any available port
    handler = SimpleHTTPRequestHandler
    httpd = TCPServer(("0.0.0.0", port), handler)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

# Start the HTTP server in a separate thread so it doesn't block the bot's functionality
threading.Thread(target=start_http_server, daemon=True).start()

# Your bot's main functionality
if __name__ == "__main__":
    try:
        print("Starting arbitrage bot...")
        check_sports()  # Call the function to check for arbitrage opportunities
    except Exception as e:
        print(f"Critical error: {str(e)}")
