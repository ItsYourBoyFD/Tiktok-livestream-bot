import os
import sys
import logging
from typing import List, Optional

# Configure logging
logger = logging.getLogger(__name__)

def clearConsole():
    """Optimized console clearing with better error handling"""
    try:
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
    except Exception as e:
        logger.error(f"Error clearing console: {e}")

def setConsoleTitle(content: str) -> bool:
    """Optimized console title setting with better error handling"""
    try:
        if os.name == 'posix':
            sys.stdout.write(f"\33]0;{content}\a")
            sys.stdout.flush()
            return True
        elif os.name == 'nt':
            os.system(f"title {content}")
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error setting console title: {e}")
        return False

def readFile(filename: str, method: str = 'r', encoding: str = 'utf-8') -> Optional[List[str]]:
    """Optimized file reading with better error handling and memory efficiency"""
    try:
        with open(filename, method, encoding=encoding) as f:
            # Use list comprehension for better memory efficiency
            content = [line.rstrip('\n\r') for line in f if line.strip()]
            return content
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return None
    except PermissionError:
        logger.error(f"Permission denied accessing file: {filename}")
        return None
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        return None

def readProxiesFile() -> List[str]:
    """Optimized proxy file reading with better error handling and retry logic"""
    path = os.path.join("Data", "Proxies.txt")
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            proxies = readFile(path, 'r')
            if proxies is not None:
                # Filter out empty lines and invalid proxies
                valid_proxies = [proxy.strip() for proxy in proxies if proxy.strip() and ':' in proxy]
                logger.info(f"Loaded {len(valid_proxies)} valid proxies")
                return valid_proxies
            else:
                logger.warning(f"Failed to read proxies file (attempt {retry_count + 1}/{max_retries})")
        except Exception as e:
            logger.error(f"Error reading proxies file (attempt {retry_count + 1}/{max_retries}): {e}")
        
        retry_count += 1
        if retry_count < max_retries:
            logger.info("Retrying in 2 seconds...")
            import time
            time.sleep(2)
    
    logger.error("Failed to load proxies after maximum retries")
    return []

def validate_proxy(proxy: str) -> bool:
    """Validate proxy format"""
    try:
        if ':' not in proxy:
            return False
        host, port = proxy.split(':', 1)
        if not host or not port.isdigit():
            return False
        return True
    except:
        return False

def get_system_info() -> dict:
    """Get system information for optimization"""
    import platform
    import psutil
    
    return {
        'platform': platform.system(),
        'python_version': platform.python_version(),
        'cpu_count': os.cpu_count(),
        'memory_total': psutil.virtual_memory().total if 'psutil' in sys.modules else 'Unknown',
        'memory_available': psutil.virtual_memory().available if 'psutil' in sys.modules else 'Unknown'
    }