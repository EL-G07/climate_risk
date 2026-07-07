import os
import subprocess
import sys
import time

def main():
    port = os.environ.get("PORT", "10000")
    print(f"🚀 Starting Voilà on port {port}")

    # The corrected, explicit command
    cmd = [
        "voila",
        "prediction.ipynb",
        f"--port={port}",
        "--no-browser",
        "--VoilaConfiguration.ip=0.0.0.0",
        f"--VoilaConfiguration.port={port}",
        "--VoilaConfiguration.base_url=/",
        "--VoilaConfiguration.file_whitelist=['.*']"
    ]

    print(f"Running: {' '.join(cmd)}")
    sys.stdout.flush()

    try:
        # Use Popen for better control and to keep the process alive
        process = subprocess.Popen(cmd)
        process.wait()
    except Exception as e:
        print(f"❌ Error starting Voilà: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()