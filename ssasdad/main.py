import xlrd
import json

dosya_yolu = "/home/dzx/Belgeler/GitHub/LAZY/ssasdad/22.xls"

# 1) XLS dosyasını aç
workbook = xlrd.open_workbook(dosya_yolu)
sheet = workbook.sheet_by_index(0)

# 2) İlk satırı kolon başlıkları (headers) olarak alalım
headers = []
for col_idx in range(sheet.ncols):
    # Hücre değeri (içinde \n varsa bile tek satırda string olarak gelir)
    val = sheet.cell_value(0, col_idx)
    # Boş ise "Unnamed_Column_X" diyebilirsiniz veya istediğiniz gibi işleyebilirsiniz
    if not val:
        val = f"Unnamed_Column_{col_idx}"
    headers.append(val)

# 3) Sonraki satırları (row_idx = 1'den başlayarak) veri olarak oku
data = []
for row_idx in range(1, sheet.nrows):
    row_data = {}
    for col_idx in range(sheet.ncols):
        key = headers[col_idx]
        value = sheet.cell_value(row_idx, col_idx)
        row_data[key] = value
    data.append(row_data)

# 4) JSON’a yazalım
json_dosya = "cikti.json"
with open(json_dosya, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Dönüştürme tamamlandı! => {json_dosya}")
