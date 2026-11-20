# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Exam
from .models import Question
from .models import Result


@login_required
def start_exam(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    # Check if already given

    already_attempted = Result.objects.filter(
        student=request.user,
        exam=exam
    ).exists()

    if already_attempted:

        return render(
            request,
            'already_attempt.html'
        )

    questions = Question.objects.filter(
        exam=exam
    )

    if request.method == "POST":

        score = 0

        for q in questions:

            selected = request.POST.get(
                str(q.id)
            )

            if selected == q.correct_answer:
                score += 1

        total = questions.count()

        percentage = (
            score / total
        ) * 100

        Result.objects.create(
            student=request.user,
            exam=exam,
            score=score,
            total_questions=total,
            percentage=percentage
        )

        return redirect(
            'result'
        )

    return render(
        request,
        'test.html',
        {
            'exam': exam,
            'questions': questions
        }
    )
@login_required
def result_view(request):

    result = Result.objects.filter(
        student=request.user
    ).latest('id')

    return render(
        request,
        'result.html',
        {
            'result': result
        }
    )
