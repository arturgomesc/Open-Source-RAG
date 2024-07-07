FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HUGGINGFACEHUB_API_TOKEN=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

EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py"]