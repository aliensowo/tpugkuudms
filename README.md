# DB
    
    the local development uses sqlite as a database 
    to use the program in the settings.py file, change the SQLALCHEMY_DATABASE_URL parameter
    The database for local development is stored in the file sqlite.db 
    The database schema is set up and restored automatically    

# First steps

    git clone https://github.com/aliensowo/tpugkuudms.git
    cd tpugkuudms
    pip install -r requirements.txt

# Start in develop mode project
    python main.py

# Start in prod mode project

    dist/main.exe

# Generate .py from .ui files

    python gui_generator.py

# Make build

    pyinstaller --onefile -w .\main.py

# Fast auto Restore DB 

    python restore_db_data.py