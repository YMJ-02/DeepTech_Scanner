import os

def create_project_structure():
    """
    Creates the directory and initial file structure for the DeepTech News Automation Bot.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define directories to create
    directories = [
        "src",
        "data",
        "assets",
        "prompts",
        "logs",
        "config"
    ]
    
    # Define placeholder files to create
    files = [
        "src/scraper.py",
        "src/ai_translator.py",
        "src/image_maker.py",
        "src/sns_uploader.py",
        "config/.env"
    ]
    
    print("Initializing DeepTech_Scanner project structure...\n")
    
    # Create directories
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"[+] Directory created: {dir_path}")
        
    # Create files
    for file in files:
        file_path = os.path.join(base_dir, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                # Add a brief module docstring for context
                if file.endswith('.py'):
                    f.write(f'"""\nAuto-generated module: {os.path.basename(file)}\n"""\n')
            print(f"[+] File created: {file_path}")

if __name__ == "__main__":
    create_project_structure()
    print("\nProject structure setup complete!")
