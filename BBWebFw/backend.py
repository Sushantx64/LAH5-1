import brotli
from webob import Request, Response
from parse import parse
#from BBWebFw.FileRenderer import Template
import inspect
import urllib.request as httpRequest
import os, sys, re, datetime
from gunicorn.app.base import Application, Config
import gunicorn
from gunicorn.workers import sync
from gunicorn import glogging
from gunicorn.app.wsgiapp import run
import hashlib

class api:
    """
    docstring
    """
    def __init__(self, wrapper, name, server, path, dev=False):
        wrapper.urls = {}
        wrapper.server = server
        wrapper.name = name
        wrapper.out404 = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Document</title>\n</head>\n<body>\n    Hello\n</body>\n</html>'
        wrapper.error = {"urlcatcherexists": "ERR:URL_CATCHER_ALREADY_EXISTS"}

    async def checkReload():
        for file in os.listdir("/"):
            if file.endswith(".py"):
                print(os.path.join("/mydir", file))
        #if keyboard.is_pressed('ctrl+r'):
        #    print('a key has ben pressed')

    def md5(f):
        hash_md5 = hashlib.md5()
        with open(f, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def __call__(wrapper, environ, start_response):
        request = Request(environ)
        #print(wrapper.printIP(environ))
        response = wrapper.handle_request(request)
        with open("logs/access-log-"+datetime.datetime.now().strftime("%Y-%m-%d")+ ".txt", "a+") as f:
            f.write("\n")
            f.write((wrapper.getIP(environ) + ' - - [' +
                     (datetime.date.today().__str__()) + ' ' +
                     (datetime.datetime.now().strftime("%H:%M:%S")) + ']' +
                     request.method))
            f.write("\n")
            f.write("Request" + ":" + request.path)
            f.write("\n")
            f.write("Response Code" + ":" + response.status_code.__str__())
            f.write("\n")
        wrapper.getIP(environ)
        return response(environ, start_response)

    def getFileType(wrapper, f):
            wrapper.extList = {
                ".css": "text/css",
                ".html": "text/html",
                ".htm": "text/html",
                ".ico": "image/vnd.microsoft.icon",
                ".js": "text/javascript",
                ".svg": "image/svg",
                ".xml": "text/xml",
                ".jp2": "image/x-jp2",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".json": "text/json",
                ".png": "image/png",
                ".txt": "text/plain",
                ".map": "application/json",
                ".webp": "image/webp",
            }
            wrapper.noText = {
                ".ico": "image/ico",
                ".jp2": "image/x-jp2",
                ".jpg": "image/jpg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
            }
            fileType = wrapper.extList[os.path.splitext(f)[1]]

            return fileType, fileType in wrapper.noText.values()

    def handle_request(wrapper, request):
            #user_agent = request.environ.get('HTTP_USER_AGENT')
            response = Response()
            response.status_code = 200
            response.text = "Empty Response"

            handler, kwargs = wrapper.find_handler(request)
            compress = True
            if handler is not None:
                if (inspect.isclass(handler)):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is not None:
                        handler(request, response, **kwargs)
                    else:
                        wrapper.err503(response)
                else:            
                    handler(request, response, **kwargs)
                if compress:
                    response.body = brotli.compress(response.text.encode())
                    response.content_encoding = "br"
            else:
                try:
                    try:
                        FileType, noText = wrapper.getFileType(request.path)
                        print(FileType, noText)
                        response.content_type = FileType
                        if (noText):
                            print("\n\n****************\n\n")
                            print("loc:", wrapper.root + "/static" + request.path)

                            response.body = open(wrapper.root + "/static" + request.path, "rb").read()
                        else:
                            print("\n\n****************\n\n")
                            print("loc:", wrapper.root + "/static" + request.path)
                            response.text = open(wrapper.root + "/static" + request.path).read()

                        response.cache_control = "max-age=" + str(wrapper.staticCache)
                    except Exception as e:
                        print(e)
                        wrapper.err404(response)
                except Exception as e:
                    print(e)
                    response.text = "Well My Work Was Not Clean Enough, but...<br><b>Thats A Server Problem</b>"
                    response.status_code = 500
            return response

    def catchURL(wrapper, path):
        def wrapperFunction(handler):
            if (not (wrapper.urls.__contains__(path))):
                wrapper.urls[path] = handler
                print(wrapper.urls[path])
                return handler
            else:
                print("hi")
                raise AssertionError(wrapper.error["urlcatcherexists"])
                return wrapper.error["urlcatcherexists"]

        return wrapperFunction

    def find_handler(wrapper, request):
        for path, handler in wrapper.urls.items():
            print(path, " ", request.path, " ", parse(path, request.path))
            parseOut = parse(path, request.path)
            if parseOut is not None:
                print(handler)
                return handler, parseOut.named

        return None, None

    def return_external(wrapper, response, domain, uri, mimetype=None):
        FileType, noText = wrapper.getFileType(uri)
        if mimetype == None:
            response.content_type = FileType

        if (noText):
            response.body = httpRequest.urlopen(domain + uri).read()
        else:
            try:
                response.text = httpRequest.urlopen(domain + uri).read()
            except:
                response.text = httpRequest.urlopen(domain +
                                                    uri).read().decode()
        pass

    def err404(wrapper, response):
        response.status_code = 404
        response.text = wrapper.out404

    def err503(wrapper, response):
        response.status_code = 404
        response.text = wrapper.out503

    def setError(wrapper, code, data):
        if code == 404:
            wrapper.out404 = data
        elif code == 503:
            wrapper.out503 = data
        else:
            raise Exception("Invalid Error Code")

    def getIP(environ):
        try:
            return environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            return environ['REMOTE_ADDR']

    def run(wrapper, app, host):
        print("run")
        if wrapper.server.upper() == "GUNICORN":
            if (wrapper.name).endswith(".py"):
                wrapper.fname = wrapper.name
                wrapper.name = (wrapper.name).replace(".py", "")
            else:
                wrapper.fname = wrapper.name + ".py"

            sys.argv = [
                re.sub(r'(-script\.pyw|\.exe)?$', '', "env/bin/gunicorn"),
                wrapper.name + ':' + app, "-b", host
            ]
            print(sys.argv)
            sys.exit(run())
        elif wrapper.server.upper() == "BJOERN":
            import bjoern
            bjoern.run(app, **(host.split(":")))