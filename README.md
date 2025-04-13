![image](https://github.com/user-attachments/assets/2cb1f15a-48e8-4b9e-8e6a-07d439cde2f8)

# Marcello Dynamics Setup Guide

This guide will walk you through the process of setting up the Marcello Dynamics project on your local machine, including installing dependencies and running the project.

## Prerequisites

- **Git**: Version control system to clone the repository.
- **Python 3.11**: Required version of Python for the project.
- **pip**: Python package manager to install dependencies.

## Steps

### 1. Install Git

If you don't have Git installed, you can download and install it from the official website:

- [Download Git](https://git-scm.com/)

Follow the instructions for your operating system.

### 2. Clone the Repository

Once you have Git installed, open your terminal (Command Prompt, PowerShell, or terminal for macOS/Linux) and run the following command to clone the repository:

git clone https://github.com/dagl1/Marcello_dynamics


Navigate into the cloned directory:


### 3. Install Python 3.11

Ensure that Python 3.11 is installed on your system. You can download the latest version of Python from the official website:

- [Download Python 3.11](https://www.python.org/downloads/release/python-3110/)

After installing, verify the installation by running:
python --version

is should return `Python 3.11.x`.

### 4. Create a Virtual Environment

It's a good practice to use a virtual environment to manage project-specific dependencies. To create one, run the following command:

python -m venv venv

Activate the virtual environment:

- On Windows:
.\venv\Scripts\activate
Once activated, your terminal prompt should show the virtual environment's name.

### 5. Install the Project Requirements

With the virtual environment activated, install the required dependencies by running:
This will install all the necessary Python packages listed in the `requirements.txt` file.

### 6. Run the Project

Finally, you can run the project by executing the `main.py` script:
python main.py

This should start the program and perform the desired functionality.

## Troubleshooting

- If you encounter issues with package installations, make sure you're using the correct version of Python and that the virtual environment is activated.
- Ensure that all required packages are properly listed in `requirements.txt`.
