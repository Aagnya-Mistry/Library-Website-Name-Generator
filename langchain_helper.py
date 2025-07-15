from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from typing import Optional, List
import google.generativeai as genai
from secret_key import llm_auth_key


# Configure Gemini
genai.configure(api_key=llm_auth_key)


# Custom Gemini Wrapper for LangChain
class GeminiLLM(LLM):
    model: str = "gemini-1.5-flash"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text

    @property
    def _llm_type(self) -> str:
        return "google_gemini_llm"


# Instantiate our custom Gemini LLM
llm = GeminiLLM()

def generate_website_name_and_list(genre):
    # Name Chain
    prompt_template_name = PromptTemplate(
        input_variables=['genre'],
        template="I want to open a website to store all {genre} books. Suggest a decent name for this."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key='website_name')

    # Books Chain
    prompt_template_books = PromptTemplate(
        input_variables=['website_name'],
        template='Suggest some books for the website named {website_name}.'
    )
    books_chain = LLMChain(llm=llm, prompt=prompt_template_books, output_key='list_of_books')   

    # Sequential Chain
    chain = SequentialChain(
        chains=[name_chain, books_chain],
        input_variables=['genre'],
        output_variables=['website_name', 'list_of_books']
    )

    response = chain({'genre': genre})
    return response


if __name__ == "__main__":
    result = generate_website_name_and_list("Fiction")
    print(result)
