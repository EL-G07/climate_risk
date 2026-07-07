import os
import sys
import subprocess

def main():
    port = os.environ.get("PORT", "10000")
    print(f"🚀 Starting application on port {port}")
    sys.stdout.flush()

    # Step 1: Convert ALL notebooks to Python scripts
    notebooks = [
        "climaticscoring.ipynb",
        "Financial_risk_tool.ipynb",
        "prediction.ipynb"
    ]
    
    for nb in notebooks:
        print(f"📄 Converting {nb} to script...")
        try:
            subprocess.run([
                sys.executable, "-m", "nbconvert",
                "--to", "script",
                nb
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error converting {nb}: {e.stderr.decode()}")
            # Continue even if one fails
    
    # Step 2: Fix the imports in prediction.py
    print("🔧 Fixing imports in prediction.py...")
    try:
        with open("prediction.py", "r") as f:
            content = f.read()
        
        # Remove the import_ipynb line
        content = content.replace("import import_ipynb", "# import_ipynb removed")
        content = content.replace("import Financial_risk_tool", "import Financial_risk_tool as fr")
        
        with open("prediction.py", "w") as f:
            f.write(content)
        print("✅ Imports fixed!")
    except Exception as e:
        print(f"⚠️ Could not fix imports: {e}")

    # Step 3: Run the main script with Jupyter server
    print("🚀 Starting the application...")
    cmd = [
        sys.executable,
        "prediction.py",
        "--port=" + port,
        "--ip=0.0.0.0",
        "--no-browser"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    sys.stdout.flush()
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
