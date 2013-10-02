from flask import Flask, url_for, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    title = 'Cygnus Gymnasium'
    return render_template('index.html', title=title)

@app.route('/<name>/')
def page(name):
    title = name.capitalize() + ' | Cygnus Gymnasium'
    page = name + '.html'
    return render_template(page, title=title)

@app.route('/over/<a>/<b>')
def aboutpage(a,b):
    title = 'Schoolklimaat | Cygnus Gymnasium'
    return render_template('schoolklimaat.html', title=title)

@app.route('/nieuws/<a>/<b>/<c>/')
def newsmessage(a,b,c):
    return render_template('nieuwsbericht.html')

@app.route('/fotos/<a>/<b>/')
def photoalbum(a,b):
    return render_template('fotoalbum.html')

@app.route('/login/', methods=['POST'])
def login():
    title = 'Schoolklimaat | Cygnus Gymnasium'
    return redirect(url_for('dashboard'))

@app.route('/login/', methods=['GET'])
def showlogin():
    return render_template('login.html')

@app.route('/zoek/autocompletion/', methods=['POST'])
def results():
    return render_template('autocompletion.html')

@app.route('/getrooster/<ref>/<idn>/')
def getrooster(ref,idn):
    import urllib2
    response = urllib2.urlopen('http://www.cygnusgymnasium.nl/ftp_cg/roosters/infoweb/index.php?ref='+ref+'&id='+idn)
    html = response.read()
    return html


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
