from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Строка подключения к базе данных PostgreSQL
DATABASE_URL = 'postgresql://postgres:KUrQtCQmJznCNXnpOfSeiXlgHZfgExpK@postgres.railway.internal:5432/railway'

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL, echo=True)

# Создание сессии для работы с базой данных
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание сессии
session = Session()

# Проверка соединения и создание всех таблиц, если их нет
Base.metadata.create_all(bind=engine)
from models import User, Role, Task

# Создание нового пользователя
new_user = User(tg_id=12345, role=Role.DREAMER)

# Добавляем нового пользователя в сессию
session.add(new_user)
session.commit()

# Создание задачи для этого пользователя
new_task = Task(description="Создать новое событие", creator=new_user)

# Добавляем задачу в сессию
session.add(new_task)
session.commit()

print("Пользователь и задача добавлены в базу данных!")

# Проверка таблиц в базе данных
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Таблицы в базе данных:", tables)

# Пример добавления данных
from models import User, Role, Task

# Создание нового пользователя
new_user = User(tg_id=12345, role=Role.DREAMER)

# Добавляем нового пользователя в сессию
session.add(new_user)
session.commit()

# Создание задачи для этого пользователя
new_task = Task(description="Создать новое событие", creator=new_user)

# Добавляем задачу в сессию
session.add(new_task)
session.commit()

print("Пользователь и задача добавлены в базу данных!")

# Закрытие сессии
session.close()
