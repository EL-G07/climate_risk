import os
import subprocess
import sys

def main():
    # Get the port Render wants us to use
    try:
        port = int(os.environ.get("PORT", 10000))
    except ValueError:
        port = 10000

    print(f"🚀 Starting Voilà on port {port}")

    # This is the key command with explicit binding to 0.0.0.0
    cmd = [
        "voila",
        "prediction.ipynb",
        "--port", str(port),
        "--no-browser",
        "--VoilaConfiguration.ip=0.0.0.0",
        "--VoilaConfiguration.port=" + str(port),
        # Additional options to ensure it binds correctly
        "--VoilaConfiguration.base_url=/",
        "--VoilaConfiguration.file_whitelist=['.*']"
    ]

    print(f"Running: {' '.join(cmd)}")
    sys.stdout.flush()  # Ensure logs are sent to Render immediately

    try:
        # Run the command and wait for it to finish
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Voilà failed with error code: {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()