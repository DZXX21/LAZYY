import json

# JSON dosyanızın yolunu belirtin
input_json_file = "cikti.json"
output_html_file = "output.html"

# JSON dosyasını oku
with open(input_json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# data değişkeni bir listeyse, her eleman bir satır (dict) olarak düşünülür.
# Eğer JSON yapınız farklı ise ona göre uyarlayabilirsiniz.
# Örneğin: data = data["items"] vb. gibi.

# İlk satır (dict) üzerinden sütun adlarını alalım
# Sütun adlarını sabitlemek istiyorsanız elle de verebilirsiniz.
columns = data[0].keys()

# HTML tablo kodunu oluşturma
html_content = "<html>\n"
html_content += "<head>\n"
html_content += "    <meta charset='UTF-8'>\n"
html_content += "    <title>JSON to HTML Table</title>\n"
html_content += "</head>\n"
html_content += "<body>\n"
html_content += "    <table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse;'>\n"
html_content += "        <thead>\n"
html_content += "            <tr>\n"

# Sütun başlıkları
for col in columns:
    html_content += f"                <th>{col}</th>\n"
html_content += "            </tr>\n"
html_content += "        </thead>\n"
html_content += "        <tbody>\n"

# Her bir satır (dict) için tablo gövdesini doldur
for row in data:
    html_content += "            <tr>\n"
    for col in columns:
        # İlgili sütunda değer yoksa boş string atayalım
        cell_value = row.get(col, "")
        html_content += f"                <td>{cell_value}</td>\n"
    html_content += "            </tr>\n"

html_content += "        </tbody>\n"
html_content += "    </table>\n"
html_content += "</body>\n"
html_content += "</html>"

# Ortaya çıkan HTML içeriğini dosyaya yazalım
with open(output_html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML tablo '{output_html_file}' dosyasına yazıldı.")
