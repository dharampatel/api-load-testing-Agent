import json

def generate_payload_node(state):
    print("🧠 [Node] Generating payloads for endpoints...")

    endpoints = getattr(state, "endpoints", None)
    if not endpoints:
        raise ValueError("No endpoints found in state. Make sure parse_swagger_node ran successfully.")

    generated_payloads = {}

    for ep in endpoints:
        method = ep.get("method", "GET")
        url = ep.get("url", "")
        payload = {}

        if "body" in ep and isinstance(ep["body"], dict):
            payload = ep["body"]
        else:
            payload = {"example": "test"}

        generated_payloads[url] = {
            "method": method,
            "payload": payload
        }

    print(f"✅ Generated payloads for {len(generated_payloads)} endpoints.")
    return state.model_copy(update={"payloads": generated_payloads})
