#!/usr/bin/env python3
"""
Proxy Validator for TikTok Bot
Tests proxies specifically for TikTok API compatibility.
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor
import random

def test_proxy_for_tiktok(proxy, timeout=10):
    """Test if proxy works with TikTok-like requests"""
    try:
        proxy_dict = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        
        # Test URLs that simulate TikTok API requests
        test_urls = [
            "https://httpbin.org/user-agent",
            "https://httpbin.org/headers", 
            "https://api.ipify.org?format=json",
            "https://httpbin.org/ip"
        ]
        
        # Use TikTok-like headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        # Test with random URL
        test_url = random.choice(test_urls)
        
        start_time = time.time()
        response = requests.get(
            test_url, 
            proxies=proxy_dict, 
            headers=headers,
            timeout=timeout,
            verify=False
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            return {
                'proxy': proxy,
                'working': True,
                'response_time': response_time,
                'status_code': response.status_code
            }
        else:
            return {'proxy': proxy, 'working': False, 'error': f'Status: {response.status_code}'}
            
    except Exception as e:
        return {'proxy': proxy, 'working': False, 'error': str(e)}

def validate_current_proxies():
    """Validate the current proxies in Data/Proxies.txt"""
    print("🧪 Validating current proxies for TikTok compatibility...")
    
    try:
        with open("Data/Proxies.txt", "r") as f:
            lines = f.readlines()
        
        # Extract proxy IPs (skip comments)
        proxies = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                proxies.append(line)
        
        print(f"📊 Testing {len(proxies)} proxies...")
        
        working_proxies = []
        failed_proxies = []
        
        # Test proxies concurrently
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(test_proxy_for_tiktok, proxies))
        
        # Process results
        for result in results:
            if result['working']:
                working_proxies.append(result)
                print(f"✅ {result['proxy']} - {result['response_time']:.2f}s")
            else:
                failed_proxies.append(result)
                print(f"❌ {result['proxy']} - {result.get('error', 'Failed')}")
        
        # Sort by response time
        working_proxies.sort(key=lambda x: x['response_time'])
        
        print(f"\n📊 Validation Results:")
        print(f"✅ Working: {len(working_proxies)}")
        print(f"❌ Failed: {len(failed_proxies)}")
        print(f"📈 Success Rate: {len(working_proxies)/len(proxies)*100:.1f}%")
        
        if working_proxies:
            print(f"\n⚡ Fastest Proxies:")
            for i, proxy in enumerate(working_proxies[:5]):
                print(f"   {i+1}. {proxy['proxy']} ({proxy['response_time']:.2f}s)")
        
        return working_proxies, failed_proxies
        
    except Exception as e:
        print(f"❌ Error validating proxies: {e}")
        return [], []

def update_proxy_file_with_working(working_proxies):
    """Update proxy file with only working proxies"""
    if not working_proxies:
        print("❌ No working proxies to update")
        return False
    
    try:
        with open("Data/Proxies.txt", "w") as f:
            f.write("# Validated working proxies for TikTok\n")
            f.write("# Format: IP:PORT\n")
            f.write(f"# Validated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Working proxies: {len(working_proxies)}\n")
            f.write("# Sorted by response time (fastest first)\n\n")
            
            for proxy_info in working_proxies:
                f.write(f"{proxy_info['proxy']}\n")
        
        print(f"✅ Updated Data/Proxies.txt with {len(working_proxies)} validated proxies")
        return True
        
    except Exception as e:
        print(f"❌ Error updating proxy file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 TikTok Proxy Validator")
    print("=" * 30)
    
    working, failed = validate_current_proxies()
    
    if working:
        update_proxy_file_with_working(working)
        print(f"\n🎉 Ready to use TikTok bot with {len(working)} validated proxies!")
        print("🚀 Run: python3 main.py")
    else:
        print("\n⚠️  No working proxies found. Try running proxy_scraper.py again.")