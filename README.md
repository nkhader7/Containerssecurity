# Containerssecurity

This project demonstrates how to scan infrastructure-as-code with [Checkov](https://www.checkov.io/) and review remediation guidance through a Streamlit application backed by an LLM.

## Prerequisites

- Docker or another OCI-compliant runtime that can pull the `bridgecrew/checkov` image.
- Python 3.11+ (only required if you prefer to run the Streamlit app locally without Docker).
- An OpenAI API key if you want LLM-powered remediation suggestions (optional; the UI falls back to static guidance when not configured).

## Running the automated Checkov scan

Use the helper script to run Checkov inside a container and export the results to `artifacts/checkov_report.json`:

```bash
./scripts/run_checkov.sh
```

The script mounts the repository into the official Checkov container and saves the JSON report locally so the Streamlit app can ingest it.

## Reviewing results in the Streamlit app

### Docker Compose workflow

A `docker-compose.yml` file is provided to orchestrate both the scan and the Streamlit interface:

```bash
# Run the scan and launch the dashboard
OPENAI_API_KEY=sk-... docker compose up
```

The `checkov` service runs once to refresh the report, and the `streamlit` service starts the dashboard at [http://localhost:8501](http://localhost:8501).

### Local Python workflow

Alternatively, install the dependencies and launch Streamlit directly:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
CHECKOV_REPORT_PATH=artifacts/checkov_report.json streamlit run streamlit_app/app.py
```

Upload a Checkov JSON report from the sidebar or rely on the default path if the automated scan has already populated it. Select a failed check to inspect the details and, if an OpenAI API key is configured, request an AI-generated remediation suggestion.

## Container YAML reference

For platforms that consume a generic container specification, `container.yaml` captures the same workflow: one job runs the Checkov scan, and a second job launches the Streamlit remediation assistant with the generated report mounted as a shared artifact.
