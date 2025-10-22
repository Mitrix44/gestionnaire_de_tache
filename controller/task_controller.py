# -*- coding: utf-8 -*-

import uuid
import json
import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import QMessageBox


class TaskController:
    def __init__(self, ui, main_window):
        """
        Initialise le contrôleur de tâches
        
        Args:
            ui: L'interface utilisateur générée par Qt Designer
            main_window: La fenêtre principale pour les modales
        """
        self.ui = ui
        self.main_window = main_window
        self.selected_task = None
        self.data_folder = "data"
        
        # Créer le dossier data s'il n'existe pas
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        
        # Charger toutes les tâches au démarrage
        self.load_all_tasks("Tous")
    
    def create_new_task(self):
        """
        Crée une nouvelle tâche avec un UUID unique
        """
        # Générer un UUID unique
        task_id = str(uuid.uuid4())
        
        # Créer les dates (aujourd'hui et demain)
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        # Créer l'objet tâche
        task_data = {
            "ID": task_id,
            "Titre": "Nouvelle tâche",
            "Description": "Nouvelle description",
            "DateStart": today.strftime("%Y-%m-%d"),
            "DateEnd": tomorrow.strftime("%Y-%m-%d"),
            "Status": "À faire",
            "Commentaires": []
        }
        
        # Créer le fichier JSON dans le dossier data
        file_path = os.path.join(self.data_folder, f"{task_id}.json")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(task_data, f, ensure_ascii=False, indent=2)
            
            # Définir cette tâche comme selected_task
            self.selected_task = task_data
            
            # Mettre à jour les champs UI
            self.update_ui_with_task(task_data)
            
            # Rafraîchir l'affichage des tâches
            self.load_all_tasks("Tous")
            
            print(f"Tâche créée avec succès : {task_id}")
            
        except Exception as e:
            print(f"Erreur lors de la création de la tâche : {e}")
    
    def save_task(self):
        """
        Sauvegarde la tâche sélectionnée
        """
        # Vérifier si une tâche est sélectionnée
        if not self.selected_task:
            self.show_info_message(
                "Aucune tâche n'est sélectionné",
                "Veuillez d'abord créer ou sélectionner une tâche avant de sauvegarder."
            )
            return
        
        try:
            # Récupérer les données depuis l'interface utilisateur
            task_data = self.selected_task.copy()
            
            # Mettre à jour les données avec les valeurs actuelles de l'UI
            if hasattr(self.ui, 'selectedTitle'):
                task_data["Titre"] = self.ui.selectedTitle.text()
            
            if hasattr(self.ui, 'selectedDescription'):
                task_data["Description"] = self.ui.selectedDescription.toPlainText()
            
            if hasattr(self.ui, 'selectedStartDate'):
                task_data["DateStart"] = self.ui.selectedStartDate.date().toString("yyyy-MM-dd")
            
            if hasattr(self.ui, 'selectedEndDate'):
                task_data["DateEnd"] = self.ui.selectedEndDate.date().toString("yyyy-MM-dd")
            
            if hasattr(self.ui, 'selecteStatus'):
                task_data["Status"] = self.ui.selecteStatus.currentText()
            
            # Sauvegarder le fichier JSON
            file_path = os.path.join(self.data_folder, f"{task_data['ID']}.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(task_data, f, ensure_ascii=False, indent=2)
            
            # Mettre à jour selected_task avec les nouvelles données
            self.selected_task = task_data
            
            # Rafraîchir l'affichage des tâches
            self.load_all_tasks("Tous")
            
            # Afficher un message de confirmation
            self.show_success_message("Tâche sauvegardé avec succès")
            
            print(f"Tâche sauvegardée : {task_data['ID']}")
            
        except Exception as e:
            self.show_error_message("Erreur lors de la sauvegarde", f"Une erreur s'est produite : {str(e)}")
            print(f"Erreur lors de la sauvegarde : {e}")
    
    def update_ui_with_task(self, task_data):
        """
        Met à jour l'interface utilisateur avec les données de la tâche
        
        Args:
            task_data: Dictionnaire contenant les données de la tâche
        """
        # Mettre à jour le titre
        if hasattr(self.ui, 'selectedTitle'):
            self.ui.selectedTitle.setText(task_data["Titre"])
        
        # Mettre à jour la description
        if hasattr(self.ui, 'selectedDescription'):
            self.ui.selectedDescription.setPlainText(task_data["Description"])
        
        # Mettre à jour les dates
        if hasattr(self.ui, 'selectedStartDate'):
            start_date = datetime.strptime(task_data["DateStart"], "%Y-%m-%d").date()
            self.ui.selectedStartDate.setDate(start_date)
        
        if hasattr(self.ui, 'selectedEndDate'):
            end_date = datetime.strptime(task_data["DateEnd"], "%Y-%m-%d").date()
            self.ui.selectedEndDate.setDate(end_date)
        
        # Rafraîchir l'affichage des commentaires
        self.refresh_comments_display()
    
    def clear_comments_view(self):
        """
        Vide la vue des commentaires (supprime seulement les frames de commentaires)
        """
        # Vider le layout des commentaires (verticalLayout)
        if hasattr(self.ui, 'verticalLayout_2'):
            layout = self.ui.verticalLayout_2.layout()
            if layout:
                # Supprimer seulement les frames de commentaires (QFrame)
                widgets_to_remove = []
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        # Supprimer seulement les QFrame (frames de commentaires)
                        from PySide6.QtWidgets import QFrame
                        if isinstance(widget, QFrame):
                            widgets_to_remove.append(widget)
                
                # Supprimer les widgets identifiés
                for widget in widgets_to_remove:
                    layout.removeWidget(widget)
                    widget.deleteLater()
    
    def create_comment(self):
        """
        Crée un nouveau commentaire pour la tâche sélectionnée
        """
        # Vérifier si une tâche est sélectionnée
        if not self.selected_task:
            self.show_info_message(
                "Aucune tâche sélectionnée",
                "Veuillez d'abord créer ou sélectionner une tâche avant d'ajouter un commentaire."
            )
            return
        
        try:
            # Ajouter le commentaire à la tâche sélectionnée
            comment_id = str(uuid.uuid4())
            new_comment = {
                "id": comment_id,
                "text": "Nouveau commentaire",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.selected_task["Commentaires"].append(new_comment)
            
            # Sauvegarder le fichier JSON
            file_path = os.path.join(self.data_folder, f"{self.selected_task['ID']}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.selected_task, f, ensure_ascii=False, indent=2)
            
            # Rafraîchir l'affichage des commentaires
            self.refresh_comments_display()
            
            print(f"Commentaire créé avec succès : {comment_id}")
            
        except Exception as e:
            self.show_error_message("Erreur lors de la création du commentaire", f"Une erreur s'est produite : {str(e)}")
            print(f"Erreur lors de la création du commentaire : {e}")
    
    def refresh_comments_display(self):
        """
        Rafraîchit l'affichage des commentaires
        """
        # Vider d'abord l'affichage actuel
        self.clear_comments_view()
        
        # Récupérer le layout des commentaires
        if not hasattr(self.ui, 'verticalLayout_2'):
            return
        
        layout = self.ui.verticalLayout_2.layout()
        if not layout:
            return
        
        # Afficher chaque commentaire
        for comment in self.selected_task.get("Commentaires", []):
            self.create_comment_widget(layout, comment)
    
    def create_comment_widget(self, layout, comment):
        """
        Crée un widget pour afficher un commentaire
        
        Args:
            layout: Le layout où ajouter le widget
            comment: Dictionnaire contenant les données du commentaire
        """
        from PySide6.QtWidgets import QFrame, QHBoxLayout, QPlainTextEdit, QPushButton, QVBoxLayout
        
        # Créer une frame pour le commentaire
        comment_frame = QFrame()
        comment_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        comment_frame.setMaximumHeight(100)
        
        # Layout horizontal pour la frame
        frame_layout = QHBoxLayout(comment_frame)
        
        # Zone de texte pour le commentaire
        comment_text = QPlainTextEdit()
        comment_text.setPlainText(comment["text"])
        comment_text.setMaximumHeight(80)
        comment_text.setMaximumWidth(400)
        
        # Bouton de suppression
        delete_button = QPushButton("🗑️")
        delete_button.setMaximumWidth(40)
        delete_button.setMaximumHeight(40)
        delete_button.clicked.connect(lambda: self.delete_comment(comment["id"]))
        
        # Ajouter les éléments au layout
        frame_layout.addWidget(comment_text)
        frame_layout.addWidget(delete_button)
        
        # Ajouter la frame au layout principal
        layout.addWidget(comment_frame)
    
    def delete_comment(self, comment_id):
        """
        Supprime un commentaire
        
        Args:
            comment_id: ID du commentaire à supprimer
        """
        try:
            # Supprimer le commentaire de la tâche sélectionnée
            self.selected_task["Commentaires"] = [
                comment for comment in self.selected_task["Commentaires"] 
                if comment["id"] != comment_id
            ]
            
            # Sauvegarder le fichier JSON
            file_path = os.path.join(self.data_folder, f"{self.selected_task['ID']}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.selected_task, f, ensure_ascii=False, indent=2)
            
            # Rafraîchir l'affichage
            self.refresh_comments_display()
            
            print(f"Commentaire supprimé : {comment_id}")
            
        except Exception as e:
            self.show_error_message("Erreur lors de la suppression du commentaire", f"Une erreur s'est produite : {str(e)}")
            print(f"Erreur lors de la suppression du commentaire : {e}")
    
    def delete_task(self):
        """
        Supprime la tâche sélectionnée
        """
        # Vérifier si une tâche est sélectionnée
        if not self.selected_task:
            self.show_info_message(
                "Aucune tâche sélectionnée",
                "Veuillez d'abord créer ou sélectionner une tâche avant de la supprimer."
            )
            return
        
        try:
            # Supprimer le fichier JSON
            file_path = os.path.join(self.data_folder, f"{self.selected_task['ID']}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Réinitialiser les champs UI
            self.reset_ui_fields()
            
            # Vider la tâche sélectionnée
            self.selected_task = None
            
            # Rafraîchir l'affichage des tâches
            self.load_all_tasks("Tous")
            
            # Afficher un message de confirmation
            self.show_success_message("Tâche supprimée avec succès")
            
            print(f"Tâche supprimée avec succès")
            
        except Exception as e:
            self.show_error_message("Erreur lors de la suppression de la tâche", f"Une erreur s'est produite : {str(e)}")
            print(f"Erreur lors de la suppression de la tâche : {e}")
    
    def reset_ui_fields(self):
        """
        Remet à zéro tous les champs de l'interface utilisateur
        """
        # Réinitialiser le titre
        if hasattr(self.ui, 'selectedTitle'):
            self.ui.selectedTitle.setText("")
        
        # Réinitialiser la description
        if hasattr(self.ui, 'selectedDescription'):
            self.ui.selectedDescription.setPlainText("")
        
        # Réinitialiser les dates (aujourd'hui et demain)
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        if hasattr(self.ui, 'selectedStartDate'):
            self.ui.selectedStartDate.setDate(today.date())
        
        if hasattr(self.ui, 'selectedEndDate'):
            self.ui.selectedEndDate.setDate(tomorrow.date())
        
        # Réinitialiser le statut
        if hasattr(self.ui, 'selecteStatus'):
            self.ui.selecteStatus.setCurrentText("À faire")
        
        # Vider la vue des commentaires
        self.clear_comments_view()
    
    def load_all_tasks(self, status="Tous"):
        """
        Charge tous les fichiers JSON du dossier data et les affiche dans verticalLayout_1
        
        Args:
            status: Statut pour filtrer les tâches ("Tous" pour afficher toutes les tâches)
        """
        try:
            # Vider d'abord l'affichage actuel
            self.clear_tasks_display()
            
            # Récupérer le layout des tâches
            if not hasattr(self.ui, 'verticalLayout_1'):
                return
            
            layout = self.ui.verticalLayout_1.layout()
            if not layout:
                return
            
            # Charger tous les fichiers JSON du dossier data
            if not os.path.exists(self.data_folder):
                return
            
            json_files = [f for f in os.listdir(self.data_folder) if f.endswith('.json')]
            
            tasks_displayed = 0
            
            for json_file in json_files:
                file_path = os.path.join(self.data_folder, json_file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        task_data = json.load(f)
                    
                    # Filtrer selon le statut
                    if status == "Tous" or task_data.get("Status", "") == status:
                        # Créer un widget pour afficher la tâche
                        self.create_task_widget(layout, task_data)
                        tasks_displayed += 1
                    
                except Exception as e:
                    print(f"Erreur lors du chargement de {json_file}: {e}")
            
            print(f"Chargement terminé : {tasks_displayed} tâches affichées (filtre: {status})")
            
        except Exception as e:
            print(f"Erreur lors du chargement des tâches : {e}")
    
    def clear_tasks_display(self):
        """
        Vide l'affichage des tâches dans verticalLayout_1
        """
        if not hasattr(self.ui, 'verticalLayout_1'):
            return
        
        layout = self.ui.verticalLayout_1.layout()
        if not layout:
            return
        
        # Supprimer tous les widgets du layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def create_task_widget(self, layout, task_data):
        """
        Crée un widget pour afficher une tâche
        
        Args:
            layout: Le layout où ajouter le widget
            task_data: Dictionnaire contenant les données de la tâche
        """
        from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
        
        # Créer une frame pour la tâche
        task_frame = QFrame()
        task_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        task_frame.setMaximumHeight(80)
        task_frame.setMinimumHeight(60)
        
        # Rendre la frame cliquable
        task_frame.mousePressEvent = lambda event: self.select_task(task_data)
        
        # Layout horizontal pour la frame
        frame_layout = QHBoxLayout(task_frame)
        
        # Layout vertical pour les informations de la tâche
        info_layout = QVBoxLayout()
        
        # Titre de la tâche
        title_label = QLabel(task_data.get("Titre", "Sans titre"))
        title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        
        # Date de début
        start_date = task_data.get("DateStart", "N/A")
        if start_date != "N/A":
            try:
                # Convertir de YYYY-MM-DD vers dd/mm/YYYY
                from datetime import datetime
                date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d/%m/%Y")
            except:
                formatted_date = start_date
        else:
            formatted_date = "N/A"
        
        date_label = QLabel(f"Début: {formatted_date}")
        date_label.setStyleSheet("font-size: 10px; color: gray;")
        
        # Statut
        status = task_data.get("Status", "N/A")
        status_label = QLabel(f"Statut: {status}")
        status_label.setStyleSheet("font-size: 10px; color: blue;")
        
        # Ajouter les labels au layout d'informations
        info_layout.addWidget(title_label)
        info_layout.addWidget(date_label)
        info_layout.addWidget(status_label)
        
        # Ajouter le layout d'informations au layout horizontal
        frame_layout.addLayout(info_layout)
        
        # Ajouter la frame au layout principal
        layout.addWidget(task_frame)
    
    def select_task(self, task_data):
        """
        Sélectionne une tâche et met à jour l'interface
        
        Args:
            task_data: Dictionnaire contenant les données de la tâche
        """
        try:
            # Vérifier que task_data est bien un dictionnaire
            if not isinstance(task_data, dict):
                print(f"Erreur : task_data n'est pas un dictionnaire : {type(task_data)}")
                return
            
            # Définir cette tâche comme sélectionnée
            self.selected_task = task_data
            
            # Mettre à jour l'interface avec les données de la tâche
            self.update_ui_with_task(task_data)
            
            print(f"Tâche sélectionnée : {task_data.get('ID', 'N/A')}")
            
        except Exception as e:
            print(f"Erreur lors de la sélection de la tâche : {e}")
            print(f"Type de task_data : {type(task_data)}")
            print(f"Contenu de task_data : {task_data}")
    
    def filter_tasks_by_status(self, status):
        """
        Filtre les tâches par statut
        
        Args:
            status: Statut pour filtrer les tâches
        """
        self.load_all_tasks(status)
    
    def show_info_message(self, title, message):
        """
        Affiche une modale d'information
        
        Args:
            title: Titre de la modale
            message: Message à afficher
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Information")
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def show_success_message(self, message):
        """
        Affiche une modale de succès
        
        Args:
            message: Message à afficher
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Succès")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def show_error_message(self, title, message):
        """
        Affiche une modale d'erreur
        
        Args:
            title: Titre de la modale
            message: Message à afficher
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erreur")
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def get_selected_task(self):
        """
        Retourne la tâche actuellement sélectionnée
        
        Returns:
            dict: Dictionnaire contenant les données de la tâche sélectionnée ou None
        """
        return self.selected_task
    
    def set_selected_task(self, task_data):
        """
        Définit la tâche sélectionnée
        
        Args:
            task_data: Dictionnaire contenant les données de la tâche
        """
        self.selected_task = task_data
