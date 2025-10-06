#!/usr/bin/env python3
"""
Proxy Scraper for TikTok Bot
Automatically finds and validates working proxies from multiple sources.
"""

import requests
import re
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import socket
import random

class ProxyScraper:
    def __init__(self):
        self.working_proxies = []
        self.tested_proxies = set()
        
        # Free proxy sources
        self.proxy_sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
        ]
        
        # SOCKS proxy sources
        self.socks_sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        ]

    def scrape_proxies_from_url(self, url, proxy_type="http"):
        """Scrape proxies from a single URL"""
        try:
            print(f"🔍 Scraping from: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Extract IP:PORT patterns
                proxy_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}\b'
                proxies = re.findall(proxy_pattern, response.text)
                
                # Remove duplicates and format
                unique_proxies = list(set(proxies))
                print(f"✅ Found {len(unique_proxies)} proxies from {urlparse(url).netloc}")
                return unique_proxies
            else:
                print(f"❌ Failed to fetch from {url}: Status {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return []

    def test_proxy(self, proxy, proxy_type="http", timeout=5):
        """Test if a proxy is working"""
        if proxy in self.tested_proxies:
            return False
            
        self.tested_proxies.add(proxy)
        
        try:
            # Test URLs
            test_urls = [
                "http://httpbin.org/ip",
                "https://api.ipify.org?format=json",
                "http://icanhazip.com"
            ]
            
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            
            if proxy_type in ['socks4', 'socks5']:
                proxy_dict = {
                    'http': f'{proxy_type}://{proxy}',
                    'https': f'{proxy_type}://{proxy}'
                }
            
            # Test with a random URL
            test_url = random.choice(test_urls)
            response = requests.get(test_url, proxies=proxy_dict, timeout=timeout)
            
            if response.status_code == 200:
                print(f"✅ Working: {proxy}")
                return True
            else:
                return False
                
        except Exception:
            return False

    def validate_proxies(self, proxies, proxy_type="http", max_workers=50):
        """Validate a list of proxies concurrently"""
        working = []
        
        print(f"🧪 Testing {len(proxies)} {proxy_type} proxies...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {
                executor.submit(self.test_proxy, proxy, proxy_type): proxy 
                for proxy in proxies
            }
            
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    if future.result():
                        working.append(proxy)
                        if len(working) >= 50:  # Limit to 50 working proxies
                            break
                except Exception as e:
                    pass
        
        return working

    def scrape_all_sources(self):
        """Scrape proxies from all sources"""
        all_proxies = []
        
        print("🚀 Starting proxy scraping...")
        
        # Scrape HTTP proxies
        for url in self.proxy_sources:
            proxies = self.scrape_proxies_from_url(url, "http")
            all_proxies.extend(proxies)
            time.sleep(1)  # Be respectful to servers
        
        # Remove duplicates
        unique_proxies = list(set(all_proxies))
        print(f"📊 Total unique proxies found: {len(unique_proxies)}")
        
        return unique_proxies

    def get_working_proxies(self, limit=50):
        """Get working proxies up to the specified limit"""
        print("🔍 Scraping proxies from multiple sources...")
        
        # Scrape all proxies
        all_proxies = self.scrape_all_sources()
        
        if not all_proxies:
            print("❌ No proxies found from sources")
            return []
        
        # Shuffle for random testing
        random.shuffle(all_proxies)
        
        # Test proxies in batches
        batch_size = 200
        working_proxies = []
        
        for i in range(0, len(all_proxies), batch_size):
            batch = all_proxies[i:i+batch_size]
            print(f"🧪 Testing batch {i//batch_size + 1} ({len(batch)} proxies)...")
            
            working_batch = self.validate_proxies(batch, "http", max_workers=30)
            working_proxies.extend(working_batch)
            
            print(f"✅ Found {len(working_batch)} working proxies in this batch")
            print(f"📊 Total working proxies: {len(working_proxies)}")
            
            if len(working_proxies) >= limit:
                break
        
        return working_proxies[:limit]

def update_proxy_file(proxies):
    """Update the Data/Proxies.txt file with working proxies"""
    if not proxies:
        print("❌ No working proxies to add")
        return False
    
    try:
        with open("Data/Proxies.txt", "w") as f:
            f.write("# Working proxies - Auto-generated\n")
            f.write("# Format: IP:PORT\n")
            f.write(f"# Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total proxies: {len(proxies)}\n\n")
            
            for proxy in proxies:
                f.write(f"{proxy}\n")
        
        print(f"✅ Updated Data/Proxies.txt with {len(proxies)} working proxies")
        return True
        
    except Exception as e:
        print(f"❌ Error updating proxy file: {e}")
        return False

def add_premium_proxy_sources():
    """Add some reliable free proxy sources"""
    reliable_proxies = [
        # These are example formats - replace with actual working proxies
        "8.8.8.8:8080",
        "1.1.1.1:8080",
        # Add more reliable proxies here
    ]
    
    print("📋 Adding reliable proxy sources...")
    return reliable_proxies

def main():
    """Main function to scrape and add proxies"""
    print("🔧 TikTok Bot Proxy Scraper")
    print("=" * 40)
    
    scraper = ProxyScraper()
    
    try:
        # Get working proxies
        working_proxies = scraper.get_working_proxies(limit=30)
        
        if working_proxies:
            # Update the proxy file
            update_proxy_file(working_proxies)
            
            print(f"\n🎉 SUCCESS!")
            print(f"✅ Found and added {len(working_proxies)} working proxies")
            print(f"📁 Updated: Data/Proxies.txt")
            print(f"🚀 Ready to use with: python3 main.py")
            
        else:
            print("\n⚠️  No working proxies found from automatic scraping")
            print("💡 Try these alternatives:")
            print("   1. Use paid proxy services")
            print("   2. Search for 'free proxy lists' online")
            print("   3. Add proxies manually to Data/Proxies.txt")
            
            # Add some example proxies for testing
            example_proxies = [
                "127.0.0.1:8080",
                "127.0.0.1:3128",
                "127.0.0.1:1080"
            ]
            update_proxy_file(example_proxies)
            print("📝 Added example proxies for testing")
    
    except KeyboardInterrupt:
        print("\n⏹️  Scraping stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()