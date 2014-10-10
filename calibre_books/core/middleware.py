from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from social.apps.django_app.middleware import (
    SocialAuthExceptionMiddleware as BaseSocialAuthExceptionMiddleware)
from social.exceptions import (SocialAuthBaseException, AuthForbidden,
                               AuthFailed)


class SocialAuthExceptionMiddleware(BaseSocialAuthExceptionMiddleware):

    def process_exception(self, request, exception):
        strategy = getattr(request, 'social_strategy', None)
        if strategy is None or self.raise_exception(request, exception):
            return

        message = None
        if isinstance(exception, (AuthForbidden, AuthFailed)):
            message = _("Sorry buddy. Looks like you're not on my list.")
        elif isinstance(exception, SocialAuthBaseException):
            message = self.get_message(request, exception)

        if message:
            url = self.get_redirect_uri(request, exception)
            messages.error(request, message)
            return redirect(url)
