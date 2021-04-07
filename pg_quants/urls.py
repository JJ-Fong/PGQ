from django.urls import path,include

from . import views







urlpatterns = [
	path('quants/', views.pq_quants, name = 'main')
]