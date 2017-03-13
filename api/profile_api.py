from flask import Blueprint
from flask import request
from flask import render_template
from flask import url_for
from flask import jsonify
from flask import send_file
from werkzeug import secure_filename
import os
from models.profile import Profile

import time
import random

from app import app
from app import Session

mod = Blueprint('profile_api', __name__)


@mod.route('/profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'GET':
        submit_url = url_for('.user_profile', _method='POST')
        return render_template('profile_form.html', submit_url=submit_url)
    else:
        session = Session()
        try:
            form = request.form
            username = form['username']

            if username_already_used(session, username):
                return "Username %s is already used. Click on <a href='%s'>Back</a> to go back" \
                       % (username, url_for(user_profile))

            prof = Profile()
            prof.userid = gen_random_uid()
            prof.username = username
            prof.created = str(int(time.time() * 1000))
            prof.firstname = form['firstname']
            prof.lastname = form['lastname']
            prof.age = form['age']
            prof.bio = form['biography']
            prof.gender = form['gender']

            file = request.files['image']
            img_filename = secure_filename(file.filename)
            prof.image = img_filename

            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], prof.userid + '_' + img_filename))
            except Exception:
                pass

            session.add(prof)
            session.commit()
        except Exception:
            session.rollback()

        return "Profile submitted. Click on <a href='%s'>Back</a> to go back" % url_for('.user_profile')


@mod.route('/profiles', methods=['GET', 'POST'])
def user_profiles():
    session = Session()
    try:
        profiles = get_user_profiles(session)

        if request.method == 'POST' and request.content_type == 'application/json':
            data = [{'userid': x.userid, 'username': x.username} for x in profiles]
            return jsonify({'users': data})
        else:
            return render_template('user_profiles.html', profiles=profiles)
    except Exception as ex:
        session.rollback()

        raise ex


@mod.route('/profile/<userid>', methods=['GET', 'POST'])
def detail_user_profile(userid):
    session = Session()
    try:
        prof = get_detail_user_profile(session, userid)

        if not prof:
            return "User with userid %s does not exist." % userid

        if request.method == 'POST' and request.content_type == 'application/json':
            data = {
                'userid': prof.userid,
                'username': prof.username,
                'firstname': prof.firstname,
                'lastname': prof.lastname,
                'image': prof.image,
                'gender': prof.gender,
                'age': prof.age,
                'profile_created_on': prof.created
            }
            return jsonify(data)
        else:
            return render_template('detail_user_profile.html', profile=prof,
                                   img_link=url_for('.profile_image', userid=prof.userid))
    except Exception as ex:
        session.rollback()
        raise ex


@mod.route('/profile/image/<userid>', methods=['GET'])
def profile_image(userid):
    session = Session()
    try:
        prof = get_detail_user_profile(session, userid)

        fp = os.path.join(app.config['UPLOAD_FOLDER'], prof.userid + '_' + prof.image)
        return send_file(fp, mimetype='image/png')
    except Exception as ex:
        session.rollback()

        raise ex


def gen_random_uid():
    s1 = str(random.randint(0, 100000))
    s2 = str(int(time.time()))

    return s1 + s2


def get_user_profiles(session):
    return session.query(Profile).all()


def get_detail_user_profile(session, userid):
    return session.query(Profile).filter(Profile.userid == userid).first()


def username_already_used(session, username):
    return session.query(Profile).filter(Profile.username == username).first() is not None
