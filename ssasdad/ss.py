import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    # Çalışma dizininin tam yolunu alıyoruz
    base_path = os.getcwd()
    file_path = os.path.join(base_path, "output.html")
    
    # Dosyanın varlığını kontrol ediyoruz
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as f:
            html_content = f.read()
        return html_content
    else:
        return f"<h1>Hata:</h1><p>{file_path} dosyası bulunamadı.</p>", 404

if __name__ == '__main__':
    # Tüm ağ arayüzlerinden bağlantı kabul etmek için host '0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)
