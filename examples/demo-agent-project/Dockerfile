FROM python:3.12

ENV OPENAI_API_KEY=sk-proj-FAKE-DEMO-KEY
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "agent.py"]
