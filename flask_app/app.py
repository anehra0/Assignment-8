from flask import Flask, render_template, request, redirect, url_for
import DAL
import os

app = Flask(__name__)

# Ensure DB/table exist. Use before_first_request if available; otherwise
# call init directly (some older Flask versions/environment proxies may not
# expose the decorator at import-time in this environment).
if hasattr(app, 'before_first_request'):
    @app.before_first_request
    def ensure_db():
        DAL.init_db()
else:
    # Fallback: initialize now
    DAL.init_db()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/projects')
def projects():
    # Read projects from the database and pass to the template
    projects = DAL.get_all_projects()
    return render_template('projects.html', projects=projects)


@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image = request.form.get('image', '').strip()

        # Basic server-side validation
        if title:
            DAL.save_project(title, description, image)
            return redirect(url_for('projects'))
        else:
            # If title is missing, re-render form (could add flash messages)
            return render_template('add_project.html', error='Title is required', title=title, description=description, image=image)

    # GET -> show the add-project form
    return render_template('add_project.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


if __name__ == "__main__":
    # Get host and port from environment variables, with defaults
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host=host, port=port, debug=debug)