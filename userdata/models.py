from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )



from django.db import models

# Create your models here.
class lang(models.Model):
    language = models.CharField(max_length=50)
    def __str__(self):
        return self.language

class category(models.Model):
    language = models.ForeignKey(lang, on_delete=models.CASCADE)
    cat_name = models.CharField(max_length=50)
    cat_image_link = models.ImageField(blank=True, upload_to='cat_image')
    cat_added_date = models.DateField(auto_now=True)
    def __str__(self):
        return self.cat_name

class sub_category(models.Model):
    cat_name = models.ForeignKey(category, on_delete=models.CASCADE)
    sub_cat_name = models.CharField(max_length=50)
    def __str__(self):
        return self.sub_cat_name


class sms(models.Model):
    sub_cat_name = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    sms = models.TextField()
    def __str__(self):
        return self.sms

