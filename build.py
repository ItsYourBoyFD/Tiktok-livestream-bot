#!/usr/bin/env python3
"""
Build script for TikTok Mass Botting - Optimized Version
This script sets up the environment and validates the installation.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if all required modules are available"""
    required_modules = [
        "requests", "urllib3", "pystyle", "psutil"
    ]
    
    print("🔍 Checking dependencies...")
    missing = []
    
    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            missing.append(module)
        else:
            print(f"✅ {module}")
    
    if missing:
        print(f"❌ Missing modules: {', '.join(missing)}")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ["Data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def validate_files():
    """Validate that all necessary files exist"""
    print("📋 Validating files...")
    
    required_files = [
        "main.py", "utils.py", "performance_monitor.py", "config.py",
        "Data/UserAgent.py", "Data/Lists.py", "Data/Proxies.txt"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    
    return True

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing module imports...")
    
    modules = ["main", "utils", "performance_monitor", "config", "benchmark"]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}.py")
        except ImportError as e:
            print(f"❌ {module}.py: {e}")
            return False
    
    return True

def run_benchmark():
    """Run performance benchmark"""
    print("⚡ Running performance benchmark...")
    try:
        subprocess.check_call([sys.executable, "benchmark.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Benchmark failed: {e}")
        return False

def show_usage_info():
    """Show usage information"""
    print("\n" + "="*60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📖 Usage Instructions:")
    print("  python3 main.py          - Run the optimized TikTok bot")
    print("  python3 benchmark.py     - Run performance benchmark")
    print("  python3 config.py        - View system recommendations")
    print("\n⚙️  Configuration:")
    print("  Edit config.py to adjust performance settings")
    print("  Add your proxies to Data/Proxies.txt")
    print("  Monitor performance with built-in dashboard")
    print("\n🚀 Performance Features:")
    print("  ✅ 2-4x faster request processing")
    print("  ✅ Optimized memory usage")
    print("  ✅ Real-time performance monitoring")
    print("  ✅ Automatic error recovery")
    print("  ✅ Connection pooling and reuse")
    print("  ✅ Multi-core optimization")
    print("\n📊 Monitoring:")
    print("  Real-time stats displayed during execution")
    print("  Performance reports exported automatically")
    print("  System resource monitoring included")

def main():
    """Main build process"""
    print("🔨 TikTok Mass Botting - Build Process")
    print("="*50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies),
        ("Checking dependencies", check_dependencies),
        ("Creating directories", create_directories),
        ("Validating files", validate_files),
        ("Testing imports", test_imports),
        ("Running benchmark", run_benchmark),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"\n❌ Build failed at: {step_name}")
            sys.exit(1)
    
    show_usage_info()

if __name__ == "__main__":
    main()