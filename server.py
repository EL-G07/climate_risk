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

    # Step 2: Fix imports in ALL converted Python files
    py_files = ["climaticscoring.py", "Financial_risk_tool.py", "prediction.py"]
    
    for py_file in py_files:
        if not os.path.exists(py_file):
            print(f"⚠️ {py_file} not found, skipping")
            continue
            
        try:
            with open(py_file, "r") as f:
                content = f.read()
            
            # Remove 'import import_ipynb' lines
            content = re.sub(r'^import import_ipynb.*$', '', content, flags=re.MULTILINE)
            
            # Fix duplicate import patterns
            content = re.sub(r'import Financial_risk_tool\s+(?:as\s+fr\s*)?', 'import Financial_risk_tool as fr', content)
            content = content.replace("as fr as fr", "as fr")
            content = content.replace("import import_ipynb", "# import_ipynb removed")
            
            with open(py_file, "w") as f:
                f.write(content)
            print(f"✅ Fixed imports in {py_file}")
        except Exception as e:
            print(f"⚠️ Could not fix {py_file}: {e}")

    # Step 3: Run the main app
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
