from locust import HttpUser, task, between
import random

class ImageResizeUser(HttpUser):
    wait_time = between(0.01, 0.05)  

    @task
    def resize_image(self):
        image_name = "myimage.jpg"  
        dimensions = self.generate_random_dimensions()
        url = f"http://34.57.154.255/resize/{dimensions}/{image_name}"

        with self.client.get(url, catch_response=True) as response:
            
            if response.status_code == 200:
                cache_status = response.headers.get("X-Cache-Status", "N/A")
                response.success()
                print(f"URL: {url} | Status: {response.status_code} | Cache: {cache_status}")
            else:
                response.failure(f"Request failed with status {response.status_code}")

    def generate_random_dimensions(self):
        width = random.randint(1, 10) * 10  
        height = random.randint(1, 10) * 10  
        return f"{width}x{height}"


