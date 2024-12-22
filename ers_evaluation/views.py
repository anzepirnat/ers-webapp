from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import random
from .models import Recommendation, Evaluation
from django.contrib.auth.decorators import login_required
import ast

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
    #print(completed_evaluations)
    #print(type(completed_evaluations))
    #print("evaluation id: ", completed_evaluations[0].id)
    #print("evaluations id: ", [completed_evaluation.id for completed_evaluation in completed_evaluations])
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
        "previous_evaluations_id": [completed_evaluation.id for completed_evaluation in completed_evaluations],
        "recommendation": selected_text,
        "user_id": request.user.id
    }
    
    
    if request.method == "POST":
        back_btn_flag = request.POST.get("back_btn_flag")
        print("back_btn_flag: ", back_btn_flag, "back_btn_flag type: ", type(back_btn_flag))
        user_id = request.POST.get("user_id")
        recommendation_id = int(request.POST.get("recommendation_id"))
        recommendation = recommendations.filter(id=recommendation_id).first()
        print("############################################################################################################")
        print("recommendation id: ", recommendation_id)
        print("############################################################################################################")
        action = request.POST.get("action")

        if action == "Save & Continue":
            
            if back_btn_flag == "False":
                            
                rating = request.POST.get(f"rating_{recommendation.id}")
                comment = request.POST.get(f"comment_{recommendation.id}")
                
                Evaluation.objects.create(
                    recommendation=recommendation,
                    user_id=user_id,
                    rating=rating,
                    comment=comment if comment else ""
                )
                
            elif back_btn_flag == "True":
                print("\n")
                print("back button pressed")
                evaluation_id = request.POST.get("evaluation_id")
                print("evaluation_id: ", evaluation_id)
                evaluation = get_object_or_404(Evaluation, id=evaluation_id)
                print("evaluation: ", evaluation)
                evaluation.rating = request.POST.get(f"rating_{recommendation.id}")
                print("evaluation rating: ", evaluation.rating)
                evaluation.comment = request.POST.get(f"comment_{recommendation.id}")
                print("evaluation comment: ", evaluation.comment)
                evaluation.save()
                print("evaluation saved")
                
            else:
                return HttpResponse("Error 501: Invalid back button flag", status=501)

            return redirect('evaluation')

        elif action == "back":
            previous_evaluations_id = request.POST.get("previous_evaluations_id")
            previous_evaluations_id = ast.literal_eval(previous_evaluations_id)
            print("previous_evaluations_id: ", previous_evaluations_id, "previous_evaluations_id type: ", type(previous_evaluations_id))
            previous_evaluation_number = int(request.POST.get("evaluation_number")) - 1
            print("previous_evaluation_number: ", previous_evaluation_number, "previous_evaluation_number type: ", type(previous_evaluation_number))
            desired_id = previous_evaluations_id[previous_evaluation_number - 1]
            print("desired_id: ", desired_id)
            evaluation = get_object_or_404(Evaluation, id=desired_id)
            print("evaluation: ", evaluation, "evaluation type: ", type(evaluation))
            print("evalution recommendation: ", evaluation.recommendation, "evaluation recommendation type: ", type(evaluation.recommendation))
            print("evaluation rating: ", evaluation.rating, "evaluation rating type: ", type(evaluation.rating))
            print("evaluation comment: ", evaluation.comment, "evaluation comment type: ", type(evaluation.comment))
            context = {
                "evaluation_number": previous_evaluation_number,
                "previous_evaluations_id": previous_evaluations_id,
                "recommendation": evaluation.recommendation,
                "evaluation": evaluation,
                "user_id": user_id
            }
            
            return render(request, 'ers_evaluation/evaluation.html', context)
    
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