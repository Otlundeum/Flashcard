from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .form import CategorieForm, ArticleForm, VideoForm, QuizForm, QuizQuestionForm, QuizOptionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)


# Vue de connexion personnalisée
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil après connexion
        else:
            return render(request, 'login.html', {'error': "Nom d'utilisateur ou mot de passe incorrect."})
    return render(request, 'login.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'flashcards.html')

def contact(request):
  return render(request, 'contact.html')

def Apropos(request):
  return render(request, 'A propos.html')

def article(request):
  articles = Article.objects.all()
  flashcards_ia = Flashcard.objects.filter(category__nom='IA')
  flashcards_ia_json = json.dumps(list(flashcards_ia.values('question', 'answer', 'video')), cls=DjangoJSONEncoder)

  context = {
    'articles': articles,
    'flashcards_ia_json': flashcards_ia_json
  }
  return render(request, 'articles.html', context)
  
@login_required(login_url='login')
def addcategory(request):
  form= CategorieForm(request.POST)
  if request.method =='POST':
    if form.is_valid():
        form.save()
        return render(request, 'index.html', {'form': form, 'success': True})
  else:
      form = CategorieForm()
  return render(request, 'addcategory.html',{'form': form, 'success': True})

@login_required(login_url='login')
def add_article(request, id=None):
    article = None
    if id:
        article = get_object_or_404(Article, id=id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            return render(request, 'addarticle.html', {'form': form, 'article': article, 'id': article.id, 'success': True})
    else:
        form = ArticleForm(instance=article)

    return render(request, 'addarticle.html', {'form': form, 'article': article, 'id': id})

@login_required(login_url='login')
def dashboard(request):
    articles = Article.objects.order_by('id')  # Order articles by ID to show the newest at the bottom
    flashcards = Flashcard.objects.all()

    if request.method == 'POST':
        if 'add_article' in request.POST:
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                article = form.save(commit=False)
                article.auteur = request.user  # Assign the logged-in user as the author
                article.save()
                return redirect('dashboard')
        elif 'add_flashcard' in request.POST:
            video = request.FILES.get('video')
            question = request.POST.get('question')
            answer = request.POST.get('answer')
            Flashcard.objects.create(video=video, question=question, answer=answer)
            return redirect('dashboard')

    article_form = ArticleForm()
    context = {
        'articles': articles,
        'flashcards': flashcards,
        'article_form': article_form,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def supprimer(request, id):
    articles = Article.objects.get(id=id)
    articles.delete()
    return redirect('dashboard')

@login_required(login_url='login')
def update(request, id):
    articles = Article.objects.get(id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=articles)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'update.html', {'form': form})

@login_required(login_url='login')
def addvideo(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VideoForm()
    return render(request, 'addvideo.html', {'form': form})

@login_required(login_url='login')
def createquiz(request):
    flashcards = Flashcard.objects.all()
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.auteur = request.user
            quiz.save()

            # Associate selected flashcards with the quiz
            flashcard_ids = request.POST.getlist('flashcards')
            flashcards = Flashcard.objects.filter(id__in=flashcard_ids)
            quiz.flashcards.set(flashcards)

            return redirect('dashboard')
    else:
        form = QuizForm()
        
    return render(request, 'createquiz.html', {'form': form, 'flashcards': flashcards})

@login_required(login_url='login')
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                option = QuizOption.objects.filter(id=selected_option_id, question=question).first()
                if option and option.is_correct:
                    score += 1
        return render(request, 'quiz_result.html', {'score': score, 'total': total, 'quiz': quiz})
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connexion automatique après inscription
            from django.contrib.auth import login, authenticate
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige vers la page flashcards
            else:
                return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, 'success': True})

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    return render(request, 'delete_confirmation.html', {'article': article})

@login_required(login_url='login')
def delete_flashcard(request, flashcard_id):
    logger.info(f"Received request to delete flashcard with ID: {flashcard_id}")
    if request.method == 'POST':
        try:
            flashcard = get_object_or_404(Flashcard, id=flashcard_id)
            flashcard.delete()
            logger.info(f"Successfully deleted flashcard with ID: {flashcard_id}")
            return JsonResponse({'success': True, 'message': 'Flashcard supprimée avec succès'})
        except Exception as e:
            logger.error(f"Error deleting flashcard with ID: {flashcard_id}: {e}")
            return JsonResponse({'success': False, 'message': 'Erreur lors de la suppression de la flashcard'}, status=500)
    else:
        logger.warning(f"Invalid request method for deleting flashcard with ID: {flashcard_id}")
        return JsonResponse({'success': False, 'message': 'Requête invalide'}, status=400)

@login_required(login_url='login')
def create_quiz(request):
    flashcards = Flashcard.objects.all()
    logger.info("Creating a new quiz.")
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            selected_flashcards = request.POST.getlist('flashcards')
            logger.info(f"Selected flashcards: {selected_flashcards}")
            for flashcard_id in selected_flashcards:
                try:
                    flashcard = Flashcard.objects.get(id=flashcard_id)
                    quiz.flashcards.add(flashcard)
                except Flashcard.DoesNotExist:
                    logger.error(f"Flashcard with ID {flashcard_id} does not exist.")
            return JsonResponse({'success': True, 'quiz_id': quiz.id})
        else:
            logger.error("Quiz form is invalid.")
    else:
        form = QuizForm()
    return render(request, 'createquiz.html', {'form': form, 'flashcards': flashcards})

@login_required(login_url='login')
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return JsonResponse({'success': True})

@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategorieForm()
    return render(request, 'addcategory.html', {'form': form})

@login_required(login_url='login')
def get_flashcards(request):
    category = request.GET.get('category', 'all')
    logger.info(f"Fetching flashcards for category: {category}")
    if category == 'all':
        flashcards = Flashcard.objects.all()
    else:
        flashcards = Flashcard.objects.filter(category__name=category)

    if not flashcards.exists():
        logger.warning("No flashcards found for the given category.")

    flashcards_data = [
        {
            'id': flashcard.id,
            'question': flashcard.question,
            'answer': flashcard.answer,
        }
        for flashcard in flashcards
    ]
    return JsonResponse({'flashcards': flashcards_data})

@csrf_exempt
def create_flashcard(request):
    if request.method == 'POST':
        try:
            video = request.FILES.get('video')
            questions = request.POST.getlist('questions[]')
            answers = request.POST.getlist('answers[]')
            category_id = request.POST.get('category')

            if not questions or not answers or len(questions) != len(answers):
                return JsonResponse({
                    'success': False,
                    'message': 'Les questions et réponses doivent être fournies et correspondre en nombre.'
                })

            # Créer un flashcard pour chaque question/réponse
            for question, answer in zip(questions, answers):
                Flashcard.objects.create(
                    video=video,
                    question=question,
                    answer=answer,
                    category_id=category_id
                )

            return JsonResponse({
                'success': True,
                'message': 'Flashcards créés avec succès.'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })

    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée.'
    })

@csrf_exempt
def create_category(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            color = request.POST.get('color')

            if not name:
                return JsonResponse({
                    'success': False,
                    'message': 'Le nom de la catégorie est requis.'
                })

            Categorie.objects.create(name=name, color=color)

            return JsonResponse({
                'success': True,
                'message': 'Catégorie créée avec succès.'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })

    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée.'
    })

@login_required(login_url='login')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'addarticle.html', {'form': form})

def flashcards_page(request):
    flashcards = Flashcard.objects.all()
    return render(request, 'flashcards.html', {'flashcards': flashcards})
