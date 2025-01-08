# Use a Node.js base image
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package.json and yarn.lock first for caching
COPY package.json yarn.lock ./

# Install dependencies with Yarn
RUN yarn install

# Copy the rest of the code
COPY . .

# Build the application
RUN yarn build

# Use a lightweight web server, e.g., nginx
FROM nginx:stable-alpine
COPY --from=builder /app/build /usr/share/nginx/html

# Add script to generate env config at runtime
RUN apk add --no-cache bash
COPY env.sh /docker-entrypoint.d/
RUN chmod +x /docker-entrypoint.d/env.sh

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
