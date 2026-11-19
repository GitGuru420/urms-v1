from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .models import Routine, Department, Faculty, FacultyAdminProfile, DeptAdminProfile, Teacher, Room, Timeslot, Course
import csv
from django.http import HttpResponse


# PUBLIC & AUTHENTICATION VIEWS
def landing_page(request):
    return render(request, 'routines/index.html')

def redirect_based_on_role(user):
    if user.is_superuser:
        return redirect('superuser_dashboard')
    elif hasattr(user, 'facultyadminprofile'):
        return redirect('faculty_admin_dashboard')
    elif hasattr(user, 'deptadminprofile'):
        return redirect('dept_admin_dashboard')
    elif hasattr(user, 'teacher'):
        return redirect('teacher_dashboard')
    return redirect('landing_page')

def user_login(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)
        
    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        p = request.POST.get('password', '').strip()
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect_based_on_role(user)
        else:
            messages.error(request, "Invalid credentials. Unauthorized clearance denied.")
    return render(request, 'routines/login.html')

def user_logout(request):
    logout(request)
    return redirect('landing_page')


def view_routine(request):
    return HttpResponse("Public routine view (Branch 9) | <a href='/'>Home</a>")

# ======================
# TEMPORARY PLACEHOLDERS
# ======================
@login_required(login_url='login')
def superuser_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')
    return HttpResponse("Superuser dashboard (Branch 5) | <a href='/logout/'>Logout</a>")

@login_required(login_url='login')
def faculty_admin_dashboard(request):
    if not hasattr(request.user, 'facultyadminprofile'):
        return redirect('login')
    return HttpResponse("Faculty Admin dashboard (Branch 6) | <a href='/logout/'>Logout</a>")

@login_required(login_url='login')
def dept_admin_dashboard(request):
    if not hasattr(request.user, 'deptadminprofile'):
        return redirect('login')
    return HttpResponse("Dept Admin dashboard (Branch 7) | <a href='/logout/'>Logout</a>")

@login_required(login_url='login')
def teacher_dashboard(request):
    if not hasattr(request.user, 'teacher'):
        return redirect('login')
    return HttpResponse("Teacher dashboard (Branch 8) | <a href='/logout/'>Logout</a>")