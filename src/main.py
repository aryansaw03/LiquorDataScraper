import os
from config import WEBSITES_TO_SCAPE


def clear_data_folder():
    data_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    for filename in os.listdir(data_folder_path):
        file_path = os.path.join(data_folder_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def scrape_website(website):
    scraper = website['scraper'](
        website["baseURL"], os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', f'{website["name"]}.csv'))
    scraper.scrape()


def clean_and_rescrape_all():
    clear_data_folder()
    for website in WEBSITES_TO_SCAPE:
        scrape_website(website)


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Clear Data Folder")
        print("2. Scrape a Specific Website")
        print("3. Clean and Rescrape All (Not recommended due to website ban)")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            clear_data_folder()
            print("Data folder cleared.")
        elif choice == '2':
            print("Select a website to scrape:")
            for i, website in enumerate(WEBSITES_TO_SCAPE, start=1):
                print(f"{i}. {website['name']}")
            website_choice = int(input("Enter your choice: ")) - 1
            scrape_website(WEBSITES_TO_SCAPE[website_choice])
            print(f"{WEBSITES_TO_SCAPE[website_choice]['name']} scraped.")
        elif choice == '3':
            clean_and_rescrape_all()
            print("All websites cleaned and rescraped.")
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main_menu()
