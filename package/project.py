from flask_restful import Resource, Api, request
from flask import render_template_string
from package.model import conn

class Projects(Resource):
    """It contain all the api carryign the activity with aand specific project"""

    def get(self):
        """Api to retive all the project from the database"""
        print("reached here")
        projects = conn.execute("SELECT * FROM project  ORDER BY project_id DESC").fetchall()
        return projects


    def post(self):
        """api to add the project in the database"""
        projectInput = request.get_json(force=True)
        name=projectInput['name']
        owner=projectInput['owner']
        status=projectInput['status']
        cost_estimate=projectInput['cost_estimate']
        if (owner[0].isnumeric()!=True):
            print("reached here")
            projectInput['project_id']=conn.execute('''INSERT INTO project(name,owner,status,cost_estimate)
                VALUES(?,?,?,?)''', (name,owner,status,cost_estimate)).lastrowid
            conn.commit()
        else:
            raise Exception("Error: Owner name must not start with a number") 
        return projectInput

class Project(Resource):
    """It contains all apis doing activity with the single project entity"""

    def get(self,id):
        """api to retrive details of the project by it id"""

        project = conn.execute("SELECT * FROM project WHERE project_id=?",(id,)).fetchall()
        return project

    def delete(self,id):
        """api to delete the patiend by its id"""

        conn.execute("DELETE FROM project WHERE project_id=?",(id,))
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """api to update the project by it id"""

        projectInput = request.get_json(force=True)
        name=projectInput['name']
        owner=projectInput['owner']
        status=projectInput['status']
        cost_estimate=projectInput['cost_estimate']
        conn.execute("UPDATE project SET name=?,owner=?,status=?,cost_estimate=? WHERE project_id=?",
                     (name,owner,status,cost_estimate,id))
        conn.commit()
        return projectInput