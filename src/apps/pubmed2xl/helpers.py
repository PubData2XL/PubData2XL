"""."""
import urllib.request as urllib
#import requests #substitute of urllib requires installation.
from xml.etree import ElementTree
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'\
             + 'AppleWebKit/537.36 (KHTML, like Gecko)'\
             + 'Chrome/76.0.3809.100 Safari/537.36'

def get_all_data(article):
    """."""
    article_data = {}
    article_data["PMID"] = get_data("PMID", article)
    article_data["PMC ID"] = get_data("PMC", article)
    article_data["Title"] = get_data("TI", article)
    article_data["Author(s)"] = get_data("AU", article)
    article_data["Author(s) Full Name"] = get_data("FAU", article)
    article_data["Author(s) Affiliation"] = get_data("AD", article)
    article_data["Corporate Author"] = get_data("CN", article)
    article_data["Collaborator(s)"] = get_data("IR", article)
    article_data["Collaborator(s) Full Name"] = get_data("FIR", article)
    article_data["Collaborator(s) Affiliation"] = get_data("IRAD", article)
    article_data["Source"] = get_data("SO", article)
    article_data["Transliterated Title"] = get_data("TT", article)
    article_data["Journal Title Abbreviation"] = get_data("TA", article)
    article_data["Journal Title"] = get_data("JT", article)
    article_data["ISSN"] = get_data("IS", article)
    article_data["Volume"] = get_data("VI", article)
    article_data["Issue"] = get_data("IP", article)
    article_data["Pages"] = get_data("PG", article)
    article_data["Place of Publication"] = get_data("PL", article)
    abstract = get_data("AB", article)
    if not abstract:
        abstract = ' '.join(article.get("OAB", ""))
    article_data["Abstract"] = abstract
    copyright = get_data("CI", article)
    if not copyright:
        copyright = get_data("OCI", article)
    article_data["Copyright Information"] = copyright
    article_data["Language"] = get_data("LA", article)
    article_data["Publication Type"] = get_data("PT", article)
    article_data["MeSH Terms"] = get_data("MH", article)
    article_data["Grant Number"] = get_data("GR", article)
    article_data["Number of References"] = get_data("RF", article)
    article_data["General Note"] = get_data("GN", article)
    article_data["Date of Publication"] = get_data("DP", article)
    article_data["Date of Electronic Publication"] = get_data("DEP", article)
    article_data["Date Created"] = get_data("DA", article)
    article_data["Date Completed"] = get_data("DCOM", article)
    article_data["Date Revised"] = get_data("LR", article)
    article_data["MeSH Date"] = get_data("MHDA", article)
    article_data["Entrez Date"] = get_data("EDAT", article)
    article_data["Status"] = get_data("STAT", article)
    article_data["Publication Status"] = get_data("PST", article)
    article_data["Publication History Status"] = get_data("PHST", article)
    article_data["Article Identifier"] = get_data("AID", article)
    article_data["NLM Unique ID"] = get_data("IR", article)
    article_data["Location Identifier"] = get_data("LID", article)
    article_data["Manuscript Identifier"] = get_data("MID", article)
    article_data["Secondary Source ID"] = get_data("SI", article)
    article_data["Publishing Model"] = get_data("PUBM", article)
    article_data["Comment on"] = get_data("CON", article)
    article_data["Comment in"] = get_data("CIN", article)
    article_data["Erratum in"] = get_data("EIN", article)
    article_data["Erratum for"] = get_data("EFR", article)
    article_data["Corrected and Republished in"] = get_data("CRI", article)
    article_data["Corrected and Republished from"] = get_data("CRF", article)
    article_data["Owner"] = get_data("OWN", article)
    return article_data

def get_data(element, source):
    """."""
    value = source.get(element, "")
    if isinstance(value, list):
        value = '||'.join(value)
    return value

def get_xml(url):
    '''
    Gets source etree and content encoding by given url

    file:// schema is also supported
    '''
    headers = { 'User-Agent' : USER_AGENT }
    req = urllib.Request(url, None, headers)
    #response = urllib.urlopen(req)
    # with urllib.urlopen(req) as response:
    #     xml_file = ElementTree.parse(response)
    #     return xml_file
    # response.close()
    response = urllib.urlopen(req)
    xml_file = ElementTree.parse(response)
    # response = requests.get(url, headers=headers)
    # response.raw.decode_content = True
    # xml_file = ElementTree.fromstring(response.content)
    return xml_file
