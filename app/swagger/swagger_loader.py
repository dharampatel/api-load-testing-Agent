# swagger_loader.py
import json
import yaml
from typing import Dict, List, Any, Tuple

def load_swagger_from_file(path: str) -> Dict[str, Any]:
    """Load swagger (OpenAPI) JSON or YAML and return as dict."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        # Try JSON first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # fallback to YAML
            return yaml.safe_load(text)

def extract_endpoints(swagger: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Returns list of endpoints with method, path, summary, description and parameters snippet.
    Each item:
    {
      "path": "/api/login",
      "method": "POST",
      "summary": "Login user",
      "description": "longer description",
      "parameters": [...],
      "requestBody": {...}  # optional
    }
    """
    endpoints = []
    paths = swagger.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            # OpenAPI v3 uses requestBody, v2 may use parameters
            summary = details.get("summary") or details.get("operationId") or ""
            description = details.get("description", "")
            parameters = details.get("parameters", [])
            request_body = details.get("requestBody")  # might be present
            endpoints.append({
                "path": path,
                "method": method.upper(),
                "summary": summary,
                "description": description,
                "parameters": parameters,
                "requestBody": request_body
            })
    return endpoints

def pretty_print_endpoints(endpoints: List[Dict[str, Any]]) -> None:
    for i, ep in enumerate(endpoints, start=1):
        print(f"{i}. {ep['method']} {ep['path']}")
        if ep.get("summary"):
            print(f"   Summary: {ep['summary']}")
        if ep.get("description"):
            desc = ep['description'] if len(ep['description']) < 200 else ep['description'][:197] + "..."
            print(f"   Desc: {desc}")
        if ep.get("parameters"):
            params = [p.get("name") for p in ep["parameters"] if isinstance(p, dict)]
            if params:
                print(f"   Params: {params}")
        if ep.get("requestBody"):
            print(f"   RequestBody: present")
        print()
