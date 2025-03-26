from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# CVSS skoruna göre risk seviyesini belirleme (HTML sınıfı olarak)
def get_severity_color(cvss_score):
    if cvss_score is None:
        return "low"
    if cvss_score >= 9.0:
        return "critical"
    elif cvss_score >= 7.0:
        return "high"
    elif cvss_score >= 4.0:
        return "medium"
    else:
        return "low"

# Belirtilen CVE'nin detaylarını çekme
def fetch_cve_details(cve_id):
    url = f"https://cvedb.shodan.io/cve/{cve_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "id": cve_id,
                "severity": get_severity_color(data.get("cvss_v3", 0)),
                "description": data.get("summary", "No description available.")[:8888],
                "cvss_v3": data.get("cvss_v3", "N/A"),
                "references": data.get("references", [])
            }
    except Exception as e:
        pass
    return {}

# IP taraması – Shodan InternetDB'den veri çekme ve CVE detaylarını ekleme
def scan_ip(ip):
    url = f"https://internetdb.shodan.io/{ip}"
    result = {"ip": ip, "ports": [], "cves": [], "hostnames": []}
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            result["ports"] = data.get("ports", [])
            result["hostnames"] = data.get("hostnames", [])
            if "vulns" in data:
                for cve in data["vulns"]:
                    cve_info = fetch_cve_details(cve)
                    if cve_info:
                        result["cves"].append(cve_info)
    except Exception as e:
        pass
    return result

# Kullanıcının seçtiği onay kutularına göre sonuçları filtreleme
def prepare_results(result, flags):
    output = {"ip": result["ip"]}
    # Varsayılan olarak tüm bilgileri göster
    if flags.get("show_ports") or not any(flags.values()):
        output["ports"] = result.get("ports", [])
    if flags.get("show_hosts") or not any(flags.values()):
        output["hostnames"] = result.get("hostnames", [])
    if flags.get("show_cves") or flags.get("show_cve_ports") or not any(flags.values()):
        output["cves"] = result.get("cves", [])
        if flags.get("show_cve_ports"):
            output["ports"] = result.get("ports", [])
    return output

# Ana sayfa: Tek IP taraması
@app.route("/")
def index():
    return render_template("index.html")

# Dosya ile tarama sayfası
@app.route("/file")
def file_scan_page():
    return render_template("file_scan.html")

# Tek IP taraması endpoint'i
@app.route("/scan", methods=["POST"])
def scan():
    ip = request.form.get("ip")
    if not ip:
        return jsonify({"error": "IP adresi gerekli"}), 400

    flags = {
        "show_cves": request.form.get("show_cves") == "on",
        "show_ports": request.form.get("show_ports") == "on",
        "show_hosts": request.form.get("show_hosts") == "on",
        "show_cve_ports": request.form.get("show_cve_ports") == "on"
    }
    scan_result = scan_ip(ip)
    prepared_result = prepare_results(scan_result, flags)
    return jsonify(prepared_result)

# Dosya ile tarama endpoint'i
@app.route("/scan_file", methods=["POST"])
def scan_file():
    if "file" not in request.files:
        return jsonify({"error": "Dosya yüklenmedi"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Geçerli bir dosya seçin"}), 400

    ips = file.read().decode("utf-8").splitlines()
    flags = {
        "show_cves": request.form.get("show_cves") == "on",
        "show_ports": request.form.get("show_ports") == "on",
        "show_hosts": request.form.get("show_hosts") == "on",
        "show_cve_ports": request.form.get("show_cve_ports") == "on"
    }
    results = []
    for ip in ips:
        result = scan_ip(ip)
        prepared = prepare_results(result, flags)
        results.append(prepared)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

