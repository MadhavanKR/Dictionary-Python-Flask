from app import db,loginManager,current_app;
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash;
from flask_login import UserMixin;

UserWordLink = db.Table('UserWordLink',
                     db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                     db.Column('word_id',db.Integer,db.ForeignKey('words.id'))
                     );
    

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True);
    username = db.Column(db.String, unique = True, index = True);
    email = db.Column(db.String, unique = True, index = True);
    password_hash = db.Column(db.String);
    #words = db.relationship('Words',secondary=UserWordLink);
    def set_password(self,password):
        self.password_hash = generate_password_hash(password);
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password);
    
    def __repr__(self):
        return "<User {}>".format(self.username);

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True);
    word = db.Column(db.String, unique = True, index = True);
    meaning = db.Column(db.String);
    users = db.relationship('User',secondary=UserWordLink,
                            backref=db.backref("words",lazy="dynamic"));
    
    def __repr__(self):
        return "<Word {}>".format(self.word);
    
    def is_following(self,user):
        users = self.users;
        for cur_user in users:
            if cur_user.id == user.id:
                return True;
        return False;
    
@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id));

