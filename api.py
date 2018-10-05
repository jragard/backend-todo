from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from datetime import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('api.log')
file_handler.setFormatter(formatter)
rotate_handler = RotatingFileHandler(
    'api.log', maxBytes=2000, backupCount=5
)

logger.addHandler(file_handler)
logger.addHandler(rotate_handler)


TODOS = {}


class TodosList(Resource):

    def get(self):
        if len(TODOS) == 0:
            logger.debug("No todos to return yet")
            return "No Todos yet"
        else:
            logger.info("Successful GET")
            return TODOS

    def post(self):
        full_date = datetime.now()
        creation_date = (str(full_date.month) + "/" +
                         str(full_date.day) + "/" +
                         str(full_date.year)
                         )

        if len(TODOS) == 0:
            todo_id = "1"
        else:
            todo_id = str(int(max(TODOS.keys()).lstrip('todo')) + 1)

        try:
            TODOS[todo_id] = {'Title': request.form['Title'],
                              'Creation Date': creation_date,
                              'Last Updated date': creation_date,
                              'Due Date': request.form['Due'],
                              'Completed': request.form['Completed'],
                              'Completion Date': request.form
                              ['Completion Date']
                              }
            logger.info("Todo posted successfully - " + creation_date)
            return TODOS
        except Exception as e:
            logger.error(e)


class SingleTodo(Resource):
    def get(self, todo_id):
        try:
            logger.info("Single Todo successfully retrieved")
            return {todo_id: TODOS[todo_id]}
        except Exception as e:
            logger.error(e)
            return "No Todo exists with that ID"

    def put(self, todo_id):
        try:
            full_date = datetime.now()
            update_date = (str(full_date.month) + "/" +
                           str(full_date.day) + "/" +
                           str(full_date.year)
                           )

            TODOS[todo_id] = {'Title': request.form['Title'],
                              'Creation Date': TODOS[todo_id]['Creation Date'],
                              'Last Updated date': update_date,
                              'Due Date': request.form['Due'],
                              'Completed': request.form['Completed']
                              }

            if request.form['Completed'] == 'True':
                TODOS[todo_id]['Completion Date'] = update_date
            else:
                TODOS[todo_id]['Completion Date'] = 'Not Yet Completed'

            logger.info("Todo Updated Successfully")
            return {todo_id: TODOS[todo_id]}
        except Exception as e:
            logger.error(e)

    def delete(self, todo_id):
        try:
            del TODOS[todo_id]
            logger.info("Todo successfully deleted")
            return TODOS
        except Exception as e:
            logger.error(e)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


api.add_resource(TodosList, '/')
api.add_resource(SingleTodo, '/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
