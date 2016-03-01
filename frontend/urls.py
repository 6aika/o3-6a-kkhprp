from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

import frontend.views

urlpatterns = [
    url(r'^$', frontend.views.mainpage, name='mainpage'),
    url(r'^feedbacks/$', frontend.views.feedback_list, name="feedback_list"),
    url(r'^feedbacks/(?P<feedback_id>\d+)/$', frontend.views.feedback_details, name='feedback_details'),
    url(r'^feedback_form/$', frontend.views.FeedbackWizard.as_view(frontend.views.FORMS), name="feedback_form"),
    url(r'^map/$', frontend.views.map, name="map"),
    url(r'^locations_demo/$', frontend.views.locations_demo, name="locations_demo"),
    url(r'^instructions/$', frontend.views.instructions, name="instructions"),
    url(r'^statistic/$', frontend.views.statistics2, name="statistic"),
    url(r'^vote_feedback/$', frontend.views.vote_feedback, name="vote_feedback")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
