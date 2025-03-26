from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp

# OpenVAS (GVM) sunucu ayarları
HOST = '127.0.0.1'      # Sunucu IP adresi veya hostname
PORT = 9390             # Sunucu port numarası
USERNAME = 'admin'      # Kullanıcı adı
PASSWORD = 'password'   # Şifre

# TLS bağlantısı oluşturma (doğru parametre: hostname)
connection = TLSConnection(hostname=HOST, port=PORT)

# Gmp (Greenbone Management Protocol) kullanarak bağlantı açma ve işlemleri gerçekleştirme
with Gmp(connection=connection) as gmp:
    # Kullanıcı doğrulaması yapılıyor
    gmp.authenticate(username=USERNAME, password=PASSWORD)
    
    # Mevcut tarama görevlerini (tasks) alıyoruz
    tasks_response = gmp.get_tasks()
    
    # Her görevi döngü ile yazdırıyoruz
    for task in tasks_response.xpath('//task'):
        task_id = task.get('id')
        task_name = task.find('name').text
        print(f"Task ID: {task_id}, Task Name: {task_name}")
