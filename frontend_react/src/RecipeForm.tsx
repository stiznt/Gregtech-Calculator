import { useState } from "react"

type RecipeInputItem = {
    name: string,
    quantity: number
}

type RecipeOutputItem = {
    name: string,
    quantity: number,
    chance: number
}

function RecipeForm(){

    const [recipeName, setRecipeName] = useState('');
    const [recipeGroup, setRecipeGroup] = useState('');
    const [recipeType, setRecipeType] = useState('')
    const [recipeDuration, setRecipeDuration] = useState(0)
    const [recipeTier, setRecipeTier] = useState(1)
    const [recipeEnergy, setRecipeEnergy] = useState(0)
    const [recipeInputs, setRecipeInputs] = useState<RecipeInputItem[]>(() => { const a:RecipeInputItem = {name: "", quantity: 0}; return [a];});
    const [recipeOutputs, setRecipeOutputs] = useState<RecipeOutputItem[]>(() => {const a:RecipeOutputItem = {name: "", quantity: 0, chance: 100}; return [a]});

    function changeRecipeInput(index: number, newName: string, newQuantity: number){
        const newRecipeInputs = [...recipeInputs];
        newRecipeInputs[index].name = newName;
        newRecipeInputs[index].quantity = newQuantity;
        setRecipeInputs(newRecipeInputs);
    }

    function removeRecipeInput(index: number){
        const newRecipeInputs = recipeInputs.filter((item, i) => i !== index)
        setRecipeInputs(newRecipeInputs)
    }

    function addRecipeInput(){
        const x:RecipeInputItem = {name:"", quantity: 0};
        setRecipeInputs([...recipeInputs, x])
    }

    function changeRecipeOutput(index: number, newName: string, newQuantity: number, newChance: number){
        const newRecipeOutputs = [...recipeOutputs];
        newRecipeOutputs[index] = {name: newName, quantity: newQuantity, chance: newChance};
        setRecipeOutputs(newRecipeOutputs);
    }

    function addRecipeOutput(){
        const x: RecipeOutputItem = {name: "", quantity: 0, chance: 100};
        setRecipeOutputs([...recipeOutputs, x])
    }

    function removeRecipeOutput(index: number){
        setRecipeOutputs(recipeOutputs.filter((item, i) => i !== index))
    }

    function clearForm(){

    }

    return (
        <div className="recipe-form">
                <div className="form-item">
                    <label>Название рецепта</label>
                    <input value={recipeName} onChange={e => {setRecipeName(e.target.value);}}/>
                </div>
                <div className="form-item">
                    <label>Группа</label>
                    <input value={recipeGroup} onChange={e => {setRecipeGroup(e.target.value)}}/>
                </div>
                <div className="form-item">
                    <label>Вид крафта</label>
                    <input value={recipeType} onChange={e => {setRecipeType(e.target.value)}}/>
                </div>
                <div className="form-item">
                    <label>Длительность крафта</label>
                    <input type="number" value={recipeDuration} onChange={e => {setRecipeDuration(parseFloat(e.target.value))}}/>
                    <select className="duration-type">
                        <option value="1">тиков</option>
                        <option value="20">секунд</option>
                    </select>
                </div>
                <div className="form-item">
                    <label>Базовый тир рецепта</label>
                    <select value={recipeTier} onChange={e => setRecipeTier(parseInt(e.target.value))}>
                        <option value="1">LV</option>
                        <option value="2">MV</option>
                        <option value="3">HV</option>
                        <option value="4">EV</option>
                    </select>
                </div>
                <div className="form-item">
                    <label>Потребление энергии: </label>
                    <input type="number" value={recipeEnergy} onChange={e => setRecipeEnergy(parseInt(e.target.value))}/>
                    <label>EU/t</label>
                </div>
                <div className="io-section inputs">
                    <h4>Входы</h4>
                    <div className="io-section-items">
                        {
                            recipeInputs.map((item, index) => {
                                return (
                                    <div className="io-section-item" key={index}>
                                        <label>Имя:</label>
                                        <input value={item.name} onChange={e => changeRecipeInput(index, e.target.value, item.quantity)}/>
                                        <label>Кол-во:</label>
                                        <input type="number" value={item.quantity} onChange={e => changeRecipeInput(index, item.name, parseInt(e.target.value))}/>
                                        <button onClick={() => removeRecipeInput(index)}>-</button>
                                    </div>
                                )
                            })
                        }
                    </div>
                    <button onClick={() => addRecipeInput()}>+</button>
                </div>
                <div className="io-secion outputs">
                    <h4>Выходы</h4>
                    <div className="io-section-items">
                        {
                            recipeOutputs.map((item, index) => {
                                return (
                                    <div className="io-section-item" key={index}>
                                        <label>Имя:</label>
                                        <input value={item.name} onChange={e => changeRecipeOutput(index, e.target.value, item.quantity, item.chance)}/>
                                        <label>Кол-во:</label>
                                        <input type="number" value={item.quantity} onChange={e => changeRecipeOutput(index, item.name, parseInt(e.target.value), item.chance)}/>
                                        <label>Шанс:</label>
                                        <input type="number" value={item.chance} onChange={e => changeRecipeOutput(index, item.name,item.quantity, parseInt(e.target.value))}/>
                                        <button onClick={() => removeRecipeOutput(index)}>-</button>
                                    </div>
                                )
                            })
                        }
                    </div>
                    <button onClick={() => addRecipeOutput()}>+</button>
                </div>
                <div className="buttons">
                    <button onClick={() => clearForm()}>Очистить форму</button>
                    <button>Добавить рецепт</button>
                </div>
        </div>
    )

}

export default RecipeForm