from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import random
from .models import Recommendation, Evaluation
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'ers_evaluation/index.html')


@login_required
def evaluation(request):
    
    recommendations = Recommendation.objects.all()
    if not recommendations.exists():
        raise Http404("There are no recommendations to evaluate.")
    
    selected_texts = random.sample(list(recommendations), 2)  # Chooses 2 random recommendations
    context = {
        "recommendations": selected_texts,
        "user_id": request.user.id
    }
    
    if request.method == "POST": # When save button gets pressed
        user_id = request.POST.get("user_id")
        
        for recommendation in recommendations:
            rating = request.POST.get(f"rating_{recommendation.id}")
            comment = request.POST.get(f"comment_{recommendation.id}")
            
            if rating:
                Evaluation.objects.create(
                    recommendation=recommendation,
                    user_id=user_id,
                    rating=rating,
                    comment=comment if comment else ""
                )
        return redirect('result')
    
    return render(request, 'ers_evaluation/evaluation.html', context)

@login_required
def result(request):

    evaluations = Evaluation.objects.filter(user_id=request.user.id)
    if not evaluations:
        return HttpResponse("You have not evaluated any recommendations. Click begin evaluation to start.")
    context = {
        "evaluations": evaluations
    }

    return render(request, 'ers_evaluation/result.html', context)


@login_required
def delete_evaluation(request):
    if request.method == "POST":
        evaluation_id = request.POST.get("evaluation_id")
        evaluation = get_object_or_404(Evaluation, id=evaluation_id)
        evaluation.delete()
        return redirect('result')
    return HttpResponse(status=405)


@login_required
def edit_evaluation(request):
    if request.method == "POST":
        evaluation_id = request.POST.get("evaluation_id")
        evaluation = get_object_or_404(Evaluation, id=evaluation_id)
        evaluation.rating = request.POST.get("rating")
        evaluation.comment = request.POST.get("comment")
        evaluation.save()
        return redirect('result')  # Redirect to the result page after saving

    evaluation_id = request.GET.get("evaluation_id")
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    context = {
        "evaluation": evaluation
    }
    return render(request, 'ers_evaluation/edit_evaluation.html', context)