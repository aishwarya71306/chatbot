from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest

from config import Config
from services.ai_service import AIService, AIServiceError
from services.image_service import ImageService, ImageServiceError

app = Flask(__name__)
app.config.from_object(Config)
ai_service = AIService(Config)
image_service = ImageService(Config)


def error_response(message, status=400):
    return jsonify({"success": False, "error": message}), status


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/chat")
def chat():
    try:
        payload = request.get_json(silent=True)
    except BadRequest:
        return error_response("Request body must contain valid JSON.")
    if not isinstance(payload, dict):
        return error_response("Request body must be a JSON object.")
    message = payload.get("message")
    conversation = payload.get("conversation", [])
    if not isinstance(message, str) or not message.strip():
        return error_response("Please enter a message.")
    if not isinstance(conversation, list):
        return error_response("Conversation must be a list.")
    try:
        response = ai_service.generate_response(message.strip(), conversation)
        return jsonify({"success": True, "response": response})
    except AIServiceError as error:
        return error_response(str(error), error.status_code)


@app.post("/api/generate-image")
def generate_image():
    try:
        payload = request.get_json(silent=True)
    except BadRequest:
        return error_response("Request body must contain valid JSON.")
    if not isinstance(payload, dict):
        return error_response("Request body must be a JSON object.")
    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return error_response("Please describe the image you want.")
    try:
        image_url = image_service.generate_image(prompt.strip())
        return jsonify({"success": True, "image_url": image_url, "prompt": prompt.strip()})
    except ImageServiceError as error:
        return error_response(str(error), error.status_code)


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return error_response("API route not found.", 404)
    return error


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
