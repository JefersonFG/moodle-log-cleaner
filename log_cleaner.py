import argparse


# Main cleaning function
def clean_dataset(source_dataset_path, student_list, target_dataset_path) -> None:
    raise Exception("Not implemented")


# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Use this tool to clean the logs obtained from moodle, removing 
        entries unrelated to students, such as entries from admins and professors.''')
    parser.add_argument("source_path", help="Path to the moodle logs to clean")
    parser.add_argument("student_list", help="Path to the list of students exported on moodle")
    parser.add_argument("target_path", help="Path to save the cleaned logs")

    args = parser.parse_args()
    clean_dataset(args.source_path, args.student_list, args.target_path)
