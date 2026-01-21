import subprocess
import google.generativeai as genai
from celery import Celery

# إعداد Celery للربط مع Redis
celery = Celery("tasks", broker="redis://cyber_redis:6379/0", backend="redis://cyber_redis:6379/0")

# إعداد الذكاء الاصطناعي بمفتاحك الخاص
genai.configure(api_key="AIzaSyAkDnjLo9gSf2yN5z7XluKF2AlSYkr4LOQ")
model = genai.GenerativeModel('gemini-1.5-flash')

@celery.task(name="tasks.run_nmap")
def run_nmap(target):
    # 1. تنفيذ الفحص الحقيقي داخل حاوية كالي (بدون محاكاة)
    try:
        cmd = ["docker", "exec", "cyber_kali", "nmap", "-sV", target]
        raw_result = subprocess.check_output(cmd).decode()
    except Exception as e:
        raw_result = f"Error executing Nmap: {str(e)}"

    # 2. صياغة الطلب للذكاء الاصطناعي للتحليل الأمني
    prompt = f"""
    بصفتك خبير أمن سيبراني محترف، قم بتحليل نتائج Nmap التالية:
    {raw_result}
    
    مطلوب تقرير مفصل باللغة العربية يتضمن:
    1. قائمة المنافذ المفتوحة والخدمات المكتشفة.
    2. الثغرات المحتملة بناءً على إصدارات الخدمات (CVEs).
    3. توصيات أمنية فورية (Remediation).
    """
    
    response = model.generate_content(prompt)
    
    return {
        "raw_data": raw_result,
        "ai_analysis": response.text
    }
