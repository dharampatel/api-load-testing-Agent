import subprocess
import os
import json
from app.locust_test.locust_builder import build_locust_file


def run_locust_node(state):
    print("🧠 [Node] Running Locust load test...")

    swagger_path = state.swagger_path
    base_url = state.base_url
    users = state.users
    spawn_rate = state.spawn_rate
    run_time = state.run_time
    endpoints = state.endpoints or []
    payloads = getattr(state, "payloads", [])

    print(f"🌐 Using Base URL: {base_url}")

    # ✅ Always save results inside project/app folder
    base_dir = os.path.join(os.path.dirname(__file__), "..")  # one level up (app/)
    results_dir = os.path.abspath(os.path.join(base_dir, "loadtest_results"))
    os.makedirs(results_dir, exist_ok=True)
    csv_prefix = os.path.join(results_dir, "locust_result")

    print(f"📁 Results will be saved in: {results_dir}")

    # ✅ Sanitize payloads
    fixed_payloads = []
    for p in payloads:
        if isinstance(p, dict):
            fixed_payloads.append(p)
        elif isinstance(p, list):
            fixed_payloads.extend(p)
        else:
            print(f"⚠️ Skipping invalid payload type: {type(p)}")

    if not fixed_payloads:
        print("⚠️ No valid payloads found, continuing with empty payloads.")
    else:
        print(f"✅ Using {len(fixed_payloads)} valid payloads.")

    # ✅ Build Locust test file dynamically
    build_locust_file(swagger_path, base_url, list(range(len(endpoints))))

    # Save payloads preview
    with open(os.path.join(results_dir, "payloads_preview.json"), "w") as f:
        json.dump(fixed_payloads[:5], f, indent=2)

    print("💾 Payload preview saved.")

    # ✅ Run Locust headlessly and direct CSV output path
    try:
        result = subprocess.run(
            [
                "locust",
                "-f", "locustfile_dynamic.py",
                "--headless",
                "-u", str(users),
                "-r", str(spawn_rate),
                "--run-time", run_time,
                "--csv", csv_prefix
            ],
            check=False,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            error_path = os.path.join(results_dir, "locust_error.log")
            with open(error_path, "w") as f:
                f.write(result.stderr or "No stderr output")
            print(f"❌ Locust failed. See log: {error_path}")
            raise RuntimeError("Locust failed. Check error log for details.")

    except Exception as e:
        print(f"❌ Error running Locust: {e}")
        raise

    # ✅ Locate CSV with absolute path
    csv_path = os.path.join(results_dir, "locust_result_stats.csv")
    if not os.path.exists(csv_path):
        print("⚠️ locust_result_stats.csv not found in:", results_dir)
        summary_text = f"❌ Locust test failed — CSV not found in {results_dir}"
    else:
        print(f"✅ Load test complete → {csv_path}")
        summary_text = (
            f"✅ Locust test completed successfully!\n"
            f"🌐 Base URL: {base_url}\n"
            f"👥 Users: {users}\n"
            f"⚡ Spawn Rate: {spawn_rate}/s\n"
            f"⏱️ Run Time: {run_time}\n"
            f"🧩 Endpoints Tested: {len(endpoints)}\n"
            f"📊 Results File: {csv_path}"
        )

    # ✅ Return full CSV path
    return state.model_copy(update={
        "locust_result_csv": csv_path,
        "summary": summary_text
    })
