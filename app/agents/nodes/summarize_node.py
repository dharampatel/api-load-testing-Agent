import os
import pandas as pd

def summarize_node(state):
    print("[Node] Summarizing Locust results...")
    csv_path = state.locust_result_csv
    if not csv_path or not os.path.exists(csv_path):
        raise FileNotFoundError(" Locust results CSV not found")

    df = pd.read_csv(csv_path)
    summary_lines = ["Summary by Endpoint:"]

    for _, row in df.iterrows():
        endpoint = f"{row.get('Type', '')} {row.get('Name', '')}"
        reqs = row.get('Request Count', row.get('# requests', 0))
        fails = row.get('Failure Count', row.get('# fails', 0))
        avg = row.get('Average Response Time', row.get('Average response time', 0))
        summary_lines.append(f"- {endpoint}: {reqs} reqs, {fails} fails, Avg {avg:.2f} ms")

    total_fails = df.get('Failure Count', df.get('# fails', pd.Series())).sum()
    if total_fails == 0:
        summary_lines.append("\nNo failures recorded.")
    else:
        summary_lines.append(f"\nTotal Failures: {int(total_fails)}")

    summary_text = "\n".join(summary_lines)
    print(summary_text)

    return state.model_copy(update={"summary": summary_text})
