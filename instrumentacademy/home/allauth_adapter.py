from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def pre_social_login(self, request, sociallogin):        # Disable signup when using social authentication
        user = sociallogin.user
        if not user.username:
            # If the user doesn't have a username, set it to their Google ID
            user.username = sociallogin.account.uid

        if not user.email:
            # If the user doesn't have an email, set it to the email from the Google account
            user.email = sociallogin.account.extra_data.get('email', '')

        # Save the changes to the user object
        user.save()