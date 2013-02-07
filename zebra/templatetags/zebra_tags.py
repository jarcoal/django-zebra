from django.core.urlresolvers import reverse
from django import template
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from zebra.conf import options


register = template.Library()

def _set_up_zebra_form(context):
    if not "zebra_form" in context:
        if "form" in context:
            context["zebra_form"] = context["form"]
        else:
            raise Exception, "Missing stripe form."
    context["STRIPE_PUBLISHABLE"] = options.STRIPE_PUBLISHABLE
    return context


@register.inclusion_tag('zebra/_stripe_js_and_set_stripe_key.html', takes_context=True)
def zebra_head_and_stripe_key(context):
    return _set_up_zebra_form(context)


@register.inclusion_tag('zebra/_basic_card_form.html', takes_context=True)
def zebra_card_form(context):
    return _set_up_zebra_form(context)


@register.inclusion_tag('zebra/_stripe_checkout_script.html')
def zebra_checkout_script(name=None, description=None, image=None, amount=None, label=None, panel_label=None, address=None):
	"""
	Renders the Stripe checkout form.
	https://stripe.com/docs/checkout
	"""

	#these values have no defaults in the interface
	attrs = {
		'name': name,
		'description': description,
		'image': image,
		'amount': amount,
	}

	#these values do, so we only insert them into context if they've been populated.
	if label is not None:
		attrs['label'] = label

	if panel_label is not None:
		attrs['panel-label'] = panel_label

	if address is not None:
		attrs['address'] = address

	return { 'attrs': attrs, 'STRIPE_PUBLISHABLE': options.STRIPE_PUBLISHABLE }