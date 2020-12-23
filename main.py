from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
from pytz import timezone
import pytz
from datetime import datetime

#That function parse url requests for GET
def parse_get_req(req):
    parsed_req = [i for i in req.split('/') if i != '']
    return "/".join(parsed_req)

#It converts elements and keys of dict from bytes to utf8
def convert_bytes_to_utf (dict):
    new_dict = {}
    for i in dict.items():
        key,item = i
        key = key.decode('utf8')
        if isinstance(item,str):
            item = item.decode('utf8')
        elif isinstance(item,list):
            item = [j.decode('utf8') for j in item]
        new_dict[key]=item
    return new_dict

#Converts datetime from one time zone to another
def convert_df(dt,firtst_tz,second_tz):
    #Covert datetime format
    try:
        loc_dt = datetime.strptime(dt, '%m.%d.%Y %H:%M:%S')
    except:
        loc_dt = datetime.strptime(dt, '%I:%M%p %Y-%m-%d')

    firtst_tz = timezone(firtst_tz)
    second_tz = timezone(second_tz)

    localized_dt = firtst_tz.localize(loc_dt)
    result = localized_dt.astimezone(second_tz)
    return result

#GET request that gives current datetime of time zone
def get_dt(req):
    loc_dt = datetime.now()
    right_req = True

    if req == '':
        tz = timezone('Etc/GMT')
    else:
        try:
            tz = timezone(req)
        except:
            right_req = False
    if right_req:
        result = loc_dt.astimezone(tz)
        status = '200 OK'
    else:
        result = 'error'
        status = '400 ERROR'

    return (status,str(result))

#POST request that converts time from one timezone to an another
def post_convert(date,tz,target_tz):
    try:
        result = convert_df(date, tz, target_tz)
        status = '200 OK'
    except:
        result = 'Error'
        status = '400 ERROR'
    return (status, str(result))

#POST request that finds differences between two times in different time zones
def post_datediff(first_date,first_tz,second_date,second_tz):
    try:
        first_dt_GMT = convert_df(first_date, first_tz, 'Etc/GMT')
        second_dt_GMT = convert_df(second_date, second_tz, 'Etc/GMT')
        result = (first_dt_GMT - second_dt_GMT).total_seconds()
        status = '200 OK'
    except:
        result = 'Error'
        status = '400 ERROR'
    return (status, str(result))

def application (environ, start_response):

    #Get info about request
    req_method = environ['REQUEST_METHOD']
    path_info = environ['PATH_INFO']

    #GET requests
    if req_method == 'GET':
        req = parse_get_req(path_info)
        status, response_body = get_dt(req)

    #POST requests
    elif req_method == 'POST':
        # the environment variable CONTENT_LENGTH may be empty or missing
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        #get data and processing its
        request_body = environ['wsgi.input'].read(request_body_size)
        request_body = parse_qs(request_body)
        request_body = convert_bytes_to_utf (request_body)

        #POST convert request
        if path_info == '/api/v1/convert':
            date = request_body.get('date', [])[0]
            tz = request_body.get('tz', [])[0]
            target_tz = request_body.get('target_tz', [''])[0]
            status, response_body = post_convert(date,tz,target_tz)

        # POST diff request
        elif path_info == '/api/v1/datediff':
            first_date = request_body.get('first_date', [''])[0]
            first_tz = request_body.get('first_tz', [''])[0]
            second_date = request_body.get('second_date', [''])[0]
            second_tz = request_body.get('second_tz', [''])[0]
            status, response_body = post_datediff(first_date,first_tz,second_date,second_tz)
        else:
            response_body = 'Error'
            status = '400 BAD REQUEST'

    #content type is text/html
    response_headers = [
        ('Content-Type', 'text/html'),
    ]
    start_response(status, response_headers)
    return [response_body.encode()]

#Run a server
httpd = make_server('localhost', 8051, application)
httpd.serve_forever()