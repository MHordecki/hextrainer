from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty()

class Deck(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    owner = db.ReferenceProperty(User)

    origin = db.SelfReferenceProperty()

    created = db.DateTimeProperty()

class DeckUser(db.Model):
    deck = db.ReferenceProperty(Deck)
    user = db.ReferenceProperty(User)
    
    metadata = db.TextProperty()

class Card(db.Model):
    deck = db.ReferenceProperty(Deck)
    data = db.TextProperty()

    origin = db.SelfReferenceProperty()

