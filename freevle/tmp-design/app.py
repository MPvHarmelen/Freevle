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

@app.route('/login/', methods=['POST'])
def login():
    title = 'Schoolklimaat | Cygnus Gymnasium'
    return redirect(url_for('dashboard'))

@app.route('/login/', methods=['GET'])
def showlogin():
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
