import ssl
import time
import queue
import threading
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from http import cookiejar

import requests
# Lazily import heavy UI deps to reduce import-time overhead
Colorate = Colors = Write = Add = Center = None

from Data.UserAgent import UserAgent
from Data.Lists import DeviceTypes, Platforms, Channel, ApiDomain
from utils import *

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
r                                 = requests.Session()
# Configure connection pooling and defaults for better throughput
r.verify                           = False
r.trust_env                        = True  # allow env proxies if present
try:
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    # Increase pool connections and mount adapters for http/https
    adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100,
                          max_retries=Retry(total=0, connect=0, read=0, redirect=0, backoff_factor=0))
    r.mount('http://', adapter)
    r.mount('https://', adapter)
except Exception:
    # If adapter import fails, continue with default session
    pass
countQueue                        = queue.Queue()
sentRequests                      = 0
stopEvent                         = threading.Event()

r.cookies.set_policy(BlockCookies())
def _ensure_styles_imported():
    global Colorate, Colors, Write, Add, Center
    if Colorate is None:
        from pystyle import Colorate as _Colorate, Colors as _Colors, Write as _Write, Add as _Add, Center as _Center
        Colorate, Colors, Write, Add, Center = _Colorate, _Colors, _Write, _Add, _Center


def Banner():
    _ensure_styles_imported()
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
    proxy         = {f'{proxyType}': f'{proxyType}://{choice(proxyList)}'}
    platform      = choice(Platforms)
    osVersion     = randint(1, 12)
    DeviceType    = choice(DeviceTypes)
    headers       = {
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "user-agent": choice(UserAgent)
                    }
    appName       = choice(["tiktok_web", "musically_go"])
    Device_ID     = randint(1000000000000000000, 9999999999999999999)
    apiDomain     = choice(ApiDomain)
    channelLol    = choice(Channel)
    URI           = f"https://{apiDomain}/aweme/v1/aweme/stats/?channel={channelLol}&device_type={DeviceType}&device_id={Device_ID}&os_version={osVersion}&version_code=220400&app_name={appName}&device_platform={platform}&aid=1988"
    data          = f"item_id={itemID}&play_delta=1"

    try:
        req = r.post(URI, headers=headers, data=data, proxies=proxy, timeout=5)
        return True
    except:
        return False

def sendShare():
    platform = choice(Platforms)
    osVersion = randint(1, 12)
    DeviceType = choice(DeviceTypes)
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": choice(UserAgent)
    }
    appName = choice(["tiktok_web", "musically_go"])
    Device_ID = randint(1000000000000000000, 9999999999999999999)
    apiDomain = choice(ApiDomain)
    channelLol = choice(Channel)
    URI = f"https://{apiDomain}/aweme/v1/aweme/stats/?channel={channelLol}&device_type={DeviceType}&device_id={Device_ID}&os_version={osVersion}&version_code=220400&app_name={appName}&device_platform={platform}&aid=1988"
    data = f"item_id={itemID}&share_delta=1"

    proxy = {f'{proxyType}': f'{proxyType}://{choice(proxyList)}'}
    try:
        req = r.post(URI, headers=headers, data=data, proxies=proxy, timeout=5)
        return True
    except:
        return False

def clearURL(link):
    parsedURL = urlparse(link)
    host = parsedURL.hostname.lower()
    if "vm.tiktok.com" == host or "vt.tiktok.com" == host:
        UrlParsed = urlparse(r.head(link, verify=False, allow_redirects=True, timeout=5).url)
        return UrlParsed.path.split("/")[3]
    else:
        UrlParsed = urlparse(link)
        return UrlParsed.path.split("/")[3]

def proccessThread(sendProccess):
    while not stopEvent.is_set():
        if sendProccess():
            countQueue.put(1)

def countThread():
    global sentRequests
    while not stopEvent.is_set():
        countQueue.get()
        sentRequests += 1
        if amount > 0:
            if sentRequests >= amount:
                stopEvent.set()

def progressThread():
    last_print = 0.0
    while not stopEvent.is_set():
        start = time.time()
        startReq = sentRequests
        time.sleep(0.5)
        end = time.time()
        endReq = sentRequests

        elapsed = end - start
        elapsedReq = endReq - startReq
        now = time.time()
        if now - last_print >= 0.5:
            print(f"{sentRequests} sent requests! {elapsedReq/elapsed if elapsed>0 else 0:.2f} req/s", end="\r")
            last_print = now
    # finalize line so the next print starts on new line
    print("")

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

    workers = []
    for n in range(nThreads):
        t = threading.Thread(target=proccessThread, args=(sendProcess,), daemon=True)
        t.start()
        workers.append(t)
    # Wait until stopEvent is set (desired amount reached) then exit
    try:
        while not stopEvent.is_set():
            time.sleep(0.2)
    except KeyboardInterrupt:
        stopEvent.set()
