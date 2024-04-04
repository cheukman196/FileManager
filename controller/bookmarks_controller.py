import sqlite3
from contextlib import closing
from pathlib import Path
from pydoc import html

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from view.bookmarks_view import BookmarksView
from view.edit_bookmark_message import EditBookmarkMessage
from view.error_message import ErrorMessageBox


class BookmarksController:
    def __init__(self, main_view_controller, current_dir):
        self.DATABASE_PATH = "data/Bookmark.db"
        self.main_view_controller = main_view_controller
        self.current_dir = current_dir
        self.bookmarks_view = BookmarksView(self, current_dir)
        self.load_bookmark_list()

    # query data base and load view model
    def load_bookmark_list(self):
        self.bookmarks_view.my_bookmarks_list.clear()  # clear previous records
        try:
            with (sqlite3.Connection(self.DATABASE_PATH) as conn):
                conn.row_factory = sqlite3.Row
                with closing(conn.cursor()) as c:
                    c.execute('''SELECT * FROM Bookmarks ''')  # query
                    results = c.fetchall()
                    for row in results:
                        item = QListWidgetItem(row["name"], self.bookmarks_view.my_bookmarks_list)
                        item.setToolTip(row["path"])  # path stored in tooltip
                        item.setData(Qt.ItemDataRole.UserRole, row["bookmark_id"])  # DB id stored in UserRole
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))

    # enable visit / edit / delete buttons on selecting a bookmark
    def click_bookmark(self):
        has_clicked_item = True if self.bookmarks_view.my_bookmarks_list.currentItem() else False
        self.bookmarks_view.enable_bookmark_buttons(has_clicked_item)

    # visit bookmark on double clicking
    def double_click_bookmark(self):
        has_clicked_item = True if self.bookmarks_view.my_bookmarks_list.currentItem() else False
        self.bookmarks_view.enable_bookmark_buttons(has_clicked_item)
        if has_clicked_item:
            self.visit_bookmark()

    # visiting a bookmark
    def visit_bookmark(self):
        try:
            path = self.bookmarks_view.my_bookmarks_list.currentItem().toolTip()  # path stored in tooltip
            if not path:
                raise OSError("No path stored for this bookmark")
            elif not Path(path).exists():
                raise OSError(f"The given folder cannot be found in this system:\n{path}")
            self.main_view_controller.visit_page_by_path_string(path)
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            if self.main_view_controller.directory_stack.current_dir.path != path:
                self.main_view_controller.directory_stack.visit_new_page(path)
            self.main_view_controller.update_navigation_bar_and_button_state()
            self.bookmarks_view.close()

    # adding a bookmark
    def add_bookmark(self):
        try:
            # get text from input
            path = self.bookmarks_view.current_page_textbox.text()
            bookmark_name = html.escape(self.bookmarks_view.bookmark_name_textbox.text())

            # validate input and path integrity
            if not path or path == "" or not Path(path).exists():
                ErrorMessageBox("Bookmark creation error", "The bookmark path is not found or doesn't exist.")
                self.bookmarks_view.return_button.click()
                return
            if not bookmark_name or bookmark_name == "":
                ErrorMessageBox("Bookmark creation error", "Please enter a name for your bookmark.")
                self.bookmarks_view.bookmark_name_textbox.setFocus()
                return

            # on passing checks
            with sqlite3.Connection(self.DATABASE_PATH) as conn:
                conn.row_factory = sqlite3.Row
                with closing(conn.cursor()) as c:
                    query = '''INSERT INTO Bookmarks (path, name)
                                VALUES (?, ?)'''
                    c.execute(query, (path, bookmark_name))
                    if c.lastrowid:
                        self.bookmark_message(bookmark_name, path, "created")
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            self.load_bookmark_list()  # reload bookmark list on success

    # opens a bookmark edit window
    def open_edit_bookmark_message(self):
        try:
            path = self.bookmarks_view.my_bookmarks_list.currentItem().toolTip()
            name = self.bookmarks_view.my_bookmarks_list.currentItem().text()
            # pass path and name to window
            self.edit_bookmark_message = EditBookmarkMessage(name, path, self)
        except Exception as e:
            return ErrorMessageBox("Error", str(e))

    # if bookmark edit input is valid, persist changes to DB
    def edit_bookmark(self, name, link):
        # get id to identify the item in DB
        id = self.bookmarks_view.my_bookmarks_list.currentItem().data(Qt.ItemDataRole.UserRole)
        if not id:
            return ErrorMessageBox("Bookmark Error", "Cannot identify current bookmark in database.")
        try:
            with (sqlite3.Connection(self.DATABASE_PATH) as conn):
                with closing(conn.cursor()) as c:
                    c.execute('''UPDATE Bookmarks
                                SET name = ?, path = ?
                                WHERE bookmark_id = ?''', (name, link, id))
                    if c.rowcount == 1:
                        self.bookmark_message(name, link, "updated")
                    else:
                        return ErrorMessageBox("Bookmark Error", "Unexpected error in editing bookmark.")
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            self.load_bookmark_list()  # reload list on success

    # delete bookmark
    def delete_bookmark(self):
        path = self.bookmarks_view.my_bookmarks_list.currentItem().toolTip()
        name = self.bookmarks_view.my_bookmarks_list.currentItem().text()
        id = self.bookmarks_view.my_bookmarks_list.currentItem().data(Qt.ItemDataRole.UserRole)
        print(id)
        if self.bookmark_delete_confirmation_prompt():
            try:
                with (sqlite3.Connection(self.DATABASE_PATH) as conn):
                    with closing(conn.cursor()) as c:
                        c.execute('''DELETE FROM Bookmarks
                                    WHERE bookmark_id = ?''', (id,))
                        if c.rowcount == 1:
                            self.bookmark_message(name, path, "deleted")
                        else:
                            return ErrorMessageBox("Bookmark Error", "Unexpected error in editing bookmark.")
            except OSError as e:
                return ErrorMessageBox("OS Error", str(e))
            except Exception as e:
                return ErrorMessageBox("Error", str(e))
            self.load_bookmark_list()  # reload on succcess

    # opens a window to indicate operation successful
    # action = operation (in past tense) e.g. Bookmark created/edited/deleted successfully
    def bookmark_message(self, name, path, action):
        success_msg = QMessageBox()
        success_msg.setWindowTitle(f"Bookmark {action}!")
        success_msg.setText(f"Bookmark {action} successfully.\nName: {name}\nPath: {path}")
        success_msg.setIcon(QMessageBox.Icon.Information)
        success_msg.exec()

    # prompt to confirm user wants to delete bookmark
    def bookmark_delete_confirmation_prompt(self):
        path = self.bookmarks_view.my_bookmarks_list.currentItem().toolTip()
        name = self.bookmarks_view.my_bookmarks_list.currentItem().text()
        try:
            prompt = QMessageBox()
            prompt.setWindowTitle("Delete Bookmark")
            prompt.setText(f"Delete the following bookmark?\nName: {name}\nPath: {path}")
            prompt.setIcon(QMessageBox.Icon.Question)
            prompt.addButton(QMessageBox.StandardButton.Yes)
            prompt.addButton(QMessageBox.StandardButton.Cancel)
            prompt.exec()
            self.prompt = prompt
            if prompt.button(QMessageBox.StandardButton.Yes).clicked:
                return True
            elif prompt.button(QMessageBox.StandardButton.Cancel).clicked:
                return False
            else:
                return False
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
