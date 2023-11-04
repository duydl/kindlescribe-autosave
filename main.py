import mailbox
import quopri
import re
import requests
import os
import time
import json
from urllib.parse import unquote, urlparse, parse_qs
from datetime import datetime, timedelta, timezone

# Function to prompt the user for settings
def get_user_settings():
    settings = {
        "email_path": input("Enter the path to your Thunderbird Local Folders: "),
        "output_folder": input("Enter the output folder for saving downloaded PDFs: "),
        "max_retries": int(input("Enter the maximum number of download retries: "))
    }
    return settings

# Function to load or create configuration settings
def load_settings():
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            settings = json.load(file)
    else:
        settings = get_user_settings()
        with open("config.json", "w") as file:
            json.dump(settings, file)
    return settings

# Function to check if an email is older than 7 days
def is_email_old(email_date, days=7):
    now = datetime.now(timezone.utc)
    email_date = datetime.strptime(email_date, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=timezone.utc)
    print(now, email_date)
    return (now - email_date) > timedelta(days=days)

# Main function to process emails
def process_emails():
    # Load or create settings
    settings = load_settings()

    # Open the mbox file
    href_pattern = r'href="([^"]*)"'

    # Path to your Thunderbird Local Folders
    email_path = settings["email_path"]
    output_folder = settings["output_folder"]

    # Maximum number of download retries
    max_retries = settings["max_retries"]

    mails = mailbox.mbox(email_path)

    for index, message in enumerate(mails):
        email_date = message['Date']
        
        # Check if the email is older than 7 days, and skip if it is
        if is_email_old(email_date):
            continue
        
        # Access email attributes
        subject = message['subject']
        from_address = message['from']
        
        # Access email content
        email_content = message.get_payload()[0]
        
        # Process or save the email content as needed
        print(f"Subject: {subject}")
        print(f"From: {from_address}")
        
        for retry in range(max_retries):
            try:
                decoded_html = quopri.decodestring(email_content.get_payload().encode('utf-8')).decode('utf-8')
                href = re.findall(href_pattern, decoded_html)
                href = [link for link in href if "kindle-content-requests-prod" in link][0]

                # Download the PDF
                url = unquote(href)
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)

                # Extract the direct link to the PDF file
                pdf_url = query_params.get('U', [''])[0].split("?")[0]
                pdf_filename = os.path.basename(pdf_url)
                
                output_path = os.path.join(output_folder, pdf_filename)
                
                # Use the original URL instead
                pdf_url = href
                response = requests.get(pdf_url)
                response.raise_for_status()
                with open(output_path, 'wb') as pdf_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            pdf_file.write(chunk)

                # print(f"Downloaded PDF Link (Email No. {index}): {pdf_url}")
                print(f"Saved as: {pdf_filename}")
                break
            
            except requests.exceptions.RequestException as e:
                print(str(e))
                time.sleep(5)
                continue
        else:
            print(f"Exceeded maximum number of download retries for PDF (Email No. {index}).")
        time.sleep(5)
        
if __name__ == "__main__":
    process_emails()