import os
import subprocess
import uuid
from flask import Flask, request, render_template_string

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def clear_uploads():
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>C Compiler</title>
</head>
<body>
    <h2>Upload C files and an Optional Input File</h2>
    <form action="/" method="post" enctype="multipart/form-data">
        <p>Provide the C File/s</p>
        <input type="file" name="c_files" multiple required><br><br>
        <p>Provide Input File (Optional)</p>
        <input type="file" name="input_file" accept=".txt"><br><br>
        <input type="submit" value="Compile and Run">
    </form>
    <form action="/clear" method="post">
        <input type="submit" value="Clear Uploads Folder">
    </form>
    {% if output %}
    <h3>Output:</h3>
    <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def upload_and_compile():
    if request.method == "POST":
        # Generate unique ID for this compilation
        job_id = str(uuid.uuid4())
        job_folder = os.path.join(UPLOAD_FOLDER, job_id)
        os.makedirs(job_folder)

        c_files = request.files.getlist("c_files")
        input_file = request.files.get("input_file")
        
        c_filenames = []
        for file in c_files:
            if file.filename.endswith(".c") or file.filename.endswith(".h"):
                filepath = os.path.join(job_folder, file.filename)
                file.save(filepath)
                c_filenames.append(filepath)
        
        input_filepath = None
        if input_file and input_file.filename:
            input_filepath = os.path.join(job_folder, "input.txt")
            input_file.save(input_filepath)
        
        executable = os.path.join(job_folder, "program.out")
        
        # Compile the C files while preserving original filenames
        compile_cmd = ["gcc"] + [os.path.join(job_folder, file.filename) for file in c_files] + ["-o", executable]
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if compile_result.returncode != 0:
            return render_template_string(HTML_TEMPLATE, output=f"Compilation Error:\n{compile_result.stderr}")
        
        # Run the compiled program
        run_cmd = [executable]
        if input_filepath:
            with open(input_filepath, "r") as input_file:
                run_result = subprocess.run(run_cmd, stdin=input_file, capture_output=True, text=True)
        else:
            run_result = subprocess.run(run_cmd, capture_output=True, text=True)
        
        return render_template_string(HTML_TEMPLATE, output=run_result.stdout + run_result.stderr)
    
    return render_template_string(HTML_TEMPLATE)

@app.route("/clear", methods=["POST"])
def clear_folder():
    clear_uploads()
    return render_template_string(HTML_TEMPLATE, output="Uploads folder cleared successfully.")

if __name__ == "__main__":
    os.system("git pull origin main")  # Auto-update from GitHub
    app.run(host="0.0.0.0", port=5000, debug=True)
