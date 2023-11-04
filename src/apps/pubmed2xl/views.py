"""PubMed2XL Views."""
import io
import os
import uuid
import datetime
import urllib.request as urllib
from xml.etree import ElementTree

from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from Bio import Medline
import pandas as pd

from .forms import GetPMIDsForm
from .helpers import get_all_data, get_xml

N = 300
TESTING = False
APP_PATH = os.path.dirname(os.path.abspath(__file__)) # Gets path of the _init_.py file
file_path = os.path.join(APP_PATH, "temp")
MEDLINE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed"
MEDLINE_URL = MEDLINE_URL + "&api_key=" + settings.NCBI_API_KEY
MEDLINE_URL = MEDLINE_URL + "&rettype=medline"
MEDLINE_TEXT_URL = MEDLINE_URL + "&retmode=text&id="
MEDLINE_XML_URL = MEDLINE_URL + "&retmode=xml&id="
CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
DECLARATION_AND_DOCTYPE = '''<?xml version="1.0" ?>
<!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2019//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd">
'''

def redirect_view(request, pmid):
    response = redirect(reverse("pubmed2xl:download_excel") + pmid)
    return response

def faq(request, pmid):
    """."""
    context = {'time': datetime.datetime.now().strftime ("%B %d, %Y")} #October 10, 2020
    template = "pubmed2xl/faq.html"
    context["page_h1_title"] = "PubMed2XL"
    initial = ""
    if len(pmid) >=1:
        initial = {"pmids": pmid.replace("/", "").replace(" ", "")}
    context['form'] = GetPMIDsForm(initial=initial)
    return render(request, template, context)

def download_excel(request, pmid):
    """."""
    context = {}
    if request.method == "GET":
        initial = ""
        if len(pmid) >=1:
            initial = {"pmids": pmid.replace(" ", "").replace(",", "\r\n")}
        context['form'] = GetPMIDsForm(initial=initial)
    elif request.method == "POST":
        if GetPMIDsForm(request.POST).is_valid():
            pmids = request.POST.get("pmids").strip().split('\r\n')
            data = []
            for batch in [pmids[i * N:(i + 1) * N] for i in range((len(pmids) + N - 1) // N )]:
                id_list = ""
                for pid in batch:
                    if id_list == "":
                        id_list = pid
                    else:
                        id_list = id_list + "," + pid
                text_path = file_path + "/" + str(uuid.uuid1()) + '.txt'
                urllib.urlretrieve(MEDLINE_TEXT_URL + id_list, text_path)
                with open(text_path, mode="r", encoding="utf-8") as handle:
                    articles = Medline.parse(handle)
                    for article in articles:
                        data.append(get_all_data(article))
                    handle.close()
                os.remove(text_path)
            dframe = pd.DataFrame(data)
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            dframe.to_excel(writer, sheet_name='PubMed2XL', index=False)
            writer.close()
            response = HttpResponse(output.getvalue(), content_type=CONTENT_TYPE)
            response['Content-Disposition'] = "attachment; filename=" + str(uuid.uuid1()) + ".xlsx"
            return response
        else:
            context['form'] = GetPMIDsForm(request.POST)
            return render(request, 'pubmed2xl/index.html', context)
    context["page_h1_title"] = "PubMed2XL"
    context["download_button_text"] = "Download Excel File"
    return render(request, 'pubmed2xl/index.html', context)


def download_xml(request, pmid):
    """."""
    context = {}
    template = 'pubmed2xl/xml.html'
    if request.method == "GET":
        initial = ""
        if len(pmid) >=1:
            initial = {"pmids": pmid.replace(" ", "").replace(",", "\r\n")}
        context['form'] = GetPMIDsForm(initial=initial)
    elif request.method == "POST":
        if GetPMIDsForm(request.POST).is_valid():
            pmids = request.POST.get("pmids").strip().split('\r\n')
            data = None
            for batch in [pmids[i * N:(i + 1) * N] for i in range((len(pmids) + N - 1) // N )]:
                id_list = ""
                for pid in batch:
                    if id_list == "":
                        id_list = pid
                    else:
                        id_list = id_list + "," + pid
                url = MEDLINE_XML_URL + id_list
                tree = get_xml(url)
                root = tree.getroot()
                if data is None:
                    data = root
                else:
                    data.extend(root)
            doc = ElementTree.tostring(data).decode('utf-8')
            response = HttpResponse(f"{DECLARATION_AND_DOCTYPE}{doc}", content_type="application/xml")
            response['Content-Disposition'] = "attachment; filename=" + str(uuid.uuid1()) + ".xml"
            return response
        else:
            context['form'] = GetPMIDsForm(request.POST)
            return render(request, template, context)
    context["page_h1_title"] = "PubMed2XML"
    context["download_button_text"] = "Download XML File"
    return render(request, template, context)
