# Smart Submit to CreatorDB

This Python script runs the submitCreator API endpoint for YouTube and returns information about the creators which have been added. These include:

- Which creators were added successfully
- Which creators are already in the database
- Which IDs are invalid

## Requirements

You will need Python 3 installed on your system as well as the `requests` library. I would recommend using [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to handle dependencies and virtual environments.

## How to use

Clone this repository and add a list of creators as a `.csv` file in the directory called `input.csv`. Run the script as so:

```
python main.py {INSERT_API_KEY_HERE}
```

and you will get an output in the terminal.

## TODO

- Handle API request timeouts
- Handle multi-column `.csv` files

