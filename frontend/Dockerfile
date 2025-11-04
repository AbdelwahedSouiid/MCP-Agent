# Build stage uses Node.js
FROM node:22-alpine AS builder   

WORKDIR /app
COPY . /app

# Install dependencies and build
RUN npm ci && npm run build


# Production stage uses Nginx 
FROM nginx:bookworm AS production

# Copy the built files from the builder stage
COPY --from=builder /app/dist/front-chatbot/browser /usr/share/nginx/html

# Set appropriate permissions
RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
