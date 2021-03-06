#-*- coding: UTF-8 -*-
from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Permission:
    
    '''权限设置'''
    
    ADMINISTER = 0x01
    COMMIT = 0x02
    QUERY = 0x04

class ComName(db.Model):
    
    '''竞赛项目名称表'''
    
    __tablename__ = 'comname'
    id = db.Column(db.Integer, primary_key=True)
    com_name = db.Column(db.String(128), nullable=False)
    infos = db.relationship('ComInfo', backref='com_name', lazy='dynamic') 

    def __init__(self, com_name):
        self.com_name=com_name

    def __repr__(self):
        return '<ComName %r>' % self.com_name
        
class ComInfo(db.Model):

    '''竞赛信息表'''

    __tablename__ = 'cominfo'
    id = db.Column(db.Integer, primary_key=True)
    com_nid = db.Column(db.Integer, db.ForeignKey('comname.id'), nullable=False)
    pro_name = db.Column(db.String(128), nullable=True)
    com_level = db.Column(db.String(128), nullable=False)
    com_class = db.Column(db.String(128), nullable=False)
    com_sid = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    com_tid = db.Column(db.Integer, db.ForeignKey('comteam.id'), nullable=True)
    tea1_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    tea2_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    com_time = db.Column(db.String(128), nullable=False)
    com_org = db.Column(db.String(128), nullable=False)
    is_team  = db.Column(db.Integer, nullable=False)

    def __init__(self, pro_name, com_level, com_class, com_sid, tea1_id, tea2_id, com_time, com_org, is_team):
        self.pro_name=pro_name
        self.com_level=com_level
        self.com_class=com_class
        self.com_org=com_org
        self.com_time = com_time
        self.com_sid = com_sid
        self.tea1_id=tea1_id
        self.tea2_id=tea2_id
        self.is_team = is_team
        
class ComTeam(db.Model):
    
    '''竞赛团队表'''
    
    __tablename__ = 'comteam'
    id = db.Column(db.Integer, primary_key=True)
    stu1_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    stu2_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    stu3_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    stu4_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    stu5_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    stu6_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    stu7_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    stu8_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    stu9_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __init__(self):
        pass

class Student(db.Model):
    
    '''学生表'''
    
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    stu_id = db.Column(db.String(128), nullable=False, unique=True)
    stu_name = db.Column(db.String(128), nullable=False)
    stu_academy = db.Column(db.Integer, db.ForeignKey('acachemys.id'), nullable=False)
    stu_major = db.Column(db.String(128), nullable=False)
    stu_class = db.Column(db.String(128), nullable=False)
    
    def __init__(self, stu_id, stu_name, stu_major, stu_class):
        self.stu_id = stu_id
        self.stu_name = stu_name
        self.stu_major = stu_major
        self.stu_class = stu_class
       
    def __repr__(self):
        return '<Student %r>' % self.stu_id

class Teacher(db.Model):
    
    '''教师表'''
    
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    tea_id = db.Column(db.String(128), nullable=False, unique=True)
    tea_name = db.Column(db.String(128), nullable=False)
    tea_unit = db.Column(db.String(128), nullable=False)

    def __init__(self, tea_id, tea_name, tea_unit):
        self.tea_id=tea_id
        self.tea_name=tea_name
        self.tea_unit=tea_unit

    def __repr__(self):
        return '<Teacher %r>' % self.tea_name

class Acachemy(db.Model):
    
    '''学院表'''
    
    __tablename__ = 'acachemys'
    id = db.Column(db.Integer, primary_key=True)
    aca_name = db.Column(db.String(128), nullable=False, unique=True)
    stus = db.relationship('Student', backref='acachemy', lazy='dynamic')
    
    def __init__(self, aca_name):
        self.aca_name=aca_name
    
    def __repr__(self):
        return '<Acachemy %r>' % self.aca_name

class User(UserMixin, db.Model):
    
    '''用户表'''
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, unique=True)
    user_name = db.Column(db.String(128), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return '<User %r>' % self.user_id

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions ) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissons):
        return False

    def is_administrator(self):
        return False

class Role(db.Model):
    
    '''角色表'''
    
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.role_name

    def __init__(self, role_name):
        self.role_name = role_name
    
    @staticmethod
    def insert_roles():
        roles= {
            u'教师': (0xff),
            u'学院': (0xff),
            u'管理员': (0xff)
        }
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
                role.permissions = roles[r]
                db.session.add(role)
        db.session.commit()


        
class Patent(db.Model):
    __tablename__ = 'patent'
    id = db.Column(db.Integer,primary_key=True)
    pea_type = db.Column(db.String(128),nullable=False)
    pea_name = db.Column(db.String(64),nullable=False)
    pea_inventor = db.Column(db.String(64),nullable=False)
    pea_filingdate = db.Column(db.Date,nullable=False)
    pea_patentee = db.Column(db.String(64),nullable=False)
    pea_announcement = db.Column(db.Date,nullable=False)

    def __init__(self,pea_type, pea_name, pea_inventor, pea_filingdate, pea_patentee, pea_announcement ):
        self.pea_type = pea_type
        self.pea_name = pea_name
        self.pea_inventor = pea_inventor
        self.pea_filingdate = pea_filingdate
        self.pea_patentee = pea_patentee
        self.pea_announcement = pea_announcement

    def __repr__(self):
        return '<patent %s>' % self.pea_name
