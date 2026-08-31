import './App.css';
import RecipeForm from "./components/RecipeForm.tsx"
import RecipeList from './components/RecipeList.tsx';
import SolverTable from './components/SolverTable.tsx';
import { useState } from 'react';

function App() {
  const [isRecipeListOpen, setRecipeListOpen] = useState(false);
  const [isRecipeFormOpen, setRecipeFormOpen] = useState(false);
  return (
    <div className="App">
      {/* <RecipeForm/> */}
      {/* <RecipeList/> */}
      <ModalRecipeForm isOpen={isRecipeFormOpen} onClose={() => setRecipeFormOpen(false)}/>
      <ModalRecipeList isOpen={isRecipeListOpen} onClose={() => setRecipeListOpen(false)}/>
      <SolverTable/>
      <button onClick={() => setRecipeListOpen(true)}>Добавить рецепт</button>
      <button onClick={() => setRecipeFormOpen(true)}>Создать рецепт</button>
    </div>
  );
}

function ModalRecipeForm({isOpen, onClose}){
  if (!isOpen) return null;

  return (
    <div className='modal-recipe-form'>
      <RecipeForm/>
      <button onClick={() => onClose()}>Закрыть</button>
    </div>
  )
}

function ModalRecipeList({isOpen, onClose}){
  if(!isOpen) return null;

  return (
    <div className='modal-recipe-list'>
      <RecipeList/>
      <button onClick={onClose}>Закрыть</button>
    </div>
  )
}

export default App;
