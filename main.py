# Main.py
import sys
from PyQt5.QtWidgets import QApplication
from HomeScreen import HomeScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Root directory for home screen
    root_dir = "C://Instructions Gen 4"
    folder_type = "Make"  # Define folder_type here
    home_screen = HomeScreen(root_dir, folder_type)
    home_screen.show()

    sys.exit(app.exec_())
