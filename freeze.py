from flask_frozen import Freezer
from app import app  # Certifique-se de que o nome aqui corresponde ao nome do seu arquivo principal

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()