import bottle
import redis

r_host = 'redis-11371.c212.ap-south-1-1.ec2.cloud.redislabs.com'
r_port = 11371
r_password = 'QvbmpFhlbiruysa3G0Cd0qlhA3sgeSgf'
r = redis.Redis(host=r_host, port=r_port, password=r_password)
list_A = []


@bottle.route('/redis/<key>/<value>')
def redis_set(key, value):
    r.set(key, value)
    return '{}: {}'.format(key, value)


@bottle.route('/redis/<key>')
def redis_get(key):
    r.flushdb()
    return r.get(key)


# end redis --------------------------------------------

@bottle.post('/sq')
def post_sq():
    a = bottle.request.forms.get('a')
    b = bottle.request.forms.get('b')
    c = bottle.request.forms.get('c')
    result = a + 'x&#178;+' + b + 'x+' + c + '=0('
    try:
        x_1 = (-float(b) + (float(b) ** 2 - 4 * float(a) * float(c)) ** 0.5) / 2
        x_2 = (-float(b) - (float(b) ** 2 - 4 * float(a) * float(c)) ** 0.5) / 2
    except:
        x_1 = None
        x_2 = None
    global list_A
    if isinstance(x_1, complex) or isinstance(x_2, complex) or x_1 is None:
        result += 'не имеет действительных решений)'
    else:
        result += 'x&#8321;=' + str(x_1) + ' x&#8322;=' + str(x_2) + ')'
    list_A.insert(0, result)
    return dict(list_A=list_A)


@bottle.post('/sq2')
def post_sq():
    a = bottle.request.forms.get('a')
    b = bottle.request.forms.get('b')
    c = bottle.request.forms.get('c')
    result = a + 'x&#178;+' + b + 'x+' + c + '=0('
    try:
        x_1 = (-float(b) + (float(b) ** 2 - 4 * float(a) * float(c)) ** 0.5) / 2
        x_2 = (-float(b) - (float(b) ** 2 - 4 * float(a) * float(c)) ** 0.5) / 2
    except:
        x_1 = None
        x_2 = None
    if isinstance(x_1, complex) or isinstance(x_2, complex) or x_1 is None:
        result += 'не имеет действительных решений)'
    else:
        result += 'x&#8321;=' + str(x_1) + ' x&#8322;=' + str(x_2) + ')'
    r.lpush("list", result)
    lists = r.lrange("list", 0, 10)
    for i in range(len(lists)):
        lists[i] = lists[i].decode("utf-8")
    return dict(list_A=lists)


@bottle.route('/')
def index():
    return bottle.template('static/index.html', list_A=list_A)


@bottle.error(404)
def error404(error):
    return ("oops! the page you were looked for isn't here. <a href='/'>Return Home?</a>")


bottle.run(host='0.0.0.0', port=8080)
