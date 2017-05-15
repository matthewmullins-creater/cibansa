from django.shortcuts import render,redirect
from main import util
from django.shortcuts import get_object_or_404
from main.models import CbCategory,CbQuestion,CbTopic,CbTag,CbQuestionTag,CbTopicTags
from main.forms import CbQuestionForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q

# Create your views here.


def index(request):
    categories = util.get_top_category()

    context={
        "category_cards":categories
    }
    return render(request,"main/index.html",context)


def list_topic(request,slug):
    category = get_object_or_404(CbCategory,slug=slug)
    topics = CbTopic.objects.filter(category=category.id)
    page = request.GET.get("page",1)

    paginator = Paginator(topics,2)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    context={
        "topics":topics,
        "category":category
    }
    return render(request,"main/list-topic.html",context)


def list_topic_question(request,slug):
    topic = get_object_or_404(CbTopic,slug=slug)
    context = {
        "topic":topic,
        "questions":topic.topic_questions.all(),
    }
    return render(request,"main/list-topic-questions.html",context)


def list_categories(request):
    category = CbCategory.objects.all()

    page = request.GET.get("page",1)
    paginator = Paginator(category,2)

    try:
        category = paginator.page(page)
    except PageNotAnInteger:
        category = paginator.page(1)
    except EmptyPage:
        category = paginator.page(paginator.num_pages)

    context = {
        "category":category
    }
    return render(request,"main/category-list.html",context)


def post_question(request):
    if request.method == "POST":
        form = CbQuestionForm(data=request.POST,request=request)
        if form.is_valid():
            question = form.save()
            return redirect("view-question",question.id)
    else:
        form = CbQuestionForm(request=request)
    context = {
        "form": form
    }
    return render(request,"main/post-question.html",context)


def view_question(request,id):
    question = get_object_or_404(CbQuestion,pk=id)
    related_topic = CbQuestion.objects.filter(~Q(pk=id),topic=question.topic.id)[:2]
    context ={
        "question": question,
        "related_topic":related_topic
    }
    return render(request,"main/view-question.html",context)


def question_by_tag(request,slug):
    tag = get_object_or_404(CbTag,slug=slug)
    questions = CbQuestion.objects.filter(tag=tag.id)

    context = {
        "questions":questions
    }
    return render(request,"main/questions_by_tag",context)




