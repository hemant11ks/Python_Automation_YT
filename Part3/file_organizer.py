import sys
from pathlib import Path
import shutil
import logging
import time

# Logging configuration

# filename, level, format

logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO, # ERROR, WARNING, INFO, DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s"

)

# logging info started
logging.info("File Organizer Script Started")

def organize_files(folder_path):

    # Download
    base_path = Path(folder_path)

    # Logging error if path does not exist

    if not base_path.exists():
        print("❌ Folder does not exist")
        logging.error("Provided folder does not exist")
        return

    print(f"\n📂 Organizing files in: {base_path}\n")

    # Dictionary to map fileextenstion to folder names
    # key - folder name
    # value - list of file extensions

    categories = {
        "Images": [".png", ".jpg", ".jpeg"],
        "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
        "Videos": [".mp4", ".mkv"],
        "Scripts": [".py", ".sh"], 
        "Archives": [".zip", ".rar"]
    }

    # Looping Condition

    for file in base_path.iterdir():

        # Skip condition
        if file.is_dir():
            continue

        # Extract  file extn and convert it to lower case
        # demo.PDF -> .pdf
        file_extension = file.suffix.lower()  

        # flag - file is moved or not
        # 
        file_moved = False 

        for folder_name, extensions in categories.items():
            if file_extension in extensions:
                target_folder = base_path / folder_name

                target_folder.mkdir(exist_ok=True)

                shutil.move(str(file), str(target_folder / file.name))

                logging.info(f"Moved {file.name} -> {folder_name}")

                print(f"✅ {file.name} moved to {folder_name}")

                file_moved = True

                break

            if not file_moved:
                logging.info(f"Skipped file: {file.name}")

        print("\n🎉 File organization completed!")
        logging.info("File Organizer Script Completed")
                
def main():

    # Checking if the user has provided a folder path
    if len(sys.argv) < 2:
        print("❌ Usage: python file_organizer.py <folder_path>")
        sys.exit(1)
    
    # Declarig a variable what will store the folder path
    folder_path = sys.argv[1]

    # startin -> before script -> end time
    start_time = time.time()

    # Call the automation function
    organize_files(folder_path)

    # Record end time
    end_time = time.time()

    # Print total execution time
    print(f"\n⏱ Time Taken: {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    main()

