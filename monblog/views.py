from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from blog.models import Flashcard, Category

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
                    category_id=category_id  # Correction pour utiliser le champ `category`
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

            Category.objects.create(name=name, color=color)

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