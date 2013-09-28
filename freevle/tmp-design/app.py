from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html', title=title, index=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
