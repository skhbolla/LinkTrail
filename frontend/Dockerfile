# frontend/Dockerfile
FROM node:24

WORKDIR /home

# Copy package files first for caching
COPY ./app/package*.json .

# Install dependencies
RUN npm install

# Copy source code (will be overridden by volume in dev)
COPY app .

# Start dev server
CMD ["npm", "start"]
