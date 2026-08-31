import { SolverRecipe } from "./SolverTable"

const API_URL = "http://localhost:8000/api"

type SolverTableItemProps = {
    recipe: SolverRecipe,
    onDelete?: Function
}

function SolverTableItem({recipe, onDelete} : SolverTableItemProps){

    if(recipe === undefined) {
        return (
            <tr></tr>
        )
    }

    function deleteItem(id: string){
        fetch("http://localhost:8000/api/solver/remove-recipe", {
            method: "DELETE",
            headers: {
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"recipeID": id})
        })
    }

    return (
            <tr className="solver-table-item">
                <th scope="row"></th>
                <td>{recipe.recipeName}</td>
                <td>{recipe.recipeEnergy}</td>
                <td>{
                    recipe.recipeInputs.map((data, index) => {
                        return <p key={data.resourceName}>{data.resourceName} x{data.resourceQuantity*recipe.recipeMult}</p>
                    })
                }</td>
                <td>{
                    recipe.recipeOutputs.map((data, index) => {
                        return <p key={data.resourceName + toString(index)}>{data.resourceName} x{data.resourceQuantity*recipe.recipeMult}</p>
                    })
                }</td>
                <td>
                    <button onClick={() => deleteItem(recipe.recipeID)}>X</button>
                </td>
            </tr>
    )

}

export default SolverTableItem