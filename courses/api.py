from rest_framework import  viewsets
from courses.serializers import CbCoursesSerializer
from courses.models import CbCourses

from rest_framework import permissions
from rest_framework.decorators import list_route,detail_route
from rest_framework.response import Response


class CbCoursesViewset(viewsets.ModelViewSet):
    queryset = CbCourses.objects.all()
    serializer_class = CbCoursesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
