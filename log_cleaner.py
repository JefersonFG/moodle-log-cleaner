import argparse

import pandas as pd


# Main cleaning function
def clean_dataset(source_dataset_path, student_list_path, target_dataset_path) -> None:
    """clean_dataset takes the path to the dataset to clean as well as the path to the list of students and saves the
    cleaned dataset on the target path.

    The procedure will check all events on the log for being related to a student or not, then remove the ones that
    aren't, such as events from admins and professors."""
    df = pd.read_csv(source_dataset_path)
    student_list = get_student_list_from_path(student_list_path)
    df = remove_non_student_entries(df, student_list)
    df.to_csv(target_dataset_path, index=False)


def get_student_list_from_path(student_list_path) -> list:
    """Generates a list of students from the csv passed as input"""
    df = pd.read_excel(student_list_path, header=None, engine="odf")
    return list(df[0])


def remove_non_student_entries(df, student_list) -> pd.DataFrame:
    """Goes through each entry and checks if it is related to a student from the list, removes if isn't"""
    return df[df['Nome completo'].isin(student_list)]


# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Use this tool to clean the logs obtained from moodle, removing 
        entries unrelated to students, such as entries from admins and professors.''')
    parser.add_argument("source_path", help="Path to the moodle logs to clean")
    parser.add_argument("student_list", help="Path to the list of students exported on moodle")
    parser.add_argument("target_path", help="Path to save the cleaned logs")

    args = parser.parse_args()
    clean_dataset(args.source_path, args.student_list, args.target_path)
