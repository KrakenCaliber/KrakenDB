from sqlmodel import SQLModel, Session, select, create_engine
from typing import Any, List, Optional, Type
from pathlib import Path
import click


class KrakenDB:
    def __init__(
        self, 
        app_name: str, 
        db_name: str
    ) -> None:
        self.base = Path(click.get_app_dir(app_name)).resolve()
        self.base.mkdir(parents=True, exist_ok=True)
        self.db_path = self.base / f"{db_name}.duckdb"
        self.engine = create_engine(f"duckdb:///{self.db_path}")
        SQLModel.metadata.create_all(self.engine)


    def create(
        self, 
        obj: SQLModel | List[SQLModel]
    ) -> Optional[SQLModel] | List[SQLModel]:
        with Session(self.engine) as session:
            if isinstance(obj, SQLModel):
                session.add(obj)
                session.commit()
                session.refresh(obj)
            elif isinstance(obj, List[SQLModel]):
                session.add_all(obj)
                session.commit()
                for o in obj:
                    session.refresh(o)
            else:
                raise ValueError("obj must be a SQLModel or a list of SQLModels: SQLModel | List[SQLModel]")
        return obj


    def read(
        self, 
        obj_type: Type[SQLModel], 
        all: Optional[bool] = True
    ) -> Optional[SQLModel] | List[SQLModel]:
        with Session(self.engine) as session:
            if all:
                return session.exec(select(obj_type)).all()
            else:
                return session.exec(select(obj_type)).first()[0]


    def read_by(
        self, 
        obj_type: Type[SQLModel], 
        obj_field: Any, 
        obj_value: Any, 
        all: Optional[bool] = True
    ) -> Optional[SQLModel] | List[SQLModel]:
        with Session(self.engine) as session:
            if all:
                obj = session.exec(select(obj_type).where(obj_field == obj_value)).all()
            else:
                obj = session.exec(select(obj_type).where(obj_field == obj_value)).first()[0]
        return obj


    def update(self, obj_type: Type[SQLModel], obj_field: Any, obj_value: Any, **kwargs) -> SQLModel:
        with Session(self.engine) as session:
            obj = session.exec(select(obj_type).where(obj_field == obj_value)).first()
            for key, value in kwargs.items():
                setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
        return obj


    def delete(self, obj: SQLModel | List[SQLModel]):
        with Session(self.engine) as session:
            if isinstance(obj, SQLModel):
                session.delete(obj)
            elif isinstance(obj, List[SQLModel]):
                for o in obj:
                    session.delete(o)
            session.commit()


    def erase_database(self):
        self.db_path.unlink()
        self.base.rmdir()

