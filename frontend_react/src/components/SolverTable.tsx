import { useEffect, useState } from "react"
import "./styles/SolverTable.css"
import {RecipeInputItem, RecipeOutputItem} from "../components/RecipeForm.tsx"
import SolverTableItem from "./SolverTableItem.tsx"

const API_URL = "http://localhost:8000/api"

export type SolverRecipeIngredient = {
    resourceName: string,
    resourceQuantity: number
}

export type SolverRecipe = {
    recipeID: string
    recipeName: string,
    recipeEnergy: number,
    recipeMult: number,
    recipeInputs: SolverRecipeIngredient[],
    recipeOutputs: SolverRecipeIngredient[]
}

export type Recipe = {
    id: string,
    name: string,
    energy: number,
    inputs: RecipeInputItem[]
    outputs: RecipeOutputItem[]
}

type SolverTableProps = {
    recipeList?: Recipe[]
}



function SolverTable({recipeList}: SolverTableProps){

    // const [recipes, setRecipes] = useState<Recipe[]>(defaultSolverTable(recipeList))
    const [recipes, setRecipes] = useState<SolverRecipe[]>([])

    function loadRecipes(){
        fetch(API_URL + "/solver/get-recipes").then(responce => responce.json())
        .then((data:SolverRecipe[]) => {
            setRecipes(data)
        })
    }

    useEffect(() => {
        loadRecipes()
    }, [])

    return (
        <div className="solver-table">
            <table>
                <thead>
                    <tr>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        <th scope="col">POWER</th>
                        <th scope="col">INPUTS/tick</th>
                        <th scope="col">OUTPUTS/tick</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        recipes.map((recipe, index) => {
                            return <SolverTableItem recipe={recipe} key={recipe.recipeID} onDelete={() => loadRecipes()}/>
                        })
                    }
                </tbody>
            </table>
            <button onClick={() => loadRecipes()}>Загрузить рецепты</button>
        </div>
    )
}

export default SolverTable