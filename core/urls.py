from django.urls import path
from core.views import FeedbackGroupedView, fetch_and_store_feedback


urlpatterns = [
    path('feedback/grouped/', FeedbackGroupedView.as_view(), name='feedback-grouped'),
    path('feedback/fetch/', fetch_and_store_feedback, name='fetch_and_store_feedback'),
]
