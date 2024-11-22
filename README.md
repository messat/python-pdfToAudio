
# Automated PDF Narrator

Automated PDF Narrator is a Python-based application that converts PDF documents into MP3 audio files. It also provides an interface to view the transcript of the document. The project is designed for ease of use, enabling users to listen to their documents or review their content through a clean web interface.

---

## Features

- **PDF to Audio Conversion:** Converts PDF documents into MP3 files for convenient audio playback.
- **Transcript Viewer:** Access and view the textual content of the uploaded PDF in a user-friendly format.
- **Web Interface:** Simple and intuitive web interface to upload, process, and manage PDF files.

---

## Installation and Setup Guide

### Prerequisites

Before getting started, ensure that you have the following installed on your machine:

1. **Python 3.8+**
   [Download Python](https://www.python.org/downloads/)
   
   
2. **pip (Python Package Manager):**  
   Typically included with Python. Verify installation using:
   ```bash
   pip3 --version
   ```

3. **Virtual Environment (Optional but Recommended):**  
   Helps in managing dependencies in an isolated environment.

---

### Installation Steps

1. **Clone the Repository:**
   Download or clone the project repository to your local machine:
   ```bash
   git clone <repository-link>
   cd automated-pdf-narrator
   ```

2. **Set Up a Virtual Environment (Optional):**
   Create and activate a virtual environment to isolate dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Install the required Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

---

### Running the Application

1. **Start the Application:**
   Run the following command in your terminal:
   ```bash
   python3 app.py
   ```

2. **Access the Web Interface:**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:10000/
   ```

3. **Using the Application:**
   - **Upload a PDF file:** Use the web interface to upload a PDF document.
   - **Generate Audio:** Convert the PDF to an MP3 file.
   - **View Transcript:** Check the extracted text from the PDF in the transcript viewer.

---

## How to Contribute

Contributions to this project are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your forked repository.
4. Open a pull request with a clear description of your changes.

---

## Troubleshooting

- **Dependencies Not Installing:** Ensure you are in the virtual environment and using `pip3` to install packages.
- **Application Not Starting:** Confirm Python 3.8+ is installed and `app.py` is located in the project root directory.
- **Port Issues:** If the default port (10000) is occupied, update the port in the application configuration.

---




