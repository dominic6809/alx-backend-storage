# 0x01-NoSQL

## 1. PEP 8 Style Guidelines
- Emphasized the importance of adhering to PEP 8 style guidelines for Python code.
- Key aspects include:
  - Proper indentation and spacing.
  - Naming conventions for functions and variables.
  - Line length limits for readability.

## 2. MongoDB and Python Integration
- Explored the usage of PyMongo to interact with MongoDB collections.
- Discussed functions to:
  - Count documents in a collection.
  - Aggregate and sort data, specifically for IP addresses in logs.

## 3. Logging Statistics
- Developed a Python script (`102-log_stats.py`) that provides statistics about Nginx logs:
  - Total number of logs.
  - Counts of HTTP methods (GET, POST, PUT, PATCH, DELETE).
  - Number of status checks for the `/status` path.
  - Top 10 IP addresses sorted by occurrence.

## 4. Code Implementation
- Implemented a function to print log statistics, including:
  - Using MongoDB aggregation to group and count IP addresses.
  - Outputting structured log statistics in a readable format.

## 5. Code Example
Here’s a snippet of the implemented function:

```python
def print_log_stats(mongo_collection):
    """Prints stats about Nginx logs."""
    # Count total logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")
    
    # Top 10 IPs
    ip_counts = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    
    for ip in ip_counts:
        print(f"\t{ip['_id']}: {ip['count']}")
