### Dependencies:

    requests
    pydantic
    fastapi
    sqlalchemy
    sqladmin
    uvicorn


### database.py

```py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine(
    "sqlite:///example.db",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(engine)  # Create tables
```

### main.py

```py
from fastapi import FastAPI, Depends
from sqladmin import Admin, ModelAdmin
from sqlalchemy.orm import Session
from database import engine, User, SessionLocal

app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelAdmin, model=User):
    column_list = [User.id, User.name]


admin.register_model(UserAdmin)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get('/')
async def get_users(db: Session = Depends(get_db)): return db.query(User).all()
```

### Endpoints

`localhost:8000/docs` - get all users

`localhost:8000/admin` - admin panel itself
