from pydantic import BaseModel
from typing import Optional, Union

class Identiy(BaseModel): 
    industry: str='gaming'
    task: str="sell games on multiple platforms"       # The more detailed the better
    location: str="Ho Chi Minh city, Vietnam"   # It is neccessary for developing an agent that suit the local voice

    def generate(self): 
        persona_generator = f"""
        You are an expert ML researcher and prompt engineer. You have been asked with creating a prompt which can be used to simulate a fictional user of a particular brand and service. This prompt needs to include the persons name, age, demographic, behavioral patterns, personality including big five and DISC, personality traits, frustrations, values, goals, challenges, and any other related information based on the context — Be as detailed as you need to. You will generate the prompt as a one liner starting with “You are “. This prompt is for customer of {self.industry} in {self.location}. In details, the person {self.task}. Please only return the prompt to use.
        """
        return persona_generator
    

class GenerationConfig(BaseModel): 
    temperature: float=1.
    top_p: float=1.
    max_tokens: int=512, 