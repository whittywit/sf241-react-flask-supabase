import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)

# CORS allows your React frontend (on Vercel/Netlify) to make requests to this API
CORS(app) 

# Environment Variables from Render Settings
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Initialize Supabase
if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")
else:
    supabase: Client = create_client(url, key)

# --- ROUTES ---

@app.route('/')
def index():
    """Root route to prevent 404 on the main URL"""
    return jsonify({
        "status": "online",
        "message": "Guestbook API is running. Use /guestbook to fetch data."
    }), 200

@app.route('/guestbook', methods=['GET'])
def get_entries():
    """Fetch all guestbook entries"""
    try:
        response = supabase.table("guestbook").select("*").order("created_at", desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guestbook', methods=['POST'])
def add_entry():
    """Add a new entry"""
    data = request.json
    try:
        response = supabase.table("guestbook").insert(data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/guestbook/<id>', methods=['PUT'])
def update_entry(id):
    """Update an existing entry"""
    data = request.json
    try:
        response = supabase.table("guestbook").update(data).eq("id", id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/guestbook/<id>', methods=['DELETE'])
def delete_entry(id):
    """Delete an entry"""
    try:
        supabase.table("guestbook").delete().eq("id", id).execute()
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- SERVER START ---

if __name__ == '__main__':
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' is required for Render to route traffic to your app
    app.run(host='0.0.0.0', port=port)
