from flask import Blueprint, render_template, request, redirect
import base64
from io import BytesIO
import qrcode
from barcode import Code39, Code128
from barcode.writer import ImageWriter

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        code_type = request.form['types']
        code_content = request.form['content']
        
        if code_content == "":
            return redirect('/')
        
        if "BARCODE" in code_type:
            if code_type == "BARCODE39":
                img = Code39(code_content, writer=ImageWriter())
            else:
                img = Code128(code_content, writer=ImageWriter())
            memory = BytesIO()
            img.write(memory)
            memory.seek(0)
            encodestr = base64.b64encode(memory.getvalue()).decode('utf-8')
            code = "data:image/png;base64," + encodestr
        
        elif code_type == "QR":
            memory = BytesIO()
            img = qrcode.make(code_content)
            img.save(memory)
            memory.seek(0)
            encodestr = base64.b64encode(memory.getvalue()).decode('utf-8')
            code = "data:image/png;base64," + encodestr

        return render_template('index.html', code=code, encodestr=encodestr, code_content=code_content)
    else:
        return render_template('index.html')