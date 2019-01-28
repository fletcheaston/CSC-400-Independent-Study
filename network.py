import urllib.request
#import web

class index:
    def GET(self):
        return("Hello world");

def reader():
    link = "http://10.1.9.204:8080"
    f = urllib.request.urlopen(link);
    myfile = f.read();
    data = myfile.split(b" ");
    for i in range(len(data)):
        print(data[i].decode("utf-8"));

'''def server():
    urls = ('/', 'index');
    app = web.application(urls, globals());
    app.run();'''

reader();
