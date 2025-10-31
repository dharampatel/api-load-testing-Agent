# app/locust_builder.py
import json
from app.swagger.swagger_parser import parse_swagger

LOCUST_TEMPLATE = """from locust import HttpUser, task, between
import random
import json

class APIUser(HttpUser):
    wait_time = between(1, 3)
    host = "{base_url}"

{endpoint_tasks}
"""

TASK_TEMPLATE = """    @task
    def {func_name}(self):
        url = "{path}"
        method = "{method}".upper()
        headers = {headers}
        payload = {payload}

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

            print(f"✅ {{method}} {{url}} executed successfully")

        except Exception as e:
            print(f"❌ Error executing {{method}} {{url}}: {{str(e)}}")
"""

def build_locust_file(swagger_path: str, base_url: str, selected_indexes):
    endpoints = parse_swagger(swagger_path)

    if isinstance(selected_indexes, list):
        selected = [endpoints[i] for i in selected_indexes if i < len(endpoints)]
    elif selected_indexes == "all":
        selected = endpoints
    else:
        raise ValueError("Invalid selected_indexes format")

    endpoint_tasks = ""

    for idx, ep in enumerate(selected):
        func_name = f"task_{ep['method'].lower()}_{idx}"
        path = ep["path"]

        headers = {"Content-Type": "application/json"}
        payload = {}

        # ✅ Smart defaults for known endpoints
        if "/upload-swagger" in path:
            payload = {
                "swagger_path": "/Users/dharmendrapr/Desktop/AUTOGEN/ApiLoadTesting/demo.json",
                "users": 5,
                "spawn_rate": 2,
                "run_time": "10s"
            }

        # ✅ Otherwise, generate from schema if available
        else:
            req_body = ep.get("requestBody", {})
            if req_body:
                content = req_body.get("content", {})
                app_json = content.get("application/json", {})
                schema = app_json.get("schema", {})
                props = schema.get("properties", {})
                for k, v in props.items():
                    if v.get("type") == "string":
                        payload[k] = "example"
                    elif v.get("type") == "integer":
                        payload[k] = 123
                    elif v.get("type") == "boolean":
                        payload[k] = True

        endpoint_tasks += TASK_TEMPLATE.format(
            func_name=func_name,
            path=path,
            method=ep["method"],
            headers=json.dumps(headers),
            payload=json.dumps(payload),
        )

    locust_code = LOCUST_TEMPLATE.format(
        base_url=base_url.rstrip("/"),
        endpoint_tasks=endpoint_tasks
    )

    with open("locustfile_dynamic.py", "w") as f:
        f.write(locust_code)

    print("✅ locustfile_dynamic.py generated successfully for multiple endpoints.")
