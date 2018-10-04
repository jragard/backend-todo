from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
api = Api(app)

TODOS = {}


class TodosList(Resource):

    def get(self):
        return TODOS

    def post(self):
        full_date = datetime.now()
        creation_date = str(full_date.month) + "/" + str(full_date.day) + "/" + str(full_date.year)
        if len(TODOS) == 0:
            todo_id = "1"
        else:
            todo_id = str(int(max(TODOS.keys()).lstrip('todo')) + 1)
            print todo_id
            print 'max', max(TODOS.keys())
        TODOS[todo_id] = {'Title': request.form['Title'],
                          'Creation Date': creation_date,
                          'Last Updated date': creation_date,
                          'Due Date': request.form['Due'],
                          'Completed': request.form['Completed'],
                          'Completion Date': request.form['Completion Date']
                          }



class SingleTodo(Resource):
    def get(self, todo_id):
        return {todo_id: TODOS[todo_id]}

    def put(self, todo_id):
        TODOS[todo_id] = {'Title': request.form['Title'],
                          'Due Date': request.form['Due'],
                          'Completed': request.form['Completed']
                          }
        return {todo_id: TODOS[todo_id]}

    def delete(self, todo_id):
        del TODOS[todo_id]
        return TODOS


api.add_resource(TodosList, '/')
api.add_resource(SingleTodo, '/<string:todo_id>')



if __name__ == '__main__':
    app.run(debug=True)
