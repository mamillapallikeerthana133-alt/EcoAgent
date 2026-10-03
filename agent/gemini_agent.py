from google import genai
import os


def ask_gemini(device_data):
    """
    Send device information to Gemini and get an AI explanation.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key was not found."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are EcoAgent, an AI assistant that helps users extend
the useful life of electronic devices and reduce unnecessary e-waste.

Analyze the following device:

Device Type: {device_data.get("device_type")}
Brand: {device_data.get("brand")}
Model: {device_data.get("model")}
Age: {device_data.get("age")} years
Physical Condition: {device_data.get("physical_condition")}
Power Status: {device_data.get("power_status")}
Battery Condition: {device_data.get("battery_condition")}
Main Problem: {device_data.get("main_problem")}
RAM: {device_data.get("ram")}
Storage: {device_data.get("storage")}

Explain:
1. What may be causing the problem.
2. Whether repair or upgrade could extend the device's life.
3. Whether the device could be reused or donated.
4. When recycling or safe disposal may be appropriate.

Give a practical, easy-to-understand explanation.
Do not recommend unsafe actions.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini error: {str(e)}"