from typing import TypeVar, Generic, Type, Optional, Any, List, Union, Dict

from fastapi.encoders import jsonable_encoder
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session

from app.db.base_class import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model_type: Type[ModelType]):
        self.model_type = model_type

    def get(self, db: Session, /, id: Any) -> Optional[ModelType]:
        return db.query(self.model_type).filter(self.model_type.id == id).firs()

    def get_multi(
            self, db: Session, *,
            skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model_type).offset(skip).limit(limit).all()

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model_type).all()

    def create(self, db: Session, /, dto_schema: CreateSchemaType) -> ModelType:
        dto_obj_data = jsonable_encoder(dto_schema)
        entity = self.model_type(**dto_obj_data)
        db.add(entity)
        db.commit()
        db.refresh(entity)

        return entity

    def update(
            self, db: Session, /,
            entity: ModelType,
            dto_schema: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(dto_schema, Dict):
            update_data = dto_schema
        else:
            update_data = dto_schema.dict(exclude_unset=True)

        for field in jsonable_encoder(entity):
            if field in update_data:
                setattr(entity, field, update_data[field])

        db.add(entity)
        db.commit()
        db.refresh(entity)

        return entity

    @staticmethod
    def save_or_update(db: Session, /, entity: ModelType) -> ModelType:
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, /, id: Any) -> ModelType:
        entity = db.query(self.model_type).get(id)
        db.delete(entity)
        db.commit()
        return entity
