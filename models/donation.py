from init import db, Model


class Donation(Model, db.Model):
    __tablename__ = "donations"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), index=True)

    def __init__(self, donor_id, image_id, amount):
        self.amount = amount
        self.donor_id = donor_id
        self.image_id = image_id
