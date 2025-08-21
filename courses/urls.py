from django.urls import path, include, re_path
from courses import views
from courses import api
from rest_framework import routers

courses = routers.SimpleRouter()
courses.register("", api.CbCoursesViewset, "courses")

urlpatterns = [
    path('api/v1/courses/',include(courses.urls)),
    path('list/', views.list_courses, name="list-courses"),
    re_path(r'^view/(?P<id>[0-9]+)',views.view_courses,name="view-course"),
    path('search/',views.search_courses,name="search-courses"),
]


##############

##############