# Stage 1: Build Stage
FROM node:20-bullseye AS builder

WORKDIR /app
ARG NODE_ENV="production"
ARG REACT_APP_API_URL

ENV NODE_ENV="${NODE_ENV}" \
    REACT_APP_API_URL="${REACT_APP_API_URL}"

# Copy client package files specifically
COPY client/package*.json ./
RUN npm install

# Copy client directory contents
COPY client/ ./
RUN if [ "$NODE_ENV" = "production" ]; then npm run build; fi

# Stage 2: Final Stage
FROM node:20-bullseye-slim

WORKDIR /app
RUN apt-get update && apt-get install -y curl && \
    npm install -g serve && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app /app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -v http://localhost:5000 || exit 1

CMD if [ "$NODE_ENV" = "production" ]; then \
        serve -s dist -l 5000; \
    else \
        npm run dev; \
    fi