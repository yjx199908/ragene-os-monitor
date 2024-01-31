import psutil
import time
from email_reporter import EmailReporter
import os
from datetime import datetime

env = os.environ.get("ENV")
receivers = os.environ.get("RECEIVERS").split(",")

# 监控阈值
THRESHOLD_CPU_PERCENT = 70
THRESHOLD_MEMORY_PERCENT = 70
THRESHOLD_DISK_PERCENT = 70

def send_email(subject, content):
    for receiver in receivers:
        reporter = EmailReporter(receiver)
        reporter.fill_message(subject, content)
        reporter.send()

def check_system_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    if cpu_percent > THRESHOLD_CPU_PERCENT:
        warning_msg = f"警告: CPU使用率超过{THRESHOLD_CPU_PERCENT}%，当前使用率为{cpu_percent}%"
        send_email(f"{env}环境系统资源警告", warning_msg)

    if memory_info.percent > THRESHOLD_MEMORY_PERCENT:
        warning_msg = f"警告: 内存使用率超过{THRESHOLD_MEMORY_PERCENT}%，当前使用率为{memory_info.percent}%"
        send_email(f"{env}环境系统资源警告", warning_msg)

    if disk_info.percent > THRESHOLD_DISK_PERCENT:
        warning_msg = f"警告: 磁盘空间使用率超过{THRESHOLD_DISK_PERCENT}%，当前使用率为{disk_info.percent}%"
        send_email(f"{env}环境系统资源警告", warning_msg)

if __name__ == "__main__":
    while True:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] 开始检查系统资源使用情况 --- {time_str}")
        check_system_usage()
        time.sleep(60)  # 每隔20秒检查一次