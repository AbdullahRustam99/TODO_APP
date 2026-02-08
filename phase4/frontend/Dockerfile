# Development Dockerfile for Next.js Frontend
FROM node:20-alpine

# Install dependencies for healthcheck
RUN apk add --no-cache curl libc6-compat

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY . .

# Environment variables
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# These will be overridden by docker-compose or runtime env
ENV NEXT_PUBLIC_API_URL=http://localhost:8001
ENV NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=gemini-todo-dev

# Expose por-t
EXPOSE 3000

# Health check - basic check that the server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Start the development server with hot reload
CMD ["npm", "run", "dev"]