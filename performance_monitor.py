#!/usr/bin/env python3
"""
Performance monitoring utilities for TikTok Mass Botting
This module provides tools to monitor and analyze performance metrics.
"""

import time
import psutil
import threading
from collections import deque
from dataclasses import dataclass
from typing import Optional, Dict, Any
import json
import logging

@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    timestamp: float
    requests_per_second: float
    cpu_percent: float
    memory_mb: float
    active_threads: int
    success_rate: float
    network_io: Dict[str, int]

class PerformanceMonitor:
    """Real-time performance monitoring for the bot"""
    
    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.metrics_history = deque(maxlen=window_size)
        self.start_time = time.time()
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Counters
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        # Network baseline
        self.initial_net_io = psutil.net_io_counters()
        
    def start_monitoring(self, interval: float = 1.0):
        """Start performance monitoring in background thread"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        logging.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        logging.info("Performance monitoring stopped")
    
    def _monitor_loop(self, interval: float):
        """Main monitoring loop"""
        last_requests = 0
        
        while self.monitoring:
            try:
                # Calculate requests per second
                current_requests = self.total_requests
                rps = (current_requests - last_requests) / interval
                last_requests = current_requests
                
                # System metrics
                cpu_percent = psutil.cpu_percent(interval=None)
                memory_info = psutil.virtual_memory()
                memory_mb = memory_info.used / (1024 * 1024)
                
                # Thread count
                active_threads = threading.active_count()
                
                # Success rate
                success_rate = (
                    self.successful_requests / max(self.total_requests, 1) * 100
                )
                
                # Network I/O
                current_net_io = psutil.net_io_counters()
                network_io = {
                    'bytes_sent': current_net_io.bytes_sent - self.initial_net_io.bytes_sent,
                    'bytes_recv': current_net_io.bytes_recv - self.initial_net_io.bytes_recv,
                    'packets_sent': current_net_io.packets_sent - self.initial_net_io.packets_sent,
                    'packets_recv': current_net_io.packets_recv - self.initial_net_io.packets_recv,
                }
                
                # Create metrics snapshot
                metrics = PerformanceMetrics(
                    timestamp=time.time(),
                    requests_per_second=rps,
                    cpu_percent=cpu_percent,
                    memory_mb=memory_mb,
                    active_threads=active_threads,
                    success_rate=success_rate,
                    network_io=network_io
                )
                
                self.metrics_history.append(metrics)
                
                time.sleep(interval)
                
            except Exception as e:
                logging.error(f"Error in performance monitoring: {e}")
                time.sleep(interval)
    
    def record_request(self, success: bool = True):
        """Record a request attempt"""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
    
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """Get the most recent metrics"""
        return self.metrics_history[-1] if self.metrics_history else None
    
    def get_average_metrics(self, window: Optional[int] = None) -> Dict[str, float]:
        """Calculate average metrics over specified window"""
        if not self.metrics_history:
            return {}
        
        window = window or len(self.metrics_history)
        recent_metrics = list(self.metrics_history)[-window:]
        
        if not recent_metrics:
            return {}
        
        return {
            'avg_rps': sum(m.requests_per_second for m in recent_metrics) / len(recent_metrics),
            'avg_cpu': sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
            'avg_memory_mb': sum(m.memory_mb for m in recent_metrics) / len(recent_metrics),
            'avg_threads': sum(m.active_threads for m in recent_metrics) / len(recent_metrics),
            'avg_success_rate': sum(m.success_rate for m in recent_metrics) / len(recent_metrics),
        }
    
    def get_peak_performance(self) -> Dict[str, float]:
        """Get peak performance metrics"""
        if not self.metrics_history:
            return {}
        
        return {
            'peak_rps': max(m.requests_per_second for m in self.metrics_history),
            'peak_cpu': max(m.cpu_percent for m in self.metrics_history),
            'peak_memory_mb': max(m.memory_mb for m in self.metrics_history),
            'peak_threads': max(m.active_threads for m in self.metrics_history),
        }
    
    def export_metrics(self, filename: str = "performance_report.json"):
        """Export metrics to JSON file"""
        try:
            report = {
                'session_info': {
                    'start_time': self.start_time,
                    'duration_seconds': time.time() - self.start_time,
                    'total_requests': self.total_requests,
                    'successful_requests': self.successful_requests,
                    'failed_requests': self.failed_requests,
                },
                'averages': self.get_average_metrics(),
                'peaks': self.get_peak_performance(),
                'metrics_history': [
                    {
                        'timestamp': m.timestamp,
                        'rps': m.requests_per_second,
                        'cpu_percent': m.cpu_percent,
                        'memory_mb': m.memory_mb,
                        'threads': m.active_threads,
                        'success_rate': m.success_rate,
                        'network_io': m.network_io,
                    }
                    for m in self.metrics_history
                ]
            }
            
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            logging.info(f"Performance report exported to {filename}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to export metrics: {e}")
            return False
    
    def print_summary(self):
        """Print performance summary to console"""
        if not self.metrics_history:
            print("No performance data available")
            return
        
        current = self.get_current_metrics()
        averages = self.get_average_metrics()
        peaks = self.get_peak_performance()
        
        print("\n" + "="*50)
        print("PERFORMANCE SUMMARY")
        print("="*50)
        
        if current:
            print(f"Current RPS: {current.requests_per_second:.1f}")
            print(f"Current CPU: {current.cpu_percent:.1f}%")
            print(f"Current Memory: {current.memory_mb:.1f} MB")
            print(f"Active Threads: {current.active_threads}")
            print(f"Success Rate: {current.success_rate:.1f}%")
        
        print("\nAVERAGES:")
        for key, value in averages.items():
            print(f"{key}: {value:.2f}")
        
        print("\nPEAKS:")
        for key, value in peaks.items():
            print(f"{key}: {value:.2f}")
        
        print(f"\nTotal Requests: {self.total_requests}")
        print(f"Success Rate: {self.successful_requests}/{self.total_requests}")
        print(f"Session Duration: {time.time() - self.start_time:.1f} seconds")
        print("="*50)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def start_performance_monitoring(interval: float = 1.0):
    """Start global performance monitoring"""
    performance_monitor.start_monitoring(interval)

def stop_performance_monitoring():
    """Stop global performance monitoring"""
    performance_monitor.stop_monitoring()

def record_request_result(success: bool = True):
    """Record a request result for performance tracking"""
    performance_monitor.record_request(success)

def print_performance_summary():
    """Print performance summary"""
    performance_monitor.print_summary()

def export_performance_report(filename: str = "performance_report.json"):
    """Export performance report"""
    return performance_monitor.export_metrics(filename)