import os
import sys
import subprocess
import time

def main():
    port = os.environ.get("PORT", "10000")
    print(f"🚀 Starting Jupyter Server on port {port}")
    sys.stdout.flush()

    # Step 1: Convert notebook to Python script
    print("📄 Converting notebook to Python script...")
    subprocess.run([
        sys.executable, "-m", "nbconvert",
        "--to", "script",
        "prediction.ipynb"
    ], check=True)

    # Step 2: Run the converted script with Jupyter's server
    print("🚀 Starting the application...")
    cmd = [
        sys.executable,
        "prediction.py",  # The converted script
        "--port=" + port,
        "--ip=0.0.0.0",   # This works with Jupyter!
        "--no-browser"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    sys.stdout.flush()
    
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
