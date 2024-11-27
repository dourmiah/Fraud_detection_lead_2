import smtplib

smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_user = "jedhaprojetfrauddetect2@gmail.com"
smtp_password = "xcbe anpu fewx xgfd"

try:
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    print("Connexion SMTP réussie !")
    server.quit()
except Exception as e:
    print(f"Erreur de connexion SMTP : {e}")
