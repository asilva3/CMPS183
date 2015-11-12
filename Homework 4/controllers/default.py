# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

IMAGE_URLS = [
    'https://storage.googleapis.com/lucadealfaro-share/img1.jpg',
    'https://storage.googleapis.com/lucadealfaro-share/img2.jpg',
    'https://storage.googleapis.com/lucadealfaro-share/img3.jpg',
    'https://storage.googleapis.com/lucadealfaro-share/img4.jpg',
]

def index():

    def get_thumbs(img_idx):
        if not auth.user_id:
            return None
        r = db((db.rating.user_id == auth.user_id) & (db.rating.image_id == img_idx)).select().first()
        return None if r is None else r.thumbs

    image_list = []
    for i, img_url in enumerate(IMAGE_URLS):
        image_list.append(dict(
            url=img_url,
            thumbs = get_thumbs(i),
            id=i,
        ))
    return dict(image_list=image_list)

@auth.requires_signature()
def vote():
    picid = int(request.vars.picid)
    thumbs = request.vars.thumbs
    db.rating.update_or_insert(
        ((db.rating.image_id == picid) & (db.rating.user_id == auth.user_id)),
        image_id = picid,
        user_id = auth.user_id,
        thumbs = thumbs
    )
    return "ok"


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


