from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from bases import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginPorRolView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.listar_aprendices, name='listar_aprendices'),
    path('crear/', views.crear_aprendiz, name='crear_aprendiz'),
    path('editar/<str:documento>/', views.editar_aprendiz, name='editar_aprendiz'),
    path('eliminar/<str:documento>/', views.eliminar_aprendiz, name='eliminar_aprendiz'),
    path('buscar/', views.buscar_aprendiz, name='buscar_aprendiz'),
    path('mapa/', views.mapa, name='mapa'),
]