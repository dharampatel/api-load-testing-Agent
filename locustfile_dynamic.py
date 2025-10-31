from locust import HttpUser, task, between
import random
import json

class APIUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"

    @task
    def task_get_0(self):
        url = "/sample"
        method = "GET".upper()
        headers = {"Content-Type": "application/json"}
        payload = {}

        try:
            if method == "GET":
                # ✅ Send as query parameters
                self.client.get(url, headers=headers, params=payload)
            elif method == "POST":
                # ✅ Send JSON body
                self.client.post(url, headers=headers, json=payload)
            elif method == "PUT":
                self.client.put(url, headers=headers, json=payload)
            elif method == "DELETE":
                self.client.delete(url, headers=headers)
            else:
                # ✅ For any other HTTP verbs
                self.client.request(method, url, headers=headers, json=payload)

            print(f"✅ {method} {url} executed successfully")

        except Exception as e:
            print(f"❌ Error executing {method} {url}: {str(e)}")
    @task
    def task_post_1(self):
        url = "/upload-swagger"
        method = "POST".upper()
        headers = {"Content-Type": "application/json"}
        payload = {"swagger_path": "/Users/dharmendrapr/Desktop/AUTOGEN/ApiLoadTesting/demo.json", "users": 5, "spawn_rate": 2, "run_time": "10s"}

        try:
            if method == "GET":
                # ✅ Send as query parameters
                self.client.get(url, headers=headers, params=payload)
            elif method == "POST":
                # ✅ Send JSON body
                self.client.post(url, headers=headers, json=payload)
            elif method == "PUT":
                self.client.put(url, headers=headers, json=payload)
            elif method == "DELETE":
                self.client.delete(url, headers=headers)
            else:
                # ✅ For any other HTTP verbs
                self.client.request(method, url, headers=headers, json=payload)

            print(f"✅ {method} {url} executed successfully")

        except Exception as e:
            print(f"❌ Error executing {method} {url}: {str(e)}")

