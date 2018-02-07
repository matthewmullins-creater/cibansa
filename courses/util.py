from courses.models import CbCourses


def new_courses():
    # courses = CbCourses.objects.filter(is_visible=True).order_by("-created_at")[:4]
    courses = CbCourses.objects.filter(is_visible=True).order_by("id")[:4]
    return courses
