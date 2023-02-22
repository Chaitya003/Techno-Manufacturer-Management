from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

urlpatterns = [
	url(r'^login/$',views.LogIn),
    url(r'^store/$',views.Store),
    url(r'^production/$',views.Production),
    url(r'^login-submit/$',views.LogInSubmit),
    url(r'^fetch-pipe-element/$',views.FetchElementMappingPipe),
    url(r'^save-pipe/$',views.SavePipe),
    url(r'^fetch-conductor-element/$',views.FetchElementMappingConductor),
    url(r'^save-conductor/$',views.SaveConductor),
    url(r'^fetch-mgo-element/$',views.FetchElementMappingMGO),
    url(r'^save-mgo/$',views.SaveMGO),
    url(r'^start-coil-production/$',views.StartCoilProduction),
    url(r'^fetch-draw-annealing-status/$',views.FetchCoilStatus),
    url(r'^start-process-coil/$',views.StartProcessForCoil),
    url(r'^stop-process-coil/$',views.StopProcessForCoil),
    url(r'^end-coil-production/$',views.EndCoilProduction),
]