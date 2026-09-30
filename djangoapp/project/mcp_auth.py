from rest_framework.authentication import TokenAuthentication

class MCPBearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"