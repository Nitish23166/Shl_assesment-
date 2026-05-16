import json
import re

# Read raw file as plain text
with open("raw_catalog.json", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Remove invalid control characters
raw_text = re.sub(r'[\x00-\x1F\x7F]', '', raw_text)

# Convert to JSON
data = json.loads(raw_text)

cleaned = []

for item in data:

    combined_text = f"""
    {item.get('name', '')}
    {item.get('description', '')}
    {' '.join(item.get('job_levels', []))}
    {' '.join(item.get('keys', []))}
    """

    cleaned.append({
        "name": item.get("name"),
        "url": item.get("link"),
        "description": item.get("description"),
        "job_levels": item.get("job_levels", []),
        "keys": item.get("keys", []),
        "remote": item.get("remote"),
        "adaptive": item.get("adaptive"),
        "combined_text": combined_text.strip()
    })

# Save cleaned file
with open("cleaned_catalog.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2)

print("Catalog cleaned successfully!")
print(f"Total assessments: {len(cleaned)}")