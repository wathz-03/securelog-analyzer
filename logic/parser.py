import re
from datetime import datetime
from collections import Counter

class LogParserEngine:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        
        self.ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        self.bracket_pattern = re.compile(r'\[(?P<timestamp>.*?)\]\s+(?P<type>[\w\s\-\(\)%]+):\s+(?P<message>.*)')
        self.windows_pattern = re.compile(r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})(?:,\d+)?\s+,\s+(?P<type>\w+)\s+(?P<component>\w+)\s+(?P<message>.*)')
        self.windows_fallback = re.compile(r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})(?:,\d+)?\s+(?P<type>\w+)\s+(?P<component>\w+)\s+(?P<message>.*)')

    def parse_logs(self):
        """Processes the log target dynamically and generates statistics."""
        metrics = {
            "total_entries": 0,
            "success_logins": 0,
            "failed_logins": 0,
            "suspicious_events": 0,
            "unique_ips": set(),
            "ip_counts": {},
            "distribution": Counter(),
            "timeline": {},  
            "raw_records": [],
            "recent_alerts": []
        }
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    cleaned_line = line.strip()
                    if not cleaned_line:
                        continue
                        
                    metrics["total_entries"] += 1
                    
                    ip_match = self.ip_pattern.search(cleaned_line)
                    if ip_match:
                        ip_address = ip_match.group()
                        metrics["unique_ips"].add(ip_address)
                    else:
                        ip_address = "0.0.0.0"

                    timestamp_str = ""
                    event_type = "System Log"
                    message = cleaned_line
                    date_key = "Unknown"
                    status = "Completed"
                        
                    match = self.bracket_pattern.search(cleaned_line)
                    if match:
                        data = match.groupdict()
                        event_type = data["type"].strip()
                        timestamp_str = data["timestamp"].strip()
                        message = data["message"].strip()
                        
                        try:
                            dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                            date_key = dt.strftime("%b %d")
                        except ValueError:
                            date_key = "Unknown"
                            
                    else:
                        win_match = self.windows_pattern.search(cleaned_line) or self.windows_fallback.search(cleaned_line)
                        if win_match:
                            data = win_match.groupdict()
                            timestamp_str = data["timestamp"].strip()
                            event_type = data["type"].strip() 
                            component = data["component"].strip()
                            message = f"[{component}] {data['message'].strip()}"
                            
                           
                            if ip_address == "0.0.0.0":
                                metrics["unique_ips"].add(component)
                                ip_address = component

                            try:
                                dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                                date_key = dt.strftime("%b %d")
                            except ValueError:
                                date_key = "Unknown" 

                    if ip_address != "0.0.0.0":
                        metrics["ip_counts"][ip_address] = metrics["ip_counts"].get(ip_address, 0) + 1

                    if date_key not in metrics["timeline"]:
                        metrics["timeline"][date_key] = {"total": 0, "success": 0, "failed": 0}
                    
                    metrics["timeline"][date_key]["total"] += 1
                    metrics["distribution"][event_type] += 1
                    
                    upper_type = event_type.upper()
                    upper_msg = message.upper()

                    alert_snippet = message
                    if 'match' in locals() and match and 'message' in match.groupdict():
                        alert_snippet = match.groupdict()['message']
                    elif 'win_match' in locals() and win_match and 'message' in win_match.groupdict():
                        alert_snippet = win_match.groupdict()['message']

                    if any(x in upper_type for x in ["ERROR", "FAILED", "CRITICAL"]) or any(x in upper_msg for x in ["FAIL", "ACCESS DENIED", "BRUTE FORCE"]):
                        metrics["failed_logins"] += 1
                        metrics["suspicious_events"] += 1
                        metrics["timeline"][date_key]["failed"] += 1
                        status = "Failed"
                        
                        metrics["recent_alerts"].append(("CRITICAL", f"{event_type}: {alert_snippet[:45]}..."))
                        
                    elif "WARN" in upper_type or "WARNING" in upper_msg:
                        metrics["suspicious_events"] += 1
                        status = "Failed"
                        metrics["recent_alerts"].append(("WARNING", f"Alert: {alert_snippet[:45]}..."))
                        
                    else:
                        metrics["success_logins"] += 1
                        metrics["timeline"][date_key]["success"] += 1
                    
                    metrics["raw_records"].append((message, event_type, timestamp_str if timestamp_str else "N/A", ip_address, status))
                        
        except FileNotFoundError:
            print(f"Engine Warning: Log file not found at '{self.log_file_path}'.")
            
        return metrics