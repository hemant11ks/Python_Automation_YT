
import sys                     
from pathlib import Path       
import shutil                 
import logging                 
import time                    

logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logging.info("File Organizer Script Started")

def organize_files(folder_path):
    """
    This function organizes files inside the given folder
    based on their file extensions.
    """


    base_path = Path(folder_path)

 
    if not base_path.exists():
        print("❌ Folder does not exist")
        logging.error("Provided folder does not exist")
        return

   
    print(f"\n📂 Organizing files in: {base_path}\n")

    categories = {
        "Images": [".png", ".jpg", ".jpeg"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Videos": [".mp4", ".mkv"],
        "Scripts": [".py", ".sh"], 
        "Archives": [".zip", ".rar"]
    }

   
    for file in base_path.iterdir():

       
        if file.is_dir():
            continue

        file_extension = file.suffix.lower()

       
        file_moved = False

      
        for folder_name, extensions in categories.items():

    
            if file_extension in extensions:

              
                target_folder = base_path / folder_name

                # Create folder if it doesn't already exist
                target_folder.mkdir(exist_ok=True)

                # Move file to target folder
                shutil.move(str(file), str(target_folder / file.name))

                # Log and print the move action
                logging.info(f"Moved {file.name} -> {folder_name}")
                print(f"✅ {file.name} moved to {folder_name}")

                # Mark file as moved and exit loop
                file_moved = True
                break

        if not file_moved:
            logging.info(f"Skipped file: {file.name}")

    # Print completion message
    print("\n🎉 File organization completed!")
    logging.info("File Organizer Script Completed")

def main():
    """
    This function handles command-line input
    and calls the file organizer function.
    """

    if len(sys.argv) < 2:
        print("❌ Usage: python file_organizer.py <folder_path>")
        sys.exit(1)

    # Read folder path from command line
    folder_path = sys.argv[1]

    # Record start time
    start_time = time.time()

    # Call the automation function
    organize_files(folder_path)

    # Record end time
    end_time = time.time()

    # Print total execution time
    print(f"\n⏱ Time Taken: {round(end_time - start_time, 2)} seconds")
    
if __name__ == "__main__":
    main()
