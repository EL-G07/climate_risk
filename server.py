import os
import sys
import subprocess

def main():
    # Get the port from Render's environment
    port = os.environ.get("PORT", "10000")
    print(f"🚀 Starting Voilà on port {port}")
    sys.stdout.flush()

    # Build the command
    cmd = [
        "voila",
        "prediction.ipynb",
        f"--port={port}",
        "--no-browser"
    ]

    print(f"Running: {' '.join(cmd)}")
    sys.stdout.flush()

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
