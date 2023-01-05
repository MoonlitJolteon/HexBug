# HexBug

A Discord bot for the Hex Casting mod. `buildpatterns.py`, `revealparser.py`, and `hexast.py` are heavily based on code from [hexdecode](https://github.com/gchpaco/hexdecode) and are licensed separately from the rest of the project. **Minimum Python version: 3.11.0**.

## Setup

1. Clone this repo, including submodules: `git clone --recurse-submodules <url>`
2. Optionally, set up a venv and enter it
3. Install deps: `pip install -r requirements.txt`
4. Install [hexnumgen](https://github.com/object-Object/hexnumgen-rs) by building a wheel for your system (see the README) and running `pip install path/to/wheel`
5. Create a file named `.env` following this template:

    ```env
    TOKEN="your-bot-token"
    ```

6. Run the bot: `python main.py`

## Scraping web book types

Run `python scrape_book_types.py | tee utils/book_types.py && python -m black utils/book_types.py`.
