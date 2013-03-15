from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import get_model

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