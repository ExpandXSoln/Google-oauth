from django.contrib import messages
import hashlib
import os
import requests
import json


class GoogleOAuth:
    """Google OAuth common class to implment quickly.

    Google OAuth common class to implment quickly. Please read README for more details.
    """

    def __init__(self):
        """[summary]

        [description]

        Returns:
            [type] -- [description]
        """
        return self

    def create_random():
        """Creates random string used hash for encryption.

            Create a state token to prevent request forgery.
        Returns:
            string -- Includes alphanumeric characters
        """
        return hashlib.sha256(os.urandom(1024)).hexdigest()

    def google_redirect(settings, request):
        """Method to create URL based on constants defined in setting file.

        Method to create URL based on constants defined in setting file. To initiate call to Google OAuth

        Arguments:
            settings file module / object -- [description] #@TODO : We can think of dict here. 
            request object -- request to add state (CSRF) of google to add in session

        Returns:
            url -- URL of Google with required parameter to get Auth Token
            bool -- If Error occures 
        """
        try:
            state = GoogleOAuth.create_random()
            # Kind of CSRF token for Google OAuth
            request.session['google_state'] = state
            url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&nonce={nonce}&state={state}".format(
                token_request_uri=settings.TOKEN_REQUEST_URI,
                response_type=settings.GOOGLE_RESPONSE_TYPE,
                client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                redirect_uri=settings.REDIRECT_URI,
                scope=settings.GOOGLE_SCOPE,
                nonce=state,
                state=state
            )
            return url
        except Exception as e:
            return False

    # Authenitication and get Token
    def google_authenticate(request, settings):
        """Initiate call to google to get Authentication Token  

        After we get code and verification from Google about our WEB application, our next step is to 
        initiate call to get token for Google Authentication of our application.

        Arguments:
            request object -- request to add error messages and code.
            settings file module / object -- To use constants of setting's file.

        Returns:
            dict -- Returning Google JSON / DICT with nesseccery values.
            bool -- If Error occures 
        """
        try:
            # Ensure that the error not in response and code is exist in request WSGIREQUEST object
            if 'error' in request.GET or 'code' not in request.GET:
                messages.add_message(
                    request, messages.ERROR, 'Could not login through google, please contact site administrator.')
                return HttpResponseRedirect('{loginfailed}'.format(loginfailed=settings.LOGIN_FAILED_URL))

            # Ensure that the request is not a forgery and that the user sending
            if request.GET.get('state', '') != request.session['google_state']:
                messages.add_message(
                    request, messages.ERROR, 'Could not login through google, please contact site administrator.')
                return HttpResponseRedirect('{loginfailed}'.format(loginfailed=settings.LOGIN_FAILED_URL))

            data = {'code': request.GET['code'],
                    'redirect_uri': settings.REDIRECT_URI,
                    'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                    'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                    'grant_type': 'authorization_code'
                    }
            headers = {'Content-Type': 'application/json'}
            resp = requests.post(settings.ACCESS_TOKEN_URI,
                                 headers=headers, params=data)
            return json.loads(resp.text)
        except Exception as e:
            return False

    def get_google_profile(token_data, settings):
        """[summary]

        [description]

        Arguments:
            token_data {[type]} -- [description]
            settings file module / object -- To use constants of setting's file.

        Returns:
            dict -- Returning Google JSON / DICT with nesseccery values.
            bool -- If Error occures
        """
        try:
            # this gets the google profile!!
            resp = requests.get(
                settings.GOOGLE_PROFILE + "{accessToken}".format(accessToken=token_data['access_token']))
            return json.loads(resp.text)
        except Exception as e:
            return False
