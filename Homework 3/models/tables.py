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
from datetime import datetime

db.define_table('board',
    Field('board_name'),
    Field('board_count', default=0),
    Field('last_post'),
                )

db.define_table('posts',
    Field('board_id', 'reference board'),
    Field('post_name', requires= IS_NOT_EMPTY()),
    Field('description', 'text'),
    Field('post_time', 'datetime'),
    Field('creator', 'integer', default=auth.user_id),
                )
db.posts.post_time.default = datetime.utcnow()
db.posts.board_id.readable = False
db.posts.board_id.writable = False
db.posts.post_time.writable = False
db.posts.post_time.readable = False
db.posts.id.readable = False
db.posts.creator.writable = False
db.posts.creator.readable = False
db.board.board_count.writable = False
db.board.board_count.readable = False
db.board.last_post.writable = False
db.board.last_post.readable = False