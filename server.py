import os
import sys
import subprocess
import re

def main():
    port = os.environ.get("PORT", "10000")
    print(f"🚀 Starting application on port {port}")
    sys.stdout.flush()

    # Convert notebooks
    notebooks = [
        "climaticscoring.ipynb",
        "Financial_risk_tool.ipynb", 
        "prediction.ipynb"
    ]
    
    for nb in notebooks:
        print(f"📄 Converting {nb}...")
        subprocess.run([
            sys.executable, "-m", "nbconvert",
            "--to", "script",
            nb
        ], check=False)

    # Fix imports in all files
    py_files = ["climaticscoring.py", "Financial_risk_tool.py", "prediction.py"]
    
    for py_file in py_files:
        if not os.path.exists(py_file):
            continue
        try:
            with open(py_file, "r") as f:
                content = f.read()
            content = re.sub(r'^import import_ipynb.*$', '', content, flags=re.MULTILINE)
            content = content.replace("as fr as fr", "as fr")
            with open(py_file, "w") as f:
                f.write(content)
        except Exception as e:
            print(f"⚠️ Could not fix {py_file}: {e}")

    # CRITICAL FIX: Modify prediction.py to bind to 0.0.0.0
    try:
        with open("prediction.py", "r") as f:
            content = f.read()
        
        # Replace the app.run line with the correct host and port
        # Look for app.run(debug=True, port=8051) or similar
        pattern = r'app\.run\s*\([^)]*\)'
        replacement = f'app.run(debug=False, host="0.0.0.0", port={port})'
        content = re.sub(pattern, replacement, content)
        
        # Also handle if app.run is on multiple lines
        content = re.sub(r'app\.run\s*\(\s*debug\s*=\s*True\s*,\s*port\s*=\s*8051\s*\)', 
                         f'app.run(debug=False, host="0.0.0.0", port={port})', 
                         content)
        
        with open("prediction.py", "w") as f:
            f.write(content)
        print(f"✅ Fixed app.run() to bind to 0.0.0.0:{port}")
    except Exception as e:
        print(f"⚠️ Could not fix app.run(): {e}")

    # Run the app
    cmd = [
        sys.executable,
        "prediction.py"
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
