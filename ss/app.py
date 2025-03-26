#!/usr/bin/python3
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_severity_label(cvss_score):
    """CVSS skoruna göre sade metin etiketini döndürür."""
    if cvss_score is None:
        cvss_score = 0
    if cvss_score >= 9.0:
        return "[CRITICAL]"
    elif cvss_score >= 7.0:
        return "[HIGH]"
    elif cvss_score >= 4.0:
        return "[MEDIUM]"
    else:
        return "[LOW]"

def fetch_cve_details(cve_id):
    """Belirtilen CVE için Shodan CVE API'sinden detayları getirir."""
    url = f"https://cvedb.shodan.io/cve/{cve_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "cvss_v3": data.get("cvss_v3", 0),
                "summary": data.get("summary", "No description available.")
            }
    except Exception as e:
        print(f"Error fetching {cve_id}: {e}")
    return {"cvss_v3": 0, "summary": "No description available."}

def log_results(ip, data, show_cves, show_ports, show_hosts, show_cve_ports):
    """
    Sonuçları aşağıdaki sırayla hazırlar:
      1. Açık Portlar (varsa)
      2. CVE bilgileri
      3. Hostnameler (varsa)
    """
    lines = []
    info_prefix = "[INFO]"
    
    ports = data.get("ports", [])
    vulns = data.get("vulns", [])
    hostnames = data.get("hostnames", [])
    
    # 1. Açık Portlar
    if show_ports and ports:
        ports_str = ", ".join(str(p) for p in ports)
        lines.append(f"{info_prefix} [{ip}] [PORTS: {ports_str}]")
    
    # 2. CVE'ler
    if show_cves and vulns:
        for cve in vulns:
            cve_info = fetch_cve_details(cve)
            severity = get_severity_label(cve_info["cvss_v3"])
            summary = cve_info["summary"].strip()[:80]
            lines.append(f"{info_prefix} [{ip}] [{cve}] {severity} [{summary}]")
    
    # 3. CVE + Açık Portlar
    if show_cve_ports and vulns:
        ports_str = ", ".join(str(p) for p in ports) if ports else "No ports"
        for cve in vulns:
            cve_info = fetch_cve_details(cve)
            severity = get_severity_label(cve_info["cvss_v3"])
            summary = cve_info["summary"].strip()[:80]
            lines.append(f"{info_prefix} [{ip}] [{cve}] {severity} [{summary}] [PORTS: {ports_str}]")
    
    # 4. Hostnameler
    if show_hosts and hostnames:
        hostnames_str = ", ".join(hostnames)
        lines.append(f"{info_prefix} [{ip}] [HOSTNAMES: {hostnames_str}]")
    
    return lines

def process_ip(ip, show_cves, show_ports, show_hosts, show_cve_ports):
    """Belirtilen IP için Shodan InternetDB'den verileri çekip log_results ile çıktı üretir."""
    url = f"https://internetdb.shodan.io/{ip}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not isinstance(data, dict):
                return [f"[ERROR] Invalid response format from Shodan API"]
            
            return log_results(ip, data, show_cves, show_ports, show_hosts, show_cve_ports)
        
        return [f"[ERROR] Failed to fetch data for {ip} (Status Code: {response.status_code})"]
    except requests.exceptions.RequestException as e:
        return [f"[ERROR] Request error: {str(e)}"]
    except Exception as e:
        return [f"[ERROR] Unexpected error: {str(e)}"]

@app.route("/")
def index():
    return render_template("webscan.html")

@app.route("/scan")
def scan():
    ip = request.args.get("ip", "127.0.0.1")
    show_cves = request.args.get("cves", "false").strip().lower() == "true"
    show_ports = request.args.get("ports", "false").strip().lower() == "true"
    show_hosts = request.args.get("host", "false").strip().lower() == "true"
    show_cve_ports = request.args.get("cve_ports", "false").strip().lower() == "true"
    
    results = process_ip(ip, show_cves, show_ports, show_hosts, show_cve_ports)
    return jsonify({"lines": results})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
