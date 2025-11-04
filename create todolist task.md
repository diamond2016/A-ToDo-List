### Task: create todolist page and manage in the Flask application

1. *create page todolist.html* (will replace the present one), which has a form with a title (title of the todolist) and a list of items (the todolist_item)

        title

        rows: icon of type todolistitem, title of the item, content of the item, due time of the item, checkbox "completed"

    On right of every row a "x" icon to delete the row

    Below the list of items a button "Add item" allows to add a row as next of the list, and a button "Save to do list" saves all in database.

    * If user presses "Save" and is not a registered, the system pop ups the login page, and at the end returns to save page without losing the do to list

    * If the user triggers "Save" and is authenticated, system proceeds with save in database.
    Give style to a page with layout like this ![example layout](./todolist.jpg)

1. Use main.new_todo, associated to "Create" button, adjusting code, in order to launch the page of prev point

1. complete and adjust the route *auth.add_todolist()* which manages saving of a todo list

1. complete and adjust the route *auth.edit_todolist()* which manages editing of an existing todo list, in this case:
Use the same form of 1 if possible.
Only rows not completed can be deleted ("x" right of the row)
Rows can be added to existing to do list

1. Modify index.html in order to show a list of items if the user is authenticated (user.list). Add a a block a page similar to todolist.html but in read only.