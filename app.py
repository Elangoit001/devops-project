from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    code_file = request.files['code']
    filename = code_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    code_file.save(filepath)

    try:
        result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=5)
        output = result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        output = f"❌ Error during execution: {str(e)}"

    return f"""
    <h2>✅ File uploaded: {filename}</h2>
    <strong>🧪 Output:</strong><br>
    <pre>{output}</pre>
    """

if __name__ == '__main__':
    app.run(debug=True)
