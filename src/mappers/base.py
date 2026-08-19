from collections.abc import Sequence

from pydantic import BaseModel


class DataMapper[ModelT, SchemaT: BaseModel]:
    db_model: type[ModelT]
    schema: type[SchemaT]

    def to_schema(self, orm_obj: ModelT) -> SchemaT:
        return self.schema.model_validate(
            orm_obj,
            from_attributes=True,
        )

    def to_schema_list(self, orm_list: Sequence[ModelT]) -> list[SchemaT]:
        return [self.to_schema(item) for item in orm_list]

    def to_orm(self, schema_obj: BaseModel) -> ModelT:
        return self.db_model(
            **schema_obj.model_dump(exclude_none=True)
        )
