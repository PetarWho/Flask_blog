This is a simple **Flask** Blog project.

---

## Prerequisites and setup
This app uses **MySQL** as database, so you will need one as well in order to run it (or change the database in the `.env` file).
You will also need **Python** installed on your machine.


## Setup:
1. Packages

All required Python packages are listed in `requirements.txt` file, and all packages can simply be installed by following these steps:
- Open a Terminal in the project folder
- Run this command:
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

## Enjoy 🎉🚀
