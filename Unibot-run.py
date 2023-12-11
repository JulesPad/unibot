
import subprocess
import sys
import os

# ==================================================
# ======== Utlities functions for instalation ========
# ==================================================

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return False

# ==================================================
# ======== Installing Llama CPP wrapper LLM ========
# ==================================================

install_package("llm") #base installation including llama-cpp 

#Installing version compattible with METAL, runs on GPU, provides great speed improvments

run_command("llm install llm-mlc")  

# for Apple Silicon M1/M2 Mac
run_command("llm mlc pip install --pre --force-reinstall mlc-ai-nightly mlc-chat-nightly -f https://mlc.ai/wheels")

# setting up what we've just installed
run_command("llm mlc setup")

# ==================================================
# ===Installing the Llama-2-7b-chat model (8Gb)====
# ==================================================


def get_model_path():
    # This will create a path that works for any user
    return os.path.expanduser('~/Library/Application Support/io.datasette.llm/mlc/dist/prebuilt/mlc-chat-Llama-2-7b-chat-hf-q4f16_1')


def download_model_if_not_exists(download_command):
    model_path = get_model_path()
    if not os.path.exists(model_path):
        print("\033[1;34m🚀 Starting download of the model, please wait (8GB)...\033[0m")  # Blue text
        if run_command(download_command):
            print("\033[1;32m✅ Download and installation successful.\033[0m")  
        else:
            print("\033[1;31m❌ Download or installation failed.\033[0m")  
    else:
        print("\033[1;33m⚠️ Model already exists.\033[0m") 

download_command = "llm mlc download-model Llama-2-7b-chat --alias llama2"
download_model_if_not_exists(download_command)

# ==================================================
# ========Preparing to run the chatmodel============
# ==================================================

def read_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def run_command_with_prompt(base_command, model, prompt):
    full_command = f"{base_command} -m {model} -s '{prompt}'"
    subprocess.check_call(full_command, shell=True)

prompt_text = read_prompt_from_file("prompt.txt")
base_command = "llm chat"  
model = "Llama-2-7b-chat"


# ==================================================
# ===============Instructions=======================
# ==================================================

def clear_screen():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def print_instructions():
    # Print instructions with ASCII art and colors
    print("\033[1;32m")  # Bright Green Color Start
    print("Welcome to UniBot!")
    print("\033[0m")  # Reset Color

    print("\n\033[1;34mINSTRUCTIONS:\033[0m")  # Blue Color for Instructions Header
    print("1) UniBot is here to help you navigate student life.")
    print("2) Ask about studying, sports, or social activities.")
    print("3) Unibot is a LLM based agent, it can sometimes need to be asked specific questions")
    
    print("\n\033[1;33m")  # Yellow Color
    print("Remember: UniBot is a friendly assistant.")
    print("Treat it with kindness!\n")
    print("\033[0m")  # Reset Color

def user_acknowledgement():
    # Ask for user acknowledgement
    input("Press Enter to acknowledge that you have read and understood the instructions...")

clear_screen()
print_instructions()
user_acknowledgement()


# ==================================================
# ========Start the chat session with UniBbot=======
# ==================================================

run_command_with_prompt(base_command, model, prompt_text)