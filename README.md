# 🚀 Building an Automated API Load Testing Dashboard with AI Agent, Streamlit & Locust


Modern API performance testing — powered by AI agents, Streamlit UI, and Locust for distributed load generation.

# 🧩 Overview

#### This project demonstrates how to automate API load testing end-to-end using:

. 🤖 AI Agents to analyze Swagger files and dynamically generate Locust scripts

. 📊 Streamlit Dashboard for interactive execution and result visualization

. 🐍 Locust as the scalable performance engine

#### The system automatically:

1. Reads your Swagger/OpenAPI specification

2. Builds a dynamic locustfile

3. Executes tests with configurable parameters

4. Summarizes metrics with AI-driven insights

# ⚙️ Tech Stack
1. **Python 3.13+**: 	Core language
2. **Streamlit**:	Interactive web UI
3. **Locust**:	Load testing engine
4. **FastAPI / Custom API**: 	Optional backend integration
5. **AI Agent Framework**: 	Handles orchestration, summarization, and test logic

 # 🧠 Architecture

        ┌──────────────┐
        │ Swagger File │
        └──────┬───────┘
               │
               ▼
        🤖 AI Agent parses endpoints
               │
               ▼
      🧱 Generates dynamic locustfile
               │
               ▼
        🚀 Executes headless Locust test
               │
               ▼
       📊 Streamlit UI displays results


# 🧪 Key Features

1. **Dynamic Test Generation:** Builds load tests directly from Swagger specs

2. **Headless Execution:** Runs Locust seamlessly with subprocess

3. **Automated CSV Parsing:** AI agent summarizes locust_result_stats.csv

4. **Interactive UI:** Visual dashboards and test controls in Streamlit

5. **Error-Safe Workflows:** Handles missing payloads and logs automatically

# 🧾 Sample Output

#### CLI Logs

✅ Load test complete → /app/agents/loadtest_results/locust_result_stats.csv
Summary by Endpoint:
- GET /sample: 18 reqs, 0 fails, Avg 12.75 ms
- POST /upload-swagger: 24 reqs, 0 fails, Avg 10.79 ms

# Streamlit Dashboard

. Displays request counts, response times, and failure rates

. Saves CSVs automatically for further analysis

<img width="1661" height="772" alt="Screenshot 2025-10-31 at 9 37 12 AM" src="https://github.com/user-attachments/assets/659a0877-8987-4df0-91c3-2d97671702d0" />

<img width="1663" height="875" alt="Screenshot 2025-10-31 at 9 37 42 AM" src="https://github.com/user-attachments/assets/f022d047-5d62-49fe-965e-6957153b36b8" />


# 🔮 Future Enhancements

1. 🧩 Multi-Agent Support (payload generation, anomaly detection)

2. 📈 Real-time metrics streaming during test execution

3. ☁️ Cloud scaling with distributed Locust workers

4. 🧠 AI insights & recommendations after test runs

5. 🔗 CI/CD integration for automated performance gating

# 🏁 Conclusion

This project transforms traditional load testing into a self-driven, intelligent process — from parsing APIs to visualizing results — with zero manual scripting.
It’s a foundation for the next generation of AI-assisted QA engineering.

⚡ "Test smarter, not harder — let AI handle the load."



