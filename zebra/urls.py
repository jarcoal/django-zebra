from django.conf.urls import patterns, include, url
from zebra import views
from zebra.conf import options

urlpatterns = patterns('',
    url(r'^webhooks/$', views.webhooks, name='webhooks'),
)

#If oauth settings are in place, load the oauth views
if options.STRIPE_CLIENT_ID and options.STRIPE_CLIENT_SECRET and options.STRIPE_REDIRECT_URI:
	urlpatterns += patterns('',
		url(r'^oauth2redirect/$', views.OAuth2RedirectView.as_view(), name='oauth2redirect'),
	)