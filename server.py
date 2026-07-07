import os
import sys
import subprocess

def main():
    # Get the port from Render's environment
    port = os.environ.get("PORT", "10000")
    
    # Set the IP environment variable for Jupyter Server
    os.environ["JUPYTER_SERVER_IP"] = "0.0.0.0"
    
    print(f"🚀 Starting Voilà on port {port}")
    sys.stdout.flush()

    # Build the command - this is the simplest version
    cmd = [
        "voila",
        "prediction.ipynb",
        f"--port={port}",
        "--no-browser"
    ]

    print(f"Running: {' '.join(cmd)}")
    print(f"Environment JUPYTER_SERVER_IP: {os.environ.get('JUPYTER_SERVER_IP')}")
    sys.stdout.flush()

    try:
        # Run the command
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Voilà failed with error code: {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
