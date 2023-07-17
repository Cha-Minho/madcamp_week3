from django.contrib import admin
from django.urls import path, include
from accounts import views
from chat import views_chat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # 로그아웃 URL 패턴 추가
    path('live/', views.live, name='live'),
    path('get_session_data/', views.get_session_data, name='get_session_data'),
    path('chat/', views_chat.index, name='chat'),
    path('chat/<str:room_name>/', views_chat.room, name='room'),
    path('chat_list/', views_chat.chat_list, name='chat_list'),
    path('create_chat_room/', views_chat.create_chat_room, name='create_chat_room'),
    path('proxy/<path:path>', views.proxy_view),
    path('replay/', views.replay, name='replay'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
