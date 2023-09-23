import requests
import base64
from transformers import pipeline

def summarize_readme(github_link):
    summarizer = pipeline("summarization")

    # Construct the API URL for the README file
    api_url = github_link.replace("github.com", "api.github.com/repos")
    api_url += '/readme'
    response = requests.get(api_url)

    
    if response.status_code == 200:
        readme_content_base64 = response.json()['content']
        readme_content = base64.b64decode(readme_content_base64).decode('utf-8')

        # Generate the summary
        summary = summarizer(readme_content, max_length=150, min_length=100, do_sample=False)
        summary_text = summary[0]['summary_text']
        print(summary_text)
        return summary_text
    else:
        print(f"Failed to fetch README. Status code: {response.status_code}")
        return ""
