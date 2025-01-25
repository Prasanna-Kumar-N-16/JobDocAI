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

@app.route('/generate', methods=['POST'])
def generate_resume_coverletter():
    data = request.json
    job_desc = data.get('jobDescription')
    user_exp = load_experience_config()

    # Load resume template
    # Create a base resume string from user_exp
    base_resume = f"""
    Name: {user_exp.get('name', '')}
    Email: {user_exp.get('email', '')}
    Phone: {user_exp.get('phone', '')}
    Objective: {user_exp.get('objective', '')}
    Education: {user_exp.get('education', '')}
    Experience: {user_exp.get('experience', '')}
    Skills: {user_exp.get('skills', '')}
    """

    prompt = f"""
    Given the following base resume:

    {base_resume}

    And the job description:

    {job_desc}

    Please provide:
    1. An updated resume tailored to the job description.
    2. A cover letter for this job application.

    Format the response as follows:
    [RESUME]
    (Updated resume content here)
    [/RESUME]

    [COVER_LETTER]
    (Cover letter content here)
    [/COVER_LETTER]
    """

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
    