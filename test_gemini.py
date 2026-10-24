from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="Say hello in one short sentence."
)

print(response.text)