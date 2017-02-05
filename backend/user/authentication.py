from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class JSONWebTokenAuthenticationCookie(JSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        """
        Return value of 'auth_token' cookie, with contain jwt if
        user is logged in.
        """

        #print(request.COOKIES)
        #print(request.COOKIES.get('auth_token'))
        return request.COOKIES.get('auth_token')
