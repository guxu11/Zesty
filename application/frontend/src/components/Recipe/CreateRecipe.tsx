// CreateRecipePage.tsx

import React, { useState, ChangeEvent } from 'react'
import '../../styles/CreateRecipe.css'
import { useAuth } from '../Context/AuthContext'
import { Link, useNavigate } from 'react-router-dom'
import NavigationBar from '../NavigationBar'
import { BiTrash } from 'react-icons/bi'
import {
  defaultRecipeImgUrl,
  defaultUploadImgeUrl,
  generateLoadingGif,
} from '../../constants'

// Define the interface for the props
interface CreateRecipePageProps {
  // Props definition here
}

interface Ingredient {
  name: string
  amount: string
  category: number
}

interface Instruction {
  stepDesc: string
  stepImg: string
}

// Define the CreateRecipePage component
const CreateRecipePage: React.FC = () => {
  const { userInfo, isLoggedIn } = useAuth()
  let userId = 0

  if (userInfo === null) {
    userId = 0
  } else {
    userId = userInfo.userId
  }

  let navigate = useNavigate()
  // State variables and logic here

  const [success, setSuccess] = useState(false) // State to track registration success
  const [errorMessage, setErrorMessage] = useState('') // State to track error message

  const [isLoading, setIsLoading] = useState(false)
  const [submitLoading, setSubmitLoading] = useState(false)

  const [recipeTitle, setRecipeTitle] = useState('')
  const [description, setDescription] = useState('')

  const [image, setImage] = useState<File | null>(null)
  const [imageUrl, setImageUrl] = useState('')

  const [ingredients, setIngredients] = useState<Ingredient[]>([
    { name: '', amount: '', category: 0 },
  ])
  const [instructions, setInstructions] = useState<Instruction[]>([
    { stepDesc: '', stepImg: '' },
  ])
  const [difficulty, setDifficulty] = useState('')

  // Function to handle form submission
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    // Handle form submission logic here

    setSubmitLoading(true)

    console.log('I am creating recipe')
    // Add code here to handle form submission, such as sending data to server
    // You can perform form validation here before submitting the data
    const currentDate = new Date()

    const formattedDate = currentDate.toLocaleString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false, // Use 24-hour format
    })

    try {
      if (image) {
        const formData = new FormData()
        formData.append('file', image)
        const response = await fetch(`${VITE_API_URL}/api/recipe/upload`, {
          method: 'POST',
          body: formData,
        })

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        const data = await response.json()
        console.log('Response from server:', data)

        // Handle response from server as needed
        if (data.statusCode === 0) {
          // Registration success
          console.log('successful fetch image url:' + data.data.url)
          setImageUrl(data.data.url)
        } else {
        }
        // Append the selected file to the FormData object

        try {
          // setImageUrl(data.data.url);
          console.log('set image url:' + imageUrl)
          const response = await fetch(`${VITE_API_URL}/api/recipe/create`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              userId: userId,
              recipeName: recipeTitle,
              category: 3,
              recipePicture: data.data.url,
              description: description,
              cookingTime: '30min',
              recipeType: 1,
              difficulty: mapDifficultyToValue(difficulty),
              postIme: formattedDate,
              ingredients: ingredients,
              steps: instructions,
            }),
          })

          if (!response.ok) {
            throw new Error('Network response was not ok')
          }

          const responseData = await response.json()
          console.log('Response from server:', responseData)
          // Handle response from server as needed
          if (responseData.statusCode === 0) {
            // Registration success
            setSuccess(true)
            navigate('/')
          } else if (responseData.statusCode === 100100) {
            // Show error messaalreadyge if statusCode is 100100
            setErrorMessage('failed to.')
          }
        } catch (error) {
          console.error('Error:', error)
        }
      } else {
        try {
          const response = await fetch(`${VITE_API_URL}/api/recipe/create`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              userId: userId,
              recipeName: recipeTitle,
              category: 3,
              recipePicture: defaultRecipeImgUrl,
              description: description,
              cookingTime: '30min',
              recipeType: 1,
              difficulty: mapDifficultyToValue(difficulty),
              postIme: formattedDate,
              ingredients: ingredients,
              steps: instructions,
            }),
          })

          if (!response.ok) {
            throw new Error('Network response was not ok')
          }

          const responseData = await response.json()
          console.log('Response from server:', responseData)
          // Handle response from server as needed
          if (responseData.statusCode === 0) {
            // Registration success
            setSuccess(true)
            setSubmitLoading(false)
            navigate('/')
          } else if (responseData.statusCode === 100100) {
            // Show error messaalreadyge if statusCode is 100100
            setErrorMessage('failed to.')
          }
        } catch (error) {
          console.error('Error:', error)
        }
      }
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const uploadImageToServer = async (
    file: File,
  ): Promise<string | undefined> => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${VITE_API_URL}/api/recipe/upload`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    const data = await response.json()
    return data.statusCode === 0 ? data.data.url : undefined
  }

  const handleImageChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setImage(file)
      const imageUrl = await uploadImageToServer(file)
      console.log('i am in handleImageChange function')
      console.log(imageUrl)
      if (imageUrl) {
        setImageUrl(imageUrl)
      }
    }
  }

  const handleInstructionImageChange = (
    index: number,
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = e.target.files?.[0] // Get the first file selected by the user
    if (file) {
      const reader = new FileReader()
      reader.onload = () => {
        const dataURL = reader.result as string
        const updatedInstructions = [...instructions]
        updatedInstructions[index].stepImg = dataURL
        setInstructions(updatedInstructions)
      }
      reader.readAsDataURL(file) // Read the file as a data URL
    }
  }

  const handleIngredientNameChange = (index: number, value: string) => {
    const newIngredients = [...ingredients]
    newIngredients[index].name = value
    setIngredients(newIngredients)
  }

  const handleIngredientAmountChange = (index: number, value: string) => {
    const newIngredients = [...ingredients]
    newIngredients[index].amount = value
    setIngredients(newIngredients)
  }

  const handleAddIngredient = () => {
    setIngredients([...ingredients, { name: '', amount: '', category: 1 }])
  }

  const handleRemoveIngredient = (index: number) => {
    const newIngredients = [...ingredients]
    newIngredients.splice(index, 1)
    setIngredients(newIngredients)
  }

  const handleInstructionChange = (index: number, value: string) => {
    const newInstructions = [...instructions]
    newInstructions[index].stepDesc = value
    setInstructions(newInstructions)
  }

  const handleAddInstruction = () => {
    setInstructions([...instructions, { stepDesc: '', stepImg: '' }])
  }

  const handleRemoveInstruction = (index: number) => {
    const newInstructions = [...instructions]
    newInstructions.splice(index, 1)
    setInstructions(newInstructions)
  }

  const generateRecipe = async () => {
    try {
      setIsLoading(true)
      clearForm()

      const response = await fetch(`${VITE_API_URL}/api/generate/recipes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          img_url: imageUrl,
        }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()

      if (data.statusCode === 0) {
        const cleanedJsonString = data.recipeData

        const parsedData = cleanedJsonString
        console.log('i am recipeData')
        console.log('parseData: ', parsedData)

        // Extract the first value from the key-value pair
        const keys = Object.keys(parsedData) // Get all keys

        const ingredientsData = parsedData['recipeIngredients']
        console.log('ingredientsData: ', ingredientsData)
        const parsedIngredients = Object.entries(ingredientsData).map(
          ([name, amount]: [string, unknown]) => ({
            name,
            amount: amount as string,
            category: 0,
          }),
        )

        const instructionsData = parsedData['recipeInstructions']

        const parsedInstructions = instructionsData.map((stepDesc: string) => {
          return { stepDesc, stepImg: '' }
        })
        setRecipeTitle(parsedData['recipeTitle'])
        setDescription(parsedData['recipeDescription'])
        setIngredients(parsedIngredients)
        setInstructions(parsedInstructions)
        setDifficulty(capitalizeFirstLetter(parsedData['recipeDifficulty']))
      } else {
        console.error('failed to generate recipes')
      }
    } catch (error) {
      console.error('Error detecting ingredients:', error)
    } finally {
      setIsLoading(false) // Set loading state to false when function finishes
    }
  }

  function capitalizeFirstLetter(str: string): string {
    return str
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ')
  }

  // clear the form
  const clearForm = () => {
    setRecipeTitle('')
    setDescription('')
    // setImage(null);
    setIngredients([{ name: '', amount: '', category: 0 }])
    setInstructions([{ stepDesc: '', stepImg: '' }])
    setDifficulty('')
  }

  // JSX template for the component
  return (
    <>
      <NavigationBar />
      <div className='create-recipe-page'>
        <div className='create-recipe-form-container'>
          <form onSubmit={handleSubmit} className='create-recipe-form'>
            <div className='create-recipe-container'>
              <h2 className='create-recipe-element'>Create Recipe</h2>
            </div>

            <hr />

            <div className='container' id='name-description-image'>
              <div className='row'>
                {/* First Column */}
                <div className='col-md-6'>
                  {/* First Row in First Column */}
                  <div className='row' style={{ height: '33.33%' }}>
                    <div className='col-md-12'>
                      <div id='recipeTitle'>
                        <label className='label'>Recipe Title:</label>
                        <div className='input-container'>
                          <input
                            type='text'
                            value={recipeTitle}
                            onChange={(e) => setRecipeTitle(e.target.value)}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                  {/* Second Row in First Column */}
                  <div className='row' style={{ height: '66.66%' }}>
                    <div className='col-md-12 '>
                      <div
                        id='recipeDesc d-flex flex-column '
                        style={{ height: '100%' }}
                      >
                        <label className='label'> Description:</label>
                        <div className='input-container flex-grow-1'>
                          <textarea
                            // type="text"
                            style={{ width: '100%' }}
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Second Column */}

                <div className='col-md-6'>
                  {/* Single Row in Second Column */}
                  <div className='row'>
                    {/* <div className="col-md-12"> */}
                    <div
                      id='recipeImg'
                      style={{
                        width: '100%',
                        height: '100%',
                        overflow: 'hidden',
                      }}
                    >
                      <img
                        src={
                          image
                            ? URL.createObjectURL(image)
                            : defaultUploadImgeUrl
                        } // Use selected image if available, otherwise use placeholder image
                        alt=''
                        style={{
                          width: '100%',
                          height: '100%',
                          cursor: 'pointer',
                        }}
                        onClick={() =>
                          document.getElementById('fileInput')?.click()
                        }
                      />
                      {/* Transparent file input overlaid on top of the image */}
                      <input
                        id='fileInput'
                        type='file'
                        accept='image/*'
                        style={{ display: 'none' }}
                        onChange={handleImageChange}
                      />
                    </div>
                    {/* </div> */}
                  </div>
                  <div className='row'>
                    <div className='d-flex justify-content-center'>
                      {isLoading ? (
                        <img
                          src={generateLoadingGif}
                          style={{
                            width: '100px', // Example width
                            height: '50px', // Example height
                            // Additional styles...
                          }}
                          alt='Loading...'
                        />
                      ) : (
                        <button
                          type='button'
                          id='generateRecipeButton'
                          onClick={generateRecipe}
                          style={{
                            width: '200px', // Example width
                            height: '50px', // Example height
                            // Additional styles...
                          }}
                        >
                          Generate Recipe
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <hr />

            <div className='create-recipe-container' id='ingredients'>
              <label className='label'> Ingredients:</label>
              {ingredients.map((ingredient, index) => (
                <div className='create-recipe-element' key={index}>
                  <input
                    className='input-box'
                    type='text'
                    value={ingredient.name}
                    onChange={(e) =>
                      handleIngredientNameChange(index, e.target.value)
                    }
                    placeholder='Ingredient Name'
                  />
                  <input
                    className='input-box'
                    type='text'
                    value={ingredient.amount}
                    onChange={(e) =>
                      handleIngredientAmountChange(index, e.target.value)
                    }
                    placeholder='Amount'
                  />
                  <div
                    className='bi-trash-button'
                    onClick={() => handleRemoveIngredient(index)}
                  >
                    <BiTrash />
                  </div>
                </div>
              ))}
              <button
                id='add-ingredient-button'
                type='button'
                onClick={handleAddIngredient}
              >
                Add Ingredient
              </button>
            </div>

            <hr />

            <div className='create-recipe-container'>
              <label className='label'>Instructions:</label>
              {instructions.map((instruction, index) => (
                <div
                  className='create-recipe-element'
                  key={index}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    marginLeft: '0',
                  }}
                >
                  <label className='step-label'>Step {index + 1}</label>
                  <div className='step'>
                    <textarea
                      value={instruction.stepDesc}
                      className='instruction-box'
                      onChange={(e) =>
                        handleInstructionChange(index, e.target.value)
                      }
                      style={{ marginRight: '8px' }}
                    />

                    <div
                      className='bi-trash-button'
                      onClick={() => handleRemoveInstruction(index)}
                    >
                      <BiTrash />
                    </div>
                  </div>

                  <div
                    className='step-img-container'
                    style={{ display: 'flex', alignItems: 'center' }}
                  >
                    <input
                      type='file'
                      onChange={(e) => handleInstructionImageChange(index, e)}
                      style={{ display: 'none' }}
                      accept='image/*'
                      id={`fileInput-${index}`}
                    />

                    <button
                      type='button'
                      className='add-step-img-button'
                      onClick={() =>
                        document.getElementById(`fileInput-${index}`)?.click()
                      }
                    >
                      Upload Image
                    </button>
                  </div>

                  {instruction.stepImg && (
                    <div style={{ marginTop: '8px' }}>
                      <div
                        style={{
                          width: '200px',
                          height: '200px',
                          overflow: 'hidden',
                        }}
                      >
                        <img
                          src={instruction.stepImg}
                          alt={`Step ${index + 1}`}
                          className='image-preview'
                          style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover',
                          }}
                        />
                      </div>
                    </div>
                  )}
                </div>
              ))}

              <button
                type='button'
                id='add-instruction-button'
                onClick={handleAddInstruction}
              >
                Add Instruction
              </button>
            </div>

            <hr />

            <div className='create-recipe-container'>
              <div className='create-recipe-element'>
                <label
                  htmlFor='difficulty-select'
                  style={{
                    width: '200px', // Adjust width as needed
                    marginRight: '10px', // Add spacing between label and select
                  }}
                >
                  Difficulty Level:
                </label>
                <select
                  id='difficulty-select'
                  value={difficulty}
                  onChange={(e) => {
                    setDifficulty(e.target.value)
                  }}
                  className='difficulty-select'
                >
                  <option value=''>Select Difficulty</option>
                  <option value='Easy'>Easy</option>
                  <option value='Medium'>Medium</option>
                  <option value='Hard'>Hard</option>
                </select>
              </div>
            </div>

            <hr />

            <div
              className='create-recipe-container'
              id='submit-button-container'
            >
              {submitLoading ? (
                <img
                  src={generateLoadingGif}
                  style={{
                    width: '100px', // Example width
                    height: '50px', // Example height
                    // Additional styles...
                  }}
                  alt='Loading...'
                />
              ) : (
                <button
                  id='create-submit-button'
                  type='submit'
                  style={{
                    width: '200px', // Example width
                    height: '50px', // Example height
                    // Additional styles...
                  }}
                >
                  Submit Recipe
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </>
  )
}

const mapDifficultyToValue = (selectedDifficulty: string): number => {
  switch (selectedDifficulty) {
    case '':
      return 0 // Default value (optional)
    case 'Easy':
      return 1
    case 'Medium':
      return 3
    case 'Hard':
      return 5
    default:
      return 0 // Handle unexpected values (optional)
  }
}

// Export the CreateRecipePage component
export default CreateRecipePage
