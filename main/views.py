from django.shortcuts import render,redirect
from main import util
from django.shortcuts import get_object_or_404
from main.models import CbCategory,CbQuestion,CbTopic,CbTag,CbQuestionTag,CbTopicTags
from main.forms import CbQuestionForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.http import  HttpResponse,HttpResponseNotAllowed
import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from articles.util import new_articles
from main.forms import ContactForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from articles.models import CbArticle

# Create your views here.


def contact_thank_you(request):

    return render(request,"main/contact-thank-you.html")


def index(request):
    categories = util.get_top_category()
    articles = new_articles()
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            phone = request.POST.get("phone","")
            email = request.POST.get('email', '')
            form_content = request.POST.get('content', '')
            # contact information
            template =get_template('main/emails/contact_template.txt')
            context ={
                'contact_name': "{} {}".format(first_name,last_name),
                'phone': phone,
                'contact_email': email,
                'form_content': form_content,
            }
            content = template.render(context)
            email = EmailMessage(
                "New contact form submission",
                content,
                to=[settings.CONTACT_FORM_EMAIL],
                reply_to=[email]
            )
            email.send()
            return redirect('contact-thank-you')
    context={
        "category_cards": categories,
        "articles": articles,
        'form': form_class,
    }
    return render(request,"main/index.html",context)


def list_topic(request,slug):
    category = get_object_or_404(CbCategory,slug=slug)
    topics = CbTopic.objects.filter(category=category.id,is_visible=True)
    page = request.GET.get("page",1)
    tags = CbTag.objects.all()
    paginator = Paginator(topics,settings.REST_FRAMEWORK.get("PAGE_SIZE"))
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    context={
        "topics":topics,
        "tags":tags,
        "category":category
    }
    return render(request,"main/list-topic.html",context)


def list_topic_question(request,slug):
    topic = get_object_or_404(CbTopic,slug=slug)
    questions = topic.topic_questions.filter(is_deleted=False)
    page = request.GET.get("page",1)
    paginator = Paginator(questions,settings.REST_FRAMEWORK.get("PAGE_SIZE"))

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    context = {
        "topic":topic,
        "questions":questions,
    }
    return render(request,"main/list-topic-questions.html",context)


def list_categories(request):
    category = CbCategory.objects.filter(is_visible=True)

    page = request.GET.get("page",1)
    paginator = Paginator(category,settings.REST_FRAMEWORK.get("PAGE_SIZE"))

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


@login_required
def post_question(request):
    try:
        topic = CbTopic.objects.get(pk=request.GET.get("tp",""))
    except:
        topic=None

    try:
        category = CbCategory.objects.get(pk=request.GET.get("c",""))
    except:
        category = None

    if request.method == "POST":

        form = CbQuestionForm(data=request.POST,request=request)
        if form.is_valid():
            question = form.save()
            if request.POST.getlist("tag"):
                question.question_tags.all().delete()
                for tag in request.POST.getlist("tag"):
                    CbQuestionTag.objects.create(
                        question=question,
                        tag=CbTag.objects.get(pk=tag)
                    )
            return redirect("view-question",question.id)
    else:
        form = CbQuestionForm(request=request)
    context = {
        "form": form,
        "topic": topic,
        "category": category
    }
    return render(request,"main/post-question.html",context)

@login_required
def edit_question(request,question):
    question = get_object_or_404(CbQuestion,pk=question)
    if request.user.id == question.owner.id:
        if request.method == "POST":
            form = CbQuestionForm(request.POST,instance=question,request=request)
            if form.is_valid():
                question = form.save()
                question.question_tags.all().delete()
                if request.POST.getlist("tag"):
                    for tag in request.POST.getlist("tag"):
                        CbQuestionTag.objects.create(
                            question=question,
                            tag=CbTag.objects.get(pk=tag)
                        )
                return redirect("view-question",question.id)
        else:
            form = CbQuestionForm(instance=question,request=request)
        context = {
            "form": form,
            "question": question,
        }
        return render(request,"main/edit-question.html",context)
    else:
        return HttpResponseNotAllowed("You cannot edit this question")


def view_question(request,id):
    question = get_object_or_404(CbQuestion,pk=id)
    related_topic = CbQuestion.objects.filter(~Q(pk=id),topic=question.topic.id)[:2]
    context ={
        "question": question,
        "related_topic":related_topic
    }
    return render(request,"main/view-question.html",context)


def question_by_tag(request,slug):
    # tag = get_object_or_404(CbTag,slug=slug)
    questions = CbQuestionTag.objects.filter(tag__slug=slug)
    page = request.GET.get("page", 1)
    paginator = Paginator(questions, settings.REST_FRAMEWORK.get("PAGE_SIZE"))

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    context = {
        "questions":questions
    }
    return render(request,"main/questions_by_tag.html",context)


def get_topic_by_category(request):
    topics = CbTopic.objects.filter(category=request.GET.get("category"))
    topics_array=[]
    for t in topics:
        topics_array.append({"id":t.id,"name":t.title})
    return HttpResponse(json.dumps(topics_array))


# def search_questions(request):
#     result = CbQuestion.objects.filter(title__icontain=request.GET.get("q",""))
#     context = {
#         "result": result
#     }
#     return render(request,"main/question-search-result.html",context)


def search_topics(request):
    result = CbTopic.objects.filter(title__icontain=request.GET.get("q"))
    context = {
        "result": result
    }
    return render(request,"main/list-topic.html",result)


def tag_search(request):
    sqs = CbTag.objects.filter(name__icontains=request.GET.get("q"))
    tag_array = []
    for t in sqs:
        tag_array.append({"id": t.id, "label": t.name, "value": t.name})
    return HttpResponse(json.dumps(tag_array), content_type="application/json")


def question_search(request):
    q = request.GET.get("q","")
    results = CbQuestion.objects.filter(Q(title__icontains=q)| Q(category__name__icontains=q)|
                                          Q(topic__title__icontains=q))
    page = request.GET.get("page", 1)
    paginator = Paginator(results, settings.REST_FRAMEWORK.get("PAGE_SIZE"))

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {
        "results": results,
    }
    return render(request, "main/question-search-result.html", context)


def topic_search(request):
    category = get_object_or_404(CbCategory,pk=request.GET.get("cat",""))
    q = request.GET.get("q","")
    topics = CbTopic.objects.filter(title__icontains=q,category=request.GET.get("cat"))
    page = request.GET.get("page", 1)
    paginator = Paginator(topics, settings.REST_FRAMEWORK.get("PAGE_SIZE"))

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    context = {
        "topics": topics,
        "category":category,
    }
    return render(request, "main/list-topic.html", context)


def question_auto_complete(request):
    q = request.GET.get("q")
    sqs = CbQuestion.objects.filter(Q(title__icontains=q)| Q(category__name__icontains=q)|
                                          Q(topic__title__icontains=q))[:10]
    question_array = []
    for t in sqs:
        question_array.append({"id": t.id, "label": t.title, "value": t.title,"link":reverse("view-question",kwargs={"id":t.id})})
    return HttpResponse(json.dumps(question_array), content_type="application/json")

#
# def question_by_tag(request,tag):
#     questions = CbQuestionTag.objects.filter(tag__slug=tag)
#     page = request.GET.get("page", 1)
#     paginator = Paginator(questions, settings.REST_FRAMEWORK.get("PAGE_SIZE"))
#
#     try:
#         questions = paginator.page(page)
#     except PageNotAnInteger:
#         questions = paginator.page(1)
#     except EmptyPage:
#         questions = paginator.page(paginator.num_pages)
#
#     context={
#         "question": questions
#     }
#
#     return render(request,"",context)

# def contact_us(request):
#
#     return



