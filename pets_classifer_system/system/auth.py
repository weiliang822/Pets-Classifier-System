from rest_framework.authentication import SessionAuthentication


class CustomAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass
