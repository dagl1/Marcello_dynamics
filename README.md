# Marcello_dynamics
Marcello Dynamics Setup Guide
This guide will walk you through the process of setting up the Marcello Dynamics project on your local machine, including installing dependencies and running the project.

Prerequisites
Git: Version control system to clone the repository.

Python 3.11: Required version of Python for the project.

pip: Python package manager to install dependencies.

Steps
1. Install Git
If you don't have Git installed, you can download and install it from the official website:

Download Git

Follow the instructions for your operating system.

2. Clone the Repository
Once you have Git installed, open your terminal (Command Prompt, PowerShell, or terminal for macOS/Linux) and run the following command to clone the repository:

bash
Copy
Edit
git clone https://github.com/dagl1/Marcello_dynamics
Navigate into the cloned directory:

bash
Copy
Edit
cd Marcello_dynamics
3. Install Python 3.11
Ensure that Python 3.11 is installed on your system. You can download the latest version of Python from the official website:

Download Python 3.11

After installing, verify the installation by running:

bash
Copy
Edit
python --version
This should return Python 3.11.x.

4. Create a Virtual Environment
It's a good practice to use a virtual environment to manage project-specific dependencies. To create one, run the following command:

bash
Copy
Edit
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy
Edit
.\venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Once activated, your terminal prompt should show the virtual environment's name.

5. Install the Project Requirements
With the virtual environment activated, install the required dependencies by running:

bash
Copy
Edit
pip install -r requirements.txt
This will install all the necessary Python packages listed in the requirements.txt file.

6. Run the Project
Finally, you can run the project by executing the main.py script:

bash
Copy
Edit
python main.py
