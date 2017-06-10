from application import db

class Metadata(db.Model):
    __tablename__ = 'metadata'
    id = db.Column(db.Integer, primary_key=True)
    docid = db.Column(db.String(64), index=True, unique=False)
    recordid = db.Column(db.String(512), index=False, unique=False)
    oclc = db.Column(db.String(512), index=False, unique=False)
    locnum = db.Column(db.String(512), index=False, unique=False)
    author = db.Column(db.String(512), index=False, unique=False)
    imprint = db.Column(db.String(512), index=False, unique=False)
    date = db.Column(db.String(512), index=False, unique=False)
    birthdate = db.Column(db.String(512), index=False, unique=False)
    firstpub = db.Column(db.String(512), index=False, unique=False)
    enumcron = db.Column(db.String(512), index=False, unique=False)
    subjects = db.Column(db.String(512), index=False, unique=False)
    title = db.Column(db.String(512), index=False, unique=False)
    nationality = db.Column(db.String(512), index=False, unique=False)
    gender = db.Column(db.String(512), index=False, unique=False)
    genretags = db.Column(db.String(512), index=False, unique=False)
    

class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey("metadata.id"))
    token = db.Column(db.String(128), index=True, unique=False)
    term_id = db.Column(db.Integer, db.ForeignKey("terms.id"))
    pos = db.Column(db.String(128), index=True, unique=False)
    stem = db.Column(db.String(128), index=True, unique=False)
    lemma = db.Column(db.String(128), index=True, unique=False)


class Terms(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(128), index=True, unique=True)
    oed_first = db.Column(db.String(128), index=True, unique=False)
    oed_last = db.Column(db.String(128), index=True, unique=False)
    oed_list = db.Column(db.String(128), index=True, unique=False)
    dictcom = db.Column(db.String(128), index=True, unique=False)

class Counts(db.Model):
    __tablename__ = 'counts'
    counts_id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.String(64), index=True, unique=False)
    work_id = db.Column(db.Integer, db.ForeignKey("metadata.id"))
    type = db.Column(db.String(64), index=True, unique=False)
    type_count = db.Column(db.Integer)

class Genres(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey("metadata.id"))
    genre = db.Column(db.String(128), index=True)
