import os
import zipfile
import io
from flask import Flask, request, send_file, jsonify
from cairosvg import svg2eps
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size 16MB

# Endpoint untuk mengkonversi SVG ke EPS
@app.route('/convert', methods=['POST'])
def convert_svg_to_eps():
    try:
        # Cek apakah ada file yang diupload
        if 'files' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diupload'}), 400
        
        files = request.files.getlist('files')
        scale = float(request.form.get('scale', 1.0))  # Default scale 1.0
        
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        # Buat buffer untuk file ZIP
        zip_buffer = io.BytesIO()
        
        # Buat file ZIP di memory
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                if file and file.filename.lower().endswith('.svg'):
                    # Baca konten SVG
                    svg_content = file.read()
                    
                    # Konversi ke EPS
                    eps_content = svg2eps(bytestring=svg_content, scale=scale)
                    
                    # Tambahkan ke ZIP dengan nama yang sesuai
                    eps_filename = os.path.splitext(secure_filename(file.filename))[0] + '.eps'
                    zip_file.writestr(eps_filename, eps_content)
        
        # Reset pointer buffer
        zip_buffer.seek(0)
        
        # Kirim file ZIP sebagai response
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='converted_files.zip'
        )
    
    except Exception as e:
        return jsonify({'error': f'Gagal mengonversi file: {str(e)}'}), 500

# Endpoint untuk info API
@app.route('/', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'SVG to EPS Converter API',
        'description': 'API untuk mengkonversi file SVG ke EPS',
        'endpoints': {
            '/': 'GET - Info API',
            '/convert': 'POST - Konversi SVG ke EPS (upload file dengan key "files" dan parameter "scale")'
        },
        'scale_options': [f'{i}x' for i in range(1, 11)]
    })

# if __name__ == '__main__':
#     app.run()
