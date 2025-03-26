const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

// JSON istek gövdesini ayrıştırmak için middleware
app.use(express.json());
// Public klasöründeki statik dosyaları sun
app.use(express.static(path.join(__dirname, 'public')));

app.post('/save', (req, res) => {
  const jsonData = req.body;
  const filePath = path.join(__dirname, 'public', 'cikti.json');
  
  fs.writeFile(filePath, JSON.stringify(jsonData, null, 2), (err) => {
    if (err) {
      console.error("Dosya kaydedilemedi:", err);
      return res.status(500).send("Dosya kaydedilemedi.");
    }
    res.send("Dosya başarıyla kaydedildi.");
  });
});

app.listen(PORT, () => {
  console.log(`Sunucu ${PORT} portunda çalışıyor.`);
});
