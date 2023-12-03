import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# AWS S3 Configuration
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name="us-east-1"
)
bucket_name = os.environ.get('S3_BUCKET_NAME')  # Replace with your S3 bucket name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def list_files():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, )
        files = [file['Key'] for file in response.get('Contents', [])] if 'Contents' in response else []
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        s3.upload_fileobj(file, bucket_name, file.filename)
        return jsonify({'message': f'{file.filename} uploaded successfully'})
    else:
        return jsonify({'message': 'No file provided'}), 400

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        s3.delete_object(Bucket=bucket_name, Key=filename)
        return jsonify({'message': f'{filename} deleted successfully'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
