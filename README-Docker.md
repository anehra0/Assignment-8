# Personal Website Assignment - Docker Setup

This Flask personal website has been Dockerized for easy deployment and development.

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Direct Flask app: http://localhost:5000
   - With nginx (production): http://localhost:80

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t personal-website .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 personal-website
   ```

## Development vs Production

### Development Mode
```bash
# Run with development settings
FLASK_ENV=development docker-compose up --build
```

### Production Mode
```bash
# Run with nginx reverse proxy
docker-compose --profile production up --build
```

## Environment Variables

- `FLASK_ENV`: Set to `development` for debug mode, `production` for production
- `FLASK_HOST`: Host to bind to (default: 0.0.0.0)
- `FLASK_PORT`: Port to bind to (default: 5000)

## File Structure

```
├── Dockerfile              # Main Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── .dockerignore          # Files to exclude from Docker build
├── nginx.conf             # Nginx configuration for production
├── flask_app/             # Flask application
│   ├── app.py            # Main Flask application
│   ├── DAL.py            # Database access layer
│   ├── projects.db       # SQLite database
│   ├── static/           # Static files (CSS, images)
│   └── templates/        # HTML templates
└── files/                # Additional files (resume)
```

## Database Persistence

The SQLite database (`projects.db`) is mounted as a volume to ensure data persistence across container restarts.

## Health Checks

The application includes health checks that verify the Flask app is responding correctly.

## Troubleshooting

1. **Port already in use:**
   - Change the port mapping in `docker-compose.yml`
   - Or stop other services using port 5000

2. **Database issues:**
   - The database will be created automatically on first run
   - Check file permissions if you encounter database errors

3. **Static files not loading:**
   - Ensure the static files are properly copied into the container
   - Check nginx configuration if using the production profile
