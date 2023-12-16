"""Seed file to make sample data for users db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Post.query.delete()

# Add users
stamos = User(first_name='John', last_name='Stamos', image_url="https://pyxis.nymag.com/v1/imgs/283/746/709a300b26da59b4950aa2dfeec3d0a03f-27-john-stamos-silo.rvertical.w330.png")
hader = User(first_name='Bill', last_name='Hader', image_url="https://variety.com/wp-content/uploads/2022/12/Bill_Hader-1.png")
reynolds = User(first_name='Ryan', last_name='Reynolds', image_url="https://static.wixstatic.com/media/e59907_a366bf5ce7ef48a98af5b99e46d3404f~mv2.png/v1/fill/w_392,h_392,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/Image-empty-state.png")
jackman = User(first_name='Hugh', last_name='Jackman', image_url="https://variety.com/wp-content/uploads/2020/12/Hugh_Jackman.png")
carrey = User(first_name='Jim', last_name='Carrey', image_url="https://celebrityendorsers.com/wp-content/uploads/2022/08/Jim-Carrey.png")
freeman = User(first_name='Morgan', last_name='Freeman', image_url="https://vz.cnwimg.com/thumb-900x/wp-content/uploads/2020/01/Morgan-Freeman.jpg")
hepburn = User(first_name='Audrey', last_name='Hepburn', image_url="https://www.pngmart.com/files/22/Audrey-Hepburn-PNG-Transparent.png")

#Add Posts
u1p1 = Post(title="User 1 Post 1", content="PlsWork", user=stamos)
u1p2 = Post(title="User 1 Post 2", content="PlsWork2", user=stamos)
u1p3 = Post(title="User 1 Post 3", content="PlsWork3", user=stamos)
u2p1 = Post(title="User 2 Post 1", content="PlsWork", user=hader)
u2p2 = Post(title="User 2 Post 2", content="PlsWork2", user=hader)
u2p3 = Post(title="User 2 Post 3", content="PlsWork3", user=hader)
u3p1 = Post(title="User 3 Post 1", content="PlsWork", user=reynolds)
u3p2 = Post(title="User 3 Post 2", content="PlsWork2", user=reynolds)
u3p3 = Post(title="User 3 Post 3", content="PlsWork3", user=reynolds)
u4p1 = Post(title="User 4 Post 1", content="PlsWork", user=jackman)
u4p2 = Post(title="User 4 Post 2", content="PlsWork2", user=jackman)
u4p3 = Post(title="User 4 Post 3", content="PlsWork3", user=jackman)
u5p1 = Post(title="User 5 Post 1", content="PlsWork", user=carrey)
u5p2 = Post(title="User 5 Post 2", content="PlsWork2", user=carrey)
u5p3 = Post(title="User 5 Post 3", content="PlsWork3", user=carrey)
u6p1 = Post(title="User 6 Post 1", content="PlsWork", user=freeman)
u6p2 = Post(title="User 6 Post 2", content="PlsWork2", user=freeman)
u6p3 = Post(title="User 6 Post 3", content="PlsWork3", user=freeman)
u7p1 = Post(title="User 7 Post 1", content="PlsWork", user=hepburn)
u7p2 = Post(title="User 7 Post 2", content="PlsWork2", user=hepburn)
u7p3 = Post(title="User 7 Post 3", content="PlsWork3", user=hepburn)

# Add new objects to session, so they'll persist
db.session.add_all([stamos,hader,reynolds,jackman,carrey,freeman,hepburn])
# db.session.add (stamos)
# db.session.add (hader)
# db.session.add (reynolds)
# db.session.add (jackman)
# db.session.add (carrey)
# db.session.add (freeman)
# db.session.add (hepburn)
db.session.add_all([u1p1,u2p1,u3p1,u4p1,u5p1,u6p1,u7p1])
db.session.add_all([u1p2,u2p2,u3p2,u4p2,u5p2,u6p2,u7p2])
db.session.add_all([u1p3,u2p3,u3p3,u4p3,u5p3,u6p3,u7p3])

# Commit--otherwise, this never gets saved!
db.session.commit()