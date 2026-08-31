import { useEffect, useState } from "react"

const API_URL = "http://localhost:8000/api"

type RecipeListItem = {
    id: string,
    name: string
}

function addRecipe(id: string){
    fetch(API_URL + "/solver/add-recipe", {
        method: "POST",
        headers: {
            'accept': "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"recipeID": id})
    })
}

function deleteRecipe(id: string){
    fetch(API_URL + "/delete-recipe", {
        method: "DELETE",
        headers: {
            'accept': "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({recipeID: id})
    })
}

function RecipeList(){

    const [recipeList, setRecipeList] = useState<RecipeListItem[]>([])

    useEffect(() => {

        fetch(API_URL + "/get-recipes").then(responce => responce.json())
        .then((data:RecipeListItem[]) => {
            // console.log(data)
            const recipes = data.map((recipe) => {const x:RecipeListItem = {id: recipe["id"], name: recipe["name"]}; return x})
            setRecipeList(recipes)
        })

    }, [recipeList])

    return (
        <div className="recipe-list">
            {
                recipeList.map((item, index) => {
                    return (
                        <div className="recipe-list-item" key={index}>
                            <label>{item.name}</label>
                            <button onClick={() => addRecipe(item.id)}>+</button>
                            <button>edit</button>
                            <button onClick={() => deleteRecipe(item.id)}>X</button>
                        </div>
                    )
                })
            }
        </div>
    )
}

export default RecipeList