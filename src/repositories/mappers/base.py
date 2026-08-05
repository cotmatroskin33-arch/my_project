class DataMapper:
    db_model = None  # ORM модель
    schema = None  # Pydantic схема (по умолчанию)

    def to_schema(self, orm_obj, schema=None):
        """ORM → Pydantic"""
        if orm_obj is None:
            return None

        target_schema = schema or self.schema
        if target_schema is None:
            raise ValueError("Schema not set in mapper")

        return target_schema.model_validate(orm_obj, from_attributes=True)

    def to_schema_list(self, orm_list, schema=None):
        """Список ORM → список Pydantic"""
        return [self.to_schema(item, schema=schema) for item in orm_list]

    def to_orm(self, schema_obj):
        """Pydantic → ORM"""
        if isinstance(schema_obj, dict):
            return self.db_model(**schema_obj)
        return self.db_model(**schema_obj.model_dump(exclude_none=True))
