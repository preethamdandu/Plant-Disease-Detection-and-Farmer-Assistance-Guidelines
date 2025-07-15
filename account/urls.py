from django.urls import path
from . import views

app_name="account"

urlpatterns = [
    path('',views.index,name="index"),
    path('farmerlogin',views.farmerlogin,name="farmerlogin"),
    path('volunteerlogin',views.volunteerlogin,name="volunteerlogin"),
    path('farmersignup',views.farmersignup,name="farmersignup"),
    path('volunteersignup',views.volunteersignup,name="volunteersignup"),
    path('selectcity',views.selectcity,name="selectcity"),
    path('selectcity1',views.selectcity1,name="selectcity1"),
    path('predictindex',views.predictindex,name="predictindex"),
    path('diseaseupload',views.diseaseupload,name="diseaseupload"),
    path('predictImage',views.predictImage,name='predictImage'),
    path('citySelect',views.citySelect,name='citySelect'),
    path('weatherfetch',views.weatherfetch,name='weatherfetch'),
    path('questions',views.questions,name='questions'),
    path('questions1',views.questions1,name='questions1'),
    path('newques',views.newques,name='newques'),
    path('queshigh',views.queshigh,name='queshigh'),
    path('queshigh1',views.queshigh1,name='queshigh1'),
    path('comsub',views.comsub,name='comsub'),
    path('comsub1',views.comsub1,name='comsub1'),
    path('volunteerdash',views.volunteerdash,name='volunteerdash'),
    path('pending_questions', views.pending_questions, name='pending_questions'),
    path('answer_history', views.answer_history, name='answer_history'),
    path('resource_list', views.resource_list, name='resource_list'),
    path('upload_resource', views.upload_resource, name='upload_resource'),
    path('message_list', views.message_list, name='message_list'),
    path('send_message', views.send_message, name='send_message'),
    
    # New advanced features
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/dashboard_stats/', views.dashboard_stats, name='dashboard_stats'),
    path('api/search/', views.advanced_search, name='advanced_search'),
    #path('weatherdata',views.weatherdata,name='weatherdata'),
    path('logout',views.logout,name="logout")
]
