from flask import Flask, request, jsonify, render_template, Response
import mysql.connector
import os

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'user': 'rabin',
    'password': 'Rabin@123',
    'host': 'mysql-db',  # Update to MySQL server IP or hostname
    'database': 'file_storage_db',
    'port': 3306,  # Update to MySQL server port
    'auth_plugin': 'mysql_native_password'  # Use the default authentication plugin
}

# Route for rendering index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute('INSERT INTO files (name, content) VALUES (%s, %s)', (file.filename, file.read()))
        file_id = cursor.lastrowid

        file_path = os.path.join('/app/uploads', str(file_id))
        file.save(file_path)

        connection.commit()
        connection.close()

        return jsonify({'message': 'File uploaded successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for getting list of files
@app.route('/files')
def get_files():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute('SELECT id, name FROM files')
        files = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

        connection.close()
        # Render files.html and pass 'files' data to the template
        return render_template('files.html', files=files)
    except mysql.connector.Error as err:
        # Log the error for debugging
        app.logger.error(f"MySQL Error: {err.msg}")

        # Return JSON response with error message
        return jsonify({'error': f"MySQL Error: {err.msg}"}), 500
    except Exception as e:
        # Log any unexpected exception for debugging
        app.logger.error(f"Unexpected Error: {str(e)}")

        # Return JSON response with error message
        return jsonify({'error': 'Failed to fetch file list.'}), 500

# Route for downloading a file
@app.route('/download/<int:file_id>')
def download_file(file_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute('SELECT name FROM files WHERE id = %s', (file_id,))
        file_data = cursor.fetchone()

        if not file_data:
            return jsonify({'error': 'File not found.'}), 404

        file_name = file_data[0]
        file_path = os.path.join('/app/uploads', str(file_id))

        with open(file_path, 'rb') as f:
            file_content = f.read()

        response = Response(file_content, mimetype='application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)