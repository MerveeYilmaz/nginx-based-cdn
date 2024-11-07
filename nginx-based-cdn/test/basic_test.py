import requests
import random
import time
import concurrent.futures


base_url = "http://34.57.154.255/resize/"



def generate_random_dimensions():
    width = random.randint(1, 20) * 100  
    height = random.randint(1, 20) * 100  
    return f"{width}x{height}"



def make_request(image_name):
    dimensions = generate_random_dimensions()
    url = f"{base_url}{dimensions}/{image_name}"

    start_time = time.time()  
    try:
        response = requests.get(url, timeout=10)  
        elapsed_time = time.time() - start_time  
        cache_status = response.headers.get("X-Cache-Status", "N/A")  
        return (url, response.status_code, elapsed_time, cache_status)
    except requests.exceptions.RequestException as e:
        elapsed_time = time.time() - start_time
        return (url, "Error", elapsed_time, "N/A")



def main():
    image_name = "myimage.jpg"  
    num_requests = 1000  

    hit_count = 0
    miss_count = 0
    na_count = 0
    success_count = 0
    error_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        future_to_request = {executor.submit(make_request, image_name): i for i in range(num_requests)}

        for future in concurrent.futures.as_completed(future_to_request):
            url, status_code, elapsed_time, cache_status = future.result()
            print(f"URL: {url} | Status: {status_code} | Time: {elapsed_time:.4f} seconds | Cache: {cache_status}")

            
            if cache_status == "HIT":
                hit_count += 1
            elif cache_status == "MISS":
                miss_count += 1
            elif cache_status == "N/A":
                na_count += 1

            
            if status_code == 200:
                success_count += 1
            else:
                error_count += 1

        
    total_requests = hit_count + miss_count + na_count
    hit_ratio = (hit_count / total_requests) * 100 if total_requests > 0 else 0
    miss_ratio = (miss_count / total_requests) * 100 if total_requests > 0 else 0

    
    total_success = success_count + error_count
    success_ratio = (success_count / total_success) * 100 if total_success > 0 else 0
    error_ratio = (error_count / total_success) * 100 if total_success > 0 else 0

    print(f"\nTotal Requests: {total_requests}")
    print(f"Cache Hits: {hit_count} ({hit_ratio:.2f}%)")
    print(f"Cache Misses: {miss_count} ({miss_ratio:.2f}%)")
    print(f"Success Responses (200): {success_count} ({success_ratio:.2f}%)")
    print(f"Error Responses: {error_count} ({error_ratio:.2f}%)")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Total time for 1000 requests: {time.time() - start_time:.4f} seconds")
