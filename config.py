"""
Configuration settings for optimized TikTok Mass Botting
Adjust these settings based on your system capabilities and requirements.
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class PerformanceConfig:
    """Performance optimization settings"""
    
    # Connection settings
    max_connections_per_host: int = 100
    max_total_connections: int = 200
    connection_timeout: float = 5.0
    read_timeout: float = 10.0
    
    # Retry settings
    max_retries: int = 3
    retry_backoff_factor: float = 0.1
    retry_status_codes: tuple = (429, 500, 502, 503, 504)
    
    # Threading settings
    max_worker_threads: Optional[int] = None  # Auto-detect based on CPU
    thread_pool_size_multiplier: int = 4  # threads = CPU_count * multiplier
    
    # Queue settings
    request_queue_size: int = 10000
    queue_timeout: float = 1.0
    
    # Caching settings
    cache_size: int = 1000
    enable_request_caching: bool = True
    
    # Monitoring settings
    enable_performance_monitoring: bool = True
    monitoring_interval: float = 1.0
    
    # Logging settings
    log_level: str = "WARNING"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    enable_request_logging: bool = False
    
    # Rate limiting
    enable_rate_limiting: bool = False
    requests_per_second_limit: Optional[float] = None
    
    def __post_init__(self):
        """Auto-configure settings based on system capabilities"""
        if self.max_worker_threads is None:
            cpu_count = os.cpu_count() or 4
            self.max_worker_threads = min(cpu_count * self.thread_pool_size_multiplier, 1000)

@dataclass
class NetworkConfig:
    """Network-related configuration"""
    
    # User agents for rotation
    user_agents: tuple = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    )
    
    # Device types for API requests
    device_types: tuple = (
        "SM-G973F", "SM-G975F", "SM-G988B", "Pixel", "Pixel 2", "Pixel 3", 
        "iPhone12,1", "iPhone12,3", "iPhone13,1", "iPhone13,2"
    )
    
    # Platforms
    platforms: tuple = ("android", "ios")
    
    # App names
    app_names: tuple = ("tiktok_web", "musically_go")
    
    # Channels
    channels: tuple = ("googleplay", "appstore", "h5")
    
    # API domains (add more as discovered)
    api_domains: tuple = (
        "api16-normal-c-useast1a.tiktokv.com",
        "api19-normal-c-useast1a.tiktokv.com",
        "api21-normal-c-useast1a.tiktokv.com",
        "api22-normal-c-useast1a.tiktokv.com",
    )
    
    # Proxy settings
    proxy_rotation_enabled: bool = True
    proxy_validation_enabled: bool = False  # Validate proxies before use
    proxy_timeout: float = 5.0

@dataclass
class AppConfig:
    """Application configuration"""
    
    # File paths
    proxy_file_paths: tuple = (
        "Data/Proxies.txt",
        "proxies.txt", 
        "Proxies.txt",
        "data/proxies.txt"
    )
    
    # Output settings
    enable_colored_output: bool = True
    progress_update_interval: float = 1.0
    
    # Safety settings
    max_requests_per_session: int = 1000000  # Prevent runaway processes
    auto_stop_on_high_error_rate: bool = True
    error_rate_threshold: float = 0.8  # Stop if 80% of requests fail
    
    # Export settings
    auto_export_performance_report: bool = True
    performance_report_filename: str = "performance_report.json"

# Global configuration instances
PERFORMANCE = PerformanceConfig()
NETWORK = NetworkConfig()
APP = AppConfig()

def get_optimized_settings() -> Dict[str, Any]:
    """Get recommended settings based on system capabilities"""
    import psutil
    
    # System info
    cpu_count = os.cpu_count() or 4
    memory_gb = psutil.virtual_memory().total / (1024**3)
    
    recommendations = {
        "threads": min(cpu_count * 4, 500),
        "connections_per_host": min(100, cpu_count * 10),
        "queue_size": min(10000, int(memory_gb * 1000)),
        "cache_size": min(1000, int(memory_gb * 100)),
    }
    
    # Adjust based on available memory
    if memory_gb < 4:
        recommendations["threads"] = min(recommendations["threads"], 100)
        recommendations["queue_size"] = min(recommendations["queue_size"], 1000)
    elif memory_gb > 16:
        recommendations["threads"] = min(recommendations["threads"] * 2, 1000)
    
    return recommendations

def print_system_info():
    """Print system information and recommendations"""
    import psutil
    
    cpu_count = os.cpu_count() or 4
    memory_gb = psutil.virtual_memory().total / (1024**3)
    
    print("System Information:")
    print(f"  CPU Cores: {cpu_count}")
    print(f"  Memory: {memory_gb:.1f} GB")
    print(f"  Platform: {os.name}")
    
    recommendations = get_optimized_settings()
    print("\nRecommended Settings:")
    for key, value in recommendations.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print_system_info()