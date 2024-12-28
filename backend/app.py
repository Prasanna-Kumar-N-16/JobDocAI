from flask import Flask , jsonify
from flask_cors import CORS
import yaml
from pathlib import Path 

app= Flask(__name__)

# applying CORS 
CORS(app)

BASE_DIR = Path(__file__).parent.parent

print(BASE_DIR)

def load_experience_config():
    """Load experience data from YAML configuration file"""
    with open('config/experience.yaml', 'r') as file:
        return yaml.safe_load(file)


@app.route('/generate',methods=['GET'])
def generate_resume_coverletter():
    return jsonify({"data":"successful"})


if __name__=="__main__":
    app.run(debug=True)
    