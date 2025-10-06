import ssl
import time
import queue
import threading
import logging
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from http import cookiejar
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import weakref

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pystyle import Colorate, Colors, Write, Add, Center

# Fallback data in case Data module is missing
try:
    from Data.UserAgent import UserAgent
    from Data.Lists import DeviceTypes, Platforms, Channel, ApiDomain
except ImportError:
    # Fallback data
    UserAgent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    DeviceTypes = ["SM-G973F", "Pixel", "iPhone12,1"]
    Platforms = ["android", "ios"]
    Channel = ["googleplay", "appstore"]
    ApiDomain = ["api16-normal-c-useast1a.tiktokv.com", "api19-normal-c-useast1a.tiktokv.com"]

from utils import *
from performance_monitor import performance_monitor, record_request_result
from config import PERFORMANCE, NETWORK, APP
class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

# Configure logging
logging.basicConfig(level=logging.WARNING)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Optimized session with connection pooling and retry strategy
def create_optimized_session():
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "POST"],
        backoff_factor=0.1
    )
    
    # Configure HTTP adapter with connection pooling
    adapter = HTTPAdapter(
        pool_connections=100,
        pool_maxsize=100,
        max_retries=retry_strategy,
        pool_block=False
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.cookies.set_policy(BlockCookies())
    
    return session

# Global variables
countQueue = queue.Queue(maxsize=10000)  # Prevent unbounded growth
sentRequests = 0
completed = False
session_pool = weakref.WeakSet()  # Track sessions for cleanup

# Cache for random values to reduce computation overhead
@lru_cache(maxsize=1000)
def get_cached_random_values():
    """Pre-generate random values for better performance"""
    return {
        'platform': choice(Platforms),
        'os_version': randint(1, 12),
        'device_type': choice(DeviceTypes),
        'user_agent': choice(UserAgent),
        'app_name': choice(["tiktok_web", "musically_go"]),
        'device_id': randint(1000000000000000000, 9999999999999999999),
        'api_domain': choice(ApiDomain),
        'channel': choice(Channel)
    }

# Pre-computed header template for performance
BASE_HEADERS = {
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
}
def Banner():
    clearConsole()
    Banner1 = r"""
╔╦╗  ╦  ╦╔═  ╔═╗  ╦ ╦  ╔═╗  ╦═╗  ╔═╗
 ║   ║  ╠╩╗  ╚═╗  ╠═╣  ╠═╣  ╠╦╝  ║╣ 
 ╩   ╩  ╩ ╩  ╚═╝  ╩ ╩  ╩ ╩  ╩╚═  ╚═╝
        discord.gg/devcenter
"""

    Banner2 = r"""
  ,           ,
 /             \
((__-^^-,-^^-__))
 `-_---' `---_-'
  <__|o` 'o|__>
     \  `  /
      ): :(
      :o_o:
       "-" 
       """

    print(Center.XCenter(Colorate.Vertical(Colors.yellow_to_red, Add.Add(Banner2, Banner1, center=True), 2)))

def sendView():
    """Optimized view sending function with connection reuse and caching"""
    try:
        # Get or create session for this thread
        session = getattr(threading.current_thread(), 'session', None)
        if session is None:
            session = create_optimized_session()
            threading.current_thread().session = session
            session_pool.add(session)
        
        # Use cached random values for better performance
        values = get_cached_random_values()
        
        # Build proxy configuration
        proxy = {proxyType: f'{proxyType}://{choice(proxyList)}'}
        
        # Optimize headers creation
        headers = BASE_HEADERS.copy()
        headers["user-agent"] = values['user_agent']
        
        # Pre-format URI for better performance
        URI = (f"https://{values['api_domain']}/aweme/v1/aweme/stats/"
               f"?channel={values['channel']}&device_type={values['device_type']}"
               f"&device_id={values['device_id']}&os_version={values['os_version']}"
               f"&version_code=220400&app_name={values['app_name']}"
               f"&device_platform={values['platform']}&aid=1988")
        
        data = f"item_id={itemID}&play_delta=1"
        
        response = session.post(URI, headers=headers, data=data, 
                              proxies=proxy, timeout=PERFORMANCE.connection_timeout, verify=False)
        success = response.status_code < 400
        record_request_result(success)
        return success
        
    except requests.exceptions.RequestException as e:
        logging.debug(f"Request failed: {e}")
        record_request_result(False)
        return False
    except Exception as e:
        logging.error(f"Unexpected error in sendView: {e}")
        record_request_result(False)
        return False

def sendShare():
    """Optimized share sending function with connection reuse and caching"""
    try:
        # Get or create session for this thread
        session = getattr(threading.current_thread(), 'session', None)
        if session is None:
            session = create_optimized_session()
            threading.current_thread().session = session
            session_pool.add(session)
        
        # Use cached random values for better performance
        values = get_cached_random_values()
        
        # Build proxy configuration (if available)
        proxy = {proxyType: f'{proxyType}://{choice(proxyList)}'} if 'proxyList' in globals() else {}
        
        # Optimize headers creation
        headers = BASE_HEADERS.copy()
        headers["user-agent"] = values['user_agent']
        
        # Pre-format URI for better performance
        URI = (f"https://{values['api_domain']}/aweme/v1/aweme/stats/"
               f"?channel={values['channel']}&device_type={values['device_type']}"
               f"&device_id={values['device_id']}&os_version={values['os_version']}"
               f"&version_code=220400&app_name={values['app_name']}"
               f"&device_platform={values['platform']}&aid=1988")
        
        data = f"item_id={itemID}&share_delta=1"
        
        response = session.post(URI, headers=headers, data=data, 
                              proxies=proxy, timeout=PERFORMANCE.connection_timeout, verify=False)
        success = response.status_code < 400
        record_request_result(success)
        return success
        
    except requests.exceptions.RequestException as e:
        logging.debug(f"Request failed: {e}")
        record_request_result(False)
        return False
    except Exception as e:
        logging.error(f"Unexpected error in sendShare: {e}")
        record_request_result(False)
        return False

def clearURL(link):
    """Optimized URL parsing with better error handling"""
    try:
        parsedURL = urlparse(link)
        host = parsedURL.hostname.lower() if parsedURL.hostname else ""
        
        if host in ("vm.tiktok.com", "vt.tiktok.com"):
            # Use a temporary session for URL resolution
            temp_session = create_optimized_session()
            try:
                response = temp_session.head(link, verify=False, allow_redirects=True, timeout=5)
                UrlParsed = urlparse(response.url)
                path_parts = UrlParsed.path.split("/")
                return path_parts[3] if len(path_parts) > 3 else None
            finally:
                temp_session.close()
        else:
            path_parts = parsedURL.path.split("/")
            return path_parts[3] if len(path_parts) > 3 else None
            
    except Exception as e:
        logging.error(f"Error parsing URL {link}: {e}")
        return None

def proccessThread(sendProccess):
    """Optimized worker thread with better error handling"""
    thread_local_session = None
    try:
        while not completed:
            try:
                if sendProccess():
                    countQueue.put(1, timeout=1)  # Prevent blocking
            except queue.Full:
                # Queue is full, skip this iteration
                time.sleep(0.001)
            except Exception as e:
                logging.debug(f"Error in process thread: {e}")
                time.sleep(0.01)  # Brief pause on error
    finally:
        # Clean up thread-local session
        if hasattr(threading.current_thread(), 'session'):
            try:
                threading.current_thread().session.close()
            except:
                pass

def countThread():
    """Optimized counting thread with better performance"""
    global sentRequests, completed
    try:
        while True:
            try:
                countQueue.get(timeout=1)
                sentRequests += 1
                if amount > 0 and sentRequests >= amount:
                    completed = True
                    break
            except queue.Empty:
                if completed:
                    break
                continue
    except Exception as e:
        logging.error(f"Error in count thread: {e}")

def progressThread():
    """Optimized progress reporting with better accuracy"""
    last_requests = 0
    try:
        while not completed:
            start_time = time.time()
            start_requests = sentRequests
            
            time.sleep(1)
            
            end_time = time.time()
            end_requests = sentRequests
            
            elapsed = end_time - start_time
            requests_per_second = (end_requests - start_requests) / elapsed if elapsed > 0 else 0
            
            print(f"\r{end_requests} sent requests! {requests_per_second:.1f} req/sec", end="", flush=True)
            
            if completed:
                break
    except Exception as e:
        logging.error(f"Error in progress thread: {e}")

def cleanup_sessions():
    """Clean up all active sessions"""
    for session in list(session_pool):
        try:
            session.close()
        except:
            pass

def main():
    """Optimized main function with better resource management"""
    global itemID, proxyType, proxyList, amount
    
    try:
        clearConsole()
        Banner()
        
        # Get user input
        VideoURI = str(Write.Input("Video Link > ", Colors.yellow_to_red, interval=0.0001))
        amount = int(Write.Input("Amount (0=inf) > ", Colors.yellow_to_red, interval=0.0001))
        nThreads = int(Write.Input("Thread Amount > ", Colors.yellow_to_red, interval=0.0001))
        
        # Optimize thread count based on system capabilities
        import os
        max_threads = min(nThreads, os.cpu_count() * 4)  # Reasonable limit
        if max_threads != nThreads:
            print(f"Optimizing thread count from {nThreads} to {max_threads} for better performance")
            nThreads = max_threads
        
        clearConsole()
        Banner()
        
        sendType = int(Write.Input("[0] - Views\n[1] - Shares > ", Colors.yellow_to_red, interval=0.0001))
        clearConsole()
        Banner()
        
        # Parse video URL
        itemID = clearURL(VideoURI)
        if not itemID:
            print("Error: Could not parse video URL. Please check the link.")
            return
        
        # Proxy configuration
        proxy_types = {"0": "http", "1": "socks4", "2": "socks5"}
        while True:
            proxy_input = Write.Input("Select proxy type:\n[0] - http\n[1] - socks4\n[2] - socks5 > ", 
                                    Colors.yellow_to_red, interval=0.0001)
            if proxy_input in proxy_types:
                proxyType = proxy_types[proxy_input]
                break
            print("Invalid selection. Please choose 0, 1, or 2.")
        
        # Load proxies with error handling
        try:
            proxyList = readProxiesFile()
            if not proxyList:
                print("Warning: No proxies loaded. Performance may be affected.")
                proxyList = ["127.0.0.1:8080"]  # Fallback
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return
        
        clearConsole()
        Banner()
        
        print(Colorate.Horizontal(Colors.yellow_to_red, "Performance optimizations enabled"))
        print(Colorate.Horizontal(Colors.yellow_to_red, "Bot started! Check your video stats in 5 minutes!"))
        
        # Start performance monitoring
        if APP.enable_performance_monitoring:
            performance_monitor.start_monitoring(APP.progress_update_interval)
        
        # Select send function
        if sendType == 0:
            sendProcess = sendView
        elif sendType == 1:
            sendProcess = sendShare
        else:
            print(f"Error: Invalid send type {sendType}")
            return
        
        # Start monitoring threads
        count_thread = threading.Thread(target=countThread, daemon=True)
        progress_thread = threading.Thread(target=progressThread, daemon=True)
        
        count_thread.start()
        progress_thread.start()
        
        # Start worker threads with ThreadPoolExecutor for better management
        with ThreadPoolExecutor(max_workers=nThreads, thread_name_prefix="Worker") as executor:
            # Submit all worker tasks
            futures = [executor.submit(proccessThread, sendProcess) for _ in range(nThreads)]
            
            try:
                # Wait for completion or interruption
                while not completed:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nStopping bot...")
                completed = True
            
            # Wait for all threads to complete
            for future in futures:
                try:
                    future.result(timeout=5)
                except:
                    pass
        
        print(f"\nCompleted! Total requests sent: {sentRequests}")
        
        # Stop monitoring and print summary
        if APP.enable_performance_monitoring:
            performance_monitor.stop_monitoring()
            performance_monitor.print_summary()
            
            if APP.auto_export_performance_report:
                performance_monitor.export_metrics(APP.performance_report_filename)
        
    except Exception as e:
        logging.error(f"Error in main: {e}")
        print(f"An error occurred: {e}")
    finally:
        cleanup_sessions()
        if APP.enable_performance_monitoring:
            performance_monitor.stop_monitoring()

if __name__ == "__main__":
    main()
