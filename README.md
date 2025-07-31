## Description
This is a simple **Flask** Blog project, utilizing Markdown and the Obsidian notebook theme called **Spectrum** by *Wiktoria Mielcarek*.

- You can login or create an account.

  ![image](https://github.com/user-attachments/assets/3b174625-f888-4f3e-9d1f-4d2e8c32b5a6)

- While logged in, you can see all the articles that have been created on the app.

  ![image](https://github.com/user-attachments/assets/7f0804de-fb24-4f42-940f-7035a6ffcb94)

- You can read existing articles.

  ![image](https://github.com/user-attachments/assets/4b757c97-984c-499b-82e3-d6dd17aca248)

- You can create a new post.

  ![image](https://github.com/user-attachments/assets/2c014e5c-a7c8-4e1c-b639-3d25188b0456)

- When you create a post, you can edit or delete it.

  ![image](https://github.com/user-attachments/assets/cec99628-a288-497e-a076-8d5c326b3c8c)

- Each article has views count - measuring your post's performance (how many people have viewed your post).

  ![image](https://github.com/user-attachments/assets/e7d0903a-b247-48ca-8ad8-7e4ed0c12bd5)

- You get messages for successful operations or errors.

  ![image](https://github.com/user-attachments/assets/c2d68731-5e40-4670-9bd9-c465fb98f554)


---

## Prerequisites and setup
This app uses **MySQL** as database, so you will need one as well in order to run it (or change the database in the `.env` file).
You will also need **Python** installed on your machine.


## Setup:
1. Packages

All required Python packages are listed in `requirements.txt` file, and all packages can simply be installed by following these steps:
- Open a Terminal in the project folder and create `venv` (virtual environment) folder, by running this command:
```bash
python -m venv venv
```
- Now activate the virtual environment so that packages are encapsulated and associate with this project only (this way you will not install the packages on your machine but only in this project inside the `venv folder`. To activate it, run this command in the terminal:

> For WINDOWS:
```bash
venv\Scripts\activate
```

> For LINUX/MAC:
```bash
source venv/bin/activate
```

- Now inside the virtual environment install the packages by running this command:
```bash
pip install -r ./requirements.txt
```

2. Environment Variables

> IMPORTANT: You will have to create a `.env` file (or rename the `.env.example` file to `.env`)

Inside the `.env` file you will have to enter your database credentials in order to establish connection, and also enter a *SECRET_KEY* which can be randomly generated or just typed by hand.

## Run the app:
After setting everything up, you can simply run the app using:
```bash
flask --app main.py run
```

If you want to change the port as by default the app will run on port **5000**, you can change the port in the `main.py` file or even easier you can just add the flag **port** to the run command, like this:
```bash
flask --app main.py run --port 5001
```  

### ISSUES/ERRORS - If for any reason you cannot run the app, follow this guide:
1. Make sure that you have activated the virtual environment `venv`
2.  Make sure the packages are installed and then execute the command to run the app.
3. If you still have issues and cannot run it, open a Terminal as Administrator, navigate to the folder and then try to execute the command.
4. And as final option, instead of using `flask --app main.py run` try running it using `python main.py`

## Enjoy 🎉🚀
