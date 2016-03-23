#! -*- coding:utf8 -*-

'''
Prerequisite:
pip install sqlalchemy
'''
import re
import sys

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, validates

reload(sys)
sys.setdefaultencoding('utf8')

USERNAME_REG = re.compile('[a-zA-Z]+[a-zA-Z_\-\.]*$')

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    # Here we define columns for the table user
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 报警系统里的用户名
    name = Column(String(250), nullable=False, unique=True)
    # 用户介绍
    intro = Column(String(1024), default="")
    # 报警系统里登记的邮箱
    email = Column(String(250), nullable=False)
    # 报警系统里登记的电话
    phone = Column(String(250), nullable=False)

    @validates('email')
    def validate_email(self, key, value):
        assert '@' in value, "email should be an valid email address"
        return value

    @validates('name')
    def validate_name(self, key, value):
        assert USERNAME_REG.match(value), 'name could only contains "a-zA-Z_-"'
        return value

    def m_dict(self):
        return {
            "name": self.name,
            "email": self.email or "",
            "phone": self.phone or "",
            "empid": self.empid,
        }

   def __repr__(self):
       return '<User %r>' % self.name

    def __unicode__(self):
        return self.name


class Group(db.Model):
    __tablename__ = 'group'
    # Here we define columns for the table group
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 组名
    name = Column(String(250), nullable=False, unique=True)
    # 组介绍
    intro = Column(String(1024), default="")
    # 值周方式
    period = Column(Integer, default=7)
    # 组管理员
    admin_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    admin = relationship(User)

    def m_dict(self):
        return {
            "name": self.name,
            "intro": self.intro or "",
            "admin": self.admin.name or "",
        }

   def __repr__(self):
       return '<Group %r>' % self.name

    def __unicode__(self):
        return self.name


class RelGroupUser(db.Model):
    __tablename__ = 'rel_group_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    group = relationship(Group)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    # 值日天数
    period = Column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint('group_id', 'user_id', name="gid_uid"), )


"""
engine = create_engine(SQLITE_ADDR + 'monitor.db')
db.Model.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def get_session():
    return DBSession()

"""
