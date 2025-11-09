FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY streamlit_app ./streamlit_app
COPY artifacts ./artifacts

ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    CHECKOV_REPORT_PATH=/app/artifacts/checkov_report.json

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app/app.py"]
