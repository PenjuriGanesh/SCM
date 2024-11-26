import random
import smtplib

# SMTP settings for sending emails
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'penjuriganesh2002@gmail.com'  
SENDER_PASSWORD = 'jsrd tmvg hfef tvfd'  #For enhanced security use an app Password with Gmail instead of your regular account password




# To Generate 6 - didgit OTP using Random Library
def generate_otp():
    otp = random.randint(100000, 999999)
    return otp


