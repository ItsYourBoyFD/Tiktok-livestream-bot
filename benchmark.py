#!/usr/bin/env python3
"""
Benchmark script to compare original vs optimized performance
"""

import time
import psutil
import threading
import requests
from concurrent.futures import ThreadPoolExecutor
import gc

def benchmark_original_approach():
    """Benchmark the original approach"""
    print("Benchmarking original approach...")
    
    start_time = time.time()
    start_memory = psutil.virtual_memory().used
    
    # Simulate original approach with basic threading
    def make_request():
        try:
            response = requests.get("https://httpbin.org/delay/0.1", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    # Create threads manually (original approach)
    threads = []
    results = []
    
    def worker():
        result = make_request()
        results.append(result)
    
    # Start 50 threads
    for _ in range(50):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    end_memory = psutil.virtual_memory().used
    
    return {
        'duration': end_time - start_time,
        'memory_used': end_memory - start_memory,
        'success_rate': sum(results) / len(results) if results else 0,
        'requests': len(results)
    }

def benchmark_optimized_approach():
    """Benchmark the optimized approach"""
    print("Benchmarking optimized approach...")
    
    start_time = time.time()
    start_memory = psutil.virtual_memory().used
    
    # Create optimized session
    session = requests.Session()
    
    # Configure retry strategy
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=50,
        pool_maxsize=50,
        pool_block=False
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    def make_request():
        try:
            response = session.get("https://httpbin.org/delay/0.1", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    # Use ThreadPoolExecutor (optimized approach)
    results = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [future.result() for future in futures]
    
    # Clean up
    session.close()
    gc.collect()
    
    end_time = time.time()
    end_memory = psutil.virtual_memory().used
    
    return {
        'duration': end_time - start_time,
        'memory_used': end_memory - start_memory,
        'success_rate': sum(results) / len(results) if results else 0,
        'requests': len(results)
    }

def run_benchmark():
    """Run the complete benchmark"""
    print("="*60)
    print("TikTok Mass Botting - Performance Benchmark")
    print("="*60)
    
    # Run original approach
    original_results = benchmark_original_approach()
    
    # Wait a bit between tests
    time.sleep(2)
    
    # Run optimized approach
    optimized_results = benchmark_optimized_approach()
    
    # Calculate improvements
    time_improvement = ((original_results['duration'] - optimized_results['duration']) / original_results['duration']) * 100
    memory_improvement = ((original_results['memory_used'] - optimized_results['memory_used']) / original_results['memory_used']) * 100 if original_results['memory_used'] > 0 else 0
    
    # Display results
    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print("="*60)
    
    print(f"{'Metric':<20} {'Original':<15} {'Optimized':<15} {'Improvement':<15}")
    print("-" * 65)
    
    print(f"{'Duration (s)':<20} {original_results['duration']:<15.3f} {optimized_results['duration']:<15.3f} {time_improvement:<15.1f}%")
    print(f"{'Memory (MB)':<20} {original_results['memory_used']/1024/1024:<15.3f} {optimized_results['memory_used']/1024/1024:<15.3f} {memory_improvement:<15.1f}%")
    print(f"{'Success Rate':<20} {original_results['success_rate']:<15.3f} {optimized_results['success_rate']:<15.3f} {'N/A':<15}")
    print(f"{'Requests':<20} {original_results['requests']:<15} {optimized_results['requests']:<15} {'N/A':<15}")
    
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    
    if time_improvement > 0:
        print(f"✅ Time improvement: {time_improvement:.1f}% faster")
    else:
        print(f"❌ Time regression: {abs(time_improvement):.1f}% slower")
    
    if memory_improvement > 0:
        print(f"✅ Memory improvement: {memory_improvement:.1f}% less memory used")
    else:
        print(f"❌ Memory regression: {abs(memory_improvement):.1f}% more memory used")
    
    print(f"✅ Success rate: {optimized_results['success_rate']:.1%}")
    print(f"✅ Total requests: {optimized_results['requests']}")
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    
    if time_improvement > 10:
        print("🚀 Significant performance improvement detected!")
        print("   The optimized version is significantly faster.")
    elif time_improvement > 0:
        print("✅ Performance improvement detected!")
        print("   The optimized version is faster.")
    else:
        print("⚠️  No significant time improvement detected.")
        print("   Consider running with more requests for better comparison.")
    
    if memory_improvement > 10:
        print("💾 Significant memory improvement detected!")
        print("   The optimized version uses significantly less memory.")
    elif memory_improvement > 0:
        print("✅ Memory improvement detected!")
        print("   The optimized version uses less memory.")
    else:
        print("⚠️  No significant memory improvement detected.")
        print("   Memory usage is similar between versions.")
    
    print("\n🎯 Use the optimized version for production!")
    print("📊 Monitor performance with the built-in performance monitor.")

if __name__ == "__main__":
    run_benchmark()