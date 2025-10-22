import PySide6
import socket
import sys
from views.interface import Ui_MainWindow
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QMainWindow, QWidget, QApplication, QComboBox
from PySide6.QtCore import Qt
from controller import TaskController
print(PySide6.__version__)
print(PySide6.QtCore.__version__)



# print(f"IP publique : {get_public_ip()}")

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    
    # Initialiser le contrôleur de tâches
    self.task_controller = TaskController(self.ui, self)
    
    # Récupérer les QVBoxLayout et appliquer l'alignement
    self.setup_layouts()
    
    # Connecter les boutons
    self.connect_buttons()
  
  def setup_layouts(self):
    # Récupérer verticalLayout_1 (dans le premier scrollArea)
    if hasattr(self.ui, 'verticalLayout_1'):
      vertical_layout_1 = self.ui.verticalLayout_1.layout()
      if vertical_layout_1:
        vertical_layout_1.setAlignment(Qt.AlignTop)
    
    # Récupérer verticalLayout (dans le deuxième scrollArea)
    if hasattr(self.ui, 'verticalLayout_2'):
      vertical_layout = self.ui.verticalLayout_2.layout()
      if vertical_layout:
        vertical_layout.setAlignment(Qt.AlignTop)
  
  def connect_buttons(self):
    # Connecter le bouton avec l'objectName "create"
    create_button = self.findChild(QPushButton, "create")
    if create_button:
      create_button.clicked.connect(self.task_controller.create_new_task)
    
    # Connecter le bouton avec l'objectName "save"
    save_button = self.findChild(QPushButton, "save")
    if save_button:
      save_button.clicked.connect(self.task_controller.save_task)
    
    # Connecter le bouton avec l'objectName "createComment"
    create_comment_button = self.findChild(QPushButton, "createComment")
    if create_comment_button:
      create_comment_button.clicked.connect(self.task_controller.create_comment)
    
    # Connecter le bouton avec l'objectName "delete_2"
    delete_button = self.findChild(QPushButton, "delete_2")
    if delete_button:
      delete_button.clicked.connect(self.task_controller.delete_task)
    
    # Connecter le ComboBox avec l'objectName "filterStatus"
    filter_combo = self.findChild(QComboBox, "filterStatus")
    if filter_combo:
      filter_combo.currentTextChanged.connect(self.task_controller.filter_tasks_by_status)
  

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())