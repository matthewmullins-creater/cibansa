from django.template import Library
from bs4 import BeautifulSoup

register = Library()

@register.filter
def remove_tag(markup,tag):
    soup = BeautifulSoup(markup,"html5lib")
    if soup.find_all(tag):
        for t in soup.find_all(tag):
            t.replace_with("")
    return soup.prettify()
