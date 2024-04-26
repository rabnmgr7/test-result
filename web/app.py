from flask import Flask, request, jsonify, render_template, send_file
import mysql.connector
import os
import time

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
    time.sleep(10)
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

        # Insert file metadata into database
        cursor.execute('INSERT INTO files (name) VALUES (%s)', (file.filename,))
        file_id = cursor.lastrowid

        # Save file to uploads directory
        file_path = os.path.join('uploads', str(file_id))
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
        return jsonify(files), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        file_path = os.path.join('uploads', str(file_id))

        return send_file(file_path, attachment_filename=file_name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)