# Use a Node.js base image
FROM node:18 AS builder

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

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
