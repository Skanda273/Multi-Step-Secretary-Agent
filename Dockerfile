FROM python:3.10

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Build the frontend dashboard so the dist folder is available
WORKDIR /app/openenv-dashboard
RUN npm install
RUN npm run build

# Go back to the main app directory
WORKDIR /app

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["/bin/bash", "start.sh"]
