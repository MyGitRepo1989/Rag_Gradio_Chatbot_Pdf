#pip install -q -U google-generativeai

# @title
import pandas as pd
import random
import numpy as np
import os
os.environ['GOOGLE_API_KEY'] = 'asdaSsyDxW-Zqxk3sUAesdNW_sRas8a'
import time
import google.generativeai as genai

data= pd.read_csv("weather_data_all.csv")

def get_modal():
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model_google = genai.GenerativeModel('gemini-1.5-flash')
    return model_google




def make_data(data, modal_google):
    #flood_risk_google=[]
    #fire_risk_google=[]
    #drought_risk_google=[]
    #tornado_risk_google=[]
    earthquake_risk_google=[]
    model_google.generate_content("reset").text
    for i in range(data.shape[0]):
        print(i)
        text = data.earthquake_risk_comments[i]
        
        prompt = (
            f"As a house property insurance analyst, read the following property risk review text and rewrite it in exactly two lines, "
            f"without adding any labels, headings, or additional comments. Maintain the original context and risk level, and avoid location-specific details. "
            f"Here is the text: '{text}'"
            )
        prompt_variants = [
            f"{prompt} Could you make it sound more formal?",
            f"Please provide a detailed answer for: {prompt}",
            f"Summarize the main points of: {prompt}",
            ]
        selected_prompt = random.choice(prompt_variants)

        model_google.temperature = random.choice([0.5,0.1,0.7,0.9,0.2])
        model_google.top_k = random.choice([30, 50, 100])  # Adjusts sampling to top-k words
        model_google.top_p = random.choice([0.8, 0.9, 0.95])  # Nucleus sampling

        response = model_google.generate_content(selected_prompt).text
        earthquake_risk_google.append(response)

        print("Original:",text)
        print("Synthetic:",response)
        print("_____")
        time.sleep(5)
    return earthquake_risk_google



if __name__== main:
    model_google = get_modal()
    earthquake_risk_google = make_data(data modal_google)
    data['earthquake_risk_google']=pd.Series(earthquake_risk_google)
    