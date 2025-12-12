from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from gui import *
import csv

class Logic(QMainWindow, Ui_StudentGrades):
    def __init__(self):
        '''
        This Function runs the reset function, then handles any button presses with the appropriate function
        '''
        super().__init__()
        self.setupUi(self)
        self.total_reset()
        self.csv_check()
        self.submitButton.clicked.connect(self.student_score_submit)
        self.searchButton.clicked.connect(self.search_button_pressed)
        self.searchFindButton.clicked.connect(self.student_found_toggle)
        self.searchSubmitButton.clicked.connect(self.submit_score_change)

    def total_reset(self):
        '''
        This Function resets all the elements
        '''
        self.searchNameLineEdit.setText("")
        self.searchNameLineEdit.setVisible(False)
        self.searchNameLineEdit.setEnabled(False)
        self.searchFindButton.setVisible(False)
        self.searchFindButton.setEnabled(False)
        self.searchErrorLabel.setVisible(False)
        self.searchNameLabel.setText('')
        self.searchScoreLabel.setVisible(False)
        self.searchScoreLineEdit.setVisible(False)
        self.searchScoreLineEdit.setEnabled(False)
        self.searchGradeLabel.setText('')
        self.searchSubmitButton.setVisible(False)
        self.searchSubmitButton.setEnabled(False)
        self.searchScoreErrorLabel.setText('')
        self.nameLineEdit.setText('')
        self.scoreLineEdit.setText('')

    def csv_check(self):
        '''
        This Function re-creates the csv file and formats its headers
        '''
        csv_create_file = open('data.csv', 'w', newline='')
        csv_writer = csv.DictWriter(csv_create_file, fieldnames=['Student Name', 'Student Score'])
        csv_writer.writeheader()
        csv_create_file.close()

    def student_score_submit(self):
        '''
        This Function will check input and save to csv file if all is correct
        '''
        found_name = False
        student_name = (self.nameLineEdit.text()).strip()
        try:
            student_score = int(self.scoreLineEdit.text())
        except ValueError:
            self.submitErrorLabel.setText('Score must be an integer')
        else:
            if 0 <= student_score <= 100:
                with open('data.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        if student_name in row:
                            found_name = True
                            self.submitErrorLabel.setText('Student Name Already Exists')
                if not found_name:
                    with open('data.csv', 'a', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([student_name, student_score])
                    self.submitErrorLabel.setText('Submit Student\'s Score')
            else:
                self.submitErrorLabel.setText('Score must be between 0 and 100')
        self.total_reset()

    def search_button_pressed(self):
        '''
        This function simply pulls up the first three (name, find, and error) elements
        '''
        self.searchFindButton.setVisible(True)
        self.searchFindButton.setEnabled(True)
        self.searchNameLineEdit.setVisible(True)
        self.searchNameLineEdit.setEnabled(True)
        self.searchErrorLabel.setVisible(True)

    def student_found_toggle(self):
        '''
        This Function will add the rest of the fields depending on whether the student was found or not, seperate for simplicity
        '''
        student_name = (self.searchNameLineEdit.text()).strip()
        found_name = False
        score = 0
        max_score = 0
        with open('data.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row['Student Score']) > max_score:
                    max_score = int(row['Student Score'])
                if student_name == row['Student Name']:
                    found_name = True
                    score = int(row['Student Score'])
        if found_name:
            self.searchNameLabel.setText(student_name)
            self.searchScoreLabel.setVisible(True)
            self.searchScoreLineEdit.setVisible(True)
            self.searchScoreLineEdit.setEnabled(True)
            self.searchScoreLineEdit.setText(str(score))
            if score >= max_score-10:
                self.searchGradeLabel.setText('Student Grade: A')
            elif score >= max_score-20:
                self.searchGradeLabel.setText('Student Grade: B')
            elif score >= max_score-30:
                self.searchGradeLabel.setText('Student Grade: C')
            elif score >= max_score-40:
                self.searchGradeLabel.setText('Student Grade: D')
            else:
                self.searchGradeLabel.setText('Student Grade: F')
            self.searchSubmitButton.setVisible(True)
            self.searchSubmitButton.setEnabled(True)
            self.searchErrorLabel.setText('Student name found')

        else:
            self.searchErrorLabel.setText('Student name not found')
            self.searchNameLabel.setText('')
            self.searchScoreLabel.setVisible(False)
            self.searchScoreLineEdit.setVisible(False)
            self.searchScoreLineEdit.setEnabled(False)
            self.searchScoreLineEdit.setText('')
            self.searchGradeLabel.setText('')
            self.searchSubmitButton.setVisible(False)
            self.searchSubmitButton.setEnabled(False)


    def submit_score_change(self):
        '''
        This Function checks and submits the score change
        '''
        student_name = (self.searchNameLineEdit.text()).strip()
        new_score = 0
        try:
            new_score = int(self.searchScoreLineEdit.text())
        except ValueError:
            self.searchScoreErrorLabel.setText('Score must be an integer')
        else:
            if 0 <= new_score <= 100:
                old_student_list = []
                old_score_list = []
                with open('data.csv', 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        if student_name == row['Student Name']:
                            old_score_list.append(str(new_score))
                            old_student_list.append(row['Student Name'])
                        else:
                            old_score_list.append(row['Student Score'])
                            old_student_list.append(row['Student Name'])

                self.csv_check()

                with open('data.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    for i in range(len(old_student_list)):
                        csv_writer.writerow([old_student_list[i], old_score_list[i]])
                max_score = 0

                with open('data.csv', 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        if max_score < int(row['Student Score']):
                            max_score = int(row['Student Score'])

                if new_score >= max_score - 10:
                    self.searchGradeLabel.setText('Student Grade: A')
                elif new_score >= max_score - 20:
                    self.searchGradeLabel.setText('Student Grade: B')
                elif new_score >= max_score - 30:
                    self.searchGradeLabel.setText('Student Grade: C')
                elif new_score >= max_score - 40:
                    self.searchGradeLabel.setText('Student Grade: D')
                else:
                    self.searchGradeLabel.setText('Student Grade: F')
                self.searchScoreLineEdit.setText(str(new_score))

            else:
                self.searchScoreErrorLabel.setText('Score must be between 0 and 100')



