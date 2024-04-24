from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Base upload directory

class FileForm(FlaskForm):
    content_count = IntegerField('Number of Files', validators=[DataRequired()])
    folder_name = StringField('Folder Name', validators=[DataRequired()], default='default_folder')
    submit = SubmitField('Create Files')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()
    default_filenames = session.get('default_filenames', [])
    folder_name = session.get('folder_name', 'default_folder')  # Get default folder name from session
    form.folder_name.data = folder_name  # Pre-fill form with folder name from session

    if form.validate_on_submit():
        content_count = form.content_count.data
        filenames = request.form.getlist('filename')
        contents = request.form.getlist('content')
        folder_name = form.folder_name.data

        # Save filenames and folder name in the session
        session['default_filenames'] = filenames
        session['folder_name'] = folder_name

        # Create folder if specified by the user
        custom_folder_path = request.form.get('custom_folder_path')
        if custom_folder_path:
            full_folder_path = custom_folder_path
        else:
            full_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
            os.makedirs(full_folder_path, exist_ok=True)

        # Write files
        for content, filename in zip(contents, filenames):
            file_path = os.path.join(full_folder_path, filename + '.txt')
            with open(file_path, 'w') as file:
                file.write(content)

        # Success message
        success_message = f"Files successfully created in folder: {full_folder_path}"
        return render_template('index.html', form=form, success_message=success_message)

    return render_template('index.html', form=form, content_count=form.content_count.data if form.content_count.data else 0, default_filenames=default_filenames)

if __name__ == '__main__':
    app.run(debug=True)
