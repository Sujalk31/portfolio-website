from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),

    path('add-project/', views.add_project, name='add_project'),
    path('edit-project/<slug:slug>/', views.edit_project, name='edit_project'),
    path('delete-project/<slug:slug>/', views.delete_project, name='delete_project'),
    path('delete-screenshot/<slug:slug>/<int:index>/', views.delete_screenshot, name='delete_screenshot'),

    path('profile/', views.edit_profile, name='edit_profile'),

    path('skills/', views.manage_skills, name='manage_skills'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/edit/<str:skill_id>/', views.edit_skill, name='edit_skill'),
    path('skills/delete/<str:skill_id>/', views.delete_skill, name='delete_skill'),

    path('experience/', views.manage_experience, name='manage_experience'),
    path('experience/add/', views.add_experience, name='add_experience'),
    path('experience/edit/<str:exp_id>/', views.edit_experience, name='edit_experience'),
    path('experience/delete/<str:exp_id>/', views.delete_experience, name='delete_experience'),

    path('education/', views.manage_education, name='manage_education'),
    path('education/add/', views.add_education, name='add_education'),
    path('education/edit/<str:edu_id>/', views.edit_education, name='edit_education'),
    path('education/delete/<str:edu_id>/', views.delete_education, name='delete_education'),
]