import requests 
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__href = ""
        self.__x86 = False
        self.__count = 0
        self.__mode = 0
    
    def handle_starttag(self, tag, attrs):
        if self.__mode == 0:
            if tag == "a" and self.__x86:
                for att in attrs:
                    if att[0] == "href":
                        self.__href = att[1]
                        break
                self.__x86 = False
        else:
            if tag == "a":
               for att in attrs:
                    if att[0] == "id" and att[1] == "download_link":
                        print(attrs[-1][1])
                        self.__href = attrs[-1][1]


    def handle_data(self, data):
        if self.__mode == 0:  
            if data == "x86" and self.__count ==0:
                self.__x86 = True
                self.__count = self.__count + 1
    
    def get_href(self):
        return self.__href
    
    def set_mode(self,mode):
        self.__mode = mode

baseUrl = "https://www.apkmirror.com";
URL = "https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Android&num=1&offset=0"
r = requests.get(URL)
data = r.json() 
version = data[0]['version']
print(version)
#version = version.replace(".", "-");
URL = "https://apkpure.com/google-chrome-fast-secure/com.android.chrome/variant/%s-APK" % version
print(URL)
r = requests.get(URL)
parser = MyHTMLParser()
parser.feed(r.text)
link = "https://apkpure.com" + parser.get_href()
print(link)
r = requests.get(link,allow_redirects=True)
#print(r)
#open('chrome_browser.apk', 'wb').write(r.content)
parser.set_mode(1);
parser.feed(r.text)
r = requests.get(parser.get_href(),allow_redirects=True)
#print(r)
open('/root/chrome_browser.apk', 'wb').write(r.content)
