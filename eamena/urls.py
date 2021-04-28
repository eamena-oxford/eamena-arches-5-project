from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from eamena.views.resource import ResourceEditorView
uuid_regex = settings.UUID_REGEX

#overriding from arches.app.resource import ResourceEditorView
#comment-out line 10 to switch view back to core Arches

urlpatterns = [
	url(r"^resource/(?P<resourceid>%s)$" % uuid_regex, ResourceEditorView.as_view(), name="resource_editor"),
    url(r'^', include('arches.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
