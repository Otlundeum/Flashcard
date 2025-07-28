from django import forms
from .models import *

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Entrez le nom de la catégorie'})
        }
        labels = {
            'nom': 'Nom de la catégorie',
        }

class ArticleForm(forms.ModelForm):
    titre=forms.CharField(label='titre de l\'article',max_length=100,required=True)
    description=forms.CharField(label='description de l\'article',max_length=100,required=True)
    images=forms.ImageField(label='image de l\'article',required=True)
    id_Categorie=forms.ModelChoiceField(queryset=Categorie.objects.all(),widget=forms.Select(attrs={'class':'form-control'}),label='categorie de l\'article')

    class Meta:
        model = Article
        fields = ['titre','description','images','id_Categorie']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Entrez le titre de l\'article'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Entrez la description de l\'article'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control','placeholder': 'Entrez l\'image de l\'article'}),
            'id_Categorie': forms.Select(attrs={'class': 'form-control','placeholder': 'Entrez la catégorie de l\'article'}),
        }

class VideoForm(forms.ModelForm):
    titre = forms.CharField(label='Titre de la vidéo', max_length=200, required=True)
    video_file = forms.FileField(label='Fichier vidéo', required=True)
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), label='Catégorie')
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), label='Auteur')

    class Meta:
        model = Video
        fields = ['titre', 'video_file', 'categorie', 'auteur']

class QuizForm(forms.ModelForm):
    titre = forms.CharField(label='Titre du quiz', max_length=200, required=True)
    video = forms.FileField(label='Vidéo du quiz (optionnel)', required=False)
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), label='Catégorie')
    auteur = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), label='Auteur')

    class Meta:
        model = Quiz
        fields = ['titre', 'video', 'categorie', 'auteur']

class QuizQuestionForm(forms.ModelForm):
    question_text = forms.CharField(label='Question', widget=forms.Textarea(attrs={'class':'form-control', 'rows': 2}))

    class Meta:
        model = QuizQuestion
        fields = ['question_text']

class QuizOptionForm(forms.ModelForm):
    option_text = forms.CharField(label='Option', max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_correct = forms.BooleanField(label='Bonne réponse', required=False)

    class Meta:
        model = QuizOption
        fields = ['option_text', 'is_correct']
