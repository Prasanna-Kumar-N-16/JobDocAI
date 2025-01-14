from flask import Flask , jsonify , request
from flask_cors import CORS
import yaml , os
from dotenv import load_dotenv
from pathlib import Path 
import openai
from jinja2 import Template

app= Flask(__name__)

# applying CORS 
CORS(app)

BASE_DIR = Path(__file__).parent.parent

# Load environment variables from the config directory
env_path = BASE_DIR / 'config' / '.env'
load_dotenv(env_path)

openai.api_key = os.getenv('OPENAI_API_KEY')


def load_experience_config():
    """Load experience data from YAML configuration file"""
    yaml_path = BASE_DIR / 'config' / 'experience.yaml'
    try:
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Experience config not found at {yaml_path}")

@app.route('/generate', methods=['GET'])
def generate_resume_coverletter():
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "objective": "To secure a software engineering position.",
        "education": "B.Sc. in Computer Science, XYZ University, 2022",
        "experience": "Software Engineer at ABC Corp (2022-2023)",
        "skills": "Python, Java, Flask, React"
    }

    with open('resume_template.txt', 'r') as file:
        template = Template(file.read())

    # Render resume
    resume = template.render(user_data)
    print(resume)

@app.route('/generate', methods=['POST'])
def generate_resume_coverletter():
    data = request.json
    job_desc = data.get('jobDescription')
    user_exp = load_experience_config()

    try:
        # Call the OpenAI Chat API
        resume_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert career coach."},
                {"role": "user", "content": f"Create a resume based on: {user_exp} for the job: {job_desc}"}
            ]
        )

        # Extract the response text
        generated_text = resume_response['choices'][0]['message']['content']
        return jsonify({"data": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__=="__main__":
    app.run(debug=True)
    