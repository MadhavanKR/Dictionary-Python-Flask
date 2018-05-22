import requests;
import xml.etree.ElementTree as ET
#from app import app;

def getWordMeaning(word):
    baseurl = "https://www.dictionaryapi.com/api/v1/references/collegiate/xml/";
    url = baseurl + word;
    params = {"key":"396338bb-5f4a-4cf4-8dc3-c04601312b19"};
    response = requests.get(url=url, params = params);
    meaning = extractMeaning(response.text);
    return meaning;

def extractMeaning(xmlresponse):
    print(xmlresponse);
    root = ET.fromstring(xmlresponse);
    meaning="";
    for entryTag in root.findall("entry"):
        for defTag in entryTag.findall("def"):
            for dt in defTag.findall("dt"):
                meaning = meaning+"~~"+dt.text;
    return meaning;