 
"""main function that takes in test_type argument"""
import os
import sys


def main(test_type):
    target_directory = "unit"
    if test_type == "integration":
        target_directory = "integration"
    elif test_type == "unit":
        target_directory = "unit"
    elif test_type == "all":
        target_directory = "."
    elif test_type == "model":
        target_directory = "model"

    command = f"pytest tests/{target_directory} --spec"
    os.system(command)


if __name__ == '__main__':
    
    main(sys.argv[1] or 'unit')