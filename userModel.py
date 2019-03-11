from main import db,bcrypt


class AuthenticationModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    fullName = db.Column(db.String(120),nullable=False,unique=True)
    password = db.Column(db.String(),nullable=True)
    email = db.Column(db.String(50),nullable=False,unique=True)

    # CREATE
    def createUser(self):
        db.session.add(self)
        db.session.commit()


    # read
    @classmethod
    def fetch_all(cls,email,password):
        records = AuthenticationModel.query.filter_by(email=email,password=password)
        if records.first():
            return True
        else:
            return False

    #check email
    @classmethod
    def checkEmailExist(cls,email):
        records = AuthenticationModel.query.filter_by(email=email)
        if records.first():
            return True
        else:
            return False

    # checking password
    @classmethod
    def userpass(cls,email,password):
        print(password)
        record = AuthenticationModel.query.filter_by(email=email).first()


        print(record.password)
        print(record.id)
        print(record.email)

        if record and bcrypt.check_password_hash(record.password,password):
            return True
        else:
            return False

    @classmethod
    def fetch_user_id(cls,email):
        return cls.query.filter_by(email=email).first().id


        # if record and bcrypt.check_password_hash(password,password):
        #     return  True
        #     # if password == record.password:
        #     #     return True
        #     # else:
        #     #     return False
        # else:
        #     return False