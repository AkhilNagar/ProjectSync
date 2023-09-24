# import openai

# # Define your OpenAI API key
# api_key = "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"

# # Function to get code suggestions
# def get_code_suggestions(code):
#     openai.api_key = api_key

#     prompt = f"Suggest code improvements for the following Python code:\n\n{code}\n\nSuggestions:"

#     response = openai.Completion.create(
#         engine="text-davinci-002",  # Use the appropriate engine
#         prompt=prompt,
#         max_tokens=50,  # Adjust the number of tokens as needed
#         temperature=0.7,  # Adjust the temperature for creativity
#         n = 1  # Number of suggestions to generate
#     )

#     return response.choices[0].text.strip()

# # Sample Python code
# python_code = """
# def calculate_average(numbers):
#     total = sum(numbers)
#     count = len(numbers)
#     average = total / count
#     return average
# """

# # Get code suggestions
# suggestions = get_code_suggestions(python_code)

# # Print code suggestions
# print(suggestions)