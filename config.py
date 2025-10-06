"""
Configuration file for performance optimization
"""
import os
from typing import Dict, Any

class Config:
    """Configuration class with performance-optimized defaults"""
    
    # HTTP Configuration
    HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT', '5'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    CONNECTION_POOL_SIZE = int(os.getenv('CONNECTION_POOL_SIZE', '100'))
    MAX_POOL_CONNECTIONS = int(os.getenv('MAX_POOL_CONNECTIONS', '100'))
    
    # Threading Configuration
    MAX_THREADS = int(os.getenv('MAX_THREADS', '1000'))
    DEFAULT_THREADS = int(os.getenv('DEFAULT_THREADS', '100'))
    THREAD_TIMEOUT = int(os.getenv('THREAD_TIMEOUT', '30'))
    
    # Performance Monitoring
    ENABLE_PERFORMANCE_MONITORING = os.getenv('ENABLE_PERFORMANCE_MONITORING', 'true').lower() == 'true'
    MONITORING_INTERVAL = float(os.getenv('MONITORING_INTERVAL', '1.0'))
    MAX_METRICS_HISTORY = int(os.getenv('MAX_METRICS_HISTORY', '100'))
    
    # Memory Optimization
    ENABLE_MEMORY_OPTIMIZATION = os.getenv('ENABLE_MEMORY_OPTIMIZATION', 'true').lower() == 'true'
    MAX_MEMORY_USAGE_MB = int(os.getenv('MAX_MEMORY_USAGE_MB', '1024'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    ENABLE_DEBUG_LOGGING = os.getenv('ENABLE_DEBUG_LOGGING', 'false').lower() == 'true'
    
    # Request Configuration
    REQUEST_DELAY_MS = int(os.getenv('REQUEST_DELAY_MS', '0'))
    ENABLE_REQUEST_CACHING = os.getenv('ENABLE_REQUEST_CACHING', 'true').lower() == 'true'
    CACHE_SIZE = int(os.getenv('CACHE_SIZE', '1000'))
    
    # Proxy Configuration
    PROXY_TIMEOUT = int(os.getenv('PROXY_TIMEOUT', '5'))
    MAX_PROXY_RETRIES = int(os.getenv('MAX_PROXY_RETRIES', '3'))
    ENABLE_PROXY_ROTATION = os.getenv('ENABLE_PROXY_ROTATION', 'true').lower() == 'true'
    
    @classmethod
    def get_http_config(cls) -> Dict[str, Any]:
        """Get HTTP configuration dictionary"""
        return {
            'timeout': cls.HTTP_TIMEOUT,
            'max_retries': cls.MAX_RETRIES,
            'pool_connections': cls.CONNECTION_POOL_SIZE,
            'pool_maxsize': cls.MAX_POOL_CONNECTIONS,
            'pool_block': False
        }
    
    @classmethod
    def get_threading_config(cls) -> Dict[str, Any]:
        """Get threading configuration dictionary"""
        return {
            'max_workers': cls.MAX_THREADS,
            'thread_name_prefix': 'TikTokBot',
            'thread_timeout': cls.THREAD_TIMEOUT
        }
    
    @classmethod
    def get_monitoring_config(cls) -> Dict[str, Any]:
        """Get monitoring configuration dictionary"""
        return {
            'enabled': cls.ENABLE_PERFORMANCE_MONITORING,
            'interval': cls.MONITORING_INTERVAL,
            'max_history': cls.MAX_METRICS_HISTORY
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration values"""
        try:
            # Validate numeric values
            assert cls.HTTP_TIMEOUT > 0, "HTTP_TIMEOUT must be positive"
            assert cls.MAX_RETRIES >= 0, "MAX_RETRIES must be non-negative"
            assert cls.CONNECTION_POOL_SIZE > 0, "CONNECTION_POOL_SIZE must be positive"
            assert cls.MAX_THREADS > 0, "MAX_THREADS must be positive"
            assert cls.MONITORING_INTERVAL > 0, "MONITORING_INTERVAL must be positive"
            
            return True
        except AssertionError as e:
            print(f"Configuration validation error: {e}")
            return False