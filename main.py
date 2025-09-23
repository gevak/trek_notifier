import dotenv
import requests
import json
import os
import smtplib
from email.mime.text import MIMEText

dotenv.load_dotenv()

def send_notification_email(subject, body, recipients):
    """
    Sends an email using the provided Gmail service.
    
    Args:
        subject (str): The subject line of the email.
        body (str): The plain text body of the email.
        recipients (list): A list of email addresses to send to.
    """
    try:
      sender = 'emailnotifier17@gmail.com'
      password = os.getenv('GMAIL_APP_PASSWORD')
      msg = MIMEText(body)
      msg['Subject'] = subject
      msg['From'] = sender
      msg['To'] = ', '.join(recipients)
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
          smtp_server.login(sender, password)
          smtp_server.sendmail(sender, recipients, msg.as_string())
      print("Message sent!")
        
    except HttpError as error:
        print(f"An error occurred while sending email: {error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def check_websites_for_changes(site_patterns, email_recipients):
    """
    Checks a dictionary of websites for a list of expected text patterns.
    
    If none of the patterns for a given URL are found, it sends a
    notification email. It also notifies if a site fails to load.
    
    Args:
        site_patterns (dict): {url: [pattern1, pattern2, ...]}
        email_recipients (list): List of email addresses to notify.
    """
    if not email_recipients:
        print("Warning: No email recipients configured. Will print to console only.")
    
    # Use a common browser user-agent to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Keep track of sites that have changed
    changed_sites = []

    for url, patterns in site_patterns.items():
        print(f"Checking: {url}")
        
        try:
            # --- 1. Fetch the website content ---
            response = requests.get(url, headers=headers, timeout=15)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            
            html_content = response.text
            
            # --- 2. Check for patterns ---
            for pattern in patterns:
                if pattern in html_content:
                    print(f"  -> Found expected pattern: '{pattern[:50]}...'")
                else:
                  # --- 3. Notify if ANY pattern was not found ---
                  print(f"  -> !!! CHANGE DETECTED: Expected pattern: {pattern} not found on {url}")
                  changed_sites.append(url)
                  
                  subject = f"Website Change Detected: {url}"
                  body = (
                      f"A change was detected on {url}.\n\n"
                      f"The site no longer contains the expected text pattern:\n'{pattern}'\n\n"
                  )
                  body += "\nPlease check the website manually."
                  
                  if email_recipients:
                      send_notification_email(subject, body, email_recipients)
                  break

            else:
                print(f"  -> Status: OK")

        except requests.exceptions.HTTPError as http_err:
            print(f"  -> !!! ERROR: HTTP error occurred for {url}: {http_err}")
            subject = f"Website Check FAILED: {url}"
            body = f"Failed to check {url} due to an HTTP error: {http_err}"
            if email_recipients and gmail_service:
                send_notification_email(gmail_service, subject, body, email_recipients)
                
        except requests.exceptions.RequestException as req_err:
            print(f"  -> !!! ERROR: Failed to fetch {url}: {req_err}")
            subject = f"Website Check FAILED: {url}"
            body = f"Failed to check {url} due to a request error: {req_err}"
            if email_recipients and gmail_service:
                send_notification_email(gmail_service, subject, body, email_recipients)

    if not changed_sites:
        print("\nCheck complete. All websites contain all expected patterns.")
    else:
        print(f"\nCheck complete. Changes detected on {len(changed_sites)} site(s): \n{changed_sites}.")


# Main
def main():
    # --- Load Config ---
    config_filename = 'config.json'
    try:
        with open(config_filename, 'r') as f:
            config = json.load(f)
        
        PATTERNS_TO_CHECK = config.get('site_patterns', {})
        RECIPIENT_EMAILS = config.get('email_recipients', [])
        
        if not PATTERNS_TO_CHECK:
            print("Error: 'site_patterns' not found or empty in config.json")
        if not RECIPIENT_EMAILS:
            print("Warning: 'email_recipients' not found or empty in config.json. No emails will be sent.")
            
        # --- Run the Check ---
        if PATTERNS_TO_CHECK:
            print("\nStarting website check...")
            check_websites_for_changes(PATTERNS_TO_CHECK, RECIPIENT_EMAILS)
        else:
            print("Could not run check because no sites are configured.")

    except FileNotFoundError:
        print(f"Error: Configuration file '{config_filename}' not found.")
        print("Please run the previous cell to create it.")
    except json.JSONDecodeError:
        print(f"Error: Could not parse '{config_filename}'. Please check its format.")


if __name__ == '__main__':
    main()