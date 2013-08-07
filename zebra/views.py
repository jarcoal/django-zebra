from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import get_model
from django.views.generic import RedirectView
from urllib import urlencode

import json, stripe, logging

from zebra.conf import options
from zebra.signals import WEBHOOK_MAP

log = logging.getLogger("zebra.%s" % __name__)
stripe.api_key = options.STRIPE_SECRET


def _try_to_get_customer_from_customer_id(stripe_customer_id):
    if options.ZEBRA_CUSTOMER_MODEL:
        m = get_model(*options.ZEBRA_CUSTOMER_MODEL.split('.'))
        try:
            return m.objects.get(stripe_customer_id=stripe_customer_id)
        except:
            pass
    return None


@csrf_exempt
def webhooks(request):
    """
    Handles all known webhooks from stripe, and calls signals.
    Plug in as you need.
    """
    if request.method != "POST":
        return HttpResponse("Invalid Request.", status=400)

    event_json = json.loads(request.body)
    event_key = event_json['type'].replace('.', '_')

    if event_key in WEBHOOK_MAP:
        WEBHOOK_MAP[event_key].send(sender=None, full_json=event_json)

    return HttpResponse(status=200)

#backwards compat
webhooks_v2 = webhooks

class OAuth2RedirectView(RedirectView):
    """
    Redirects the client to Stripe to authorize an oauth token.
    """

    url = 'https://connect.stripe.com/oauth/authorize'
    permanent = False
    response_type = 'code'
    scope = 'read_write'
    client_id = options.STRIPE_CLIENT_ID
    redirect_uri = options.STRIPE_REDIRECT_URI

    def get_redirect_url(self):
        """
        """
        params = {
            'scope': self.get_scope(),
            'client_id': self.get_client_id(),
            'redirect_uri': self.get_redirect_uri(),
            'response_type': self.get_response_type(),
        }

        return self.url + '?' + urlencode(params)

    def get_response_type(self):
        return self.response_type

    def get_client_id(self):
        return self.client_id

    def get_scope(self):
        return self.scope

    def get_redirect_uri(self):
        return self.redirect_uri