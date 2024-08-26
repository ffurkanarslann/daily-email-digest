# Unread Email Checker

This Python script connects to an IMAP email server and retrieves unread emails from the previous day across multiple folders. It's designed to help you stay on top of your recent, unread messages.

## Features

- Connects to IMAP servers using SSL
- Retrieves unread emails from the previous day
- Checks multiple folders, excluding specified ones
- Displays subject, sender, and date for each unread email
- Uses environment variables for secure credential management

## Prerequisites

- Python 3.6+
- `python-dotenv` library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/unread-email-checker.git
   cd unread-email-checker
   ```

2. Install the required dependencies:
   ```
   pip install python-dotenv
   ```

3. Create a `.env` file in the project root and add your email credentials:
   ```
   USERNAME=your_email@example.com
   PASSWORD=your_email_password
   IMAP_SERVER=imap.your-email-provider.com
   IMAP_PORT=993
   ```

## Usage

Run the script with:

```
python main.py
```

The script will connect to your email server, check for unread emails from yesterday in various folders, and display the results.

## Customization

- Add or modify the `IGNORED_FOLDERS` in your `.env` file to exclude additional folders from being checked. For example:
  ```
  IGNORED_FOLDERS=Spam,Trash,Archive
  ```
- Adjust the time range by modifying the `timedelta` value in the `get_unread_emails()` function.

## License

[MIT License](LICENSE)

## Planned Features

- Automatic deletion of promotional emails using AI
- Daily email digest summarized by AI
- Gmail integration
- Separate integrations for GPT and Claude AI