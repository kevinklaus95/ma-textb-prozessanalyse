from django.contrib import admin
from django.urls import path, include  # add this
from rest_framework import routers  # add this
from analyzer import views  # add this

router = routers.DefaultRouter()  # add this
router.register(r'hours', views.HoursView, 'hours')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('distinct-project-ids/', views.distinct_project_ids),
    path('start-analysis/', views.start_analysis),
    path('start-custom-analysis/', views.start_custom_analysis)
]