from flask import Blueprint, request, send_file
import io
import base64
from PIL import Image

download_bp = Blueprint('download', __name__)

@download_bp.route('/download', methods=['POST'])
def download():
    img = request.form['img']
    code_content = request.form['content']
    
    memory = io.BytesIO()
    decodedimg = base64.b64decode(img)
    image = Image.open(io.BytesIO(decodedimg))
    image.save(memory, format='PNG')
    memory.seek(0)
    
    return send_file(
        memory,
        mimetype='image/png',
        download_name=f'{code_content}.png',
        as_attachment=True
    )