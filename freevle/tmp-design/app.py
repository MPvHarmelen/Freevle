import requests
from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Cygnus Gymnasium'
    return render_template('index.html', title=title)


@app.route('/<name>/', methods=['POST','GET'])
def page(name):
    title = name.capitalize() + ' | Cygnus Gymnasium'
    page = name + '.html'
    return render_template(page, title=title)


@app.route('/intern/')
def intern():
    title = 'Interne Informatie | Cygnus Gymnasium'
    page = 'intern.html'
    return render_template(page, title=title, loggedin=True)


@app.route('/info/<a>/<b>/')
def aboutpage(a,b):
    title = 'Schoolklimaat | Cygnus Gymnasium'
    return render_template('schoolklimaat.html', title=title)


@app.route('/nieuws/archief/')
def newsarchive():
    title = 'Archief Nieuws | Cygnus Gymnasium'
    return render_template('nieuwsarchief.html', title=title)

@app.route('/nieuws/<a>/<b>/<c>/')
def newsmessage(a,b,c):
    title = 'Opening Schip | Nieuws | Cygnus Gymnasium'
    return render_template('nieuwsbericht.html', title=title)


@app.route('/fotos/<a>/<b>/')
def photoalbum(a,b):
    title = 'Jihlava | Foto\'s | Cygnus Gymnasium'
    return render_template('fotoalbum.html', title=title)

@app.route('/fotos/archief/')
def photosarchive():
    title = 'Archief Foto\'s | Cygnus Gymnasium'
    return render_template('fotosarchief.html', title=title)


@app.route('/login/', methods=['POST'])
def login():
    return redirect(url_for('intern'))


@app.route('/login/', methods=['GET'])
def showlogin():
    title = 'Login | Cygnus Gymnasium'
    return render_template('login.html', title=title)


@app.route('/zoek/autocompletion/', methods=['POST'])
def results():
    return render_template('autocompletion.html')


@app.route('/getrooster/<ref>/<id_user>/')
def getrooster(ref,id_user):
    rooster_url = 'http://www.cygnusgymnasium.nl/ftp_cg/roosters/infoweb/index.php?ref={0}&id={1}'.format(ref, id_user)
    response = requests.get(rooster_url)
    html = response.text
    return html

@app.route('/rooster/<ref>/<id_user>/')
def rooster(ref,id_user):
    roostername = 'Floris Jansen'
    return render_template('rooster.html', ref=ref, id_user=id_user, roostername=roostername)


@app.route('/admin/')
def admindashboard():
    title = 'Admin | Cygnus Gymnasium'
    return render_template('admin/dashboard.html', title=title)

@app.route('/admin/pages/')
def adminpages():
    title = 'Pagina\'s | Admin | Cygnus Gymnasium'
    return render_template('admin/pages.html', title=title)

@app.route('/admin/pages/editor/')
def adminpageseditor():
    title = 'Gebouw | Pagina\'s | Admin | Cygnus Gymnasium'
    return render_template('admin/pages-editor.html', title=title)

@app.route('/admin/news/')
def adminnews():
    title = 'Nieuws | Admin | Cygnus Gymnasium'
    return render_template('admin/news.html', title=title)

@app.route('/admin/news/editor/')
def adminnewseditor():
    title = 'Opening Schip | Nieuws | Admin | Cygnus Gymnasium'
    return render_template('admin/news-editor.html', title=title)

@app.route('/admin/soon/')
def adminsoon():
    title = 'Binnenkort | Admin | Cygnus Gymnasium'
    return render_template('admin/soon.html', title=title)

@app.route('/admin/soon/editor/')
def adminsooneditor():
    title = 'Open dag | Binnenkort | Admin | Cygnus Gymnasium'
    return render_template('admin/soon-editor.html', title=title)

@app.route('/admin/photos/')
def adminphotos():
    title = 'Foto\'s | Admin | Cygnus Gymnasium'
    return render_template('admin/photos.html', title=title)

@app.route('/admin/photos/editor/')
def adminphotoseditor():
    title = 'Jihlava | Foto\'s | Admin | Cygnus Gymnasium'
    return render_template('admin/photos-editor.html', title=title)

@app.route('/admin/frontpage/')
def adminfrontpage():
    title = 'Voorpagina | Admin | Cygnus Gymnasium'
    return render_template('admin/frontpage.html', title=title)

@app.route('/admin/users/')
def adminusers():
    title = 'Gebruikers | Admin | Cygnus Gymnasium'
    return render_template('admin/users.html', title=title)

@app.route('/admin/users/editor/')
def adminuserseditor():
    title = 'Jan Modaal | Gebruikers | Admin | Cygnus Gymnasium'
    return render_template('admin/users-editor.html', title=title)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
