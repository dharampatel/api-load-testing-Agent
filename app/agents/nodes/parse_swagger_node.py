from app.swagger.swagger_parser import parse_swagger

def parse_swagger_node(state):
    print("[Node] Parsing Swagger file...")
    endpoints = parse_swagger(state.swagger_path)
    print(f"Parsed {len(endpoints)} endpoints.")
    return state.model_copy(update={"endpoints": endpoints})
