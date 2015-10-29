# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from datetime import date

def index():
    today = date.today()
    board_list = db().select(db.board.ALL, orderby='last_post desc')
    for i in board_list:
        board_id = i['id']
        i.board_count = db(db.posts.post_time >= today and db.posts.board_id == board_id).count()

    form = SQLFORM(db.board)
    if form.process().accepted:
        session.flash = T("New Board Added")
        redirect(URL('default', 'index'))
    return dict(board_list=board_list, form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def post():
    board = db.board(request.args(0))
    posts = db(db.posts.board_id == board.id).select(orderby='post_time desc')
    form = SQLFORM(db.posts)
    form.vars.board_id = board.id

    if form.process().accepted:
        session.flash = T("New Post Added")
       ###trying to set last post to the last created post time
        board.last_post = datetime.utcnow()
        board.update_record()
        redirect(URL('default', 'post', args=[board.id]))
    return dict(posts=posts, form=form, board=board)

def edit():
    post = db.posts(request.args(0))
    board = post.board_id
    if post is None:
        session.flash = T('No such post')
        redirect(URL('default', 'post'))
    form = SQLFORM(db.posts, record = post)
    back_button = A('Back', _class='btn btn-success', _href= URL('default', 'post', args=[post.board_id]))
    if form.process().accepted:
        session.flash = T('The data was edited')
        board.last_post = datetime.utcnow()
        board.update_record()
        redirect(URL('default', 'post', args=[post.board_id]))
    return dict(form=form, back_button=back_button)

def delete():
    post = db.posts(request.args(0))
    board = post.board_id
    if post is None:
        session.flash = T('No such post')
        redirect(URL('default', 'post'))
    db(db.posts.id == post.id).delete()
    session.flash = T('The data was deleted')
    redirect(URL('default', 'post', args=[board.id]))
    return dict(form=form)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


