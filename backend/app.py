from flask import Flask , jsonify , request
from flask_cors import CORS
import yaml , os
from dotenv import load_dotenv
from pathlib import Path 
import openai

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


@app.route('/generate',methods=['POST'])
def generate_resume_coverletter():
    data = request.json
    job_desc = data.get('jobDescription')
    user_exp=load_experience_config()
    resume_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert career coach."},
            {"role": "user", "content": f"Create a resume based on: {user_exp} for the job: {job_desc}"}
        ]
    )
    return jsonify({"data":resume_response})


if __name__=="__main__":
    app.run(debug=True)
    