from pydantic import BaseModel, validator, Field


class CardProducts(BaseModel):
    article: int = Field(alias='id')
    brand: str
    title: str = Field(alias='name')


class CardData(BaseModel):
    products: list[CardProducts]


class CardModel(BaseModel):
    data: CardData
    params: dict
    state: int


class ExcelData(BaseModel):
    numbers: list

    @validator('numbers')
    def validate_numbers(cls, values):
        if not all(isinstance(value, int) for value in values):
            raise ValueError('All elements in first column must be integers')
        return values
