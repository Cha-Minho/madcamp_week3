from django.contrib import admin
from django.urls import path, include
from accounts import views
from chat import views_chat

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # 로그아웃 URL 패턴 추가
    path('stream_video/', views.stream_video, name='stream_video'),
    path('live/', views.live, name='live'),
    path('get_session_data/', views.get_session_data, name='get_session_data'),
    path('community/', views_chat.chatting, name='community'),
    path('community/<str:room_name>/', views_chat.room, name='room'),
    path('proxy/<path:path>', views.proxy_view),
]
