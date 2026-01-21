import subprocess
import google.generativeai as genai
from celery import Celery

celery = Celery("tasks", broker="redis://cyber_redis:6379/0", backend="redis://cyber_redis:6379/0")

genai.configure(api_key="AIzaSyAkDnjLo9gSf2yN5z7XluKF2AlSYkr4LOQ")
model = genai.GenerativeModel('gemini-1.5-flash')

def run_tool_and_analyze(cmd, tool_name):
    try:
        raw_result = subprocess.check_output(cmd).decode()
        prompt = f"تحليل أمني احترافي لنتائج أداة {tool_name}:\n{raw_result}\nقدم الثغرات والحلول باللغة العربية."
        ai_analysis = model.generate_content(prompt).text
        return {"raw": raw_result, "analysis": ai_analysis}
    except Exception as e:
        return {"error": str(e)}

@celery.task(name="tasks.run_nmap")
def run_nmap(target):
    return run_tool_and_analyze(["docker", "exec", "cyber_kali", "nmap", "-sV", target], "Nmap")

@celery.task(name="tasks.run_sqlmap")
def run_sqlmap(url):
    return run_tool_and_analyze(["docker", "exec", "cyber_kali", "sqlmap", "-u", url, "--batch", "--banner"], "SQLMap")

@celery.task(name="tasks.run_nikto")
def run_nikto(target):
    return run_tool_and_analyze(["docker", "exec", "cyber_kali", "nikto", "-h", target], "Nikto")
