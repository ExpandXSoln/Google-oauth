###### Read below link to understand Google AOuth
[https://developers.google.com/identity/protocols/OpenIDConnect](https://developers.google.com/identity/protocols/OpenIDConnect) 

###### Login to create and create APPLICATION and get Client ID and SECRET
[https://console.developers.google.com/](https://console.developers.google.com/)

###### Put following constansts into **settings.py**
###### Change values of constants as per your need 
- LOGIN_URL = '/login'
- LOGIN_REDIRECT_URL = '/dashboard'
- LOGIN_FAILED_URL = '/'

- TOKEN_REQUEST_URI = "https://accounts.google.com/o/oauth2/v2/auth"
- ACCESS_TOKEN_URI = "https://www.googleapis.com/oauth2/v4/token"
- GOOGLE_PROFILE = "https://www.googleapis.com/oauth2/v3/userinfo?access_token="
- GOOGLE_SCOPE = "openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
- GOOGLE_RESPONSE_TYPE = "code"

- SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='YOUR GOOGLE APPLICATION CLIENT ID'
- SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YOUR GOOGLE APPLICATION SECRET'
- REDIRECT_URI = "http://127.0.0.1:8000/auth/complete/google-oauth2/" #URL which you define in Google Application / console

###### Put following namespaces into url
###### `View`put your view name

- url(r'^authlogin/$', View.google_login, name='authlogin'), #authlogin the link you have passed for Google Auth Login. 
- url(r'^auth/complete/google-oauth2/$', View.site_authentication, name='googleauthenticate'), #redirect uri which you have given in Google console.

###### Put following code into your `View.google_login` method
###### Consider project as your django project

```
from project.GoogleOAuth.Google import GoogleOAuth
from project import settings
from django.contrib import messages

def google_login(request):
    try:
        url = GoogleOAuth.google_redirect(settings,request)
        if url:
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, 'Could not login through google, please contact site administrator.')
            return HttpResponseRedirect('{loginfailed}'.format(loginfailed = settings.LOGIN_FAILED_URL))
    except Exception as e:
        return HttpResponseRedirect(settings.LOGIN_URL)
```
###### Put following code into your `View.site_authentication` method
###### Consider project as your django project

```
from project.GoogleOAuth.Google import GoogleOAuth
from project import settings
from django.contrib import messages

def site_authentication(request):
    token_data = GoogleOAuth.google_authenticate(request,settings)
    google_profile = GoogleOAuth.get_google_profile(token_data,settings)
```    
###### NOW process to `google_profile` json we got from google. :simple_smile:
