import os
import sys
import logging
from pathlib import Path
from functools import lru_cache

def clearConsole():
    """Optimized console clearing function"""
    try:
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
    except Exception as e:
        logging.debug(f"Failed to clear console: {e}")

def setConsoleTitle(Content):
    """Optimized console title setting with error handling"""
    try:
        if os.name == 'posix':
            sys.stdout.write(f"\33]0;{Content}\a")
            sys.stdout.flush()
        elif os.name == 'nt':
            os.system(f"title {Content}")
    except Exception as e:
        logging.debug(f"Failed to set console title: {e}")

@lru_cache(maxsize=32)
def readFile(filename, method='r'):
    """Optimized file reading with caching and better error handling"""
    try:
        file_path = Path(filename)
        if not file_path.exists():
            logging.warning(f"File not found: {filename}")
            return []
        
        with open(file_path, method, encoding='utf8', errors='ignore') as f:
            content = [line.strip() for line in f if line.strip()]
            return content
    except Exception as e:
        logging.error(f"Error reading file {filename}: {e}")
        return []

def readProxiesFile():
    """Optimized proxy file reading with multiple fallback locations"""
    proxy_paths = [
        Path("Data") / "Proxies.txt",
        Path("proxies.txt"),
        Path("Proxies.txt"),
        Path("data") / "proxies.txt"
    ]
    
    for path in proxy_paths:
        try:
            if path.exists():
                proxies = readFile(str(path), 'r')
                if proxies:
                    logging.info(f"Loaded {len(proxies)} proxies from {path}")
                    return proxies
        except Exception as e:
            logging.debug(f"Failed to read proxies from {path}: {e}")
    
    # Generate some default proxies if none found
    logging.warning("No proxy file found, using default proxies")
    return [
        "127.0.0.1:8080",
        "127.0.0.1:3128",
        "127.0.0.1:1080"
    ]

def create_data_directory():
    """Create Data directory if it doesn't exist"""
    try:
        Path("Data").mkdir(exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create Data directory: {e}")
        return False