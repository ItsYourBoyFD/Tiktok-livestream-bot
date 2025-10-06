import os
import sys
from functools import lru_cache

def clearConsole():
    """Clear console with optimized OS detection."""
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')

def setConsoleTitle(Content):
    """Set console title with optimized OS detection."""
    if os.name == 'posix':
        sys.stdout.write(f"\33]0;{Content}\a")
        sys.stdout.flush()
    elif os.name == 'nt':
        os.system(f"title {Content}")

@lru_cache(maxsize=1)
def readFile(filename, method):
    """Read file with caching for frequently accessed files.
    
    Note: Only use caching for read-only files that don't change.
    """
    with open(filename, method, encoding='utf8') as f:
        content = [line.strip('\n') for line in f]
    return content

def readProxiesFile():
    """Optimized proxy file reading with better error handling."""
    path = os.path.join("Data", "Proxies.txt")
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Use optimized file reading
            with open(path, 'r', encoding='utf8') as f:
                # Use list comprehension for better performance
                proxies = [line.strip() for line in f if line.strip()]
            
            if not proxies:
                print(f"⚠ Warning: Proxies.txt is empty!")
                return []
            
            print(f"✓ Loaded {len(proxies):,} proxies from {path}")
            return proxies
            
        except FileNotFoundError:
            print(f"✗ Error: {path} not found!")
            retry_count += 1
            if retry_count >= max_retries:
                print("Creating empty Proxies.txt file...")
                os.makedirs("Data", exist_ok=True)
                with open(path, 'w', encoding='utf8') as f:
                    f.write("")
                return []
        except Exception as e:
            print(f"✗ Error reading Proxies.txt: {e}")
            retry_count += 1
    
    return []
