from django.shortcuts import render
from .fun_module import pg_quants_data, pg_pos_list, pg_date_list
from rest_framework import viewsets
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import generics

# Create your views here.

#class HeroViewSet(viewsets.ModelViewSet):
#    queryset = Hero.objects.all().order_by('name')
#    serializer_class = HeroSerializer

class PGPosViewset(viewsets.GenericViewSet):
	def list(self, request):
		return Response(pg_pos_list())

class PGDatesViewset(viewsets.GenericViewSet):
	def list(self, request):
		return Response(pg_date_list())
		

class PGQuantsViewset(viewsets.GenericViewSet): 
	def list(self, request, pos, date):
		return Response(pg_quants_data(pos, date))
