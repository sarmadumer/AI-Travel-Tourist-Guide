from flask import Flask, request, jsonify
from ai21 import AI21Client
from ai21.models.chat import ChatMessage
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# AI21 client
client = AI21Client(api_key=os.getenv("AI21_API_KEY"))

@app.route("/get_travel_info", methods=["POST"])
def get_travel_info():
    data = request.json
    country = data.get("country", "").strip()
    city = data.get("city", "").strip()

    if not country:
        return jsonify({"error": "Country is required"}), 400

    # Prompt for AI21
    prompt = f"""

You are a professional travel guide AI.

GOAL
Return a short, tourist-attractive list of destinations for the given location.

INPUT
Country: {country}
City/State: {city if city else "Not specified"}

STRICT OUTPUT RULES:
- Output MUST be valid HTML only (no Markdown, no code fences, no JSON).
- Do NOT add any text before or after the HTML.
- Keep it concise and professional.
- Use the exact structure below.

FORMAT (copy exactly, filling in the values)
<p>📍 <strong>Country:</strong> {country}</p>
<p>🏙️ <strong>City/State:</strong> {city if city else "Not specified"}</p>
<h3>✨ Highlights</h3>
<ul>
  <li><strong>Destination 1</strong> — 3–8 word teaser.</li>
  <li><strong>Destination 2</strong> — 3–8 word teaser.</li>
  <li><strong>Destination 3</strong> — 3–8 word teaser.</li>
  <li><strong>Destination 4</strong> — 3–8 word teaser.</li>
  <li><strong>Destination 5</strong> — 3–8 word teaser.</li>
  <li><strong>Destination 6</strong> — 3–8 word teaser.</li>
</ul>

CONTENT GUIDELINES
- If City/State is provided: pick well-known local spots first, then major national icons (still one list).
- If City/State is not provided: pick notable destinations across the country.
- Destination names MUST be bold (<strong>Name</strong>).
- Teasers MUST be short (no full sentences, no long explanations).
- Never include safety disclaimers, pricing, or travel logistics.
- Never include headings other than the ones specified above.
"""

    try:
        response = client.chat.completions.create(
            model="jamba-mini",   # Or jamba-instruct / jamba-large depending on access
            messages=[ChatMessage(content=prompt, role="user")],
        )
        travel_info = response.choices[0].message.content.strip()
        return jsonify({"travel_info": travel_info})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
