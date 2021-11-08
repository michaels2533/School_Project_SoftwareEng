from app import create_app,db
from app.Model.models import ElectiveTag, User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if ElectiveTag.query.count() == 0:
        eTag = ['AI', 'Machine Learning', 'Neural Networks', 'Database Systems', 'Security']
        for e in eTag:
            db.session.add(ElectiveTag(name = e))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)


