from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new-application/', views.new_application, name='new-application'),
    path('view-application/<int:pk>', views.view_application, name="view-application"),
    path('verify-pep/<int:pk>', views.submit_pep, name="verify-pep"),
    path('deny-application/<int:pk>', views.deny_application, name="deny-application"),
    path('reject-match/<int:pk>', views.reject_match, name="reject-match"),
    path('reject-pep-match/<int:pk>', views.reject_pep_match, name="reject-pep-match"),
    path('submit-risk-assessment/<int:pk>', views.submit_risk_assessment, name='submit-risk-assessment'),
]
