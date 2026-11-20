from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import Student

from exam.models import Exam
def signup_view(request):

    if request.method == "POST":

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        phone = request.POST['phone']
        enrollment = request.POST['enrollment_number']

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:

            return render(
                request,
                'signup.html',
                {
                    'error': 'Passwords Do Not Match'
                }
            )

        # Enrollment Check

        if Student.objects.filter(
            enrollment_number=enrollment
        ).exists():

            return render(
                request,
                'signup.html',
                {
                    'error': 'Enrollment Number Already Exists'
                }
            )

        # Phone Check

        if Student.objects.filter(
            phone=phone
        ).exists():

            return render(
                request,
                'signup.html',
                {
                    'error': 'Phone Number Already Exists'
                }
            )

        # Email Check

        if User.objects.filter(
            email=email
        ).exists():

            return render(
                request,
                'signup.html',
                {
                    'error': 'Email Already Registered'
                }
            )

        user = User.objects.create_user(
            username=enrollment,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        Student.objects.create(
            user=user,
            enrollment_number=enrollment,
            phone=phone
        )

        return redirect('login')

    return render(
        request,
        'signup.html'
    )
def login_view(request):

    if request.method == "POST":

        enrollment_number = request.POST[
            'enrollment_number'
        ]

        password = request.POST[
            'password'
        ]

        user = authenticate(
            request,
            username=enrollment_number,
            password=password
        )

        if user is not None:

            login(request,user)

            if user.is_staff:
                return redirect('/admin/')

            return redirect('dashboard')

        return render(
            request,
            'login.html',
            {
                'error':'Invalid Login'
            }
        )

    return render(
        request,
        'login.html'
    )
def logout_view(request):

    logout(request)

    return redirect('login')
@login_required
def dashboard(request):

    exams = Exam.objects.all()

    return render(
        request,
        'dashboard.html',
        {
            'exams': exams
        }
    )
