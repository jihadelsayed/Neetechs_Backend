from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up
from .models import CustomUser as User

# @receiver(post_save, sender=SocialAccount)
# def create_class(sender, instance, created, **kwargs):
# 	if created:
# 		user = User.objects.filter(email=instance.extra_data['email']).first()
# 		user.name = instance.extra_data['name']
# 		user.save()

@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    if sociallogin is not None:
	    if sociallogin.account.provider == 'facebook':
	        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
	        #picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"            
	        #email = user_data['email']
	        name = user_data['name']
	    user.name = name
	    user.save()