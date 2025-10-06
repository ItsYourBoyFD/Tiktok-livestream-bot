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
        logger.debug(f"Failed to clear console: {e}")

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
        logger.debug(f"Failed to set console title: {e}")
        return False

def readFile(filename: str, method: str, encoding: str = 'utf-8') -> Optional[List[str]]:
    """Optimized file reading with better error handling and memory efficiency"""
    try:
        with open(filename, method, encoding=encoding) as f:
            # Use list comprehension for better memory efficiency
            return [line.strip('\n') for line in f if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return None
    except PermissionError:
        logger.error(f"Permission denied: {filename}")
        return None
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        return None

def readProxiesFile() -> List[str]:
    """Optimized proxy file reading with retry logic and better error handling"""
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
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"Failed to read proxies file, retrying... ({retry_count}/{max_retries})")
                    time.sleep(1)
                else:
                    logger.error("Failed to read proxies file after all retries")
                    return []
        except Exception as e:
            retry_count += 1
            logger.error(f"Error reading proxies file (attempt {retry_count}): {e}")
            if retry_count < max_retries:
                time.sleep(1)
    
    return []

def validate_proxy(proxy: str) -> bool:
    """Validate proxy format"""
    if not proxy or ':' not in proxy:
        return False
    
    parts = proxy.split(':')
    if len(parts) != 2:
        return False
    
    try:
        int(parts[1])  # Check if port is numeric
        return True
    except ValueError:
        return False

def get_system_info() -> dict:
    """Get system information for performance monitoring"""
    import platform
    import psutil
    
    try:
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available
        }
    except ImportError:
        logger.warning("psutil not available for system monitoring")
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'cpu_count': os.cpu_count()
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {}