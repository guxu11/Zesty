"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import json
from apps.enums.response_status import ResponseStatus
from pathlib import Path
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import requests
import re
import inflect
from nltk.corpus import wordnet
from apps.utils.utils import extract_code_from_markdown



class GeminiService:

    def __init__(self):
        genai.configure(api_key="AIzaSyAcO-IJAQDr4_Tlc7j1TM5F3lLo36GMTOs")

        # Set up the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]


        # Create the model instance
        # model = genai.GenerativeModel('gemini-pro-vision')
        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

    def detect_ingredient(self,image_url):

        # def singularize_nouns(word):
        #     if not word:  # Check if the word is empty or None
        #         return word
        #     p = inflect.engine()
        #     return p.singular_noun(word) or word

        response = {}

        result = requests.get(image_url)
        if result.status_code == 200:
            # Read the image from the response content
            img = Image.open(BytesIO(result.content))
            # Now you can work with the image
        else:
            print("Failed to download the image from the URL")

     
        # Configure the API key

        result = self.model.generate_content(
            [
                img,
                "give me an array of name of the food(lowercase) in this image,seperated by '/' . If there are no food in this image, return no as response",
            ]
        )

        if result.text == "no\n":
            response.update(GeminiResponse.NO_FOOD)
        else:   
            print(result.text)
            clean_text = [token.lower() for token in result.text.split('/')]
            # clean_text = [token.strip() for token in clean_text]
            print(clean_text)      
            response.update({"ingredients": clean_text})
            response.update(GeminiResponse.SUCCESS)

        return response

    

    def generate_recipe(self, image_url):
        ## double check this
        """Function to create recipe based on image"""
        response = {}
        
        # print(image_url)
        result = requests.get(image_url)
        if result.status_code == 200:
            # Read the image from the response content
            img = Image.open(BytesIO(result.content))
            # Now you can work with the image
        else:
            print("Failed to download the image from the URL")

        try:
            result = self.model.generate_content([img, f"give me recipeTitle, recipeDescription, recipeIngredients(key-value pairs (key is the name of the ingredient, value is the amount)), recipeDifficulty (select among easy, medium, hard) and recipeInstructions(a list of strings)in JSON format."])
        except Exception as e:
            print("Error", e)
            response.update(GeminiResponse.FAIL)
            return response
        print("raw text: ", result.text)
        gemini_result_json = {}

        if (result.text == "-1" or result.text == -1):
            response.update(GeminiResponse.FAIL)
            return response
        try:
            clean_text = extract_code_from_markdown(result.text, "json")
            print("clean text", clean_text)
            gemini_result_json = json.loads(clean_text)
        except Exception as e:
            print("Error", e)
            response.update(GeminiResponse.FAIL)
            return response

        response.update({"recipeData": gemini_result_json})
        response.update(GeminiResponse.SUCCESS)
        return response
 

class GeminiResponse(ResponseStatus):
    SUCCESS = {"statusCode": 0, "statusMessage": "ingredient detect successful"}
    NO_FOOD = {"statusCode": 1000, "statusMessage": "no food detected"}
    FAIL = {"statusCode": 10010, "statusMessage": "fail to detect ingredient"}
