import mailbox
import quopri
import re
import requests
import os
from urllib.parse import unquote, urlparse, parse_qs
import time

href_pattern = r'href="([^"]*)"'
# Path to your Thunderbird Local Folders
local_folders_path = "C:/Users/onepi/AppData/Roaming/Thunderbird/Profiles/5wpb27lz.default-release/Mail/Local Folders/Kindle Notebook"
output_folder = "C:/Projects"

# Create the output and cache folders if they don't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(cache_folder):
    os.makedirs(cache_folder)

mbox = mailbox.mbox(local_folders_path)
for message in mbox:
    # Access email attributes
    subject = message['subject']
    from_address = message['from']
    
    # Access email content
    email_content = message.get_payload()
    
    # Process or save the email content as needed
    print(f"Subject: {subject}")
    print(f"From: {from_address}")
    for index, part in enumerate(email_content):
        decoded_html = quopri.decodestring(part.get_payload().encode('utf-8')).decode('utf-8')
        
        href_matches = re.findall(href_pattern, decoded_html)
        for href in href_matches:
                if "kindle-content-requests-prod" in href:

                    # Download the PDF
                    url = unquote(href)
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query)

                    # Extract the direct link to the PDF file
                    pdf_filename = query_params.get('U', [''])[0].split("?")[0]
                    # pdf_filename = os.path.join(output_folder, os.path.basename(pdf_url))
                    cache_path = os.path.join(cache_folder, pdf_filename)
                    output_path = os.path.join(output_folder, pdf_filename)
                    
                    # Use the original URL instead
                    pdf_url = href
                    response = requests.get(pdf_url)
                    with open(pdf_filename, 'wb') as pdf_file:
                        pdf_file.write(response.content)
                   
                   
                    print(f"Downloaded PDF Link (Part {index}): {pdf_url}")
                    print(f"Saved as: {pdf_filename}")