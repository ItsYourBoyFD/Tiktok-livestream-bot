#!/usr/bin/env python3
"""
Performance monitoring script for TikTok Mass Botting
Monitors memory usage, CPU usage, and request rates
"""

import time
import psutil
import threading
import logging
from typing import Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Data class for performance metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    requests_per_second: float
    total_requests: int

class PerformanceMonitor:
    """Performance monitoring class"""
    
    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.metrics_history: list[PerformanceMetrics] = []
        self.running = False
        self.monitor_thread = None
        self.request_count = 0
        self.last_request_count = 0
        self.start_time = time.time()
        
    def start_monitoring(self):
        """Start performance monitoring in background thread"""
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        logger.info("Performance monitoring stopped")
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last 100 metrics to prevent memory bloat
                if len(self.metrics_history) > 100:
                    self.metrics_history = self.metrics_history[-100:]
                
                # Log performance warnings
                self._check_performance_warnings(metrics)
                
                time.sleep(self.update_interval)
            except Exception as e:
                logger.error(f"Error in performance monitoring: {e}")
                
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        current_time = time.time()
        
        # CPU and memory metrics
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        
        # Request rate calculation
        elapsed_time = current_time - self.start_time
        requests_per_second = (self.request_count - self.last_request_count) / self.update_interval if elapsed_time > 0 else 0
        self.last_request_count = self.request_count
        
        return PerformanceMetrics(
            timestamp=current_time,
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            memory_available_mb=memory.available / (1024 * 1024),
            requests_per_second=requests_per_second,
            total_requests=self.request_count
        )
        
    def _check_performance_warnings(self, metrics: PerformanceMetrics):
        """Check for performance issues and log warnings"""
        # High CPU usage warning
        if metrics.cpu_percent > 90:
            logger.warning(f"High CPU usage: {metrics.cpu_percent:.1f}%")
            
        # High memory usage warning
        if metrics.memory_percent > 85:
            logger.warning(f"High memory usage: {metrics.memory_percent:.1f}%")
            
        # Low memory warning
        if metrics.memory_available_mb < 100:
            logger.warning(f"Low available memory: {metrics.memory_available_mb:.1f}MB")
            
    def increment_request_count(self):
        """Increment request counter (call this when a request is made)"""
        self.request_count += 1
        
    def get_current_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics"""
        if not self.metrics_history:
            return self._collect_metrics()
        return self.metrics_history[-1]
        
    def get_average_metrics(self, last_n: int = 10) -> Dict[str, float]:
        """Get average metrics over last N measurements"""
        if not self.metrics_history:
            return {}
            
        recent_metrics = self.metrics_history[-last_n:]
        
        return {
            'avg_cpu_percent': sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
            'avg_memory_percent': sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
            'avg_requests_per_second': sum(m.requests_per_second for m in recent_metrics) / len(recent_metrics),
            'total_requests': recent_metrics[-1].total_requests if recent_metrics else 0
        }
        
    def print_performance_summary(self):
        """Print performance summary"""
        if not self.metrics_history:
            print("No performance data available")
            return
            
        current = self.get_current_metrics()
        averages = self.get_average_metrics()
        
        print("\n" + "="*50)
        print("PERFORMANCE SUMMARY")
        print("="*50)
        print(f"Current CPU Usage: {current.cpu_percent:.1f}%")
        print(f"Current Memory Usage: {current.memory_percent:.1f}% ({current.memory_used_mb:.1f}MB)")
        print(f"Available Memory: {current.memory_available_mb:.1f}MB")
        print(f"Current Request Rate: {current.requests_per_second:.2f} req/s")
        print(f"Total Requests: {current.total_requests}")
        
        if averages:
            print(f"Average CPU Usage: {averages['avg_cpu_percent']:.1f}%")
            print(f"Average Memory Usage: {averages['avg_memory_percent']:.1f}%")
            print(f"Average Request Rate: {averages['avg_requests_per_second']:.2f} req/s")
        print("="*50)

# Global monitor instance
monitor = PerformanceMonitor()

def start_monitoring():
    """Start global performance monitoring"""
    monitor.start_monitoring()

def stop_monitoring():
    """Stop global performance monitoring"""
    monitor.stop_monitoring()

def increment_requests():
    """Increment request counter"""
    monitor.increment_request_count()

def get_performance_summary():
    """Get performance summary"""
    return monitor.print_performance_summary()