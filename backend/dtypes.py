from pydantic import BaseModel, Field

class Recipe(BaseModel):
    name: str = Field(alias="recipeName")
    group: str = Field(alias="recipeGroup")
    type: str = Field(alias="recipeType")
    duration: int = Field(alias="recipeDuration")
    tier: int = Field(alias="recipeTier")
    energy: int = Field(alias="recipeEnergy")
    inputs: dict[str, int] = Field(alias="recipeInputs")
    outputs: dict[str, list[int, float]] = Field(alias="recipeOutputs")