import re
from datetime import datetime
from collections import Counter

class LogParserEngine:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        
        # Regex to catch raw IPv4 addresses
        self.ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        # Regex to pull structural timestamp, message types, and details
        self.log_pattern = re.compile(r'\[(?P<timestamp>.*?)\]\s+(?P<type>[\w\s\-\(\)%]+):\s+(?P<message>.*)')

    def parse_logs(self):
        """Processes the log target dynamically and generates statistics."""
        metrics = {
            "total_entries": 0,
            "success_logins": 0,
            "failed_logins": 0,
            "suspicious_events": 0,
            "unique_ips": set(),
            "distribution": Counter(),
            "timeline": {},  
            "raw_records": []  
        }
        
        try:
            with open(self.log_file_path, 'r') as file:
                for line in file:
                    if not line.strip():
                        continue
                        
                    metrics["total_entries"] += 1
                    
                    # Track structural IP addresses
                    ip_match = self.ip_pattern.search(line)
                    ip_address = ip_match.group() if ip_match else "0.0.0.0"
                    if ip_match:
                        metrics["unique_ips"].add(ip_address)
                        
                    # Extract structured groups using the log regex
                    match = self.log_pattern.search(line)
                    if match:
                        data = match.groupdict()
                        event_type = data["type"].strip()
                        timestamp_str = data["timestamp"].strip()
                        message = data["message"].strip()
                        
                        # Clean up formatting for visual chart timeline categories
                        try:
                            dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                            date_key = dt.strftime("%b %d")
                        except ValueError:
                            date_key = "Unknown"
                            
                        # Ensure safe nested data mapping initialization
                        if date_key not in metrics["timeline"]:
                            metrics["timeline"][date_key] = {"total": 0, "success": 0, "failed": 0}
                            
                        metrics["timeline"][date_key]["total"] += 1
                        metrics["distribution"][event_type] += 1
                        
                        # Classification logic matching your application parameters
                        status = "Completed"
                        if "Login Success" in event_type:
                            metrics["success_logins"] += 1
                            metrics["timeline"][date_key]["success"] += 1
                        elif "Failed Login" in event_type:
                            metrics["failed_logins"] += 1
                            metrics["suspicious_events"] += 1
                            metrics["timeline"][date_key]["failed"] += 1
                        elif any(x in event_type for x in ["Brute Force", "Access Denied", "Suspicious"]):
                            metrics["suspicious_events"] += 1
                            if "Brute Force" in event_type:
                                status = "Failed" # Match the failed visual marker from your report mockup
                        
                        # Save a structured tuple to cleanly populate table views instantly
                        metrics["raw_records"].append((message, event_type, timestamp_str, ip_address, status))
                        
        except FileNotFoundError:
            print(f"[{datetime.now()}] Engine Warning: Log file not found at '{self.log_file_path}'. Check path defaults.")
            
        return metrics