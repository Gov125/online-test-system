
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Student
from exam.models import Exam


# =========================
# SIGNUP VIEW
# =========================

def signup_view(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()

        phone = request.POST.get('phone', '').strip()
        enrollment = request.POST.get('enrollment_number', '').strip()

        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Check empty fields
        if not all([
            first_name, last_name, email,
            phone, enrollment, password, confirm_password
        ]):
            return render(request, 'signup.html', {
                'error': 'All fields are required.'
            })

        # Password validation
        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Passwords Do Not Match.'
            })

        if len(password) < 8:
            return render(request, 'signup.html', {
                'error': 'Password must contain at least 8 characters.'
            })

        # Enrollment Check
        if Student.objects.filter(
            enrollment_number=enrollment
        ).exists():

            return render(request, 'signup.html', {
                'error': 'Enrollment Number Already Exists.'
            })

        # Phone Check
        if Student.objects.filter(phone=phone).exists():

            return render(request, 'signup.html', {
                'error': 'Phone Number Already Exists.'
            })

        # Email Check
        if User.objects.filter(email__iexact=email).exists():

            return render(request, 'signup.html', {
                'error': 'Email Already Registered.'
            })

        # Username Check
        if User.objects.filter(username=enrollment).exists():

            return render(request, 'signup.html', {
                'error': 'Enrollment Number Already Registered.'
            })

        # Create User
        user = User.objects.create_user(
            username=enrollment,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # Create Student Profile
        Student.objects.create(
            user=user,
            enrollment_number=enrollment,
            phone=phone
        )

        # Automatically Login
        login(request, user)

        return redirect('dashboard')

    # GET Request
    return render(request, 'signup.html')


# =========================
# LOGIN VIEW
# =========================

def login_view(request):

    if request.method == "POST":

        enrollment_number = request.POST.get(
            'enrollment_number', ''
        ).strip()

        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=enrollment_number,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect('/admin/')

            return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid Login Credentials.'
        })

    return render(request, 'login.html')

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
