from django.contrib.auth.models import User
from django.shortcuts import render, get_list_or_404,get_object_or_404, redirect
from .models import course

def courses(request):
    courses = get_list_or_404(course)
    return render(request, 'maintain/courses.html', {'courses': courses})

def home(request):
    return render(request, 'maintain/home.html')

def cou_detail(request, course_id):
    cou = get_object_or_404(course, pk=course_id)
    return render(request, 'maintain/cou_detail.html', {'cou': cou})

def course_new(request):
    if request.method == 'POST':
        course_name = request.POST['course_name']
        course_description = request.POST['course_description']
        course_type = request.POST['course_type']
        course_required_sware = request.POST['course_required_sware']
        course_instructor_sware = request.POST['course_instructor_sware']
        course_notes = request.POST['course_notes']

        user = User.objects.first()  # TODO: get the currently logged in user

        cou = course.objects.create(course_name=course_name, 
        course_description=course_description,
        course_type=course_type,
        course_required_instr_sware =course_instructor_sware ,
        course_required_sware =course_required_sware,
        course_notes = course_notes
        )

        return redirect('courses')  # TODO: redirect to the created topic page

    return render(request, 'maintain/course_new.html')