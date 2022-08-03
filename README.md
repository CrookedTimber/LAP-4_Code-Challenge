# LAP-4_Code-Challenge

## Flask API

### Installation

- Clone repo and `cd` into project folder
    - Run "pipenv install" to install the required dependencies to your virtual environment.
  

###  Usage

- Run "pipenv run start" to start the app in "http://127.0.0.1:5000"
    Go to "http://127.0.0.1:5000/all_urls" to see all urls in the SQL database.

---

## Chrome/Brave Browser Extension created with React

### Installation

- With the repo files already in your system folder open either Chrome or Brave Browser:
- Open the extension manager of your browser.
- Allow the developer mode with the switch on the top right corner.
- Click on the "Load Unpacked" option on the developer bar (top left corner).
- On the popup, navigate to the folder ".\Short-Ext\dist" of the project and click on "Select Folder".
- The extension will become accesible in the extensions menu of the browser.
* Note: The Flask API must be running on "http://127.0.0.1:5000" for the extension to work


## Pending Work

- Styling
- Adding a "Copy to Clipboard" button next to the short URL.
- Deployment

## Known Bugs

- The forms in both the API templates and the extension fail to validate the input to only allow URLs to be submitted.
  
