from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    """Get the client IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or 'unknown'


def get_user_agent(request: HttpRequest) -> str:
    """Get the user agent from the request."""
    return request.META.get('HTTP_USER_AGENT', 'unknown')[:500]  # Limit length
