import ssl
import time
import queue
import threading
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from http import cookiejar
from functools import lru_cache

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pystyle import Colorate, Colors, Write, Add, Center

try:
    from Data.UserAgent import UserAgent
    from Data.Lists import DeviceTypes, Platforms, Channel, ApiDomain
except ImportError:
    # Fallback values if Data module is not available
    UserAgent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]
    DeviceTypes = ["SM-G973N", "SM-G960F", "SM-G965F"]
    Platforms = ["android", "ios"]
    Channel = ["googleplay", "appstore"]
    ApiDomain = ["api16-normal-c-useast1a.tiktokv.com", "api19-normal-c-useast1a.tiktokv.com"]

from utils import *

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Optimized session with connection pooling and retries
def create_session():
    session = requests.Session()
    session.cookies.set_policy(BlockCookies())
    # Configure connection pooling for better performance
    adapter = HTTPAdapter(
        pool_connections=100,
        pool_maxsize=100,
        max_retries=Retry(total=0),
        pool_block=False
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

r = create_session()
countQueue = queue.Queue(maxsize=10000)  # Add max size to prevent memory issues
sentRequests = 0
completed = False

# Optimized: Pre-compute static values to reduce overhead
APP_NAMES = ["tiktok_web", "musically_go"]
DEVICE_ID_MIN = 1000000000000000000
DEVICE_ID_MAX = 9999999999999999999
BASE_HEADERS = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}

# Use thread-local storage for session objects to improve thread safety
thread_local = threading.local()

def get_thread_session():
    """Get or create a session for the current thread."""
    if not hasattr(thread_local, "session"):
        thread_local.session = create_session()
    return thread_local.session

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

# Optimized: Consolidated sendView and sendShare into a single function
def sendRequest(request_type="view"):
    """Optimized unified request function for both view and share.
    
    Args:
        request_type: "view" or "share"
    
    Returns:
        bool: True if request succeeded, False otherwise
    """
    # Use thread-local session for better thread safety
    session = get_thread_session()
    
    # Build request parameters (optimized to reduce function calls)
    proxy = {proxyType: f'{proxyType}://{choice(proxyList)}'}
    
    # Create headers with random user agent
    headers = BASE_HEADERS.copy()
    headers["user-agent"] = choice(UserAgent)
    
    # Generate random parameters
    platform = choice(Platforms)
    os_version = randint(1, 12)
    device_type = choice(DeviceTypes)
    app_name = choice(APP_NAMES)
    device_id = randint(DEVICE_ID_MIN, DEVICE_ID_MAX)
    api_domain = choice(ApiDomain)
    channel = choice(Channel)
    
    # Build URI (use string concatenation for better performance)
    uri = f"https://{api_domain}/aweme/v1/aweme/stats/?channel={channel}&device_type={device_type}&device_id={device_id}&os_version={os_version}&version_code=220400&app_name={app_name}&device_platform={platform}&aid=1988"
    
    # Set data based on request type
    delta_type = "play_delta" if request_type == "view" else "share_delta"
    data = f"item_id={itemID}&{delta_type}=1"
    
    try:
        # Use session.post with timeout and verify=False
        req = session.post(uri, headers=headers, data=data, proxies=proxy, timeout=5, verify=False)
        # Check if response is successful
        return req.status_code < 400
    except (requests.exceptions.RequestException, Exception):
        # Catch specific exceptions for better error handling
        return False

def sendView():
    """Send view request - optimized wrapper."""
    return sendRequest("view")

def sendShare():
    """Send share request - optimized wrapper."""
    return sendRequest("share")

@lru_cache(maxsize=128)
def clearURL(link):
    """Optimized URL parsing with caching for repeated URLs."""
    parsed_url = urlparse(link)
    host = parsed_url.hostname
    
    if host and host.lower() in ("vm.tiktok.com", "vt.tiktok.com"):
        try:
            # Follow redirect to get actual URL
            response = r.head(link, verify=False, allow_redirects=True, timeout=5)
            parsed_url = urlparse(response.url)
        except Exception:
            # If redirect fails, try to parse original URL
            pass
    
    # Extract video ID from path
    path_parts = parsed_url.path.split("/")
    if len(path_parts) > 3:
        return path_parts[3]
    
    # Fallback: return the link as-is if parsing fails
    return link.split("/")[-1] if "/" in link else link

def proccessThread(sendProccess):
    """Optimized process thread with better error handling."""
    while not completed:
        try:
            if sendProccess():
                countQueue.put(1, block=False)
        except queue.Full:
            # Queue is full, skip this iteration
            time.sleep(0.001)

def countThread():
    """Optimized count thread with better performance."""
    global sentRequests, completed
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

def progressThread():
    """Optimized progress thread with reduced overhead."""
    while not completed:
        start_req = sentRequests
        time.sleep(1)
        end_req = sentRequests
        
        req_per_sec = end_req - start_req
        
        # Use \r to overwrite the line without creating new lines
        print(f"{sentRequests:,} sent requests! {req_per_sec:,} requests/second.", end="\r", flush=True)
    
    # Print final stats on new line
    print(f"\n✓ Completed! Total: {sentRequests:,} requests")

if (__name__ == "__main__"):
    clearConsole(); Banner()
    VideoURI     = str(Write.Input("Video Link > ", Colors.yellow_to_red, interval=0.0001))
    amount       = int(Write.Input("Amount (0=inf) > ", Colors.yellow_to_red, interval=0.0001))
    nThreads     = int(Write.Input("Thread Amount > ", Colors.yellow_to_red, interval=0.0001)); clearConsole(); Banner()
    sendType     = int(Write.Input("[0] - Views\n[1] - Shares > ", Colors.yellow_to_red, interval=0.0001)); clearConsole(); Banner()
    itemID       = clearURL(VideoURI)
    proxyChoose  = True
    while proxyChoose:
        proxyType = Write.Input("Select proxy type:\n[0] - http\n[1] - socks4\n[2] - socks5 > ", Colors.yellow_to_red, interval=0.0001)
        if proxyType == "0":
            proxyType = "http"
            proxyChoose = False
        elif proxyType == "1":
            proxyType = "socks4"
            proxyChoose = False
        elif proxyType == "2":
            proxyType = "socks5"
            proxyChoose = False

    proxyList = readProxiesFile()
    clearConsole(); Banner()

    print(Colorate.Horizontal(Colors.yellow_to_red, f"Hits are not counted"))
    print(Colorate.Horizontal(Colors.yellow_to_red, f"Bot started! Check your video stats in 5 minutes !"))

    if sendType == 0:
        sendProcess = sendView
    elif sendType == 1:
        sendProcess = sendShare
    else:
        print(f"Error {sendType}")

    threading.Thread(target=countThread, daemon=True).start()
    threading.Thread(target=progressThread, daemon=True).start()

    for n in range(nThreads):
        threading.Thread(target=proccessThread, args=(sendProcess,), daemon=True).start()
    
    # Keep main thread alive until completion
    try:
        while not completed:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n✓ Interrupted by user")
        completed = True
