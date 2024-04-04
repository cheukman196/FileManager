
# FileEase
FileEase is a file manager that has file browsing, bookmarking and custom directory creation features. Built using Python and PyQT6 framework, FileEase offers lightweight and self-explanatory features to manage your local files.


## Installation

The project is a limited experimentation on creating applications with GUI. Given the scope of this project, no installation or executable files are available as of now. Users will need to run the ```main.py``` file directly in a IDE in a local environment.

Users will need to install the given third-party libraries using the command lines below.

```bash
    pip install PyQt6
    pip install pathvalidate
```
## Features

- File explorer
    - File sidebar
    - Return page, Next page and Parent directory access
    - Bookmarking directories
    - Copying or Moving files

- Customisable directory creation
    - Prefix and Suffixes
    - Subdirectory creation
    - Multiple directory creation   


## Acknowledgements
This project uses a number of libraries to support it's core functionailities. 

### Common Python Libraries
- `os`: features to work with the operating system and directories
- `pathlib`: features to manipulate with file paths 
- `sqlite3`: features to manage a lightweight database to handle bookmarking
- `pydoc`: features to escape html characters
- `contextlib`: features to manage resource and auto-closing

### Third-Party Libraries
- `PyQt6`: used to implement GUI, handle data and implement the application in a MVC manner
- `pathvalidate`: used to sanitize and validate user input for directory paths

### Third-Party Applications
- `QT Designer`: used to facilitate the design and setup of  PyQt6 .ui files

### Link to Third-Party Resources
- [pathvalidate](https://pypi.org/project/pathvalidate/)
- [PyQt6](https://pypi.org/project/PyQt6/)
- [QT Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html)
