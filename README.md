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