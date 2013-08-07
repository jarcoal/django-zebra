"""
Default settings for zebra
"""
import datetime
import os

from django.conf import settings


STRIPE_PUBLISHABLE = getattr(settings, 'STRIPE_PUBLISHABLE', os.environ.get('STRIPE_PUBLISHABLE', ''))
STRIPE_SECRET = getattr(settings, 'STRIPE_SECRET', os.environ.get('STRIPE_SECRET', ''))

#oauth
STRIPE_CLIENT_ID = getattr(settings, 'STRIPE_CLIENT_ID', os.environ.get('STRIPE_CLIENT_ID', ''))
STRIPE_CLIENT_SECRET = getattr(settings, 'STRIPE_CLIENT_SECRET', os.environ.get('STRIPE_CLIENT_SECRET', ''))
STRIPE_REDIRECT_URI = getattr(settings, 'STRIPE_REDIRECT_URI', os.environ.get('STRIPE_REDIRECT_URI', ''))


ZEBRA_ENABLE_APP = getattr(settings, 'ZEBRA_ENABLE_APP', False)
ZEBRA_AUTO_CREATE_STRIPE_CUSTOMERS = getattr(settings,
    'ZEBRA_AUTO_CREATE_STRIPE_CUSTOMERS', True)

_today = datetime.date.today()
ZEBRA_CARD_YEARS = getattr(settings, 'ZEBRA_CARD_YEARS',
    range(_today.year, _today.year+12))
ZEBRA_CARD_YEARS_CHOICES = getattr(settings, 'ZEBRA_CARD_YEARS_CHOICES',
    [(i,i) for i in ZEBRA_CARD_YEARS])

ZEBRA_MAXIMUM_STRIPE_CUSTOMER_LIST_SIZE = getattr(settings,
    'ZEBRA_MAXIMUM_STRIPE_CUSTOMER_LIST_SIZE', 100)

_audit_defaults = {
    'active': 'active',
    'no_subscription': 'no_subscription',
    'past_due': 'past_due',
    'suspended': 'suspended',
    'trialing': 'trialing',
    'unpaid': 'unpaid',
    'cancelled': 'cancelled'
}

ZEBRA_AUDIT_RESULTS = getattr(settings, 'ZEBRA_AUDIT_RESULTS', _audit_defaults)

ZEBRA_ACTIVE_STATUSES = getattr(settings, 'ZEBRA_ACTIVE_STATUSES',
    ('active', 'past_due', 'trialing'))
ZEBRA_INACTIVE_STATUSES = getattr(settings, 'ZEBRA_INACTIVE_STATUSES',
    ('cancelled', 'suspended', 'unpaid', 'no_subscription'))

ZEBRA_CUSTOMER_MODEL = getattr(settings, 'ZEBRA_CUSTOMER_MODEL', 'zebra.Customer' if ZEBRA_ENABLE_APP else None)