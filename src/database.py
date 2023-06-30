from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    streams = db.Column(db.Integer, nullable=False)
    tracks = db.Column(db.String(1000), nullable=False)
    genres = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    related_artists = db.relationship('RelatedArtist', backref='artist', lazy=True)

    def __repr__(self):
        return f"Artist('{self.name}', '{self.streams}', '{self.tracks}', '{self.genres}', '{self.created_at}', '{self.updated_at}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'streams': self.streams,
            'tracks': self.tracks,
            'genres': self.genres,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    