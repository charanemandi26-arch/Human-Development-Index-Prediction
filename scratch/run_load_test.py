import urllib.request
import urllib.parse
import time
import concurrent.futures
import json

# Target URL for prediction
url = "http://127.0.0.1:7860/predict"

# Sample feature inputs to send
payload = {
    "life_expectancy": "72.5",
    "mean_schooling": "10.2",
    "expected_schooling": "13.1",
    "gni": "18500",
    "gdi": "0.95",
    "gii": "0.32",
    "co2": "4.5"
}

data_encoded = urllib.parse.urlencode(payload).encode("utf-8")

def send_single_request():
    start = time.perf_counter()
    try:
        req = urllib.request.Request(url, data=data_encoded, method="POST")
        # Add headers to simulate form submission
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            response.read() # Read response to complete
            latency = time.perf_counter() - start
            return status, latency
    except Exception as e:
        latency = time.perf_counter() - start
        return "ERROR", latency

def run_scenario(name, num_users, total_reqs):
    print(f"\nRunning {name} ({num_users} Virtual Users, {total_reqs} total requests)...")
    
    # Warm up request to make sure server is awake
    send_single_request()
    
    start_time = time.perf_counter()
    latencies = []
    errors = 0
    
    # Run requests concurrently using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = [executor.submit(send_single_request) for _ in range(total_reqs)]
        for future in concurrent.futures.as_completed(futures):
            status, latency = future.result()
            if status != 200:
                errors += 1
            latencies.append(latency)
            
    total_duration = time.perf_counter() - start_time
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    throughput = len(latencies) / total_duration if total_duration > 0 else 0
    error_rate = (errors / len(latencies)) * 100 if latencies else 0
    
    print(f"  Total Duration: {total_duration:.3f} seconds")
    print(f"  Average Latency: {avg_latency * 1000:.1f} ms")
    print(f"  Maximum Latency: {max_latency * 1000:.1f} ms")
    print(f"  Throughput: {throughput:.1f} requests/sec")
    print(f"  Error Rate: {error_rate:.1f}%")
    
    return {
        "avg": avg_latency,
        "max": max_latency,
        "throughput": throughput,
        "error_rate": error_rate
    }

def main():
    print("==================================================")
    print("HDI Predictor - Performance & Load Testing Tool")
    print("==================================================")
    print(f"Testing Endpoint: {url}")
    print("Make sure your Flask server is running (python app.py) before starting!")
    
    try:
        # Check if server is running
        urllib.request.urlopen("http://127.0.0.1:7860", timeout=2)
    except Exception as e:
        print("\nERROR: Cannot connect to the Flask server.")
        print("Please start the server first in another terminal using:")
        print("  python app.py")
        return

    # Scenario 1: Baseline
    res1 = run_scenario("Scenario 1: Baseline Request", num_users=1, total_reqs=10)
    
    # Scenario 2: Load Test
    res2 = run_scenario("Scenario 2: Load Testing", num_users=5, total_reqs=50)
    
    # Scenario 3: Concurrency Spike
    res3 = run_scenario("Scenario 3: Concurrency Spike", num_users=15, total_reqs=150)
    
    print("\n" + "="*50)
    print("PERFORMANCE RESULTS SUMMARY TABLE")
    print("="*50)
    print(f"{'Metric':<25} | {'Target Value':<15} | {'Actual Value':<15} | {'Status':<8}")
    print("-"*70)
    
    def check_pass(val, target, op="<"):
        if op == "<":
            return "Pass" if val < target else "Fail"
        return "Pass" if val > target else "Fail"

    # We evaluate using the Load Testing scenario (Scenario 2) as baseline load
    avg_ms = res2["avg"] * 1000
    max_ms = res2["max"] * 1000
    tp = res2["throughput"]
    err = res2["error_rate"]
    
    print(f"{'Response Time (Avg)':<25} | {'< 2 seconds':<15} | {f'{avg_ms:.1f} ms':<15} | {check_pass(res2['avg'], 2.0)}")
    print(f"{'Response Time (Max)':<25} | {'< 5 seconds':<15} | {f'{max_ms:.1f} ms':<15} | {check_pass(res2['max'], 5.0)}")
    print(f"{'Throughput (Req/sec)':<25} | {'> 20 req/s':<15} | {f'{tp:.1f} req/s':<15} | {check_pass(tp, 20, '>')}")
    print(f"{'Error Rate':<25} | {'< 1%':<15} | {f'{err:.1f}%':<15} | {check_pass(err, 1.0)}")
    print("="*50)
    print("Take a screenshot of this output and upload it to the chat!")

if __name__ == "__main__":
    main()
