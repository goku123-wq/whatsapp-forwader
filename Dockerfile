FROM ghcr.io/puppeteer/puppeteer:latest

# We switch to root to install some global things if needed, or just run as the puppeteer user
USER root

WORKDIR /app

# Copy package.json and install
COPY package*.json ./
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
RUN npm ci

# Copy the rest of the application
COPY . .

# Ensure the puppeteer user has permissions over the app directory
RUN chown -R pptruser:pptruser /app

# Switch back to the non-privileged user for security
USER pptruser

EXPOSE 3000

# Start the application
CMD ["npm", "start"]
