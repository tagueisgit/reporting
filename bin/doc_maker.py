#!/usr/bin/env python3

import os
import logging
import subprocess

# Setting up logging
logging.basicConfig(filename='/data/practice/projects/scripts/python/reporting/logs/document_generation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_document(software_name, software_description, output_directory):
    try:
        with open('/data/practice/projects/scripts/python/reporting/templates/template.tex', 'r') as file:
            template = file.read()

        # Replace placeholders
        software_os = input("Enter the software operating system: ")
        software_libs = input("Enter the required libraries for the software: ")
        populated_template = template.replace(r'\softwareName', software_name)
        populated_template = populated_template.replace(r'\softwareDescription', software_description)
        populated_template = populated_template.replace(r'\softwareOS', software_os)
        populated_template = populated_template.replace(r'\softwareLibs', software_libs)  # Add this line
        # ... you can extend this for other placeholders ...

        output_filename = os.path.join(output_directory, f"{software_name}.tex")
        with open(output_filename, 'w') as file:
            file.write(populated_template)

        # Create the log file path
        log_file_path = os.path.join(os.path.dirname(output_filename), 'compilation.log')

        # Compile the LaTeX file to produce a PDF and capture output in log
        with open(log_file_path, 'w') as log_file:
            subprocess.run(['pdflatex', f"{software_name}.tex"], cwd=os.path.dirname(output_filename), stdout=log_file, stderr=subprocess.STDOUT, check=True)
        logging.info(f"Document '{output_filename}' has been generated and compiled successfully.")

    except FileNotFoundError:
        logging.error(f"Error: File 'template.tex' not found!")
    except subprocess.CalledProcessError:
        logging.error("Error occurred while compiling the LaTeX document.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

def main():
    try:
        software_name = input("Enter the software name: ")
        software_description = input("Enter the software description: ")

        # ... additional inputs based on the updated template ...

        output_directory = f"reports/{software_name}"
        os.makedirs(output_directory, exist_ok=True)
        generate_document(software_name, software_description, output_directory)
        print(f"Document for '{software_name}' has been generated and compiled in {output_directory}!")
    except Exception as e:
        logging.error(f"An error occurred during user interaction: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

