from uuid6 import uuid6
from pydantic import BaseModel, Field, UUID6


class Resource(BaseModel):
    id: UUID6 = Field(default=uuid6(), alias="resourceID")
    name: str = Field(alias="resourceName")

class RecipeInputIngredient(Resource):
    quantity: int = Field(alias="quantity")

class RecipeOutputIngredient(Resource):
    quantity: int = Field(alias="quantity")
    chance: float = Field(alias="chance")

class Recipe(BaseModel):
    id: UUID6  = Field(default=uuid6(), alias="recipeID")
    name: str = Field(alias="recipeName")
    group_id: UUID6 = Field(alias="recipeGroupID")
    type_id: UUID6 = Field(alias="recipeTypeID")
    duration: int = Field(alias="recipeDuration")
    tier: int = Field(alias="recipeTier")
    energy: int = Field(alias="recipeEnergy")