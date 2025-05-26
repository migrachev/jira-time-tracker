import readchar
from prompt_toolkit import prompt
from typing import TextIO, Iterator

def getUserData(defaultFileLocation: str) -> str:
    options: list[str] = [
        "Refer data from file.", 
        "Paste data as text."
    ]
    index: int = 0  # Start at the first option

    while True:
        print("How do you want to supply us with the data to process?\n")
        # Display options
        i: int; option: str
        for i, option in enumerate(options):
            if i == index:
                print(f"> \033[32m{option}\033[0m")  # Highlight the selected option
            else:
                print(f"  {option}")

        key: str = readchar.readkey()  # Wait for key press

        if key == readchar.key.UP or key == readchar.key.LEFT:
            index = (index - 1) % len(options)  # Move selection up/left
        elif key == readchar.key.DOWN or key == readchar.key.RIGHT:
            index = (index + 1) % len(options)  # Move selection down/right
        elif key == readchar.key.ENTER or key == "\r":
            break  # Confirm selection

        print("\033c", end="")  # Clear screen

    data: str = ""
    if index:
        data = prompt("Paste your input here!")
    else:
        fileLocation: str = prompt("Please provide the file location: ", default=defaultFileLocation)
        with open(fileLocation, 'r', encoding='utf-8') as dataFile:
            dataFile: TextIO
            flag: int = -1
            iterator: Iterator[str] = reversed(list(dataFile))
            while flag < 1:
                line: str = next(iterator)
                stripped: str = line.strip()
                if stripped and (line.startswith("=") or line.startswith("#")):  # comment/empty lines ignored
                    if flag == 0:
                        flag = 1
                elif stripped:
                    flag = 0
                    data = line + data
    return data