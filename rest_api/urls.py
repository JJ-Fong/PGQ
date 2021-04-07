from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter() 
router.register(r'pos_codes', views.PGPosViewset, 'PGPosViewset')
router.register(r'available_dates', views.PGDatesViewset, 'PGDatesViewset')
router.register(r'pg_quants/(?P<pos>\d+)/(?P<date>\d\d\d\d-\d\d-\d\d)', views.PGQuantsViewset, 'PGQuantsViewset')

urlpatterns = [
	path('', include(router.urls))
]
