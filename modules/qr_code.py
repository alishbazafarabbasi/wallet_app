import qrcode
import io
import base64

def generate_qr_code(data):
    if not isinstance(data, str):
        raise ValueError("Data must be a string")
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

