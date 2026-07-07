import os
import sys
import subprocess
import re

def main():
    port = os.environ.get("PORT", "10000")
    print(f"🚀 Starting application on port {port}")
    sys.stdout.flush()

    # Convert notebooks
    notebooks = ["climaticscoring.ipynb", "Financial_risk_tool.ipynb", "prediction.ipynb"]
    for nb in notebooks:
        print(f"📄 Converting {nb}...")
        subprocess.run([sys.executable, "-m", "nbconvert", "--to", "script", nb], check=False)

    # Fix imports
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

    # CRITICAL: Fix app.run() to bind to 0.0.0.0
    try:
        with open("prediction.py", "r") as f:
            content = f.read()
        content = re.sub(r'app\.run\s*\([^)]*\)', f'app.run(debug=False, host="0.0.0.0", port={port})', content)
        with open("prediction.py", "w") as f:
            f.write(content)
        print(f"✅ Fixed app.run() to bind to 0.0.0.0:{port}")
    except Exception as e:
        print(f"⚠️ Could not fix app.run(): {e}")

    # Run the app
    cmd = [sys.executable, "prediction.py"]
    print(f"Running: {' '.join(cmd)}")
    sys.stdout.flush()
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
