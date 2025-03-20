This is a simple **Flask** Blog project.

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
