#!/usr/bin/env python3
"""
Setup verification script for TikTok Bot
Checks if all components are properly configured
"""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists."""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description} missing: {dirpath}")
        return False

def check_python_syntax(filepath):
    """Check if Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ Python syntax valid: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Could not check {filepath}: {e}")
        return True

def main():
    print("🔍 TikTok Bot Setup Verification")
    print("=" * 50)
    
    checks = []
    
    # Core Python files
    print("\n📝 Core Python Files:")
    checks.append(check_file("main.py", "CLI application"))
    checks.append(check_file("utils.py", "Utility functions"))
    checks.append(check_file("web_app.py", "Web application"))
    
    # Python syntax checks
    print("\n🐍 Python Syntax Validation:")
    if os.path.exists("main.py"):
        checks.append(check_python_syntax("main.py"))
    if os.path.exists("utils.py"):
        checks.append(check_python_syntax("utils.py"))
    if os.path.exists("web_app.py"):
        checks.append(check_python_syntax("web_app.py"))
    
    # Frontend files
    print("\n🌐 Frontend Files:")
    checks.append(check_directory("templates", "Templates directory"))
    checks.append(check_file("templates/index.html", "Main HTML"))
    checks.append(check_directory("static", "Static files directory"))
    checks.append(check_file("static/css/style.css", "Stylesheet"))
    checks.append(check_file("static/js/app.js", "JavaScript"))
    
    # Configuration files
    print("\n⚙️  Configuration Files:")
    checks.append(check_file("requirements.txt", "Dependencies"))
    checks.append(check_file("Dockerfile", "Docker image"))
    checks.append(check_file("docker-compose.yml", "Docker Compose"))
    checks.append(check_file("nginx.conf", "Nginx config"))
    checks.append(check_file("gunicorn_config.py", "Gunicorn config"))
    
    # Data directory
    print("\n📁 Data Directory:")
    checks.append(check_directory("Data", "Data directory"))
    checks.append(check_file("Data/Proxies.txt", "Proxies file"))
    
    # Startup scripts
    print("\n🚀 Startup Scripts:")
    checks.append(check_file("start.sh", "Linux/Mac startup"))
    checks.append(check_file("start.bat", "Windows startup"))
    
    # Documentation
    print("\n📚 Documentation:")
    checks.append(check_file("README.md", "Main readme"))
    checks.append(check_file("DEPLOYMENT.md", "Deployment guide"))
    checks.append(check_file("WEB_INTERFACE_GUIDE.md", "Web guide"))
    checks.append(check_file("PERFORMANCE_OPTIMIZATIONS.md", "Performance docs"))
    checks.append(check_file("QUICK_REFERENCE.md", "Quick reference"))
    
    # Check proxy file content
    print("\n🌐 Proxy Configuration:")
    if os.path.exists("Data/Proxies.txt"):
        with open("Data/Proxies.txt", 'r') as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            if lines:
                print(f"✅ Found {len(lines)} proxies")
            else:
                print(f"⚠️  No proxies found (add to Data/Proxies.txt)")
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\n📊 Verification Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    
    if passed == total:
        print("\n🎉 All checks passed! Your setup is complete.")
        print("\n🚀 Next steps:")
        print("   1. Add proxies to Data/Proxies.txt")
        print("   2. Run: ./start.sh (or start.bat on Windows)")
        print("   3. Open: http://localhost:5000")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
