# Roblox Django Application

A Django-based web application with WebSocket support for real-time functionality.

## Features

- **User Authentication System**: Login and profile management
- **Real-time WebSocket Communication**: Live status updates and notifications
- **Visitor Tracking**: IP geolocation and analytics
- **Discord Integration**: Webhook notifications for system events
- **Responsive Design**: Roblox-styled interface with modern CSS

## Technology Stack

- **Backend**: Django 6.0.5 with Django Channels
- **Database**: SQLite (development) (Not used)
- **WebSocket**: Daphne ASGI server
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time**: WebSocket for live updates
- **Styling**: Custom CSS with Roblox design patterns

## Project Structure

```
roblox/
├── roblox/                 # Main project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # Project URL routing
│   ├── asgi.py           # ASGI configuration for WebSockets
│   └── wsgi.py           # WSGI configuration
├── people/                # Main application
│   ├── views.py          # Application views and logic
│   ├── urls.py           # App URL routing
│   ├── models.py         # Database models
│   ├── consumers.py      # WebSocket consumers
│   ├── templates/        # HTML templates
│   └── static/           # Static files (CSS, images)
├── static/               # Global static files
├── staticfiles/          # Collected static files
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── db.sqlite3           # Database file
```

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/modernWebDev9/roblox_discord.git
   cd roblox
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

## Running the Application

### Development Server

**Using Daphne (ASGI server with WebSocket support)**
   ```bash
   daphne -b 127.0.0.1 -p 8000 roblox.asgi:application
   ```

### Access the Application

 **Web Interface**: http://127.0.0.1:8000/people/7936348760/userprofile/

## Configuration

### Environment Settings

Key settings in `roblox/settings.py`:

- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Configure for production deployment
- `SECRET_KEY`: Should be kept secret in production
- `DATABASES`: SQLite by default, can be changed to PostgreSQL
- `CHANNEL_LAYERS`: In-memory for development, Redis recommended for production

### Discord Webhook Configuration

To enable Discord notifications:

1. Update the `WEBHOOK_URL` in `people/views.py`
2. Configure proxy settings if needed (optional)

## Features in Detail

### 1. User Authentication
- Login with username/email
- Password validation
- Session management

### 2. WebSocket Real-time Updates
- Live status notifications
- Real-time visitor tracking
- Instant feedback for user actions

### 3. Visitor Analytics
- IP address tracking
- Geolocation information
- User agent detection
- Timestamp logging

### 4. Discord Integration
- Login attempt notifications
- System status updates
- Visitor analytics reporting

## API Endpoints

### HTTP Endpoints
- `GET /`: Home page
- `GET /people/<user_id>/userprofile/`: User profile
- `GET /people/<user_id>/login/`: Login page
- `POST /people/<user_id>/login/submit/`: Login submission
- `POST /people/<user_id>/login/code/`: Verification code submission
- `POST /api/setStatus/`: Status update API

### WebSocket Endpoints
- `ws://localhost:8000/ws/status/`: WebSocket connection for real-time updates

## Deployment

### Production Considerations

1. **Use PostgreSQL instead of SQLite**
2. **Configure Redis for Channel Layers**
3. **Set up proper SSL/TLS certificates**
4. **Use environment variables for secrets**
5. **Configure production-ready static file serving**
6. **Set up monitoring and logging**

### Sample Production Commands
```bash
# Using Gunicorn with Daphne (recommended)
daphne -b 0.0.0.0 -p 8000 roblox.asgi:application

# Using Nginx as reverse proxy
# Configure Nginx to proxy requests to Daphne
```

## Security Notes

- CSRF protection enabled
- Secure cookies configured
- Password validators in place
- Production security settings recommended
- Regular dependency updates advised

## Troubleshooting

### Common Issues

1. **WebSocket connection fails**
   - Ensure Daphne is running, not the standard runserver
   - Check ASGI configuration in `asgi.py`
   - Verify WebSocket route is correctly configured

2. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATICFILES_DIRS` settings
   - Verify WhiteNoise middleware is properly configured

3. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Check database file permissions
   - Verify database connection settings

## License

This project is for educational and development purposes.

## Support

For issues and feature requests, please check the documentation or contact the development team.

---

**Note**: This application uses WebSocket technology for real-time features. Ensure your deployment environment supports ASGI servers like Daphne for full functionality.