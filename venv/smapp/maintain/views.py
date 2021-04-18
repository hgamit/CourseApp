from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404,get_object_or_404, redirect
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from constance import config
from .forms import NewTopicForm, PostForm
from .models import course, topic, post, classroom, clas_sware
import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def courses(request):
    if request.user.is_authenticated:
        queryset = list(course.objects.filter(sch_semester = config.Semester).filter(course_instructor__username=request.user))
        if request.user.is_superuser:
            queryset = list(course.objects.filter(sch_semester = config.Semester).all())        
        if queryset:
            page = request.GET.get('page', 1)
<<<<<<< HEAD
            paginator = Paginator(queryset, 10)
=======
            paginator = Paginator(queryset, 5)
>>>>>>> 7f4a9991ac37a8284e1c69b428d63580d82388b5
            
            try:
                courses = paginator.page(page)
            except PageNotAnInteger:
                # fallback to the first page
                courses = paginator.page(1)
            except EmptyPage:
                # probably the user tried to add a page number
                # in the url, so we fallback to the last page
                courses = paginator.page(paginator.num_pages)
            return render(request, 'maintain/courses.html', {'courses': courses})
        else:
            return render(request, 'maintain/courses.html', {'courses': queryset})
    else:
        return render(request, 'maintain/home.html')

def home(request):
<<<<<<< HEAD
    sware = get_list_or_404(clas_sware)
    tag_data = ""
    for ind, s_name in enumerate(sware):
        tag_data = tag_data + '{id: ' + str(ind) + ', name: "' + s_name.sware_name + '"},'
    return render(request, 'maintain/test.html', {'tag_data': tag_data})
=======
    return render(request, 'maintain/home.html')
>>>>>>> 7f4a9991ac37a8284e1c69b428d63580d82388b5

def cou_detail(request, course_id):
    cou = get_object_or_404(course, pk=course_id)
    return render(request, 'maintain/cou_detail.html', {'cou': cou})

def classroom_detail(request, course_id, class_id):
    clsroom = get_object_or_404(classroom, pk=class_id)
    cou = get_object_or_404(course, pk=course_id)
    return render(request, 'maintain/classroom_detail.html', {'clsroom': clsroom, 'cou': cou})

@method_decorator(login_required, name='dispatch')
class SwareResultsView(ListView):
    model = clas_sware
    template_name = 'maintain/clas_sware_results.html'
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@login_required
def course_topics(request, course_id):
    cou = get_object_or_404(course, pk=course_id)
    queryset = cou.course_topics.order_by('-topic_last_updated').annotate(replies=Count('topic_posts')-1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 5)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)
    return render(request, 'maintain/topics.html', {'cou': cou, 'topics': topics})

@login_required
def topic_posts(request, course_id, topic_id):
    topic_obj = get_object_or_404(topic, topic_course__pk=course_id, pk=topic_id)
    session_key = 'viewed_topic_{}'.format(topic_obj.pk)  # <-- here
    if not request.session.get(session_key, False):
        topic_obj.topic_views += 1
        topic_obj.save()
        request.session[session_key] = True
    return render(request, 'maintain/topic_posts.html', {'topic': topic_obj})

@login_required
def course_update(request, course_id):
    cou = get_object_or_404(course, pk=course_id)
    sware = get_list_or_404(clas_sware)
    tag_data = ""
    for ind, s_name in enumerate(sware):
<<<<<<< HEAD
        tag_data = tag_data + '{id: ' + str(ind) + ', name: "' + s_name.sware_name + '"},'
=======
        tag_data = tag_data + '{id: ' + str(ind) + ', name: "' + s_name.sware_name + " version " + s_name.sware_version + '"},'
>>>>>>> 7f4a9991ac37a8284e1c69b428d63580d82388b5
    
    user = request.user  # get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic_obj = form.save(commit=False)
            topic_obj.topic_course = cou
            topic_obj.topic_starter = user
            topic_obj.save()

            post_obj = post.objects.create(
                post_message=form.cleaned_data.get('post_message'),
                post_topic=topic_obj,
                post_created_by=user
            )

            return redirect('topic_posts', course_id, topic_obj.pk)   # redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'maintain/course_update.html', {'cou': cou, 'form': form, 'tag_data': tag_data})

@login_required
def reply_topic(request, course_id, topic_id):
    topic_obj = get_object_or_404(topic, topic_course__pk=course_id, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_topic = topic_obj
            post.post_created_by = request.user
            post.save()

            topic_obj.topic_last_updated = timezone.now()  # <- here
            topic_obj.save()                         # <- and here


            topic_url = reverse('topic_posts', course_id, topic_id)
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic_obj.get_page_count()
            )
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'maintain/reply_topic.html', {'topic': topic_obj, 'form': form})

@login_required
def update_post(request, course_id, topic_id, post_id):
    post_obj = get_object_or_404(post, post_topic__topic_course__pk=course_id, post_topic__pk=topic_id ,pk=post_id)
<<<<<<< HEAD
=======
    sware = get_list_or_404(clas_sware)
    tag_data = ""
    for ind, s_name in enumerate(sware):
        tag_data = tag_data + '{id: ' + str(ind) + ', name: "' + s_name.sware_name + " version " + s_name.sware_version + '"},'
    
>>>>>>> 7f4a9991ac37a8284e1c69b428d63580d82388b5
    if request.method == 'POST' and post_obj.post_created_by==request.user:
        form = PostForm(request.POST, instance=post_obj)
        if form.is_valid():
            post_update = form.save(commit=False)
            post_update.post_created_at = timezone.now()
            post_update.updated_by = request.user
            post_update.updated_at = timezone.now()
            post_update.save()
            return redirect('topic_posts', course_id, topic_id)
    else:
        form = PostForm(instance=post_obj)
<<<<<<< HEAD
    return render(request, 'maintain/edit_post.html', {'post': post_obj, 'form': form})
=======
    return render(request, 'maintain/edit_post.html', {'post': post_obj, 'form': form, 'tag_data': tag_data})
>>>>>>> 7f4a9991ac37a8284e1c69b428d63580d82388b5
