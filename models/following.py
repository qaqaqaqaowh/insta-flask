from init import db, Model


class Following(Model, db.Model):
    __tablename__ = "followings"
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    accepted = db.Column(db.Boolean)

    def __init__(self, user_id, follower_id, accepted=None):
        if accepted == None:
            accepted = True
        self.accepted = accepted
        self.user_id = user_id
        self.follower_id = follower_id
