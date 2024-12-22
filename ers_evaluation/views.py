from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import random
from .models import Recommendation, Evaluation
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'ers_evaluation/index.html')


@login_required
def evaluation(request):
    
    # Get all recommendations, if there are no recommendations, raise an error
    recommendations = Recommendation.objects.all()
    if not recommendations.exists():
        raise Http404("There are no recommendations to evaluate.")
    
    # Get evalutions that the user has already done, if there are more than XX evaluations, thank them for work
    completed_evaluations = Evaluation.objects.filter(user_id=request.user.id)
    if completed_evaluations.count() >= 3:
        context = {
            "completed_evaluations_count": completed_evaluations.count()
        }
        return render(request, 'ers_evaluation/finished.html', context)
    
    # Filter out recommendations that the user has already evaluated
    completed_evaluations_recommendation_id = [evaluation.recommendation.id for evaluation in completed_evaluations]
    unevaluated_recommendations = recommendations.exclude(id__in=completed_evaluations_recommendation_id)
    selected_text = random.choice(unevaluated_recommendations)
    
    context = {
        "evaluation_number": completed_evaluations.count() + 1,
        "recommendation": selected_text,
        "user_id": request.user.id
    }
    
    # When save/next button gets pressed
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        recommendation_id = int(request.POST.get("recommendation_id"))
        recommendation = recommendations.filter(id=recommendation_id).first()

        rating = request.POST.get(f"rating_{recommendation.id}")
        comment = request.POST.get(f"comment_{recommendation.id}")
        
        Evaluation.objects.create(
            recommendation=recommendation,
            user_id=user_id,
            rating=rating,
            comment=comment if comment else ""
        )

        return redirect('evaluation')
    
    return render(request, 'ers_evaluation/evaluation.html', context)

@login_required
def result(request):

    evaluations = Evaluation.objects.filter(user_id=request.user.id)
    if not evaluations:
        return render(request, 'ers_evaluation/no_results.html')
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