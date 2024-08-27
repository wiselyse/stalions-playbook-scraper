# Connor Stalions Playbook Scraper

This Python script scrapes a college football team's offensive playbook from `collegefootball.gg` and saves the images of the plays in a structured directory format.

## Requirements

- Python 3.x
- pip (Python package installer)

## Setup

1. **Clone the repository** or download the script.
   
2. **Create a virtual environment** (if you haven't already):

    ```bash
    python3 -m venv .venv
    ```

3. **Activate the virtual environment**:

    - On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
    - On Windows:
        ```bash
        .venv\Scripts\activate
        ```

4. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:

    ```bash
    python connorStalions.py
    ```

2. Enter the school name when prompted.

3. The script will validate if the school exists on `collegefootball.gg` and then start scraping the playbook.

4. The playbook will be saved in a directory named after the school.

## Notes

- If `pip` is not installed, you can install it by following the instructions [here](https://pip.pypa.io/en/stable/installation/).
- Ensure you have an active internet connection as the script fetches data from a live website.
- Make sure the school name matches the wording on `collegefootball.gg` (look in the url)

## License

This project is licensed under the MIT License.
