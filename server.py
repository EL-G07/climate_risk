import os
import sys
from traitlets.config import Config
from voila.app import Voila

if __name__ == "__main__":
    # Get the port from Render's environment
    port = int(os.environ.get("PORT", 10000))

    print(f"🚀 Starting Voilà on port {port}")

    # Create a configuration object
    c = Config()

    # Correctly set the IP and port for Voilà's ServerApp
    c.ServerApp.ip = '0.0.0.0'
    c.ServerApp.port = port
    c.ServerApp.open_browser = False

    # Launch Voilà with this configuration
    try:
        Voila().start(
            'prediction.ipynb',
            config=c
        )
    except Exception as e:
        print(f"❌ Error starting Voilà: {e}")
        sys.exit(1)