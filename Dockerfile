FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python", "run.py"]