from flask import render_template
from flask_login import current_user
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from gingerblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    prev_picture = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpeg':
        os.remove(prev_picture)
   
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset Your Password - Inkwell', recipients=[user.email])
    msg.body = f''' Hi {user.username}, 
To reset your Inkwell password, click the following link: 
{url_for('users.reset_token', token = token, _external = True)}

If you did not make this request, ignore this email and no changes will be made.
'''
    msg.html = render_template('email/reset_password.html', user=user, token=token)
    mail.send(msg)