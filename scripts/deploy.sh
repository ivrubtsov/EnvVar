#!/bin/bash

# Deployment script with environment variable usage

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Configuration
DEPLOY_ENV=${DEPLOY_ENVIRONMENT:-production}
DEPLOY_USER=${DEPLOY_USER:-ubuntu}
DEPLOY_HOST=${DEPLOY_HOST}
DEPLOY_PATH=${DEPLOY_PATH:-/var/www/app}
SSH_KEY=${SSH_KEY_PATH:-~/.ssh/id_rsa}

# Build configuration
NODE_ENV=${NODE_ENV:-production}
BUILD_ARGS="--mode ${NODE_ENV}"

# Docker configuration
DOCKER_REGISTRY=${DOCKER_REGISTRY:-docker.io}
DOCKER_USERNAME=${DOCKER_USERNAME}
DOCKER_PASSWORD=${DOCKER_PASSWORD}
IMAGE_NAME=${DOCKER_IMAGE_NAME:-myapp}
IMAGE_TAG=${DOCKER_IMAGE_TAG:-latest}

# Database migration
DB_MIGRATION_TIMEOUT=${DB_MIGRATION_TIMEOUT:-300}
RUN_MIGRATIONS=${RUN_MIGRATIONS:-true}

# Health check
HEALTH_CHECK_URL=${HEALTH_CHECK_URL:-http://localhost:3000/health}
HEALTH_CHECK_RETRIES=${HEALTH_CHECK_RETRIES:-5}
HEALTH_CHECK_INTERVAL=${HEALTH_CHECK_INTERVAL:-10}

# Notification
SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
NOTIFY_ON_SUCCESS=${NOTIFY_ON_SUCCESS:-true}
NOTIFY_ON_FAILURE=${NOTIFY_ON_FAILURE:-true}

echo "================================"
echo "Deployment Configuration"
echo "================================"
echo "Environment: $DEPLOY_ENV"
echo "Host: $DEPLOY_HOST"
echo "User: $DEPLOY_USER"
echo "Path: $DEPLOY_PATH"
echo "Image: $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
echo "================================"

# Validate required variables
if [ -z "$DEPLOY_HOST" ]; then
    echo "Error: DEPLOY_HOST is required"
    exit 1
fi

if [ -z "$DOCKER_USERNAME" ]; then
    echo "Error: DOCKER_USERNAME is required"
    exit 1
fi

# Docker login
echo "Logging into Docker registry..."
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "$DOCKER_REGISTRY"

# Build Docker image
echo "Building Docker image..."
docker build \
    --build-arg NODE_ENV="$NODE_ENV" \
    --build-arg BUILD_NUMBER="${BUILD_NUMBER:-unknown}" \
    -t "$DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG" \
    .

# Push image
echo "Pushing Docker image..."
docker push "$DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"

# Run database migrations if enabled
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running database migrations..."
    ssh -i "$SSH_KEY" "$DEPLOY_USER@$DEPLOY_HOST" \
        "cd $DEPLOY_PATH && docker-compose run --rm backend npm run migrate"
fi

# Deploy to server
echo "Deploying to server..."
ssh -i "$SSH_KEY" "$DEPLOY_USER@$DEPLOY_HOST" << EOF
    cd $DEPLOY_PATH
    docker-compose pull
    docker-compose up -d
    docker-compose ps
EOF

# Health check
echo "Performing health check..."
for i in $(seq 1 $HEALTH_CHECK_RETRIES); do
    if curl -f "$HEALTH_CHECK_URL" > /dev/null 2>&1; then
        echo "Health check passed"
        break
    fi
    
    if [ $i -eq $HEALTH_CHECK_RETRIES ]; then
        echo "Health check failed after $HEALTH_CHECK_RETRIES attempts"
        exit 1
    fi
    
    echo "Health check attempt $i/$HEALTH_CHECK_RETRIES failed, retrying in ${HEALTH_CHECK_INTERVAL}s..."
    sleep $HEALTH_CHECK_INTERVAL
done

# Send notification
if [ "$NOTIFY_ON_SUCCESS" = "true" ] && [ -n "$SLACK_WEBHOOK_URL" ]; then
    curl -X POST "$SLACK_WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "{\"text\":\"Deployment successful: $IMAGE_NAME:$IMAGE_TAG to $DEPLOY_ENV\"}"
fi

echo "Deployment completed successfully!"
