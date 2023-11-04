# KindleScribe Email PDF Downloader

This project allows you to automatically download PDF attachments from emails in your Thunderbird Local Folders that contain specific links. It is particularly useful for KindleScribe users who receive emails with Kindle notebook PDF links and want to automatically save them to a local folder.

## Getting Started

To use this project, you'll need to specify the path to your Thunderbird Local Folders. These folders contain the emails you want to process.

### How to Choose the Email Path

1. **Open Thunderbird**: Open your Thunderbird email client.

2. **Access Local Folders**: In Thunderbird, you may have a section called "Local Folders." These folders store emails locally on your computer.

3. **Select the Appropriate Local Folder**: Choose the Local Folder that contains the emails you want to process. This folder can be a specific account, a folder you've created, or any other relevant location.

4. **Specify the Path**: You will need to specify the path to this local folder in the project settings.

   - For Windows: The path may look like `C:\Users\YourUsername\AppData\Roaming\Thunderbird\Profiles\xxxxxxxx.default\Mail\Local Folders\YourLocalFolderName`.

   - For macOS: The path may look like `/Users/YourUsername/Library/Thunderbird/Profiles/xxxxxxx.default/Mail/Local Folders/YourLocalFolderName`.

   - For Linux: The path may look like `/home/YourUsername/.thunderbird/xxxxxxx.default/Mail/Local Folders/YourLocalFolderName`.

   Replace `YourUsername` with your actual username and `YourLocalFolderName` with the name of the local folder you want to process.

### Project Settings

In the `config.json` file, you can specify the email path, output folder, and other settings:

```json
{
    "email_path": "C:\\Users\\YourUsername\\...",
    "output_folder": "C:\\Users\\YourUsername\\Downloads\\PDFs",
    "max_retries": 3
}
```

Make sure to replace the sample paths with your actual paths.

## Usage

1. After setting up the project and specifying the email path, run the script to automatically process emails in the specified folder.

2. The script will download PDF attachments from emails that contain specific links and save them to the output folder.

3. The script will skip emails that are older than 7 days to avoid downloading outdated content.

4. You can configure the number of download retries and other settings in the `config.json` file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
