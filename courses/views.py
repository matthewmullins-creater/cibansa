from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect,redirect
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings
from main.models import CbCategory
from courses.models import CbCourses
# Create your views here.


def view_courses(request,id):
    course = get_object_or_404(CbCourses,pk=id)
    similar_courses = CbCourses.objects.filter(~Q(id=id),category=course.category,is_visible=True).order_by("-created_at")[:3]
    context = {
        "courses": course,
        "more_courses":similar_courses
    }
    return render(request,"courses/view.html",context)


def by_category(request,slug):
    c = get_object_or_404(CbCategory,slug=slug)
    courses = CbCourses.objects.filter(is_visible=True,category=c.id)
    page = request.GET.get("page", 1)
    paginator = Paginator(courses, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    category = CbCategory.objects.filter(is_visible=True)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {
        "courses": courses,
        "category": category,
        "slug":slug,
    }
    return render(request, "courses/list.html", context)


def list_courses(request):
    courses = CbCourses.objects.filter(is_visible=True).order_by("-created_at")
    page = request.GET.get("page", 1)
    paginator = Paginator(courses, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    category = CbCategory.objects.filter(is_visible=True)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {
        "courses": courses,
        "category": category,
    }
    return render(request,"courses/list.html",context)


def search_courses(request):
    courses = CbCourses.objects.filter(title__icontains=request.GET.get("q"))
    page = request.GET.get("page", 1)
    paginator = Paginator(courses, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    category = CbCategory.objects.filter(is_visible = True)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {
        "courses": courses,
        "category": category,
    }
    return render(request, "courses/list.html", context)
