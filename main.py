from database import init_db
from menu import Menu

def main():
  # Initialize the database
    init_db()
  
  # Create and start the menu
    menu = Menu()
    menu.start()

if __name__ == "__main__":
    main()