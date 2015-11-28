from django.conf import settings


def github_corner_url(request):
    return {'github_corner_url': settings.GITHUB_CORNER_URL}


def google_analytics(request):
    return {'google_analytics': settings.GOOGLE_ANALYTICS}
