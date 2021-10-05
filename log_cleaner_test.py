import csv
import os
import unittest

import pandas as pd

import log_cleaner


class CleanerTest(unittest.TestCase):
    test_dataset_path = 'test_dataset.csv'
    test_student_list_path = 'test_student_list.ods'
    cleaned_dataset_path = 'cleaned_dataset.csv'

    # List of student names present on the test dataset, cleaned dataset must contain entries for these students
    student_names = ['Test name 1', 'Test name 2']

    # List of names present on the test dataset that are not students, so cleaned dataset must not contain these names
    non_student_names = ['Administrador Moodle']

    # List of columns to be removed on the cleaned dataset
    columns_to_be_removed = [log_cleaner.affected_user_column, log_cleaner.description_column,
                             log_cleaner.origin_column, log_cleaner.ip_address_column]

    def setUp(self):
        """"setUp creates the test dataset with valid data"""
        df = pd.DataFrame(
            {
                'Hora': [
                    '"01/01/2001 10:00"',
                    '"01/01/2001 11:00"',
                    '"01/01/2001 12:00"',
                ],
                '"Nome completo"': [
                    '"Test name 1"',
                    '"Test name 2"',
                    'Administrador Moodle'
                ],
                '"Usuário afetado"': [
                    '-',
                    '"Test name 2"',
                    '-'
                ],
                '"Contexto do Evento"': [
                    '"Test course 1"',
                    '"Test course 1"',
                    '"Test course 2"'
                ],
                'Componente': [
                    'Tarefa',
                    'Tarefa',
                    'Lixeira'
                ],
                '"Nome do evento"': [
                    '"O status da submissão foi visualizado."',
                    '"Comentário visualizado"',
                    'Item excluído'
                ],
                'Descrição': [
                    '''"The user with id '123456' has viewed the submission status page for the assignment with course module id '000000'."''',
                    '''"The user with id '654321' viewed the feedback for the user with id '654321' for the assignment with course module id '000000'."''',
                    '''Item com ID 192837 foi excluído.'''
                ],
                'Origem': [
                    'test_origin',
                    'test_origin2',
                    'cli'
                ],
                '"endereço IP"': [
                    '0.0.0.0',
                    '0.0.0.1',
                    ''
                ],
            }
        )

        df.to_csv(self.test_dataset_path, index=False, quoting=csv.QUOTE_NONE)

        df = pd.DataFrame(
            {
                'Name': [
                    'Test name 1',
                    'Test name 2'
                ]
            }
        )

        with pd.ExcelWriter(self.test_student_list_path) as writer:
            df.to_excel(writer, engine="ods", header=False, index=False)

    def tearDown(self):
        """tearDown deletes both the source and the target files to clean up after the tests"""
        if os.path.exists(self.test_dataset_path):
            os.remove(self.test_dataset_path)
        if os.path.exists(self.test_student_list_path):
            os.remove(self.test_student_list_path)
        if os.path.exists(self.cleaned_dataset_path):
            os.remove(self.cleaned_dataset_path)

    def test_create_cleaned_dataset(self):
        """Tests that the cleaned dataset is created, but doesn't validate its contents"""
        log_cleaner.clean_dataset(self.test_dataset_path, self.test_student_list_path, self.cleaned_dataset_path)
        self.assertTrue(os.path.exists(self.cleaned_dataset_path), "cleaned dataset not created")

    def test_cleaned_names(self):
        """Tests that the cleaned dataset has entries for students and no entries for non students"""
        log_cleaner.clean_dataset(self.test_dataset_path, self.test_student_list_path, self.cleaned_dataset_path)
        df = pd.read_csv(self.cleaned_dataset_path)
        for name in self.student_names:
            self.assertIn(name, df.values, "cleaned dataset lost entries for a student")
        for name in self.non_student_names:
            self.assertNotIn(name, df.values, "non student entry found in the cleaned dataset")

    def test_removed_columns(self):
        """Tests columns that must be removed from the original dataset for absence on cleaned dataset"""
        log_cleaner.clean_dataset(self.test_dataset_path, self.test_student_list_path, self.cleaned_dataset_path)
        df = pd.read_csv(self.cleaned_dataset_path)
        for column in self.columns_to_be_removed:
            self.assertNotIn(column, df.columns, f"found column '{column}' in the cleaned dataset")


if __name__ == '__main__':
    unittest.main()
