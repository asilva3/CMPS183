#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('board',
             Field('author', db.auth_user, default=auth.user_id),
             Field('message_content', 'text'),
             Field('is_draft', 'boolean', default=False),
             Field('message_id'), # To uniquely identify drafts and messages.
            )

db.define_table('post',
            Field('board_id', 'reference board'),
            Field('post_content', 'text'),
            Field('description', 'text'),
            Field('creator', 'integer', default=auth.user_id),
            Field('is_post_draft', 'boolean', default=False),
            Field('post_id'),
                )
