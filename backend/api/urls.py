from django.urls import path
from .views import AskView, DocumentUploadView, HealthView

urlpatterns = [
    path('health/', HealthView.as_view()),
    path('documents/upload/', DocumentUploadView.as_view()),
    path('ask/', AskView.as_view()),
]
