const API_URL = "http://localhost:8000"

function submitRecipe(){

    recipeDuration = parseFloat(document.getElementById("recipeDuration").value)
    
    if(document.getElementById("recipeDurationType").value == "seconds") recipeDuration = recipeDuration * 20;

    if(recipeDuration === null || isNaN(recipeDuration)) recipeDuration = 0;

    recipeEnergy = parseInt(document.getElementById("recipeEnergy").value)

    if(recipeEnergy === null || isNaN(recipeEnergy)) recipeEnergy = 0;

    // get recipe inputs

    recipeInputs = {}

    const inputsContainer = document.getElementById("inputs-container");
    inputsContainer.querySelectorAll(".io-row").forEach((value, key, parent) => {
        name = value.querySelector(".io-name").value
        quantity = parseInt(value.querySelector(".io-qty").value)
        recipeInputs[name] = quantity
    })

    // get recipe outputs

    recipeOutputs = {}
    const outputsContainer = document.getElementById("outputs-container");
    outputsContainer.querySelectorAll(".io-row").forEach((value, key, parent) => {
        name = value.querySelector(".io-name").value
        quantity = parseInt(value.querySelector(".io-qty").value)
        chance = parseFloat(value.querySelector(".io-chance").value)
        recipeOutputs[name] = [quantity, chance]
    })

    data = {
        "recipeName": document.getElementById("recipeName").value,
        "recipeGroup": document.getElementById("recipeGroup").value,
        "recipeType": document.getElementById("recipeType").value,
        "recipeDuration": recipeDuration,
        "recipeTier": parseInt(document.getElementById("recipeTier").value),
        "recipeEnergy": recipeEnergy,
        "recipeInputs": recipeInputs,
        "recipeOutputs": recipeOutputs
    }

    console.log(data)

    fetch(API_URL + "/add-recipe", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }).then(responce => responce.json())
    .catch(error => console.error(error))
}

function clearForm(){
    document.getElementById("recipeName").value = ""
    document.getElementById("recipeGroup").value = ""
    document.getElementById("recipeType").value = ""
    document.getElementById("recipeDuration").value = ""
    document.getElementById("recipeTier").value = "1"
    document.getElementById("recipeEnergy").value = ""

    // remove inputs
    const inputContainer = document.getElementById("inputs-container")
    inputContainer.innerHTML = ""
    inputContainer.appendChild(createInputRow())

    // remove outputs
    const outputContainer = document.getElementById("outputs-container")
    outputContainer.innerHTML = ""
    outputContainer.appendChild(createOutputRow())
}

function addInputRow(){
    const c = document.getElementById("inputs-container");
    const row = createInputRow()
    c.appendChild(row);
}

function addOutputRow(){
    const c = document.getElementById("outputs-container");
    const row = createOutputRow();
    c.appendChild(row);
}

function removeRow(btn){
    const parent = btn.closest(".io-section");
    if(parent.querySelectorAll('.io-row').length>1) btn.parentElement.remove();
}

function createInputRow(){
    const row = document.createElement("div");
    row.className="io-row";
    row.innerHTML = '<div class="io-name-wrap"><input type="text" class="input-field io-name" placeholder="Название" autocomplete="off"><div class="tag-dropdown"></div></div><input type="number" class="input-field qty io-qty" placeholder="Кол-во" step="any" min="0"><button class="btn btn-red btn-xs" style="flex:0 0 auto;" onclick="removeRow(this)" title="Удалить">✕</button>'
    return row;
}

function createOutputRow(){
    const row = document.createElement("div");
    row.className="io-row";
    row.innerHTML = '<div class="io-name-wrap"><input type="text" class="input-field io-name" placeholder="Название" autocomplete="off"><div class="tag-dropdown"></div></div><input type="number" class="input-field qty io-qty" placeholder="К-во" step="any" min="0"><input type="number" class="input-field chance io-chance" value="100" placeholder="%" step="any" min="0" max="100"><button class="btn btn-red btn-xs" style="flex:0 0 auto;" onclick="removeRow(this)" title="Удалить">✕</button>'
    return row;
}