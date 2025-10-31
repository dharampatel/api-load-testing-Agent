from langgraph.graph import StateGraph
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.agents.nodes.parse_swagger_node import parse_swagger_node
from app.agents.nodes.generate_payload_node import generate_payload_node
from app.agents.nodes.run_locust_node import run_locust_node
from app.agents.nodes.summarize_node import summarize_node


#  Define structured state with Pydantic for validation and clarity
class LoadTestState(BaseModel):
    swagger_path: str = Field(..., description="Path to the Swagger/OpenAPI JSON file")
    users: int = Field(10, description="Number of virtual users for the load test")
    spawn_rate: int = Field(2, description="Spawn rate (users per second)")
    run_time: str = Field("10s", description="Total run time of the test")
    base_url: Optional[str] = Field(None, description="Base URL of the API")
    endpoints: Optional[List[Dict[str, Any]]] = Field(default=None, description="Parsed endpoints from Swagger")
    payloads: Optional[Dict[str, Any]] = Field(default=None, description="Generated request payloads")
    results: Optional[Dict[str, Any]] = Field(default=None, description="Load test results summary")
    locust_result_csv: Optional[str] = Field(default=None, description="Path to Locust CSV result file")
    summary: Optional[str] = Field(default=None, description="Final test summary report")


def create_load_test_graph():
    graph = StateGraph(LoadTestState)

    graph.add_node("parse_swagger", parse_swagger_node)
    graph.add_node("generate_payload", generate_payload_node)
    graph.add_node("run_locust", run_locust_node)
    graph.add_node("summary", summarize_node)

    graph.add_edge("parse_swagger", "generate_payload")
    graph.add_edge("generate_payload", "run_locust")
    graph.add_edge("run_locust", "summary")

    graph.set_entry_point("parse_swagger")

    return graph.compile()

load_graph = create_load_test_graph()

if __name__ == "__main__":
    initial_state = LoadTestState(
        swagger_path="/Users/dharmendrapr/Desktop/AUTOGEN/ApiLoadTesting/demo.json",
        users=10,
        spawn_rate=2,
        run_time="10s",
        base_url="http://localhost:8000"

    )
    final_state = load_graph.invoke(initial_state)
    print("Final State:")
    print(final_state)
