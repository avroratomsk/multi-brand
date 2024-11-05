from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from home.models import BaseSettings

try:
  email = BaseSettings.objects.get().email
except:
  email = ""

def email_send(order):
  subject = "Заказ №" + str(order.id)
  html_content = render_to_string("mail/order_mail.html", {"order": order})
  from_email = "info@xn----7sbah6bllcobpj.xn--p1ai"
  text_content = 'Не поддерживает HTML в письме'
  to = [email]
  msg = EmailMultiAlternatives(subject, text_content, from_email, to)
  msg.attach_alternative(html_content, "text/html")
  try:
    msg.send()
  except Exception as e:
    print(f"Error: {e}")
  