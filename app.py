import io
from flask import Flask, render_template, url_for, request, redirect, send_file
import qrcode
from barcode import Code39, Code128
from barcode.writer import ImageWriter 
from io import BytesIO
import base64 
from PIL import Image


app = Flask(__name__,static_folder='static')

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        code_type = request.form['types']
        code_content = request.form['content']
        if code_content == "":
            return redirect('/')
        
        if("BARCODE" in code_type):
            if(code_type == "BARCODE39"):
                img = Code39(code_content, writer=ImageWriter())
            else:
                img = Code128(code_content, writer=ImageWriter())
            memory = BytesIO()
            img.write(memory)
            memory.seek(0)
            encodestr = base64.b64encode(memory.getvalue()).decode('utf-8')
            code = "data:image/png;base64," + encodestr
        
        elif(code_type == "QR"):
            memory = BytesIO()
            img = qrcode.make(code_content)
            img.save(memory)
            memory.seek(0)
            encodestr = base64.b64encode(memory.getvalue()).decode('utf-8')
            code = "data:image/png;base64," + encodestr

        return render_template('index.html',code=code, encodestr=encodestr, code_content=code_content)
    else:
        return render_template('index.html')
    
@app.route('/download', methods=['POST'])
def download():
    img = request.form['img']
    code_content = request.form['content']
    memory = io.BytesIO()
    decodedimg = base64.b64decode(img)
    image = Image.open(io.BytesIO(decodedimg))
    image.save(memory,format='PNG')
    memory.seek(0)
    return send_file(
        memory,
        mimetype='image/png',
        download_name=f'{code_content}.png',
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=False)
