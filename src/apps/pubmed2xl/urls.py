"""."""
from django.urls import path, re_path
from django.shortcuts import redirect
from .views import redirect_view, download_excel, download_xml, faq

app_name = 'pubmed2xl'
urlpatterns = [
    re_path(r'^faq/(?P<pmid>((.{1,8}){1}(,\s?.{1,8})*)?)?$', faq, name="faq"),
    re_path(r'^xml/(?P<pmid>((.{1,8}){1}(,\s?.{1,8})*)?)?$', download_xml, name="download_xml"),
    re_path(r'^xlsx/(?P<pmid>((.{1,8}){1}(,\s?.{1,8})*)?)?$', download_excel, name="download_excel"),
    # Please note the slight diference between the regex below and the above ones.
    re_path(r"^(?P<pmid>((\d{1,8}){1}(,\s?\d{1,8})*)?)?$", redirect_view, name="landing_page"),
]

#re_path(r"^(?P<pmid>(.*))$", download_excel, name="landing_page"),