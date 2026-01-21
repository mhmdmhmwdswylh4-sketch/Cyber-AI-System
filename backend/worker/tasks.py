from celery import Celery
import subprocess

celery = Celery("tasks", broker="redis://cyber_redis:6379/0", backend="redis://cyber_redis:6379/0")

@celery.task(name="tasks.run_nmap")
def run_nmap(target):
    # تنفيذ أمر Nmap حقيقي داخل حاوية Kali Linux
    cmd = ["docker", "exec", "cyber_kali", "nmap", "-sV", target]
    result = subprocess.check_output(cmd).decode()
    return result # سيتم إرسال هذه النتيجة للذكاء الاصطناعي لتحليلها
