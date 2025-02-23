from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")
client = OpenAI(api_key=api_key)


def get_chat_completion(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0
) -> str:
    """
    Get a chat completion from OpenAI.
    
    Args:
        prompt: The text prompt to send
        model: The model to use (default: gpt-4)
        temperature: Controls randomness (0-1, default: 0)
    
    Returns:
        The completion text
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    
    except Exception as e:
        raise Exception(f"Error getting chat completion: {str(e)}")
    

def chain_workflow(query: str, steps: list[str], debug: bool = False) -> str:
    """
    Execute a chain of workflows.
    """
    input_query = query
    for i, step in enumerate(steps):
        input_prompt = f"Step {i+1}:\n{step}\n\nQuery:\n{input_query}"
        input_query = get_chat_completion(input_prompt)
        if debug:
            print("-"*80)
            print(f"Step {i+1}:\n{step}\n\nResult:\n{input_query}\n\n")
    return input_query
