
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, BigInteger, Enum
import enum
class Base(DeclarativeBase):
    pass
class Role(enum.Enum):
    DREAMER = "dreamer"
    EXECUTOR = "executor"
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    role: Mapped[Role] = mapped_column(Enum(Role))
    balance: Mapped[int] = mapped_column(default=0)
class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column(String(16))
    title: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(String(4096))
import enum
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column

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
