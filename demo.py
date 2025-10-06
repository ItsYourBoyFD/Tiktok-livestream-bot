#!/usr/bin/env python3
"""
Demo script showing how the TikTok bot works
This simulates the application flow without requiring user input.
"""

import time
import threading
from main import (
    Banner, clearConsole, sendView, sendShare, clearURL, 
    performance_monitor, cleanup_sessions
)
from config import APP
import sys

def demo_application():
    """Demonstrate the application workflow"""
    print("🎬 TikTok Bot Demo - Showing Application Flow")
    print("=" * 60)
    
    # Show the banner
    clearConsole()
    Banner()
    
    # Simulate user inputs (what you would normally type)
    demo_inputs = {
        'video_url': 'https://www.tiktok.com/@username/video/1234567890123456789',
        'amount': 100,  # Number of requests to send
        'threads': 8,   # Number of worker threads
        'send_type': 0, # 0 = Views, 1 = Shares
        'proxy_type': 'http'
    }
    
    print(f"\n📝 Demo Configuration:")
    print(f"  Video URL: {demo_inputs['video_url']}")
    print(f"  Amount: {demo_inputs['amount']} requests")
    print(f"  Threads: {demo_inputs['threads']}")
    print(f"  Type: {'Views' if demo_inputs['send_type'] == 0 else 'Shares'}")
    print(f"  Proxy Type: {demo_inputs['proxy_type']}")
    
    # Parse video URL
    print(f"\n🔍 Parsing video URL...")
    try:
        # For demo, we'll extract a mock ID since the URL is fake
        item_id = "1234567890123456789"  # Normally: clearURL(demo_inputs['video_url'])
        print(f"✅ Video ID extracted: {item_id}")
    except Exception as e:
        print(f"❌ URL parsing failed: {e}")
        return
    
    # Set global variables that the functions need
    import main
    main.itemID = item_id
    main.proxyType = demo_inputs['proxy_type']
    main.proxyList = ['127.0.0.1:8080', '127.0.0.1:3128']  # Demo proxies
    main.amount = demo_inputs['amount']
    
    # Start performance monitoring
    print(f"\n📊 Starting performance monitoring...")
    if APP.enable_performance_monitoring:
        performance_monitor.start_monitoring(1.0)
    
    # Select function based on type
    send_function = sendView if demo_inputs['send_type'] == 0 else sendShare
    function_name = "sendView" if demo_inputs['send_type'] == 0 else "sendShare"
    
    print(f"\n🚀 Starting bot with {function_name} function...")
    print(f"⚡ Performance optimizations enabled")
    print(f"🔄 Running {demo_inputs['amount']} requests with {demo_inputs['threads']} threads...")
    
    # Simulate running the bot
    start_time = time.time()
    successful_requests = 0
    failed_requests = 0
    
    # Run a few test requests to show it working
    print(f"\n📡 Testing request functions...")
    
    for i in range(5):  # Just test a few requests
        try:
            # This will use the demo proxies and show the function works
            success = send_function()
            if success:
                successful_requests += 1
                print(f"✅ Request {i+1}: Success")
            else:
                failed_requests += 1
                print(f"❌ Request {i+1}: Failed")
        except Exception as e:
            failed_requests += 1
            print(f"❌ Request {i+1}: Error - {e}")
        
        time.sleep(0.1)  # Brief pause between requests
    
    # Show performance metrics
    time.sleep(2)  # Let monitoring collect some data
    
    print(f"\n📈 Performance Results:")
    print(f"  Successful requests: {successful_requests}")
    print(f"  Failed requests: {failed_requests}")
    print(f"  Success rate: {successful_requests/(successful_requests+failed_requests)*100:.1f}%")
    
    # Stop monitoring and show summary
    if APP.enable_performance_monitoring:
        performance_monitor.stop_monitoring()
        current_metrics = performance_monitor.get_current_metrics()
        if current_metrics:
            print(f"\n📊 Live Performance Metrics:")
            print(f"  CPU Usage: {current_metrics.cpu_percent:.1f}%")
            print(f"  Memory Usage: {current_metrics.memory_mb:.1f} MB")
            print(f"  Active Threads: {current_metrics.active_threads}")
    
    # Cleanup
    cleanup_sessions()
    
    print(f"\n✅ Demo completed successfully!")
    print(f"\n💡 To run the real application:")
    print(f"   python3 main.py")
    print(f"\n🔧 To customize settings:")
    print(f"   Edit config.py and Data/Proxies.txt")

def show_interactive_flow():
    """Show what the interactive flow looks like"""
    print(f"\n🎮 Interactive Application Flow:")
    print(f"=" * 40)
    print(f"""
When you run 'python3 main.py', you'll see:

1. 🎨 Colorful ASCII banner
2. 📝 Input prompts:
   Video Link > [paste TikTok URL]
   Amount (0=inf) > [number of views/shares]
   Thread Amount > [recommended: 8-16]
   [0] - Views / [1] - Shares > [choose 0 or 1]
   Proxy type > [0=http, 1=socks4, 2=socks5]

3. 🚀 Bot starts with real-time display:
   Performance optimizations enabled
   Bot started! Check your video stats in 5 minutes!
   1,234 sent requests! 456.7 req/sec

4. 📊 Live monitoring shows:
   - Requests per second
   - Success rate
   - CPU/Memory usage
   - Active threads

5. 📈 Final report with:
   - Total requests sent
   - Performance statistics
   - Exported performance report
""")

if __name__ == "__main__":
    try:
        demo_application()
        show_interactive_flow()
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    finally:
        # Ensure cleanup
        try:
            performance_monitor.stop_monitoring()
            cleanup_sessions()
        except:
            pass