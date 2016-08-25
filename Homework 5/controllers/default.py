# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time

def index():
    #Determining if user is logged in
    count = 1
    if auth.user_id is None:
        count = 0
    #creating a unique board
    draft_id = gluon_utils.web2py_uuid()
    board_id = id
    return dict(draft_id=draft_id, count = count, board_id= board_id)

#for board messages
@auth.requires_signature()
def add_msg():
    db.board.update_or_insert((db.board.message_id == request.vars.msg_id),
            message_id=request.vars.msg_id,
            message_content=request.vars.msg,
            is_draft=json.loads(request.vars.is_draft))
    return "ok"

#for the loading boards
def load_messages():
    """Loads all messages for the user."""
    rows = db(db.board).select()
    # d = {}
    # for r in rows:
    #     d[r.message_id] = {'message_content': r.message_content}
    d = {r.message_id: {'message_content': r.message_content,
                        'is_draft': r.is_draft}
         for r in rows}
    return response.json(dict(msg_dict=d))


def view_post():
    #select the board that the post is associated with
    board = db(db.board.message_id == request.vars.msg_id).select()
    board_title = board[0].message_content
    board_id = None

    draft = gluon_utils.web2py_uuid()
    try:
        board_id = board[0].id

    #throw error if bad id, sent back to index page
    except IndexError:
        print "bad board"
        redirect(URL('default', 'index'))

    #posts_id = db(db.post.board_id == board_id).select()

    #determining if the user is logged in or not
    count = 1
    if auth.user_id is None:
        count = 0
    return dict(count = count, draft= draft, board_id=board_id, board_title=board_title)

#adding post
@auth.requires_signature()
def add_post():
    db.post.update_or_insert((db.post.post_id == request.vars.msg_id),
            post_id=request.vars.msg_id,
            board_id = request.vars.board_id,
            post_content=request.vars.msg,
            is_post_draft=json.loads(request.vars.is_post_draft))
    return "ok"

#loading post
def load_post():
    """Loads all messages for the user."""
    rows = db(db.post.board_id == request.vars.board_id).select()
    # d = {}
    # for r in rows:
    #     d[r.post_id] = {'post_content': r.post_content}
    d = {r.post_id: {'post_content': r.post_content,
                        'is_post_draft': r.is_post_draft,
                        'board_id': r.board_id,
                        'creator' : r.creator,
                     }
         for r in rows}
    return response.json(dict(post_dict=d))

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


