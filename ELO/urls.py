from django.contrib import admin
from django.urls import path, include
from utilizador import views  
from utilizador.views import criar_conta_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
     path('criar-conta/', criar_conta_view, name='criar_conta'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('password/', views.password, name='password'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('', include('utilizador.urls')),
    path('aula/', include('aulas.urls')),
    path('pesquisa/', include('pesquisa.urls')),
    path('testes/', include('testes.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

