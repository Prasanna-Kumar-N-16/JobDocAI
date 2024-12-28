from flask import Flask , jsonify
from flask_cors import CORS
import yaml
from pathlib import Path 

app= Flask(__name__)

# applying CORS 
CORS(app)

BASE_DIR = Path(__file__).parent.parent


def load_experience_config():
    """Load experience data from YAML configuration file"""
    yaml_path = BASE_DIR / 'config' / 'experience.yaml'
    try:
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Experience config not found at {yaml_path}")


@app.route('/generate',methods=['GET'])
def generate_resume_coverletter():
    return jsonify({"data":"successful"})


if __name__=="__main__":
    app.run(debug=True)
    