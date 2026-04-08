FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python", "inference.py"]