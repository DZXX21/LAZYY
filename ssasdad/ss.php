function osgb_hesaplama_form() {
    ob_start();
    ?>
    <div style="max-width: 500px; margin: auto; padding: 20px; border-radius: 10px; background: #ffffff; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); text-align: center;">
        <h3 style="color: #0073aa;">🛠️ OSGB Hizmet Süresi Hesaplama</h3>

        <!-- NACE Kodu Girişi -->
        <p style="font-weight: bold;">İşyeri NACE Kodunu Girin:</p>
        <input type="text" id="nace_kodu" placeholder="Örn: 01.11.07" style="width: 80%; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; text-align: center;" oninput="belirleTehlikeSinifi()">

        <p style="font-weight: bold; margin-top: 10px;">Sınıf: <span id="tehlike_sinifi">-</span></p>

        <!-- Çalışan Sayısı -->
        <p style="margin-top: 15px; font-weight: bold;">Çalışan Sayısını Girin:</p>
        <input type="number" id="calisan_sayisi" min="1" value="10" style="width: 80%; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; text-align: center;" oninput="hesaplaOSGB()">

        <!-- Sonuçlar -->
        <h4 style="margin-top: 20px; color: #0073aa;">📊 Hesaplama Sonuçları</h4>
        <p>👷‍♂️ <strong>İş Güvenliği Uzmanı:</strong> <span id="uzman_sonuc">-</span></p>
        <p>🏥 <strong>İşyeri Hekimi:</strong> <span id="hekim_sonuc">-</span></p>
        <p>🩺 <strong>Diğer Sağlık Personeli:</strong> <span id="dsp_sonuc">-</span></p>
    </div>

    <script>
    function belirleTehlikeSinifi() {
        let naceKodu = document.getElementById("nace_kodu").value.trim();

        fetch("<?php echo site_url(); ?>/wp-content/uploads/nace_tehlike.csv")
        .then(response => response.text())
        .then(data => {
            let lines = data.split("\n");
            let found = "Bilinmiyor";
            
            for (let i = 1; i < lines.length; i++) {
                let columns = lines[i].split(",");
                if (columns[0].trim() === naceKodu) {
                    found = columns[2].trim();
                    break;
                }
            }

            document.getElementById("tehlike_sinifi").innerText = found;
            hesaplaOSGB();
        })
        .catch(error => console.error("CSV Yüklenirken Hata:", error));
    }

    function hesaplaOSGB() {
        let tehlike = document.getElementById("tehlike_sinifi").innerText;
        let calisanSayisi = parseInt(document.getElementById("calisan_sayisi").value);

        let uzmanKatsayi = 0, hekimKatsayi = 0, dspKatsayi = 0;

        if (tehlike === "Az Tehlikeli") {
            uzmanKatsayi = 10;
            hekimKatsayi = 5;
            dspKatsayi = 0;
        } else if (tehlike === "Tehlikeli") {
            uzmanKatsayi = 20;
            hekimKatsayi = 10;
            dspKatsayi = 0;
        } else if (tehlike === "Çok Tehlikeli") {
            uzmanKatsayi = 40;
            hekimKatsayi = 15;
            dspKatsayi = calisanSayisi >= 250 ? 20 : calisanSayisi >= 50 ? 15 : calisanSayisi >= 10 ? 10 : 0;
        }

        document.getElementById("uzman_sonuc").innerText = calisanSayisi * uzmanKatsayi + " dk/ay";
        document.getElementById("hekim_sonuc").innerText = calisanSayisi * hekimKatsayi + " dk/ay";
        document.getElementById("dsp_sonuc").innerText = dspKatsayi > 0 ? calisanSayisi * dspKatsayi + " dk/ay" : "Gerekli değil";
    }
    </script>

    <?php
    return ob_get_clean();
}
add_shortcode('osgb_hesaplama', 'osgb_hesaplama_form');