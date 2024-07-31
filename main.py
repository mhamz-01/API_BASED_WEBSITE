import requests


# Function to get the number of verses in a chapter
def get_number_of_verses(chapter,limit):
    url = f"https://al-quran1.p.rapidapi.com/{chapter}/1-{limit}"
    headers = {
        "x-rapidapi-key": "57ff59a728msh25e5d1841f684f6p1e83b3jsn7e6aa0a163f5",
        "x-rapidapi-host": "al-quran1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return len(data)


# Get the chapter number from the user
chapter = input("Enter the chapter number of Quran: ")
limit=input("Uptill which verse do you want the chapter :")

# Get the number of verses in the chapter
num_verses = get_number_of_verses(chapter,limit)

# API endpoint and headers to get all verses
url = f"https://al-quran1.p.rapidapi.com/{chapter}/1-{num_verses}"
headers = {
    "x-rapidapi-key": "57ff59a728msh25e5d1841f684f6p1e83b3jsn7e6aa0a163f5",
    "x-rapidapi-host": "al-quran1.p.rapidapi.com"
}

# Make the API request
response = requests.get(url, headers=headers)

# Parse the JSON response
verses = response.json()

# Print the verses in a beautiful format
for verse_number, verse_info in verses.items():
    arabic_verse = verse_info['content']
    translation = verse_info['translation_eng']
    transliteration = verse_info['transliteration']

    print(f"Verse {verse_number}:")
    print(f"Arabic: {arabic_verse}")
    print(f"Translation: {translation}")
    print(f"Transliteration: {transliteration}")
    print("-" * 50)
