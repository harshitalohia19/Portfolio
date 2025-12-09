from flask import Flask, render_template, jsonify

app = Flask(__name__)

projects = [
    {
        "name": "Autonomous Drone Reforestation",
        "stack": ["Python", "DeepForest", "Rasterio"],
        "description": "Drone imagery pipeline for reforestation planning."
    },
    {
        "name": "AI Receipt Automation Bot",
        "stack": ["Python", "n8n", "Mistral OCR"],
        "description": "Automates receipt processing and expense tracking."
    },
]

@app.route("/")
def home():
    return render_template("index.html", projects=projects)

@app.route("/api/projects")
def api_projects():
    return jsonify(projects)

if __name__ == "__main__":
    app.run(debug=True)
