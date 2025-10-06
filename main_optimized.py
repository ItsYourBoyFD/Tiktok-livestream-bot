import ssl
import time
import queue
import threading
import logging
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from http import cookiejar
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, Any
import gc

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pystyle import Colorate, Colors, Write, Add, Center

from Data.UserAgent import UserAgent
from Data.Lists import DeviceTypes, Platforms, Channel, ApiDomain
from utils import *
from performance_monitor import start_monitoring, stop_monitoring, increment_requests, get_performance_summary

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

class OptimizedTikTokBot:
    def __init__(self):
        self.session = self._create_optimized_session()
        self.count_queue = queue.Queue()
        self.sent_requests = 0
        self.completed = False
        self.lock = threading.Lock()
        
    def _create_optimized_session(self) -> requests.Session:
        """Create an optimized session with connection pooling and retry strategy"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Configure adapter with connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=100,
            pool_maxsize=100,
            pool_block=False
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Disable SSL warnings and configure cookies
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        ssl._create_default_https_context = ssl._create_unverified_context
        session.cookies.set_policy(BlockCookies())
        
        return session

    def _generate_request_data(self, item_id: str, request_type: str) -> Dict[str, Any]:
        """Generate optimized request data to avoid code duplication"""
        platform = choice(Platforms)
        os_version = randint(1, 12)
        device_type = choice(DeviceTypes)
        app_name = choice(["tiktok_web", "musically_go"])
        device_id = randint(1000000000000000000, 9999999999999999999)
        api_domain = choice(ApiDomain)
        channel = choice(Channel)
        
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": choice(UserAgent)
        }
        
        uri = f"https://{api_domain}/aweme/v1/aweme/stats/?channel={channel}&device_type={device_type}&device_id={device_id}&os_version={os_version}&version_code=220400&app_name={app_name}&device_platform={platform}&aid=1988"
        
        delta_type = "play_delta" if request_type == "view" else "share_delta"
        data = f"item_id={item_id}&{delta_type}=1"
        
        return {
            "uri": uri,
            "headers": headers,
            "data": data
        }

    def send_request(self, item_id: str, request_type: str, proxy: Optional[Dict] = None) -> bool:
        """Send optimized request with better error handling"""
        try:
            request_data = self._generate_request_data(item_id, request_type)
            
            response = self.session.post(
                request_data["uri"],
                headers=request_data["headers"],
                data=request_data["data"],
                proxies=proxy,
                timeout=5,
                verify=False
            )
            
            # Check response status
            if response.status_code == 200:
                return True
            else:
                logger.warning(f"Request failed with status code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.debug(f"Request failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False

    def clear_url(self, link: str) -> str:
        """Optimized URL clearing with better error handling"""
        try:
            parsed_url = urlparse(link)
            host = parsed_url.hostname.lower()
            
            if host in ["vm.tiktok.com", "vt.tiktok.com"]:
                response = self.session.head(link, verify=False, allow_redirects=True, timeout=5)
                url_parsed = urlparse(response.url)
                return url_parsed.path.split("/")[3]
            else:
                return parsed_url.path.split("/")[3]
        except Exception as e:
            logger.error(f"Error clearing URL: {e}")
            return ""

    def process_thread(self, item_id: str, request_type: str, proxy_list: list, proxy_type: str):
        """Optimized thread processing with better resource management"""
        while not self.completed:
            try:
                proxy = {proxy_type: f"{proxy_type}://{choice(proxy_list)}"} if proxy_list else None
                
                if self.send_request(item_id, request_type, proxy):
                    with self.lock:
                        self.sent_requests += 1
                        self.count_queue.put(1)
                        increment_requests()  # Track for performance monitoring
                        
            except Exception as e:
                logger.error(f"Thread error: {e}")
                time.sleep(0.1)  # Brief pause on error

    def count_thread(self, amount: int):
        """Optimized counting thread"""
        while True:
            try:
                self.count_queue.get()
                if amount > 0 and self.sent_requests >= amount:
                    self.completed = True
                    break
            except Exception as e:
                logger.error(f"Count thread error: {e}")

    def progress_thread(self):
        """Optimized progress monitoring"""
        while not self.completed:
            try:
                start_time = time.time()
                start_requests = self.sent_requests
                time.sleep(1)
                end_time = time.time()
                end_requests = self.sent_requests

                elapsed_time = end_time - start_time
                elapsed_requests = end_requests - start_requests
                requests_per_second = elapsed_requests / elapsed_time if elapsed_time > 0 else 0

                print(f"{self.sent_requests} sent requests! {requests_per_second:.2f} requests/second.", end="\r")
            except Exception as e:
                logger.error(f"Progress thread error: {e}")

    def run(self, video_uri: str, amount: int, n_threads: int, send_type: int, proxy_list: list, proxy_type: str):
        """Main execution method with optimized threading"""
        item_id = self.clear_url(video_uri)
        if not item_id:
            print("Error: Could not extract video ID from URL")
            return

        request_type = "view" if send_type == 0 else "share"
        
        # Start performance monitoring
        start_monitoring()
        
        # Start background threads
        threading.Thread(target=self.count_thread, args=(amount,), daemon=True).start()
        threading.Thread(target=self.progress_thread, daemon=True).start()

        # Use ThreadPoolExecutor for better thread management
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = []
            for _ in range(n_threads):
                future = executor.submit(
                    self.process_thread, 
                    item_id, 
                    request_type, 
                    proxy_list, 
                    proxy_type
                )
                futures.append(future)
            
            # Wait for completion or all threads to finish
            try:
                while not self.completed and any(not f.done() for f in futures):
                    time.sleep(0.1)
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                self.completed = True
            finally:
                # Clean up
                for future in futures:
                    future.cancel()
                
                # Stop performance monitoring
                stop_monitoring()
                
                # Print performance summary
                get_performance_summary()
                
                # Force garbage collection
                gc.collect()

def banner():
    """Optimized banner display"""
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

def main():
    """Optimized main function"""
    try:
        banner()
        
        # Get user input with validation
        video_uri = str(Write.Input("Video Link > ", Colors.yellow_to_red, interval=0.0001))
        if not video_uri.strip():
            print("Error: Video link cannot be empty")
            return
            
        amount = int(Write.Input("Amount (0=inf) > ", Colors.yellow_to_red, interval=0.0001))
        n_threads = int(Write.Input("Thread Amount > ", Colors.yellow_to_red, interval=0.0001))
        
        if n_threads <= 0:
            print("Error: Thread amount must be positive")
            return
            
        clearConsole()
        banner()
        
        send_type = int(Write.Input("[0] - Views\n[1] - Shares > ", Colors.yellow_to_red, interval=0.0001))
        if send_type not in [0, 1]:
            print("Error: Invalid send type")
            return
            
        clearConsole()
        banner()
        
        # Proxy selection with validation
        proxy_type = None
        while proxy_type is None:
            proxy_choice = Write.Input("Select proxy type:\n[0] - http\n[1] - socks4\n[2] - socks5 > ", Colors.yellow_to_red, interval=0.0001)
            if proxy_choice == "0":
                proxy_type = "http"
            elif proxy_choice == "1":
                proxy_type = "socks4"
            elif proxy_choice == "2":
                proxy_type = "socks5"
            else:
                print("Invalid proxy type selection")

        # Load proxies
        proxy_list = readProxiesFile()
        if not proxy_list:
            print("Warning: No proxies loaded, running without proxies")
            proxy_list = []

        clearConsole()
        banner()

        print(Colorate.Horizontal(Colors.yellow_to_red, f"Hits are not counted"))
        print(Colorate.Horizontal(Colors.yellow_to_red, f"Bot started! Check your video stats in 5 minutes !"))

        # Create and run bot
        bot = OptimizedTikTokBot()
        bot.run(video_uri, amount, n_threads, send_type, proxy_list, proxy_type)
        
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()