#!/usr/bin/env python3
"""
Benchmark script to compare original vs optimized performance
"""
import time
import psutil
import threading
import sys
import os
from typing import Dict, List, Any
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from performance_monitor import PerformanceMonitor
from config import Config

class Benchmark:
    """Benchmark class for performance testing"""
    
    def __init__(self):
        self.results = {}
        self.monitor = PerformanceMonitor()
        
    def run_benchmark(self, test_name: str, test_function, *args, **kwargs) -> Dict[str, Any]:
        """Run a benchmark test and collect metrics"""
        print(f"Running benchmark: {test_name}")
        
        # Start monitoring
        self.monitor.start_monitoring(interval=0.5)
        
        # Record initial system state
        initial_cpu = psutil.cpu_percent()
        initial_memory = psutil.virtual_memory()
        initial_threads = threading.active_count()
        
        # Run the test
        start_time = time.time()
        try:
            result = test_function(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        end_time = time.time()
        
        # Stop monitoring
        self.monitor.stop_monitoring()
        
        # Collect final metrics
        final_cpu = psutil.cpu_percent()
        final_memory = psutil.virtual_memory()
        final_threads = threading.active_count()
        
        # Get performance summary
        avg_metrics = self.monitor.get_average_metrics()
        peak_usage = self.monitor.get_peak_usage()
        
        # Calculate benchmark results
        duration = end_time - start_time
        cpu_delta = final_cpu - initial_cpu
        memory_delta = final_memory.used - initial_memory.used
        thread_delta = final_threads - initial_threads
        
        benchmark_result = {
            'test_name': test_name,
            'duration': duration,
            'success': success,
            'error': error,
            'result': result,
            'system_metrics': {
                'initial_cpu': initial_cpu,
                'final_cpu': final_cpu,
                'cpu_delta': cpu_delta,
                'initial_memory_mb': initial_memory.used / (1024 * 1024),
                'final_memory_mb': final_memory.used / (1024 * 1024),
                'memory_delta_mb': memory_delta / (1024 * 1024),
                'initial_threads': initial_threads,
                'final_threads': final_threads,
                'thread_delta': thread_delta
            },
            'performance_metrics': avg_metrics,
            'peak_usage': peak_usage
        }
        
        self.results[test_name] = benchmark_result
        return benchmark_result
    
    def print_results(self):
        """Print benchmark results in a formatted way"""
        print("\n" + "="*80)
        print("BENCHMARK RESULTS")
        print("="*80)
        
        for test_name, result in self.results.items():
            print(f"\nTest: {test_name}")
            print("-" * 40)
            print(f"Duration: {result['duration']:.2f} seconds")
            print(f"Success: {result['success']}")
            
            if result['error']:
                print(f"Error: {result['error']}")
            
            sys_metrics = result['system_metrics']
            print(f"CPU Usage: {sys_metrics['initial_cpu']:.2f}% -> {sys_metrics['final_cpu']:.2f}% (Δ{sys_metrics['cpu_delta']:+.2f}%)")
            print(f"Memory Usage: {sys_metrics['initial_memory_mb']:.2f}MB -> {sys_metrics['final_memory_mb']:.2f}MB (Δ{sys_metrics['memory_delta_mb']:+.2f}MB)")
            print(f"Threads: {sys_metrics['initial_threads']} -> {sys_metrics['final_threads']} (Δ{sys_metrics['thread_delta']:+d})")
            
            if result['performance_metrics']:
                perf = result['performance_metrics']
                print(f"Average CPU: {perf['avg_cpu_percent']:.2f}%")
                print(f"Peak CPU: {perf['max_cpu_percent']:.2f}%")
                print(f"Average Memory: {perf['avg_memory_mb']:.2f}MB")
                print(f"Peak Memory: {perf['max_memory_mb']:.2f}MB")
    
    def save_results(self, filename: str = "benchmark_results.json"):
        """Save benchmark results to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")

def test_memory_allocation():
    """Test memory allocation patterns"""
    data = []
    for i in range(10000):
        data.append(f"test_string_{i}" * 100)
    return len(data)

def test_thread_creation():
    """Test thread creation and management"""
    threads = []
    results = []
    
    def worker(thread_id):
        time.sleep(0.1)
        results.append(thread_id)
    
    for i in range(100):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return len(results)

def test_http_requests():
    """Test HTTP request performance"""
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    # Create optimized session
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=10
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Test requests
    success_count = 0
    for i in range(10):
        try:
            response = session.get("https://httpbin.org/delay/0.1", timeout=5)
            if response.status_code == 200:
                success_count += 1
        except:
            pass
    
    return success_count

def test_data_structures():
    """Test data structure performance"""
    # Test list operations
    test_list = list(range(10000))
    
    # Test dictionary operations
    test_dict = {i: f"value_{i}" for i in range(10000)}
    
    # Test set operations
    test_set = set(range(10000))
    
    # Test string operations
    test_string = "test_string" * 1000
    
    return {
        'list_len': len(test_list),
        'dict_len': len(test_dict),
        'set_len': len(test_set),
        'string_len': len(test_string)
    }

def main():
    """Main benchmark function"""
    print("Starting Performance Benchmark")
    print("="*50)
    
    benchmark = Benchmark()
    
    # Run benchmarks
    benchmark.run_benchmark("Memory Allocation", test_memory_allocation)
    benchmark.run_benchmark("Thread Creation", test_thread_creation)
    benchmark.run_benchmark("HTTP Requests", test_http_requests)
    benchmark.run_benchmark("Data Structures", test_data_structures)
    
    # Print and save results
    benchmark.print_results()
    benchmark.save_results()
    
    print("\nBenchmark completed!")

if __name__ == "__main__":
    main()