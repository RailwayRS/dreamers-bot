from sqlalchemy import ForeignKey, String, Integer, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum

class Base(DeclarativeBase):
    pass

class Role(enum.Enum):
    DREAMER = "dreamer"
    EXECUTOR = "executor"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True)
    role: Mapped[Role] = mapped_column(Enum(Role))
    balance: Mapped[int] = mapped_column(default=0)
    
    # Связь с задачами (Task)
    tasks = relationship("Task", back_populates="creator")
    # Связь с откликами (Response)
    responses = relationship("Response", back_populates="user")

class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column(String(16))
    title: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(String(4096))

class AppStatus(enum.StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(String(1024))
    status: Mapped[AppStatus] = mapped_column(Enum(AppStatus), default=AppStatus.PENDING)

# Модели для задач (Task) и откликов (Response)
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship("User", back_populates="tasks")  # Связь с пользователем, создавшим задачу

    # Связь с откликами
    responses = relationship("Response", back_populates="task")

class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task: Mapped["Task"] = relationship("Task", back_populates="responses")  # Связь с задачей
    user: Mapped["User"] = relationship("User", back_populates="responses")  # Связь с пользователем, который откликнулся

