from fastapi import FastAPI
from celery import Celery

app = FastAPI()
# إعداد نظام الطوابير باستخدام Redis
celery_app = Celery("tasks", broker="redis://cyber_redis:6379/0", backend="redis://cyber_redis:6379/0")

@app.post("/scan/nmap")
def run_nmap(target: str):
    # إرسال مهمة الفحص إلى الـ Worker
    task = celery_app.send_task("tasks.run_nmap", args=[target])
    return {"task_id": task.id, "status": "Task Queued"}
