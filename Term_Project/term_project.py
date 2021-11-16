from app import create_app,db
from app.Model.models import Tag
from app.Model.models import ElectiveTag, ResearchTopicTag, User, ProgramLanguageTag

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
        tags = ['Data Structures','Machine Learning', 'High Performance Computing', 'Web Development', 'Computer Achitecture']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()

    if ElectiveTag.query.count() == 0:
        eTag = ['AI', 'Machine Learning', 'Neural Networks', 'Database Systems', 'Security']
        for e in eTag:
            db.session.add(ElectiveTag(name = e))
        db.session.commit()

    if ProgramLanguageTag.query.count() == 0:
        pTag = ['Python', 'C/C++', 'C#','Java', 'JavaScript', 'Golang']
        for p in pTag:
            db.session.add(ProgramLanguageTag(name = p))
        db.session.commit()

    if ResearchTopicTag.query.count() == 0:
        rTag =  ['Data Structures', 'Machine Learning', 'High Perfomance Computing', 'Web Development', 'Computer Architecture']
        for r in rTag:
            db.session.add(ResearchTopicTag(name = r))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)


