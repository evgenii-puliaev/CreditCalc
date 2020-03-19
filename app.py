from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def main(name=None):
    return render_template('index.html', name=name)


@app.route('/count')
@app.route('/<name>/count')
def count(name=None):
    return render_template('count.html', name=name)


@app.route('/history')
@app.route('/<name>/history')
def history(name=None):
    return render_template('history.html', name=name)


@app.route('/login')
def login(name=None):
    return render_template('login.html', name=name)


if __name__ == '__main__':
    app.run()
