### SQLite

#### database.py

```py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///./app/database.db'  # Might move it to env variables

engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

#### main.py

```py
from fastapi import FastAPI
from database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
```

#### router.py

```py
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### postgresql

[repo with tutorial](https://github.com/ianrufus/youtube/tree/main/fastapi-database)
