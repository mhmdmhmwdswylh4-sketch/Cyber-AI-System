import subprocess
import google.generativeai as genai
from celery import Celery

celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
genai.configure(api_key="AIzaSyAkDnjLo9gSf2yN5z7XluKF2AlSYkr4LOQ")
model = genai.GenerativeModel('gemini-1.5-flash')

def ai_analyze(tool, data):
    prompt = f"حلل نتائج أداة {tool} التالية وقدم تقرير ثغرات بالعربية: {data}"
    return model.generate_content(prompt).text

@celery.task(name="tasks.web_scan")
def web_scan(target):
    # تشغيل Nmap + Nikto + Dirsearch بالتوالي
    res = subprocess.check_output(f"docker exec cyber_kali nmap -sV {target}", shell=True).decode()
    return ai_analyze("Web Full Scan", res)

@celery.task(name="tasks.wifi_audit")
def wifi_audit():
    # أداة Wifite للأتمتة (تتطلب كرت وايفاي يدعم Monitor Mode)
    res = subprocess.check_output("docker exec cyber_kali wifite --showb", shell=True).decode()
    return ai_analyze("WiFi Audit", res)

@celery.task(name="tasks.db_exploit")
def db_exploit(url):
    res = subprocess.check_output(f"docker exec cyber_kali sqlmap -u {url} --batch --dbs", shell=True).decode()
    return ai_analyze("SQL Injection Audit", res)
