import time
import psutil
import os

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
    
    def start_request(self):
        self.request_count += 1
        return time.time()
    
    def end_request(self, start_timestamp):
        duration = time.time() - start_timestamp
        return {
            "duration_seconds": round(duration, 2),
            "total_requests": self.request_count,
            "memory_usage_mb": round(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024, 2),
            "uptime_minutes": round((time.time() - self.start_time) / 60, 2)
        }
    
    def get_performance_stats(self):
        return self.end_request(self.start_time)

# Global instance
monitor = PerformanceMonitor()

if __name__ == "__main__":
    # Test performance monitoring
    start = monitor.start_request()
    time.sleep(0.5)  # Simulate work
    stats = monitor.end_request(start)
    print("Performance Stats:", stats)
