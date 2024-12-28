from flask import Flask , jsonify
from flask_cors import CORS

app= Flask(__name__)

# applying CORS 
CORS(app)


@app.route('/generate',methods=['GET'])
def generate_resume_coverletter():
    return jsonify({"data":"successful"})


if __name__=="__main__":
    app.run(debug=True)
    