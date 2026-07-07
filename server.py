import os
import sys
import subprocess
import re

def main():
    port = os.environ.get("PORT", "10000")
    print(f"🚀 Starting application on port {port}")
    sys.stdout.flush()

    # Step 1: Convert ALL notebooks
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

    # Step 2: Fix imports in prediction.py (CORRECTED)
    try:
        with open("prediction.py", "r") as f:
            content = f.read()
        
        # Remove the import_ipynb line completely
        content = re.sub(r'^import import_ipynb.*$', '', content, flags=re.MULTILINE)
        
        # Remove any existing 'as fr' and add it correctly
        content = re.sub(r'import Financial_risk_tool\s+(?:as\s+fr\s*)?', 'import Financial_risk_tool as fr', content)
        
        # Remove any duplicate 'as fr' patterns
        content = content.replace("as fr as fr", "as fr")
        
        with open("prediction.py", "w") as f:
            f.write(content)
        print("✅ Imports fixed!")
    except Exception as e:
        print(f"⚠️ Could not fix imports: {e}")

    # Step 3: Run the app
    cmd = [
        sys.executable,
        "prediction.py",
        f"--port={port}",
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
