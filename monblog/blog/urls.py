from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", views.home),
    path("contact/", views.contact),
    path("Apropos/", views.Apropos, name="Apropos"),
    path('articles/', views.article,name='articles'),
    path('addcategory/', views.addcategory,name='addcategory'),
    path('addarticle/', views.add_article,name='addarticle'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('supprimer/<int:id>', views.supprimer, name='supprimer'),
    path('update/<int:id>', views.update, name='update'),
    path('register/', views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('addvideo/', views.addvideo, name='addvideo'),
    path('createquiz/', views.createquiz, name='createquiz'),
    path('take_quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('delete_article/<int:id>/', views.delete_article, name='delete_article'),
    path('delete_flashcard/<int:flashcard_id>/', views.delete_flashcard, name='delete_flashcard'),
    path('flashcards/', views.home, name='flashcards'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('get_flashcards/', views.get_flashcards, name='get_flashcards'),
    path('create_flashcard/', views.create_flashcard, name='create_flashcard'),
    path('create_category/', views.create_category, name='create_category'),
    path('flashcards/<int:pk>/delete/', views.delete_flashcard, name='delete_flashcard'),
    path('flashcards/<int:pk>/quiz/', views.create_quiz, name='create_quiz'),
    path('create_article/', views.create_article, name='create_article'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)