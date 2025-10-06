"""
Performance monitoring utilities for the TikTok bot
"""
import time
import psutil
import threading
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Data class for performance metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    requests_per_second: float
    active_threads: int
    network_io: Dict[str, int]

class PerformanceMonitor:
    """Performance monitoring class with optimized data collection"""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.is_monitoring = False
        self.monitor_thread = None
        self.start_time = None
        self.initial_network_io = None
        
    def start_monitoring(self, interval: float = 1.0):
        """Start performance monitoring in a separate thread"""
        if self.is_monitoring:
            logger.warning("Performance monitoring already running")
            return
            
        self.is_monitoring = True
        self.start_time = time.time()
        self.initial_network_io = self._get_network_io()
        
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self, interval: float):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in performance monitoring: {e}")
                time.sleep(interval)
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            
            # Get thread count
            active_threads = threading.active_count()
            
            # Get network I/O
            network_io = self._get_network_io()
            
            # Calculate requests per second (placeholder - would need integration with bot)
            requests_per_second = 0.0
            
            return PerformanceMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                requests_per_second=requests_per_second,
                active_threads=active_threads,
                network_io=network_io
            )
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return PerformanceMetrics(
                timestamp=time.time(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                requests_per_second=0.0,
                active_threads=0,
                network_io={}
            )
    
    def _get_network_io(self) -> Dict[str, int]:
        """Get network I/O statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }
        except Exception as e:
            logger.error(f"Error getting network I/O: {e}")
            return {}
    
    def get_average_metrics(self) -> Optional[Dict]:
        """Get average metrics over the monitoring period"""
        if not self.metrics_history:
            return None
        
        try:
            cpu_values = [m.cpu_percent for m in self.metrics_history]
            memory_values = [m.memory_percent for m in self.metrics_history]
            memory_mb_values = [m.memory_used_mb for m in self.metrics_history]
            thread_values = [m.active_threads for m in self.metrics_history]
            
            return {
                'avg_cpu_percent': sum(cpu_values) / len(cpu_values),
                'max_cpu_percent': max(cpu_values),
                'avg_memory_percent': sum(memory_values) / len(memory_values),
                'max_memory_percent': max(memory_values),
                'avg_memory_mb': sum(memory_mb_values) / len(memory_mb_values),
                'max_memory_mb': max(memory_mb_values),
                'avg_threads': sum(thread_values) / len(thread_values),
                'max_threads': max(thread_values),
                'monitoring_duration': time.time() - self.start_time if self.start_time else 0
            }
        except Exception as e:
            logger.error(f"Error calculating average metrics: {e}")
            return None
    
    def get_peak_usage(self) -> Optional[Dict]:
        """Get peak resource usage"""
        if not self.metrics_history:
            return None
        
        try:
            cpu_values = [m.cpu_percent for m in self.metrics_history]
            memory_values = [m.memory_percent for m in self.metrics_history]
            memory_mb_values = [m.memory_used_mb for m in self.metrics_history]
            
            return {
                'peak_cpu_percent': max(cpu_values),
                'peak_memory_percent': max(memory_values),
                'peak_memory_mb': max(memory_mb_values)
            }
        except Exception as e:
            logger.error(f"Error calculating peak usage: {e}")
            return None
    
    def print_summary(self):
        """Print performance summary"""
        avg_metrics = self.get_average_metrics()
        peak_usage = self.get_peak_usage()
        
        if not avg_metrics or not peak_usage:
            print("No performance data available")
            return
        
        print("\n" + "="*50)
        print("PERFORMANCE SUMMARY")
        print("="*50)
        print(f"Monitoring Duration: {avg_metrics['monitoring_duration']:.2f} seconds")
        print(f"Average CPU Usage: {avg_metrics['avg_cpu_percent']:.2f}%")
        print(f"Peak CPU Usage: {peak_usage['peak_cpu_percent']:.2f}%")
        print(f"Average Memory Usage: {avg_metrics['avg_memory_mb']:.2f} MB ({avg_metrics['avg_memory_percent']:.2f}%)")
        print(f"Peak Memory Usage: {peak_usage['peak_memory_mb']:.2f} MB ({peak_usage['peak_memory_percent']:.2f}%)")
        print(f"Average Active Threads: {avg_metrics['avg_threads']:.2f}")
        print(f"Max Active Threads: {avg_metrics['max_threads']}")
        print("="*50)