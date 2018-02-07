from django.conf.urls import url
from courses import views
from django.conf.urls import include
from courses import api
from rest_framework import routers

courses = routers.SimpleRouter()
courses.register("", api.CbCoursesViewset, "courses")

urlpatterns = [
    url(r'^api/v1/courses/',include(courses.urls,namespace="courses-api")),
    url(r'^list/', views.list_courses, name="list-courses"),
    url(r'^view/(?P<id>[0-9]+)',views.view_courses,name="view-course"),
    url(r'^search/',views.search_courses,name="search-courses"),
]


##############

##############