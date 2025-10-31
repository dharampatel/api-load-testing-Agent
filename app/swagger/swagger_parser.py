# swagger_parser.py
import json
from typing import List, Dict, Any

def parse_swagger(swagger_path: str) -> List[Dict[str, Any]]:
    """
    Parse Swagger/OpenAPI JSON and extract endpoint metadata.
    Supports OpenAPI 3.x specification.
    """
    with open(swagger_path, "r") as f:
        data = json.load(f)

    endpoints = []

    paths = data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            endpoint = {
                "path": path,
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "description": details.get("description", ""),
                "parameters": details.get("parameters", []),
                "requestBody": details.get("requestBody", {}),
                "tags": details.get("tags", []),
            }
            endpoints.append(endpoint)

    return endpoints


# Optional helper: for quick check
if __name__ == "__main__":
    swagger_file = "/demo.json"  # change if needed
    eps = parse_swagger(swagger_file)
    for e in eps:
        print(f"{e['method']} {e['path']}")
