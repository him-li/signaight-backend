from core.documents.base import (
    SearchRequestDoc
)
import asyncio
from core.models.person import Person
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def load_gemeni_chat_model() -> ChatGoogleGenerativeAI:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    model = ChatGoogleGenerativeAI(
            model= os.environ["GOOGLE_MODEL_NAME"],
            temperature=0.7,
            top_p=0.85,
            google_api_key=os.environ["GEMINI_API_KEY"],
        )
    return model 


model = load_gemeni_chat_model()

UNSTRUCTURED_TO_CANDIDATE_PROMPT= """Pare following url and content into structurd respose:
\n \n**person details**:\n 
DocumentSearchInput(\n    id='fd19217cad1d094301982f3fec2b93b1',\n    
urn='588baed6-60e2-4aa7-934b-f7a536eedcbb',\n     
f_name='Anna',\n    
l_name='Severinova',\n    
email_address='anna.severinova@gmail.com',\n  
doctype='SearchRequestDoc',\n  
cellphone='34672045780'\n
url = {url}\n
content={parsed_content}\n
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class ExtractedPersonalDetails(BaseModel):
    doctype: str = "ExtractedPersonalDetails"
    source_url: Optional[str] = Field(description="Source URL of the person's details")
    f_name: Optional[str] =  Field(description="First name of the person")
    l_name: Optional[str] =  Field(description="Last name of the person")
    name: Optional[str] =  Field(description="full name of the person")
    email_address: Optional[EmailStr] =  Field(description="email address of the person")
    phone_number: Optional[str] =  Field(description="phone number of the person")
    city: Optional[str] =  Field(description="city of the person")
    country: Optional[str] =  Field(description="country of the person")
    # education: Optional[str] =  Field(description="education of the person")
    # work: Optional[List[str]] =  Field(description="work history of the person")
    # query: Optional[str] =  Field(description="search query related to the person")
    # bio: Optional[str] =  Field(description="Job title")
    # username: Optional[str] =  Field(description="Job title")
    # is_rare_name: bool =  Field(description="Job title")

class ProfessionalDetails(BaseModel):
    doctype: str = "ProfessionalDetails"
    title: Optional[str] = Field(description="Job title")
    company: Optional[str] = Field(description="Company of employment")
    city: Optional[str] = Field(description="City of employment")
    industry: Optional[str] = Field(description="Industry of employment")
    skills: Optional[List[str]] = Field(description="Skills utilized in profession")

class ExtractedPerson(BaseModel):
    doctype: str = "ExtractedPerson"
    extracted_personal_details: Optional[ExtractedPersonalDetails] = None
    extracted_professional_details: Optional[ProfessionalDetails] = None




async def get_candidate_out_of_unstructured_content (search_doc : SearchRequestDoc, url: str, parsed_content: str) -> bool:
    """
    Unstructured matcher that parses unstructured dats into structurd Candidate pydantic model.
        """
    #TODO: parse searchrequestdoc into prompt
    
    # structured_model = model.with_structured_output(ExtractedPerson, method="json_schema")
    structured_model = model.with_structured_output(Person, method="json_schema")
    msg_content = UNSTRUCTURED_TO_CANDIDATE_PROMPT.format(url=url,parsed_content=parsed_content)
    tasks = []
    input_messages=[]
    message = HumanMessage(
                content=msg_content 
            )
    tasks.append(model.ainvoke([message]))
    input_messages.append(message)
        # print('Created message with content:\n\n'+msg_content)
    result = await structured_model.ainvoke([message])        
    
    # Use asyncio.gather() to run all tasks in parallel

    a=1

person=SearchRequestDoc(**{
    'urn': "588baed6-60e2-4aa7-934b-f7a536eedcbb",
    'f_name': 'Anna', 
    'l_name': 'Severinova', 
    'cellphone': '34672045780', 
    'email_address': 'anna.severinova@gmail.com'
    })
url='https://leadsforge.ai/contact/anna-severinova-4e58ee1c'
content="Log inTry it freeASAnna Severinova Email & Phone NumberChief Executive Officer | Santa Cruz De Tenerife, Canary Islands, Spain, EuropeView Anna Severinova Email & Phone NumberAbout Anna SeverinovaAnna Severinova is a Chief Executive Officer at Alaris Realty based in Santa Cruz De Tenerife, Canary Islands, Spain, Europe. Co-Founder & CEO at Alaris Realty | Real Estate Expert with 11+ Years of ExperienceCurrent Position: Chief Executive OfficerCompany: Alaris RealtyLocation: Santa Cruz De Tenerife, Canary Islands, Spain, EuropeSocial: Professional profiles availableNetwork: Extensive professional connectionsRead moreAnna Severinova's Email AddressesNo email addresses availableAnna Severinova's Phone NumbersNo phone numbers availableView Email & Phone NumberFrequently Asked Questionsabout Anna SeverinovaWhat is Anna Severinova's phone number?Anna Severinova's phone number is Contact information available.How to contact Anna Severinova?To contact Anna Severinova, send an email to Contact information available. You can also reach out via their LinkedIn profile.What is Anna Severinova's current role?Anna Severinova currently works as Chief Executive Officer at Alaris Realty.They are located in Santa Cruz De Tenerife, Canary Islands, Spain, Europe.How do I get in touch with Anna Severinova?To reach Anna Severinova, try sending your message to Contact information available. Additionally, you can connect with them on LinkedIn.What does Anna Severinova do at Alaris Realty?Anna Severinova serves as Chief Executive Officer at Alaris Realty.Co-Founder & CEO at Alaris Realty | Real Estate Expert with 11+ Years of ExperienceAnna Severinova's Email AddressesNo email addresses availableAnna Severinova's Phone NumbersNo phone numbers availableView Email & Phone NumberSearch Engine For LeadsAdd Chrome ExtensionPRODUCTSSalesforgeSales ExecutionAgent Frank#1 AI SDRPrimeforgeGoogle & MS365 InfrastructureInfraforgePrivate Email InfrastructureMailforgeDistributed Email InfrastructureWarmfo"


asyncio.run(get_candidate_out_of_unstructured_content(person,url,content),debug=True)
