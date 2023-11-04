import mailbox
import quopri
import re

href_pattern = r'href="([^"]*)"'
# Path to your Thunderbird Local Folders
local_folders_path = "C:/Users/onepi/AppData/Roaming/Thunderbird/Profiles/5wpb27lz.default-release/Mail/Local Folders/Kindle Notebook"

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
        print(f"Decoded HTML Content (Part {index}):\n{decoded_html}")
        
        href_matches = re.findall(href_pattern, decoded_html)
        # soup = BeautifulSoup(part, "html.parser")
        # formatted_content = soup.get_text()
        # print(f"{index}:\nEmail Content (formatted):\n{formatted_content}")
        print(f"Decoded HTML Content (Part {index}):\n{href_matches}")