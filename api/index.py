from pathlib import Path
import sys

# Add the root directory to Python path
root_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(root_dir)

# Import your Streamlit app
from main import main

# Create a WSGI application
def app(environ, start_response):
    # Set up response headers
    headers = [
        ('Content-type', 'text/html; charset=utf-8'),
    ]
    
    try:
        # Run the Streamlit app
        main()
        status = '200 OK'
    except Exception as e:
        status = '500 Internal Server Error'
        print(f"Error: {str(e)}")
    
    start_response(status, headers)
    return [] 