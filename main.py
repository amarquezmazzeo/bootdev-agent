import os
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

from sys_prompt import SYS_PROMPT
from declarations import available_functions
from functions.call_function import call_function


def main():
    user_prompt = ""
    flag = ""
    verbose = False
    if len(sys.argv) >= 2: 
        user_prompt = sys.argv[1]
    if len(sys.argv) >= 3:
        flag = sys.argv[2]
        verbose = True
    

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    for i in range(20):
        print(i)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYS_PROMPT))
    
        # print(response.text)

        for candidate in response.candidates:
            messages.append(candidate.content)

        if not response.function_calls:
            print(response.text)
            return response.text

        function_responses = []
        for func_call in response.function_calls:
            # print(f"Calling function: {func_call.name}({func_call.args})")
            function_result = call_function(func_call, verbose)
            if (
                not function_result.parts
                or not function_result.parts[0].function_response
            ):
                raise Exception("empty call result.")
            elif verbose:
                print(f"-> {function_result.parts[0].function_response.response}")
            messages.append(function_result)
            # print(messages)
            function_responses.append(function_result.parts[0])
        
        if not function_responses:
            raise Exception("no function responses.")

    
    if flag == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()