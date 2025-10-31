# request_generator.py (improved generate_value)
from typing import Dict, Any, List
from faker import Faker
import random

fake = Faker()

def generate_value(schema: Dict[str, Any], field_name: str = "") -> Any:
    """Generate realistic fake value based on schema and field name."""
    t = schema.get("type", "string")
    fmt = schema.get("format", "")
    desc = schema.get("description", "").lower()
    name = field_name.lower()

    # 🎯 Handle string types
    if t == "string":
        if fmt == "email" or "email" in name:
            return fake.email()
        if fmt == "date-time" or "date" in name:
            return fake.iso8601()
        if "name" in name:
            return fake.name()
        if "phone" in name or "mobile" in name:
            return fake.phone_number()
        if "address" in name:
            return fake.address()
        if "city" in name:
            return fake.city()
        if "country" in name:
            return fake.country()
        if "username" in name:
            return fake.user_name()
        if "password" in name:
            return fake.password()
        if "url" in name:
            return fake.url()
        # Default fallback
        return fake.word()

    # 🎯 Integer / number
    elif t == "integer":
        return random.randint(1, 1000)
    elif t == "number":
        return round(random.uniform(1.0, 1000.0), 2)

    # 🎯 Boolean
    elif t == "boolean":
        return random.choice([True, False])

    # 🎯 Array
    elif t == "array":
        item_schema = schema.get("items", {"type": "string"})
        return [generate_value(item_schema, field_name) for _ in range(random.randint(1, 3))]

    # 🎯 Object
    elif t == "object":
        props = schema.get("properties", {})
        return {k: generate_value(v, k) for k, v in props.items()}

    return None


def generate_query_params(parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate query params for an endpoint."""
    params = {}
    for p in parameters:
        if p.get("in") == "query":
            schema = p.get("schema", {"type": "string"})
            params[p["name"]] = generate_value(schema, p["name"])
    return params


def generate_request_body(request_body: Dict[str, Any]) -> Dict[str, Any]:
    """Generate request body based on schema."""
    if not request_body:
        return {}
    content = request_body.get("content", {})
    json_schema = (
        content.get("application/json", {})
        .get("schema", {"type": "object", "properties": {}})
    )
    if "properties" in json_schema:
        return {k: generate_value(v, k) for k, v in json_schema["properties"].items()}
    return {}


def build_request(endpoint: Dict[str, Any], base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """Build a complete request example."""
    path = endpoint["path"]
    method = endpoint["method"]
    parameters = endpoint.get("parameters", [])
    request_body = endpoint.get("requestBody")

    query_params = generate_query_params(parameters)
    query_str = (
        "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])
        if query_params else ""
    )

    json_body = generate_request_body(request_body)

    return {
        "method": method,
        "url": f"{base_url}{path}{query_str}",
        "body": json_body,
        "headers": {"Content-Type": "application/json"},
    }
