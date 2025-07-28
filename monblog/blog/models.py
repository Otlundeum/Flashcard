from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom=models.CharField(max_length=100)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom

class Article(models.Model):
    titre=models.CharField(max_length=100)
    date_publication=models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    auteur=models.ForeignKey(User,on_delete=models.CASCADE)
    id_Categorie=models.ForeignKey('Categorie',on_delete=models.CASCADE,null=True,blank=True)
    images=models.ImageField(upload_to='') 
    updatedat=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    description=models.TextField()
    id_Article=models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    auteur=models.ForeignKey(User,on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

# New models for Video and Quiz

class Video(models.Model):
    titre = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

class Quiz(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class Flashcard(models.Model):
    video = models.FileField(upload_to='flashcards/videos/', null=True, blank=True)
    question = models.TextField(default="Question par défaut")
    answer = models.TextField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)  # Correction de la référence
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
