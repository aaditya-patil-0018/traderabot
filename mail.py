import smtplib

class Sendmail:
    def __init__(self, content):
        self.EMAIL_ID = "TraderaBoot@gmail.com"
        self.EMAIL_PASSWORD = "TraderaBook123"
        self.content = content
        self.send_mail()

    def send_mail(self):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.EMAIL_ID, self.EMAIL_PASSWORD)

            subject = 'Tradera Available AD'
            body = 'The Links below are of the Items which are available to buy inside the Category you have selected.'

            # for link in self.content:
            body += f"\n{self.content}"

            msg = f"Subject: {subject}\n\n{body}"

            smtp.sendmail(self.EMAIL_ID, self.EMAIL_ID, msg) 
