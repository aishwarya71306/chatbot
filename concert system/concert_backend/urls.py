from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from events.views import event_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/events/', event_list, name='event-list'),
    path('', TemplateView.as_view(template_name='index.html'), name='dashboard'),
]
