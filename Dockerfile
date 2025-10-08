FROM docker:27-dind
WORKDIR /app
COPY . .
CMD ["docker", "compose", "up", "--build"]
