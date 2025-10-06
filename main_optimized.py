import ssl
import time
import queue
import threading
import concurrent.futures
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from http import cookiejar
from typing import Optional, List, Dict, Any
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pystyle import Colorate, Colors, Write, Add, Center

from Data.UserAgent import UserAgent
from Data.Lists import DeviceTypes, Platforms, Channel, ApiDomain
from utils import *

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

class OptimizedTikTokBot:
    """Optimized TikTok bot with improved performance and resource management"""
    
    def __init__(self):
        self.session = self._create_optimized_session()
        self.count_queue = queue.Queue()
        self.sent_requests = 0
        self.completed = False
        self.lock = threading.Lock()
        
        # Pre-computed values for better performance
        self.user_agents = UserAgent
        self.device_types = DeviceTypes
        self.platforms = Platforms
        self.channels = Channel
        self.api_domains = ApiDomain
        self.app_names = ["tiktok_web", "musically_go"]
        
        # Connection pool settings
        self.max_retries = 3
        self.timeout = 5
        
    def _create_optimized_session(self) -> requests.Session:
        """Create an optimized session with connection pooling and retry logic"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
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
        
        # Disable SSL warnings and verification (keeping original behavior)
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Set cookie policy
        session.cookies.set_policy(BlockCookies())
        
        return session
    
    def _generate_request_data(self, item_id: str, action: str) -> Dict[str, Any]:
        """Generate optimized request data with caching"""
        platform = choice(self.platforms)
        os_version = randint(1, 12)
        device_type = choice(self.device_types)
        device_id = randint(1000000000000000000, 9999999999999999999)
        api_domain = choice(self.api_domains)
        channel = choice(self.channels)
        app_name = choice(self.app_names)
        
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": choice(self.user_agents)
        }
        
        uri = f"https://{api_domain}/aweme/v1/aweme/stats/?channel={channel}&device_type={device_type}&device_id={device_id}&os_version={os_version}&version_code=220400&app_name={app_name}&device_platform={platform}&aid=1988"
        
        data = f"item_id={item_id}&{action}_delta=1"
        
        return {
            'uri': uri,
            'headers': headers,
            'data': data
        }
    
    def send_request(self, item_id: str, action: str, proxy: Optional[Dict] = None) -> bool:
        """Send optimized request with better error handling"""
        try:
            request_data = self._generate_request_data(item_id, action)
            
            response = self.session.post(
                request_data['uri'],
                headers=request_data['headers'],
                data=request_data['data'],
                proxies=proxy,
                timeout=self.timeout,
                verify=False
            )
            
            # Check if request was successful
            return response.status_code == 200
            
        except Exception as e:
            logger.debug(f"Request failed: {e}")
            return False
    
    def clear_url(self, link: str) -> str:
        """Optimized URL clearing with better error handling"""
        try:
            parsed_url = urlparse(link)
            host = parsed_url.hostname.lower()
            
            if host in ["vm.tiktok.com", "vt.tiktok.com"]:
                response = self.session.head(link, verify=False, allow_redirects=True, timeout=self.timeout)
                parsed_redirect = urlparse(response.url)
                return parsed_redirect.path.split("/")[3]
            else:
                return parsed_url.path.split("/")[3]
                
        except Exception as e:
            logger.error(f"Failed to clear URL: {e}")
            return None
    
    def process_thread(self, item_id: str, action: str, proxy_list: List[str], proxy_type: str):
        """Optimized thread processing with better resource management"""
        while not self.completed:
            try:
                proxy = {proxy_type: f"{proxy_type}://{choice(proxy_list)}"} if proxy_list else None
                
                if self.send_request(item_id, action, proxy):
                    self.count_queue.put(1)
                    
            except Exception as e:
                logger.debug(f"Thread error: {e}")
                time.sleep(0.1)  # Brief pause on error
    
    def count_thread(self, amount: int):
        """Optimized counting thread with proper synchronization"""
        while True:
            try:
                self.count_queue.get()
                with self.lock:
                    self.sent_requests += 1
                    if amount > 0 and self.sent_requests >= amount:
                        self.completed = True
                        break
            except Exception as e:
                logger.error(f"Count thread error: {e}")
                break
    
    def progress_thread(self):
        """Optimized progress monitoring"""
        last_count = 0
        last_time = time.time()
        
        while not self.completed:
            time.sleep(1)
            
            current_time = time.time()
            current_count = self.sent_requests
            
            if current_count > last_count:
                elapsed = current_time - last_time
                requests_per_second = (current_count - last_count) / elapsed
                
                print(f"{current_count} sent requests! {requests_per_second:.2f} requests/second.", end="\r")
                
                last_count = current_count
                last_time = current_time
    
    def run(self, video_uri: str, amount: int, n_threads: int, send_type: int, proxy_list: List[str], proxy_type: str):
        """Main execution method with optimized threading"""
        item_id = self.clear_url(video_uri)
        if not item_id:
            print("Failed to extract video ID from URL")
            return
        
        action = "play" if send_type == 0 else "share"
        
        # Start monitoring threads
        threading.Thread(target=self.count_thread, args=(amount,), daemon=True).start()
        threading.Thread(target=self.progress_thread, daemon=True).start()
        
        # Use ThreadPoolExecutor for better thread management
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = []
            
            for _ in range(n_threads):
                future = executor.submit(
                    self.process_thread, 
                    item_id, 
                    action, 
                    proxy_list, 
                    proxy_type
                )
                futures.append(future)
            
            # Wait for completion or all threads to finish
            try:
                concurrent.futures.wait(futures, timeout=None)
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                self.completed = True
                for future in futures:
                    future.cancel()
        
        print(f"\nBot completed. Total requests sent: {self.sent_requests}")

def Banner():
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

if __name__ == "__main__":
    clearConsole()
    Banner()
    
    # Get user input
    video_uri = str(Write.Input("Video Link > ", Colors.yellow_to_red, interval=0.0001))
    amount = int(Write.Input("Amount (0=inf) > ", Colors.yellow_to_red, interval=0.0001))
    n_threads = int(Write.Input("Thread Amount > ", Colors.yellow_to_red, interval=0.0001))
    clearConsole()
    Banner()
    send_type = int(Write.Input("[0] - Views\n[1] - Shares > ", Colors.yellow_to_red, interval=0.0001))
    clearConsole()
    Banner()
    
    # Get proxy type
    proxy_choose = True
    proxy_type = "http"  # default
    while proxy_choose:
        proxy_input = Write.Input("Select proxy type:\n[0] - http\n[1] - socks4\n[2] - socks5 > ", Colors.yellow_to_red, interval=0.0001)
        if proxy_input == "0":
            proxy_type = "http"
            proxy_choose = False
        elif proxy_input == "1":
            proxy_type = "socks4"
            proxy_choose = False
        elif proxy_input == "2":
            proxy_type = "socks5"
            proxy_choose = False
    
    # Load proxies
    proxy_list = readProxiesFile()
    clearConsole()
    Banner()
    
    print(Colorate.Horizontal(Colors.yellow_to_red, f"Hits are not counted"))
    print(Colorate.Horizontal(Colors.yellow_to_red, f"Bot started! Check your video stats in 5 minutes !"))
    
    # Create and run bot
    bot = OptimizedTikTokBot()
    bot.run(video_uri, amount, n_threads, send_type, proxy_list, proxy_type)