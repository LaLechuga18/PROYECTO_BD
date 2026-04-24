# app.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from views.login import LoginView

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()