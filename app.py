from flask import Flask, render_template, url_for
app = Flask(__name__)

# Main home page
@app.route('/')
def index(name=None):
    return render_template('index.html', url_for=url_for)

# See every note for each class that can be accessed via their own page
# (through routing?)
@app.route('/notes')
def notes(name=None):
    return render_template('notes.html', url_for=url_for)

# See every due/completed assignment for each class (with cool metrics)
@app.route('/assignments')
def assignments(name=None):
    return render_template('assignments.html', url_for=url_for)

# See class enrollment and weekly schedule
@app.route('/calendar')
def calendar(name=None):
    return render_template('calendar.html', url_for=url_for)

# Access and add/update semesters
@app.route('/settings')
def settings(name=None):
    return render_template('settings.html', url_for=url_for)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['pragma'] = 'no-cache'
    return response
