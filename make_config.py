import json

# --- IMPORTANT: EDIT YOUR EMAIL ADDRESSES HERE ---
MY_RECIPIENT_LIST = ['gevakip@gmail.com']
# ---

# This is the dictionary you provided
SITE_PATTERNS = {
    'https://www.fi.is/en/mountain-huts/hut-availability': [
        'Bookings for 2026 have not opened'
    ],
    'https://www.fi.is/en/mountain-huts/hut-availability/hut-to-hut-availability': [
        'Bookings for 2026 are not open yet'
    ],
    # You can add more sites here
    # Example of a site that will likely fail the check (for testing)
    # 'https://www.google.com': [
    #     'This specific magic phrase will not be found'
    # ]
}

# Combine into the config structure
config_data = {
    "site_patterns": SITE_PATTERNS,
    "email_recipients": MY_RECIPIENT_LIST
}

# Write the config data to a JSON file
config_filename = 'config.json'
with open(config_filename, 'w') as f:
    json.dump(config_data, f, indent=4)

print(f"Configuration file '{config_filename}' created successfully.")
print("--- Config Content ---")
print(open('config.json').read())
print("----------------------")