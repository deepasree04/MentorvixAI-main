from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# --- Configuration ---

# Initialize the Gemini 2.0 Flash model with system instructions
# This defines the persona of MENTORVIX AI
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
        "You are MENTORVIX AI, a helpful career assistant. "
        "You give concise, practical advice on career paths, skills, roadmaps, "
        "and learning resources. Keep responses friendly and to the point."
    )
)

# --- Page Views ---

@api_view(['GET'])
def home(request):
    """Renders the main landing page."""
    return render(request, "home_page/home.html")


def ai_chat_page(request):
    """Renders the dedicated AI chat interface."""
    return render(request, "chat/aichat.html")


# --- API Logic ---

@api_view(["POST"])
def ai_chat(request):
    """
    Handles POST requests from the frontend, sends user input to Gemini,
    and returns the AI's response.
    """
    # Extract the message sent from the JavaScript fetch call
    user_input = request.data.get("message")

    if not user_input:
        return Response({"error": "No input provided"}, status=400)

    try:
        # Generate content using the initialized Gemini model
        response = model.generate_content(user_input)
        
        # Return the text portion of the Gemini response
        return Response({"reply": response.text})

    except Exception as e:
        # Catch errors (e.g., API quota limits, network issues)
        return Response({"error": str(e)}, status=500)