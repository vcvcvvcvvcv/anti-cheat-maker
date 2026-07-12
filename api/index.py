import os
import requests
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Credentials (Set these in your Vercel Environment Variables dashboard)
PLAYFAB_TITLE_ID = os.environ.get("PLAYFAB_TITLE_ID", "YOUR_TITLE_ID")
PLAYFAB_SECRET_KEY = os.environ.get("PLAYFAB_SECRET_KEY", "YOUR_SECRET_KEY")
SERVER_API_KEY = os.environ.get("SERVER_API_KEY", "your_secure_api_key")

# Animated HTML Splash Page Template with custom SVG Monke
HTML_SPLASH = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backend Status</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(-45deg, #8a2be2, #4b0082, #1e90ff, #00ff7f);
            background-size: 400% 400%;
            animation: gradientAnimation 12s ease infinite;
            color: white;
            overflow: hidden;
        }

        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .status-card {
            background: rgba(0, 0, 0, 0.65);
            padding: 40px 50px;
            border-radius: 24px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }

        /* Stylized Gorilla Tag Low-Poly Inspired Monkey Wrapper */
        .gtag-monke {
            width: 100px;
            height: 100px;
            filter: drop-shadow(0 0 15px rgba(138, 43, 226, 0.8));
            animation: floatMonke 4s ease-in-out infinite;
        }

        @keyframes floatMonke {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(3deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: linear-gradient(45deg, #00ffff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        p {
            font-size: 1.2rem;
            font-weight: 500;
            letter-spacing: 1px;
            color: #b3b3b3;
        }

        .pulse-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: #00ff7f;
            border-radius: 50%;
            box-shadow: 0 0 15px #00ff7f;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.6; }
        }
    </style>
</head>
<body>

    <div class="status-card">
        <div class="gtag-monke">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <path d="M20,40 C20,20 80,20 80,40 C80,55 75,75 50,75 C25,75 20,55 20,40 Z" fill="#4a2c11"/>
                <circle cx="18" cy="40" r="10" fill="#4a2c11"/>
                <circle cx="18" cy="40" r="6" fill="#c39b7d"/>
                <circle cx="82" cy="40" r="10" fill="#4a2c11"/>
                <circle cx="82" cy="40" r="6" fill="#c39b7d"/>
                <path d="M28,45 C28,32 45,30 50,38 C55,30 72,32 72,45 C72,58 65,68 50,68 C35,68 28,58 28,45 Z" fill="#c39b7d"/>
                <rect x="38" y="42" width="6" height="6" rx="1" fill="#000000"/>
                <rect x="56" y="42" width="6" height="6" rx="1" fill="#000000"/>
                <circle cx="46" cy="54" r="2" fill="#3a200a"/>
                <circle cx="54" cy="54" r="2" fill="#3a200a"/>
                <path d="M42,60 Q50,64 58,60" stroke="#3a200a" stroke-width="2" stroke-linecap="round" fill="none"/>
            </svg>
        </div>

        <h1><span class="pulse-dot"></span>Backend Running</h1>
        <p>by exotic don't skid</p>
    </div>

</body>
</html>
"""

# ==========================================
# CORE GAME SERVICES
# ==========================================

class PlayFabManager:
    """Validates player sessions and fetches global config from PlayFab."""
    
    @staticmethod
    def verify_session_ticket(session_ticket):
        if not PLAYFAB_TITLE_ID or not PLAYFAB_SECRET_KEY:
            return True 
            
        url = f"https://{PLAYFAB_TITLE_ID}.playfabapi.com/Server/AuthenticateSessionTicket"
        headers = {
            "X-SecretKey": PLAYFAB_SECRET_KEY,
            "Content-Type": "application/json"
        }
        payload = {"SessionTicket": session_ticket}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json().get("data", {}).get("IsSessionValid", False)
            return False
        except requests.RequestException:
            return False

    @staticmethod
    def get_title_data(keys_list):
        if not PLAYFAB_TITLE_ID or not PLAYFAB_SECRET_KEY:
            return {"MOTD": "Welcome to the game! (Server Local Fallback)"}
            
        url = f"https://{PLAYFAB_TITLE_ID}.playfabapi.com/Server/GetTitleData"
        headers = {
            "X-SecretKey": PLAYFAB_SECRET_KEY,
            "Content-Type": "application/json"
        }
        payload = {"Keys": keys_list}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json().get("data", {}).get("Data", {})
            return {}
        except requests.RequestException:
            return {}

class ServerSideAntiCheat:
    """Validates physics boundaries sent by the game server/host."""
    MAX_ALLOWED_SPEED = 18.5  
    MAX_RIG_SCALE = 1.15      
    MIN_RIG_SCALE = 0.85

    @classmethod
    def validate_telemetry(cls, current_velocity, scale_factor, ping):
        latency_buffer = (ping / 1000.0) * 5.0
        dynamic_max_speed = cls.MAX_ALLOWED_SPEED + latency_buffer

        if current_velocity > dynamic_max_speed:
            return {"valid": False, "reason": "SPEED_HACK"}
        if scale_factor > cls.MAX_RIG_SCALE or scale_factor < cls.MIN_RIG_SCALE:
            return {"valid": False, "reason": "LONG_ARMS"}

        return {"valid": True, "reason": "CLEAN"}

# ==========================================
# BACKEND API ENDPOINTS
# ==========================================

@app.route('/')
def home():
    """Serves the animated status screen when accessing the main link directly."""
    return render_template_string(HTML_SPLASH)

@app.route('/api/motd', methods=['GET'])
def get_motd():
    title_data = PlayFabManager.get_title_data(["MOTD"])
    current_motd = title_data.get("MOTD", "No Message of the Day has been configured yet.")
    return jsonify({
        "success": True,
        "motd": current_motd
    }), 200

@app.route('/api/verify-player', methods=['POST'])
def verify_player():
    data = request.json or {}
    playfab_ticket = data.get("playfab_ticket")

    if not playfab_ticket:
        return jsonify({"success": False, "error": "Missing PlayFab session ticket"}), 400

    if not PlayFabManager.verify_session_ticket(playfab_ticket):
        return jsonify({"success": False, "error": "PlayFab identity validation failed"}), 401

    return jsonify({"success": True, "status": "Authenticated"}), 200

@app.route('/api/anti-cheat/check', methods=['POST'])
def check_telemetry():
    if request.headers.get("X-Server-Auth-Token") != SERVER_API_KEY:
        return jsonify({"success": False, "error": "Unauthorized endpoint access"}), 403

    data = request.json or {}
    try:
        velocity = float(data.get("velocity", 0.0))
        scale = float(data.get("scale", 1.0))
        ping = int(data.get("ping", 50))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid numerical data formats"}), 400

    result = ServerSideAntiCheat.validate_telemetry(velocity, scale, ping)
    return jsonify({
        "is_clean": result["valid"],
        "flag_status": result["reason"]
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
