#!/usr/bin/env python3


import os

from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from time import gmtime, strftime
#from werkzeug.utils import secure_filename

from ..models.world import User,Posts
# from ..src import ALLOWED_EXTENSIONS, allowed_file 

dratini = Blueprint('private',__name__,url_prefix='/private')

UPLOAD_FOLDER = '/Users/ahn.ch/Desktop/facebook_mock/app/run/src/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# @link.before_request
# def before_request():
#     g.username = None
#     if session['username']:
#         g.username = session['username']

@dratini.route('/account',methods=['GET','POST'])
def account():
    un = User(username=session['username'],password=session['password'])
    user_posts  = un.get_posts()
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if request.method == 'GET':
        try:
            return render_template('private/account.html',posts=user_posts)
        except TypeError:
            return render_template('private/account.html')
    elif request.method == 'POST':
        if request.form['posts_button'] == 'Post':
            content = request.form['post_text']
            un.make_post(content,time)
            return redirect('private/account')
        #FIXME
        elif request.form['posts_button'] == 'Delete':
            p = Posts()
            p.delete_post()
            return redirect('private/account')
        elif request.form['posts_button'] == 'Upload':
            return redirect('/save_file')
        else:
            pass
    else:
        pass

@dratini.route('/feed',methods=['GET','POST'])
def news_feed():
    un = User(username=session['username'],password=session['password'])
    if request.method == 'GET':
        every = un.get_every_post()
        return render_template('private/global.html',all_posts=every)
    elif request.method == 'POST':
        if request.form['hashtag'][0] == '#':
            query = un.search_hashtags(request.form['hashtag'])
            every = un.get_every_post()
            return render_template('private/global.html',all_posts=every,hash_posts=query)
        # elif request.form['submit'] == 'Upload':
        #     if allowed_file():
        #         return 
        #     except:
        #         pass
        # else:
        #     return render_template('private/global.html',message='You can only search HashTags')