# Moodle log cleaner

Project for cleaning moodle activity logs based on the requirements of our current project.

This script will take the logs and the list of students names as inputs and output the logs without entries from non students, such as admins and professors. It will also remove columns with data irrelevant for our current project.

## Dependencies

This project relies on the `pandas` module being available, as well as the `odfpy` module necessary for writing and reading `.ods` files, format used by moodle when exporting the list of students for a given course.

## Usage

You can run the script with python 3.9 passing the path to the logs to be cleaned, the path to the list of students and the path for the result to be saved to:

```bash
python log_cleaner.py moodle_logs.csv student_list.csv cleaned_moodle_logs.csv
```

## Testing

The tests reside on the `log_cleaner_test.py` file and use the `unittest` package, to run them execute:

```bash
python -m log_cleaner_test
```
