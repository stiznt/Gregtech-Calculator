from uuid6 import uuid6
from pydantic import BaseModel, Field, UUID6

class RecipeInputIngredient(BaseModel):
    id: int = Field(alias="recourceID")
    quantity: int = Field(alias="quantity")

class RecipeOutputIngredient(BaseModel):
    id: int = Field(alias="recourceID")
    quantity: int = Field(alias="quantity")
    chance: float = Field(alias="chance")

class Recipe(BaseModel):
    id: UUID6  = Field(default=uuid6(), alias="recipeID")
    name: str = Field(alias="recipeName")
    group_id: int = Field(alias="recipeGroupID")
    type_id: int = Field(alias="recipeTypeID")
    duration: int = Field(alias="recipeDuration")
    tier: int = Field(alias="recipeTier")
    energy: int = Field(alias="recipeEnergy")
    inputs: list[RecipeInputIngredient] = Field(alias="recipeInputs")
    outputs: list[RecipeOutputIngredient] = Field(alias="recipeOutputs")