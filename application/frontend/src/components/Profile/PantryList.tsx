import React, { useState, useRef, useEffect, ChangeEvent, lazy } from 'react'
import { BiTrash } from 'react-icons/bi'
import { loadingGif } from '../../constants'

interface PantryListProps {
  userId: number // Assuming userId is of type string
}

const PantryList: React.FC<PantryListProps> = ({ userId }) => {
  const [ingredients, setIngredients] = useState<string[]>([])
  const [addIngredientsList, setAddIngredientsList] = useState<string[]>([])
  const [removeIngredientsList, setRemoveIngredientsList] = useState<string[]>(
    [],
  )

  const [newIngredient, setNewIngredient] = useState<string>('')
  const [isEditing, setIsEditing] = useState<boolean>(false)
  const [errorMessage, setErrorMessage] = useState<string>('')

  const [isCameraOpen, setIsCameraOpen] = useState<boolean>(false)
  const [capturedImage, setCapturedImage] = useState<string | null>(null)
  const [noFoodInImage, setNoFoodInImage] = useState<boolean>(false)

  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [selectedImage, setSelectedImage] = useState<File | null>(null)

  const [isLoading, setIsLoading] = useState(false)

  const [isAscending, setIsAscending] = useState<boolean>(false)

  useEffect(() => {
    const fetchUserIngredients = async () => {
      try {
        const response = await fetch(
          `${VITE_API_URL}/api/user/userIngredients/${userId}`,
        )
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`)
        }
        const data = await response.json()
        // console.log(data.statusCode)
        if (data.statusCode === 0) {
          setIngredients(data.data)
          // console.log(data.data)
        } else {
          console.error('Failed to fetch recipes:', data.statusMessage)
          throw new Error(data.statusMessage)
        }
      } catch (error) {
        console.error('Failed to fetch recipes, using mock data:', error)
        // 使用 mock 数据更新状态
      }
    }
    fetchUserIngredients()
  }, [])

  const handleIngredientChange = (index: number, newValue: string) => {
    // Create a copy of the ingredients array
    const updatedIngredients = [...ingredients]
    // Update the value of the ingredient at the specified index
    updatedIngredients[index] = newValue
    // Update the state with the new array of ingredients
    setIngredients(updatedIngredients)
  }

  const handleAddIngredient = async () => {
    const cleanIngredient = newIngredient.trim()
    if (cleanIngredient) {
      if (ingredients.includes(cleanIngredient)) {
        setErrorMessage('The ingredient is already in the list')
      } else {
        setIngredients([...ingredients, cleanIngredient])

        const updatedIngredients = [...addIngredientsList, cleanIngredient]
        // Update the state with the new array of ingredients
        setAddIngredientsList(updatedIngredients)
        setNewIngredient('')
        setErrorMessage('')
      }
    }
  }

  const handleRemoveIngredient = async (index: number) => {
    const updatedIngredients = [...ingredients]
    const toBeRemoved = updatedIngredients[index]
    updatedIngredients.splice(index, 1)
    setIngredients(updatedIngredients)

    if (addIngredientsList.includes(toBeRemoved)) {
      const updatedIngredients = addIngredientsList.filter(
        (ingredient) => ingredient !== toBeRemoved,
      )
      // Update the state with the new array of ingredients
      setAddIngredientsList(updatedIngredients)
    } else {
      const updatedIngredients = [...removeIngredientsList, toBeRemoved]
      // Update the state with the new array of ingredients
      setRemoveIngredientsList(updatedIngredients)
    }
  }

  const handleSaveIngredients = async () => {
    setIsEditing(false)

    if (addIngredientsList || removeIngredientsList) {
      const response = await fetch(
        `${VITE_API_URL}/api/user/useringredients/edit`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            userId: userId,
            added_ingredients: addIngredientsList,
            deleted_ingredients: removeIngredientsList,
          }),
        },
      )

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      if (data.statusCode === 0) {
        console.log('ingredients saved successfully')
      } else {
        console.log('failed to saveingredients')
      }
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleAddIngredient()
    }
  }

  const handleImageFileChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedImage(file)
      const imageUrl = await uploadImageToServer(file)

      if (imageUrl) {
        await detectIngredients(imageUrl)
      }
    }
  }

  const openCamera = async () => {
    try {
      let stream
      try {
        // Try to access the back-facing camera (environment)
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: 'environment' , // Try to use back-facing camera
          },
        })
      } catch (error) {
        console.error('Error accessing back-facing camera:', error)
        try {
          // If accessing the back-facing camera fails, fall back to the front-facing camera
          stream = await navigator.mediaDevices.getUserMedia({
            video: {
              facingMode: { exact: 'user' }, // Fall back to front-facing camera
            },
          })
        } catch (error) {
          console.error('Error accessing front-facing camera:', error)
          // Handle error (e.g., display a message to the user)
        }
      }

      if (videoRef.current) {
        if (stream) {
          videoRef.current.srcObject = stream
        } else {
          console.log('The camera cannot be opened')
        }
      }
    } catch (error) {
      console.error('Error accessing camera:', error)
    }
  }

  const turnOffCamera = () => {
    // Function to stop the camera stream

    if (videoRef.current && videoRef.current.srcObject instanceof MediaStream) {
      const tracks = videoRef.current.srcObject.getTracks()
      tracks.forEach((track) => track.stop())
      videoRef.current.srcObject = null
      // console.log("Camera turned off successfully");
    } else {
      // console.log("Video element or srcObject is invalid");
    }
  }

  const capturePicture = async () => {
    // Function to capture the image from the video stream
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current
      const canvas = canvasRef.current
      const context = canvas.getContext('2d')

      if (context) {
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        context.drawImage(video, 0, 0, canvas.width, canvas.height)

        // // Convert the canvas image to a data URL
        const dataURL = canvas.toDataURL('image/png')

        setCapturedImage(dataURL)

        const file = createFileFromBase64Image(dataURL)
        const imageUrl = await uploadImageToServer(file)

        if (imageUrl) {
          detectIngredients(imageUrl)
        }
      }
    }
  }

  const createFileFromBase64Image = (dataURL: string): File => {
    const byteCharacters = atob(dataURL.split(',')[1])
    const byteNumbers = new Array(byteCharacters.length)

    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }

    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { type: 'image/png' })

    return new File([blob], 'image.png', { type: 'image/png' })
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

  const detectIngredients = async (imageUrl: string) => {
    try {
      setIsLoading(true)
      const response = await fetch(`${VITE_API_URL}/api/detect/ingredient`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          img_data: imageUrl,
        }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      console.log(data)
      console.log(data.ingredients)

      if (data.statusCode === 0) {
        if (Array.isArray(data.ingredients)) {
          setIngredients((ingredients) => [...ingredients, ...data.ingredients])

          const updatedIngredients = [
            ...addIngredientsList,
            ...data.ingredients,
          ]
          // Update the state with the new array of ingredients
          setAddIngredientsList(updatedIngredients)

          setIsEditing(true)
        } else {
          console.error('Data returned from the server is not an array')
        }
      } else if (data.statusCode === 1000) {
        setNoFoodInImage(true)
        console.log(noFoodInImage)
      } else {
        console.error('failed to detect ingredients')
      }
    } catch (error) {
      console.error('Error detecting ingredients:', error)
    } finally {
      setIsLoading(false) // Set loading state to false when function finishes
    }
  }

  // Function to handle sorting
  const handleSortIngredient = () => {
    const sortedIngredients = [...ingredients].sort()
    if (!isAscending) {
      sortedIngredients.reverse()
    }
    setIngredients(sortedIngredients)
    setIsAscending(!isAscending)
  }

  return (
    <div>
      {isLoading && (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <img
            src={loadingGif}
            alt='Loading...'
            style={{ width: '50px', height: '50px' }}
          />
        </div>
      )}
      {!isLoading && (
        <ul className='list-group mb-3'>
          <div className='row'>
            {ingredients.map((ingredient, index) => (
              <div key={index} className='col-md-4 mb-3'>
                <li className='list-group-item d-flex justify-content-between align-items-center'>
                  {isEditing ? (
                    <input
                      type='text'
                      value={ingredient}
                      style={{
                        border: 'none',
                        width: '100%',
                        height: '100%',
                        outline: 'none',
                      }}
                      onChange={(e) =>
                        handleIngredientChange(index, e.target.value)
                      }
                    />
                  ) : (
                    <span>{ingredient}</span>
                  )}

                  {isEditing && (
                    <div
                      className='bi-trash-button'
                      onClick={() => handleRemoveIngredient(index)}
                    >
                      <BiTrash />
                    </div>
                  )}
                </li>
              </div>
            ))}
          </div>
          {noFoodInImage && <p>There are no food in the image</p>}
        </ul>
      )}

      {isEditing && (
        <>
          <div className='form-group d-flex align-items-center mb-3'>
            <input
              type='text'
              className='form-control mr-2'
              placeholder='Enter new ingredient'
              value={newIngredient}
              onChange={(e) => setNewIngredient(e.target.value)}
              onKeyPress={handleKeyPress}
              style={{ flex: 1 }}
            />
            <button
              type='button'
              className='btn btn-primary mr-1'
              onClick={handleAddIngredient}
            >
              Add
            </button>
            <button
              type='button'
              className='btn btn-primary mr-1'
              onClick={handleSortIngredient}
            >
              Sort
            </button>
            <button
              type='button'
              className='btn btn-success'
              onClick={handleSaveIngredients}
            >
              Save
            </button>
          </div>
          {errorMessage && (
            <div className='text-danger mb-2'>{errorMessage}</div>
          )}{' '}
        </>
      )}
      <div className='button-container d-flex align-items-center'>
        <button
          type='button'
          className='btn btn-secondary mb-3'
          onClick={() => {
            setIsEditing(!isEditing)
            setNoFoodInImage(false)
          }}
          style={{ display: isEditing ? 'none' : 'block', margin: '10px ' }}
        >
          Edit
        </button>

        {!isCameraOpen && !capturedImage && (
          <>
            <button
              type='button'
              className='btn btn-secondary mb-3'
              onClick={() => {
                openCamera()
                setIsCameraOpen(true)
                setNoFoodInImage(false)
              }}
              style={{ display: 'block', margin: '10px ' }}
            >
              Scan
            </button>
          </>
        )}
        <input
          id='file-input'
          type='file'
          accept='image/*'
          style={{ display: 'none' }} // Hide the input visually
          onChange={handleImageFileChange}
        />
        <button
          type='button'
          className='btn btn-secondary mb-3'
          style={{ display: 'block', margin: '10px ' }}
          onClick={() => document.getElementById('file-input')?.click()} // Trigger input click
        >
          Upload
        </button>
      </div>

      {isCameraOpen && !capturedImage && (
        <>
          <button
            type='button'
            className='btn btn-danger'
            onClick={() => {
              turnOffCamera()
              setIsCameraOpen(false)
            }}
          >
            Turn Off Camera
          </button>
          <button
            type='button'
            className='btn btn-primary'
            onClick={() => {
              capturePicture()
              turnOffCamera()
              setIsCameraOpen(false)
              setCapturedImage(null)
            }}
          >
            Capture
          </button>
        </>
      )}

      <div>
        {isCameraOpen && !capturedImage && (
          <>
            <video ref={videoRef} autoPlay playsInline />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
          </>
        )}
      </div>
    </div>
  )
}

export default PantryList
