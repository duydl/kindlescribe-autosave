import mailbox
import quopri
import re
import requests
import os
import time
from urllib.parse import unquote, urlparse, parse_qs


href_pattern = r'href="([^"]*)"'
# Path to your Thunderbird Local Folders
local_folders_path = "C:\\Users\\onepi\\AppData\\Roaming\\Thunderbird\\Profiles\\5wpb27lz.default-release\\Mail\\Local Folders\\Kindle Notebook"
output_folder = "C:\\Users\\onepi\\OneDrive\\LogSync"

# Maximum number of download retries
max_retries = 3

# Create the output and cache folders if they don't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

mbox = mailbox.mbox(local_folders_path)
for index, message in enumerate(mbox):
    # Access email attributes
    subject = message['subject']
    from_address = message['from']
    
    # Access email content
    email_content = message.get_payload()
    
    # Process or save the email content as needed
    print(f"Subject: {subject}")
    print(f"From: {from_address}")
    
    for retry in range(max_retries):
        try:
            for part in email_content:
                decoded_html = quopri.decodestring(part.get_payload().encode('utf-8')).decode('utf-8')
                href_matches = re.findall(href_pattern, decoded_html)
                for href in href_matches:
                    if "kindle-content-requests-prod" in href:
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

                        print(f"Downloaded PDF Link (Part {index}): {pdf_url}")
                        print(f"Saved as: {pdf_filename}")
            break
        
        except requests.exceptions.RequestException as e:
            print(str(e))
            continue
                        
    else:
        print(f"Exceeded maximum number of download retries for PDF (Part {index}).")
    
    time.sleep(3)