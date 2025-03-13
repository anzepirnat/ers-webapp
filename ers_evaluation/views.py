from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import random
from .models import Recommendation, Evaluation, RecsContextsExplsA3, Randomization
from django.contrib.auth.decorators import login_required
import ast
from .utils import remove_last_comma

MAX_EVALUATIONS = 20

def index(request):
    return render(request, 'ers_evaluation/index.html')


@login_required
def evaluation(request):
    
    # Get all recommendations, if there are no recommendations, raise an error
    recommendations = RecsContextsExplsA3.objects.all()
    if not recommendations.exists():
        raise Http404("There are no recommendations to evaluate.")
    
    # Get evalutions that the user has already done, if there are more than XX evaluations, thank them for work
    completed_evaluations = Evaluation.objects.filter(user_id=request.user.id)
    completed_evaluations_count = completed_evaluations.count()
    if completed_evaluations_count >= MAX_EVALUATIONS:
        context = {
            "max_evaluations": MAX_EVALUATIONS,
            "completed_evaluations_count": completed_evaluations_count
        }
        return render(request, 'ers_evaluation/finished.html', context)
    
    # Filter out recommendations that the user has already evaluated
    completed_evaluations_recommendation_id = [evaluation.recommendation.id for evaluation in completed_evaluations]
    unevaluated_recommendations = recommendations.exclude(id__in=completed_evaluations_recommendation_id)
    # Selecting text will work based on user_id, so basically:
    # 1. Get all Randomization table
    # 2. Get correct column the user 
    # 3. Go through the rows and check for each if the id is in 
    unevaluated_recommendations_ids = [rec.id for rec in list(unevaluated_recommendations)]
    try:
        selected_text = unevaluated_recommendations[0]
        log.info(f"[rec.id for rec in list(unevaluated_recommendations)]: {unevaluated_recommendations_ids}")
    except IndexError as e:
        context = {
            "max_evaluations": MAX_EVALUATIONS,
            "completed_evaluations_count": completed_evaluations_count
        }
        return render(request, 'ers_evaluation/finished.html', context)
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        raise Http404(f"Unexpected error: {e}")
    
    # choosing the image to display
    annot_path = f"annots/annotImg_uID-{selected_text.elder_id}.png"
    
    log.info(f"selected_text.id: {selected_text.id}")
    
    activity_texts = selected_text.activity_texts.split(", ")
    
    context = {
        "max_evaluations": MAX_EVALUATIONS,
        "evaluation_number": completed_evaluations_count + 1,
        "recommendation": selected_text,
        "user_id": request.user.id,
        "annot_path": annot_path,
        "activity_texts": activity_texts
    }
    
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        recommendation_id = int(request.POST.get("recommendation_id"))
        recommendation = recommendations.filter(id=recommendation_id).first()
        action = request.POST.get("action")

        if action == "Save & Continue":
                                        
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

from .utils import excel_to_db, log, excel_to_db_randomization
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .forms import UploadExcelForm
from django.db import connection

def reset_auto_increment(table_name):
    """ Reset auto-increment counter for a table in MariaDB """
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")

@login_required
def edit_data(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        try:
            excel_file = request.FILES['excel_file'] # Get new data
            RecsContextsExplsA3.objects.all().delete() # Delete old data
            reset_auto_increment('ers_evaluation_recscontextsexplsa3') # Id to 1
            result = excel_to_db(excel_file) # Write new data
            
            return JsonResponse({'message': result}, status=200)
        
        except ValidationError as e:
            log.error("Validation error: %s", e)
            return JsonResponse({'error': str(e)}, status=400)

    # If it's a GET request, just render the page with the file upload form
    form = UploadExcelForm()
    return render(request, 'ers_evaluation/edit_data.html', {'form': form})


@login_required
def edit_data_randomization(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        try:
            excel_file = request.FILES['excel_file'] # Get new data
            Randomization.objects.all().delete() # Delete old data
            reset_auto_increment('ers_evaluation_recscontextsexplsa3') # Id to 1
            result = excel_to_db_randomization(excel_file) # Write new data
            
            return JsonResponse({'message': result}, status=200)
        
        except ValidationError as e:
            log.error("Validation error: %s", e)
            return JsonResponse({'error': str(e)}, status=400)

    # If it's a GET request, just render the page with the file upload form
    form = UploadExcelForm()
    return render(request, 'ers_evaluation/edit_data_randomization.html', {'form': form})