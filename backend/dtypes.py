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

class Group(BaseModel):
    id: UUID6 = Field(default=uuid6(), alias="groupID")
    name: str = Field(alias="groupName")

class Type(BaseModel):
    id: UUID6 = Field(default=uuid6(), alias="typeID")
    name: str = Field(alias="typeName")

class RecipeID(BaseModel):
    id: UUID6 = Field(alias="recipeID")

class RecipeFixed(RecipeID):
    value: float = Field(alias="fixedAmount")

class RecipeInputs(BaseModel):
    recipeID: UUID6
    inputs: list[RecipeInputIngredient]

    def getResourceQuantity(self, resourceID: str) -> int:
        for resource in self.inputs:
            if resource.id == resourceID:
                return resource.quantity
        return 0

class RecipeOutputs(BaseModel):
    recipeID: UUID6
    outputs: list[RecipeOutputIngredient]

    def getResourceQuantity(self, resourceID: str) -> int:
            for resource in self.outputs:
                if resource.id == resourceID:
                    return resource.quantity
            return 0


class Recipe(BaseModel):
    id: UUID6 = Field(default=uuid6(), alias="recipeID")
    name: str = Field(alias="recipeName")
    group_id: UUID6 = Field(alias="recipeGroupID")
    type_id: UUID6 = Field(alias="recipeTypeID")
    duration: int = Field(alias="recipeDuration")
    tier: int = Field(alias="recipeTier")
    energy: int = Field(alias="recipeEnergy")