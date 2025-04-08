# Crypto Af: Cryptocurrency Exchange Platform

#### 📽️ Video Demo: [Insert URL Here]

## 🤝 Collaborative Work

This project was developed by two people, our git username **AngeloPV** and **felipesssoa**. Below is a summary of the work done by each of us:

### AngeloPV
- Designed the overall **Model-View-Controller (MVC)** architecture. 
- Organized **Poetry** to define the project's dependencies and set up configuration from the `.env` file.
- Created the **helper folder** with reusable files, including CRUD operations related to the database for efficient use across the project, and also implemented the **send_email** functionality.
- Structured the **controller** with folders for `private_pages`, `protected_pages`, and `public_pages` to separate access controls for logged-in users and non-logged-in users. 
- Implemented **Flask routes** and **blueprints** for modular components and added a URL verification mechanism to determine if a user can access a specific page.
- Configured **SocketIO** to be used within the project, including the setup in the `app.py` file.
-  Configured **Git** for version control and linked the project to an online repository.
  
#### User Pages
- Developed the **login** and **user registration** functionality, including designing the HTML layout, implementing the form logic, and styling with **CSS** to create a user-friendly interface.
- Designed and implemented the **forgot password** page, including the HTML structure, form handling, and **CSS** for styling.


#### Pages When the user is logged in:
- Developed the **real-time notifications** feature using **SocketIO**, which allows users to receive updates in real time. This includes designing the **HTML** layout and implementing the **CSS** for the notification system on the front-end, as well as setting up the back-end logic to trigger notifications based on certain actions.
- Created the **exchange system** for cryptocurrency trading, utilizing **SocketIO** for real-time updates and bidirectional communication. Integrated the **CoinGecko API** to fetch live cryptocurrency prices, ensuring the exchange system displays up-to-date values for transactions. Also designed the **HTML** layout and styled the pages with **CSS** to provide a clean and responsive user interface.

### In general
I was responsible for the entire configuration aspect of the project, including organizing the MVC architecture, setting up dependencies with Poetry, creating auxiliary folders (helpers) with reusable functionalities such as CRUD operations and email sending, as well as configuring SocketIO for real-time communication and integrating version control using Git. I also developed various features and pages, including the registration and login pages, forgot password, notifications, and the cryptocurrency exchange system/page.<br><br>

---

### felipesssoa

#### Main accomplishments
- Developed the `dashboard`, front-end and back-end using **plotly framework** to create the dashboards and using **coingecko API** to fetch real-time updated cryptocurrency values.
- Also developed the `account page`, where the user can view and update their data and preferences. I worked on both the back-end and the front-end, also developed the `logout` and `delete account` funcionality inside the account page
- Developed the `manage page` back-end and front-end, also using **coingecko API** to fetch real-time cryptocurrencies values, and developed the `sold functionality` inside the manage page
- Developed the `buy page` back-end and front-end also using **coingecko API**
- Developed the `deposit`, `deposit confirm` and `my deposit` pages, back-end and front-end
- Also implemented the functionality to **change** the **profile picture**

#### Focused on the front-end
- Defined the `color palette` and designed the `pages layout`
- Added themes to the site, including a `light theme` and a `dark theme`
- Developed the `layouts` in the **templates folder** these were implemented on almost all pages of the site, along with other more situational features, such as the layout of the forms
- Also developed the `modals` in website and the **page for verifying the code sent by email**

### In general 
I developed functionalities related to `user data`, `cryptocurrency buying and selling` and the transaction history, `deposits` and related features such as **history and balance**. On the front-end, I worked on the `color palette`, `pages layout`, `themes`, `layouts archives`, `modals` and some pages less important.
<br><br>


# 📝 Description:

Crypto Af is an advanced cryptocurrency exchange platform designed to enable seamless buying, selling, and trading of cryptocurrencies like Bitcoin (BTC) and Ethereum (ETH). It provides a secure and user-friendly interface for users to manage their digital assets effectively. By integrating real-time market data, robust security features, and an intuitive design, Crypto Af serves as a reliable solution for both novice and experienced cryptocurrency enthusiasts.

>WARNING: 
 All the money and cryptocurrency used on the site are purely fictitious, and no real value will be accounted for.
<br><br>

## 💻 Project Structure and Technologies

The project follows the **Model-View-Controller (MVC)** design pattern to ensure separation of concerns, scalability, and maintainability:

- **Model**: Handles the database interactions and defines schemas for user accounts, transactions, and notifications.

- **View**: Uses **Flask** with **Jinja** templates and **HTML5** for rendering dynamic and responsive web pages.

- **Controller**: Manages the logic and routes using **Flask blueprints** to organize the application into modular components. The controller is further organized into:
  - **public_pages**: Contains pages that can be accessed without logging in.
  - **private_pages**: Contains pages that require the user to be logged in to access.
  - **protected_pages**: Contains pages with more restricted access, requiring additional permission checks.

- **Helper**: A folder that includes reusable files, such as CRUD operations and utility functions, that can be used throughout the entire project to avoid code repetition.

- **Static**: Stores static assets like **CSS**, **images**, and **JavaScript** files, ensuring efficient and organized access to these resources.

- **Templates**: Contains **HTML** files rendered by **Jinja**, which form the structure of the dynamic web pages.


### Package Management
The project uses **Poetry** to manage dependencies efficiently, ensuring a reproducible and organized environment.

---

### Flask Features and Integrations

- **Flask:** provides the core framework.
- **Jinja templating:** is used for rendering dynamic HTML.
- **Flask-SocketIO:** enables real-time updates and communication between users.
- **Flask Blueprints** are used to organize the application into modular components, making it easier to scale and maintain.

---

### APIs Utilized

- **CoinGecko API**: Retrieves the latest cryptocurrency prices and market data.
- **Nominatim API**: Fetches location details based on ZIP codes.
- **ViaCEP API**: Provides detailed information about ZIP codes, cities, and regions in Brazil.

---

### JavaScript Enhancements

- **Flask-SocketIO**: Ensures real-time communication and updates, enhancing interactivity.
- **SweetAlert2**: Utilized for creating custom, responsive pop-up alerts to improve user experience and provide real-time feedback during actions such as form submissions and notifications.


### Collaboration and Version Control

We use **GitLens** to enhance our collaboration and streamline the development process. GitLens allows us to work together efficiently by providing powerful Git features directly in the editor, enabling us to track changes, view file history, and make commits with ease. It helps the team to:

- Review code changes and commit history directly in the editor.
- Collaborate on features and resolve conflicts with more clarity.
- Track contributions and make informed decisions about modifications using Git commands.

<br><br>

## 🚀 Overview of Features:

1. **User Authentication and Security:**   
  Secure registration and login system with email verification.
  <br>All passwords are encrypted.
  <br><br>
  
    - *Login*
      - Log in using email or username, with your password being encrypted
      - The data will be verified if you are registered and if the account has email verification
    - *Register*
      - Checking whether each field is respectively valid, and if it is, it will be registered in the database
      - If you register, an email with a code will be sent to the user's email, and the user will need to enter the email code in the field to verify their account
    - *Forgot Password*
      - The user needs to enter their registered email and if it exists, an email will be sent with a code so that you can reset it, if the code is correct, the password reset form will appear
<br><br>

2. **Dashboard**
    Main page of website, for viewing detailed information about their cryptocurrencies, interacting with real-time charts, and accessing important financial data. The interface is designed to be intuitive and user-friendly, allowing for organized and clear access to information.
    <br>
      - Graphical Visualization
        - Real-time charts displaying Bitcoin (BTC) and Ethereum (ETH) data, enabling users to track market fluctuations live.
        - Historical charts of user transactions, allowing users to analyze the performance of their assets over time.
        - Detailed graphs of user spending, with options to view spending for the last 6 days or total spending history

      - Four Digits Password Management
        - This password is required when the user buy, trade or sell any criptocurrency, without the password, the user can't proceed
      
      - Data updates
        - The page refreshes every 10 seconds to ensure cryptocurrency and transaction information is up-to-date.
        - Data updates (charts and financial information) are optimized with a time check that ensures updates occur only every 30 seconds, preventing server overload.

      - User location
        - When the page loads, a pop-up will appear asking for the user's location. If the user accepts, their latitude and longitude will be sent to the Nominatim API, which will be responsible for getting the user's approximate postal code and saving it to the database. If the user refuses, it will be marked as unauthorized.
    <br><br>

3. **Wallet Management**  
  Managing your wallet offers several options to efficiently control your cryptocurrencies:  
  <br>
    - *Cryptocurrency Buy*  
      To buy a coin, it is necessary to first check the status. If it is available, when the user clicks on it, a pop-up will appear asking the user to enter the amount to be purchased and a four-digit password. If it is unavailable, nothing will happen.  

    - *Cryptocurrency Manage*  
      On the manage page, the user can see their balance in Bitcoin and Ethereum, respectively, and view the history of their latest transactions (purchase, exchange, or sale). 

    - *Sell*    
      The user can sell a desired amount of cryptocurrency, as long as they have an equal or greater amount than what will be sold. To perform the action, a four-digit password will also be required.

    - *Crypto-to-Crypto Exchange*  
      Real-time trading between users who hold cryptocurrencies. A user-friendly trading interface.  
      - View Trades<br>
        On the trade home page the user can see other users' trades.
        <br> And if the user has the specific currency, they can exchange it with another user, and for confirmation they will need a 4-digit password.

      - Add Trades<br>
        The user can create his own trade, choosing the currency he wants to exchange and the one he will receive in exchange, and respectively the quantity of the currency, and the minimum value that other users can start exchanging.
        <br>Afterwards, the user will be asked for a 4-digit password for verification.

      - Delete Trades<br>
        If the user has created a trade and wants to delete it, they will have the right to do so only if no other user is currently in the process of trading with that specific trade. Additionally, the system will require a 4-digit password for confirmation.

      - Search Trades<br>
        The user can search for trades based on the criteria they select: the type of currency, the maximum exchange amount, and the minimum exchange amount. However, only the type of currency is mandatory.  
  <br><br>

4. **User Notifications:**

   - Once a feature is completed by the user, a new notification will appear for them.
   - Notifications have 3 types if the user wants to organize: default, archive and favorites
<br><br>

5. **Deposit**
  <br>
  - Deposit
    On the deposits page, the user will enter an amount to be deposited and select the currency. A QR code will appear, and after scanning the QR code, the user will be redirected to a confirmation page. Once the action is completed, the amount will be deposited into the account (it is important to note that no real money will be deposited, and all the money is fictitious)

  - My deposits
    - Account balance
      Display the user balance

    - Wallet
      If the user has a wallet, will be displayed a model with the wallet details, else, will be displayed just a button that when the user click, will be created a wallet

    - Deposit history
      Display every deposit made by the user
  <br><br>

6. **Account**  
  Page where the user's preferences and data are stored
  <br>
    - Edit
      When the user clicks in the edit button, will be displayed a editable camp to edit the data/preference,
      the user only needs to select the data they want to change. After that, the user will be redirected to a page where they will be asked for their password, and an email containing a 6-digit code will be sent for user validation. After correctly entering the 6 digits, the user will be redirected again, but this time they will enter the updated data, such as the new name or the new password. It will be necessary to enter the same data in both the field and the confirmation field. After this, the edit will be made

    - Logout
      Log out the user.

    - Delete account
      Make the user's account inactive, preventing the user from accessing the account, but their transactions remain saved in the database
  <br><br>  

## ⚙️ How to Run the Project
This project was developed using Poetry, a dependency and package management tool for Python. To run the project, follow the steps below:

1. Install Poetry
Before anything else, you need to have Poetry installed. If you don't have it yet, follow the instructions in the official [Poetry documentation](https://python-poetry.org/) to install it on your system.

2. Create a Project Folder with Poetry
Once you have Poetry installed, create a folder for your project. To do this, in your terminal, run the following command inside the directory where you want to create the project:

    > poetry new project-name --src

    This will create a new folder with the necessary structure for the project, including the src folder (where the project code will be stored). Make sure that the folder created contains all the project files that are inside the finalProject folder, excluding the poetry files themselves, for example poetry lock, .env and others.

3. Manage Project Dependencies
Inside the `project-name folder`, run the following commands to install the dependencies:
    > `poetry lock`: This command creates or updates the poetry.lock file, which ensures that all project dependencies are locked to specific versions to guarantee consistent behavior across different environments.

    > `poetry install`: This command installs all the dependencies specified in the pyproject.toml file, which includes the libraries and packages necessary for your project to work. 

4. Configure the file `.env`:<br>
  - To test email sending, you need to configure a .env file with your email and Google App password. <br>
    > GMAIL_MAIL_SERVER=smtp.gmail.com <br>
      GMAIL_MAIL_PORT=587 <br>
      GMAIL_MAIL_USERNAME= your_gmail@gmail.com <br>
      GMAIL_MAIL_PASSWORD= Google app password <br>
      GMAIL_MAIL_USE_TLS=True <br>
      GMAIL_MAIL_USE_SSL=False 

    <br>How to Get Your Google App Password: <br>
    Go to this [Google page](https://support.google.com/accounts/answer/185833?hl=En) to learn how to generate an app password.<br><br>

    In the .env file, change the following environment variables:

    > EMAIL=your-email@gmail.com <br>
    EMAIL_PASSWORD=your-google-app-password

    <br>
    In addition to sending email from Google, you need to configure Outlook email so that the site can send email to users who register as Outlook: <br><br>

    > OUTLOOK_MAIL_SERVER= smtp-mail.outlook.com <br>
    OUTLOOK_MAIL_PORT= 587 <br>
    OUTLOOK_MAIL_USERNAME= your_outlook@outlook.com <br>
    OUTLOOK_MAIL_PASSWORD= your_outlook_password <br>
    OUTLOOK_MAIL_USE_TLS= True <br>
    OUTLOOK_MAIL_USE_SSL=False 

    <br>How to get your Outlook App password: <br>
    Visit this [Microsoft page](https://support.microsoft.com/en-us/account-billing/how-to-get-and-use-app-passwords-5896ed9b-4263-e681-128a-a6f2979a7944) to learn how to generate an application password. <br><br>
    
    In the .env file, change the following environment variables:
    > OUTLOOK_MAIL_USERNAME= your_outlook@outlook.com <br>
    OUTLOOK_MAIL_PASSWORD= your_outlook_password

    <br>Note: Do not share your app password with anyone, as it allows access to sending emails through your Google account. <br><br>

  - You need to download the database and run it on a system capable of hosting a database server (such as MySQL or MariaDB). The current project uses XAMPP with localhost as the default database host. If you want to change the database settings, you can do so by modifying the .env file:
    > DB_HOST=localhost <br>
      DB_USER=root <br>
      DB_PASSWORD= <br>
      DB_DATABASE=cs50 
  
5. Project Structure <br>
The project is structured as follows:

    - src/
      - finalProject/
        - __init__.py
        - other-folders-and-files.py
    - poetry.lock
    - pyproject.toml
    - README.md
    - .env
   
    <br>`pyproject.toml` Configuration: <br>
    Poetry recognizes the finalProject package inside the src folder. In the pyproject.toml file, the package configuration is as follows:

    >[tool.poetry] <br>
    packages = [ <br>
        { include = "finalProject", from = "src" }<br>
    ] <br>

    If you prefer to remove the src folder and place the finalProject package directly in the project root, you will need to change the pyproject.toml file as follows:

    > [tool.poetry] <br>
     packages = [ <br>
        { include = "finalProject" } <br>
    ]<br>

    This will make Poetry look for the package directly in the project root, without the src folder <br><br>



## 🗂️ Key Files and Their Functionality:

1. **.env** 
    - Manages environment variables for the project, including Flask configurations (like SECRET_KEY, DEBUG, and SESSION_COOKIE), email server settings (for Gmail, Yahoo, and Outlook), database connection details, file upload settings, and session management. Loads configurations from the .env file to set up various application parameters, ensuring that sensitive data like passwords and keys are securely managed.

2. **.flaskenv**
    - Defines environment variables for Flask application configuration. Sets FLASK_APP to specify the app instance, FLASK_ENV to indicate the development environment, and FLASK_RUN_EXTRA_FILES to include additional template files for automatic reloading during development.

3. **pyproject.toml**
    - Configures the project settings and dependencies for the Flask application. It defines the project name, version, and description, specifies the Python version, and lists dependencies such as Flask, Flask-Mail, and libraries for validation, QR codes, and socket communication. Additionally, it configures custom scripts and defines development dependencies (e.g., pytest) for testing. The file also specifies the build system using poetry-core.

4. **poetry.lock**
    - The `poetry.lock` file is automatically generated by Poetry when dependencies are installed or updated. It locks the exact versions of all dependencies and their sub-dependencies to ensure consistency across environments. The file contains resolved versions of all the libraries defined in the `pyproject.toml` file, as well as metadata about the installation process. It helps ensure that everyone working on the project or deploying it uses the same versions of dependencies, preventing potential issues caused by version mismatches.

5. **app.py**

    - Initializes the Flask application, registering blueprints to organize routes and modularize functionalities.
    - Calls the file responsible for configuring Flask-SocketIO integration for real-time communication.
    - Defines custom routes to serve static files (such as images and favicon).
    - Manages global notifications accessible in templates.
    - Uses the Config class to load configurations and starts the server locally on port 5000 with WebSocket support.

6. **socketio_setup.py** <br>
    - Configures and initializes Flask-SocketIO for real-time communication.
    - Defines the init_socketio function to initialize the SocketIO instance with the Flask app.
    - Registers blueprints for notifications and trade functionalities, associating them with their respective namespaces (NotificationNamespace and TradeNamespace).
    - Sets up SocketIO to handle real-time communication under the /notifications and /trade routes.


7. **routes.py**<br>
    - Defines the Routes class and manages dynamic routing using the main_routes blueprint.
    - Dynamically registers routes, processes requests based on URL parameters, and integrates logic for controllers and methods.
    - Standardizes route names and methods, verifies parameters, and dynamically loads controllers from the controller directory.
    - Handles errors using a custom Error class if routes or methods are undefined.


8. **verify_page.py**
    - Manages page access control by categorizing and validating routes as public, private, or protected.
    - Dynamically identifies available pages by scanning directories and ensures appropriate access based on session status.
    - Determines the appropriate directory for routing based on the page's type.
    - Returns error messages if access is denied or the page does not exist.


9. **config.py**
    - Loads environment variables from a .env file using the dotenv library.
    - Configures email settings for various providers (Gmail, Yahoo, Outlook) by dynamically loading values from the environment.
    - Provides methods for retrieving secret keys, database configurations, and database URIs, with fallback to default values if necessary.
    - Initializes the Flask app configuration, including session settings, logging, debug options, and cookie configurations.
    - Configures session durations, upload limits, and locale settings.

10. **context_processor.py**
    - Defines the notifications_processor function, which is used to manage and display the count of unread notifications in the session.
    - Checks if the user has viewed the notifications page (viewd_count session key). If so, the unread notifications count is reset to 0.
    - If the user is authenticated (i.e., user_id is in the session), the function retrieves the count of pending notifications using the Count_notifications class.
    - Returns the notification count as a dictionary for use in templates.

11. **renderer.py**
    - Defines the template_render function, which simplifies rendering templates with dynamic data.
    - Accepts a template file name and additional keyword arguments (**data) to pass to the template.
    - Uses Flask's render_template function to render the specified template with the provided data.

## 📁 Folders

- **controller** <br>
    The controller folder in an MVC (Model-View-Controller) framework manages the application's business logic and handles user requests. It acts as an intermediary between the model (data) and the view (user interface). The controllers in this folder receive user input through routes, process the necessary actions (such as interacting with the model), and then render the appropriate view or respond with data. In this project, the file responsible for rendering is renderer.py, which receives the name of the file and the data to be rendered.

    There are 3 more folders inside the controller:
    - `private_pages`: pages that can only be accessed by the user when logging in
    - `public_pages`: pages that the user can access without being logged in
    - `protected_pages`: control pages that the user cannot access, the files have different functionalities, from getting data from cryptocurrencies via the API, to deciding the email provider that will be used

- **models** <br>
    The models folder is responsible for managing the data and business logic of the project. It contains the definitions of data structures, which may include classes representing database tables. Additionally, the folder includes files that handle the database connection, validate data, and implement business rules related to storing and manipulating that information. The main goal of this folder is to interact with the database, ensuring that operations for reading, writing, updating, and deleting data are performed efficiently and securely.

- **helper**<br>
  The helper folder contains utility functions and classes that support the project's main functionality. 
  
    - These reusable components simplify common tasks, such as facilitating database CRUD operations with the files: `helper_select`, `helper_update`, `helper_insert`, and `helper_delete`.

    - Additionally, it includes the `send_email` file,  which handles sending emails to users, and the `generate_code` file, responsible for generating email codes. The validate.py file provides a series of functions to validate various fields, such as validate_email, validate_cpf, validate_phone, validate_password, and encryption.

    - Lastly, the `postal_code` file retrieves the user's address using the Nominatim and ViaCEP APIs.

- **static** <br> 
  The static folder is designated for storing static assets that are served directly to clients. These include resources such as CSS files, JavaScript files, images, and other static content that does not change dynamically.

  - Inside the static folder we have the `css` folder which contains style sheets used to define the visual presentation and layout of the application. Inside there are two more folders:
    - `sweet_alert`: the alert css from the sweet alert library
    - `trade`: the css of the page's modals exchange together with the page's css

  - Inside the static folder, we have the `js` directory, which contains the JavaScript files for the project. Within this directory, there are four additional subfolders:
    - `notifications`: all the JavaScript for the notifications page is located here. On this page, we utilize SocketIO to enable real-time updates without needing to refresh the entire page. For instance, this allows the user to change a notification's status, such as moving it from "Archived" to "Favorites," seamlessly.
    - `register`: the js of the register page is on this page, where we have the cpf and phone masks
    - `sweet_alert`: the js to call the alerts in general is in this folder
    - `trade`: Similar to the notifications folder, this folder contains the JavaScript for the exchange page. It also utilizes SocketIO to establish bidirectional communication between users and enable real-time updates.

  - The `images` folder stores subfolders containing images related to specific parts of the project. For example, the dashboard subfolder contains all the images associated with the dashboard.

- **templates**<br>
  The `templates` folder stores all the HTML files of the project, along with two subfolders.
  - modal: the `modal_trade` subfolder stores the modals related to the exchange page.
  - layouts: the `layouts` folder contains HTML templates that are used in other files within the templates folder. For example, form.html provides a layout that is reused in other pages that include a form.
<br><br> 

### 🎨 Design Choices and Rationale:
The layout was chosen to make efficient use of screen space without overwhelming the user with too much information or leaving too little, which could hinder comprehension. The goal was to strike a balance between an attractive and informative layout. A modern approach was chosen, using 'main' tags for the primary content area, separating it from the background to create a more original aesthetic without sacrificing the simplistic traits. Excessive use of gradients was avoided, as they would interfere with the minimalism central to the layout. Colors were selected to align with the site's theme, such as orange for Bitcoin and blue for Ethereum, with variations of these hues. For other colors, simpler shades like white, black, and gray were chosen, altering their priority based on the theme. The background color of the light theme corresponds to the text color of the dark theme, and vice versa for the other colors. <br> <br>

# Conclusion:

Crypto Af is more than just a trading platform; it’s a gateway for users to explore the cryptocurrency ecosystem securely and efficiently. By focusing on security, user experience, and scalability, the project aims to bridge the gap between traditional finance and the digital currency world.

