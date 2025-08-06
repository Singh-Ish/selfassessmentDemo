import flask
try:
    from sapp import db 
except ImportError:
    db = None
#from werkzeug.security import generate_password_hash, check_password_hash
from sapp import admin
from mongoengine import Document, IntField, StringField
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    print("Pandas not available, using openpyxl fallback")
    import openpyxl
    PANDAS_AVAILABLE = False
import os
from flask import flash,json

# Helper function to read Excel files
def read_excel_file(file_path):
    """Read Excel file and return list of dictionaries"""
    try:
        if PANDAS_AVAILABLE:
            df = pd.read_excel(file_path)
            return df.to_dict("records")
        else:
            # Use openpyxl as fallback
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
            
            # Get headers from first row
            headers = [cell.value for cell in ws[1]]
            
            # Get data from remaining rows
            data = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                row_dict = {}
                for i, value in enumerate(row):
                    if i < len(headers) and headers[i]:
                        row_dict[headers[i]] = value
                data.append(row_dict)
            
            return data
    except Exception as e:
        print(f"Error reading Excel file {file_path}: {e}")
        return []

# database  schema  are described here
class User(Document):
    # user authentication information 
    userId = IntField(unique=True) # same as student id
    email = StringField( max_length=50, unique=True)
    firstName = StringField(max_length=50)
    lastName = StringField(max_length=50)
    username = StringField(max_length=50, unique=True)
    password = StringField(max_length=50)
    
    def userUpload():
        # check if the role is student or admin 
        print("hello from the user upload function ")
        
        ro = role.objects()
        #data = User.objects()
        
        # resetting the access for students 
        
    
        for r in ro:
            if (r.rname == 'student'):
                data = User.objects(userId=r.userId)
                r.delete()
                data.delete()
        
        print("reading the excel file ")
        # adding the user details to the database 
        usr = read_excel_file('sapp/static/docs/userDetails.xlsx')
        print(usr)

        #flash("can't read the file headers", "danger")

        for u in usr:
            
            userId = u['userId']
            firstName = u['firstName']
            lastName = u['lastName']
            email = u['email']
            email = email.lower()
            
            
                
            s = User(userId=userId,firstName=firstName,lastName=lastName,email=email)
            s.save()

            ro = role(userId=userId)
            ro.save()
            #print("uploaded the new user {} to the database".format(userId))

        print("added the users to the database")    
    
    '''
    password = db.StringField()

    # user information 
    firstName = db.StringField( max_length=50)
    lastName = db.StringField( max_length=50)

    roles = db.relationship('Role',secondary='user_roles', backref = db.backref('users,lazy='dynamic'))

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password, password)

    '''


class rubics(Document):
    Indicator = StringField()
    Beginning = StringField()
    Developing = StringField()
    Accomplished = StringField()
    Exemplary = StringField()

    def uploadnew():
        #deleting all the previous data
        data = rubics.objects()
        data.delete()
        #db.DeleteMany({})
        rub = read_excel_file('sapp/static/docs/rubicsMetrix.xlsx')

        for r in rub:
            #print(r['Indicator'])
            Indicator = r['Indicator']
            Beginning = r['Level 1: Beginning']
            Developing = r['Level 2: Developing']
            Accomplished = r['Level 3: Accomplished']
            Exemplary = r['Level 4: Exemplary']
            s = rubics(Indicator=Indicator,Beginning=Beginning,Developing=Developing,Accomplished=Accomplished,Exemplary=Exemplary)
            s.save()
            print("uploaded the new rubics to the database")


class projects(Document):
    groupNo = IntField()
    title = StringField(max_length=200)
    supervisor = StringField(max_length=200)
    coSupervisor = StringField(max_length=200)
    userId = IntField(unique=True , required=True)
    lastName = StringField( max_length=50)
    firstName = StringField( max_length=50)
    assessmentStatus = IntField()

    def pupload():
        
        #deleting all the previous data
        data = projects.objects()
        data.delete()

        # reading the file from the uploaded location 
        pf = read_excel_file('sapp/static/docs/projectDetails.xlsx')
        
        # Basic data cleaning - handle missing values
        for project in pf:
            if 'coSupervisor' not in project or project['coSupervisor'] is None:
                project['coSupervisor'] = ''
            
            # Ensure required fields are not None
            for field in ['groupNo', 'userId', 'assessmentStatus']:
                if project.get(field) is None:
                    project[field] = 0

        for p in pf:
            groupNo = int(p['groupNo']) if p['groupNo'] is not None else 0
            title = p['title']
            supervisor = p['supervisor']
            coSupervisor = str(p['coSupervisor']) if p['coSupervisor'] is not None else ''
            userId = int(p['userId']) if p['userId'] is not None else 0
            lastName = p['lastName']
            firstName = p['firstName']
            assessmentStatus = int(p['assessmentStatus']) if p['assessmentStatus'] is not None else 0
            
            s = projects(groupNo=groupNo, title=title, supervisor=supervisor, coSupervisor=coSupervisor, userId=userId,
                             lastName=lastName, firstName=firstName, assessmentStatus=assessmentStatus)
            s.save()
            print("uploaded the new projects data to the database")
        


######## sa Matrix
class samatrix(Document):
    sid = IntField()
    fsid = IntField()
    fsname = StringField()
    Indicator = StringField()
    value = IntField()

    #### defining a fuction eval


    def eval():
        # doing the export the result first

        pro = projects.objects(assessmentStatus=1)

        # reading all the projects who have filled the assessment
        ru = rubics.objects.all()

        result = []
        for p in pro:
            rin = dict([('StudentId/GA', p.userId), ('LastName', p.lastName),('FirstName',
                                            p.firstName)])

            for r in ru:
                res = samatrix.objects(fsid=p.userId, Indicator=r.Indicator)
                res = res.to_json()
                res = json.loads(res)
                
                # Calculate average without pandas
                if res:
                    values = [item['value'] for item in res if 'value' in item]
                    vavg = int(sum(values) / len(values)) if values else 0
                else:
                    vavg = 0
                
                rinl = dict([(r.Indicator, vavg)])
                rin.update(rinl)

            result.append(rin)

        # adding the projects where students havent given assessment
        pro = projects.objects(assessmentStatus=0)

        # reading all the projects who have filled the assessment
        ru = rubics.objects.all()

        eresult = []
        for p in pro:
            rin = dict([('StudentId/GA', p.userId), ('LastName', p.lastName), ('FirstName',
                                                                            p.firstName)])
            for r in ru:
                vavg = 'NA'
                #print(vavg)
                rinl = dict([(r.Indicator, vavg)])

                rin.update(rinl)

            eresult.append(rin)

        
        cresult = result + eresult

        # Simple Excel output without pandas
        if PANDAS_AVAILABLE:
            df = pd.DataFrame(cresult)
            try:
                df = df.rename(columns={'6.1 Personal and group time management': 'GA 6.1', '6.2 Group culture, group dynamics': 'GA 6.2', '6.3 Leadership: initiative and mentoring, areas of expertise, and interdisciplinary teams':'GA 6.3'})
                print(df)
            except:
                print("can't change the columns")
            
            filename = 'assessmentresult.xlsx'
            df.to_excel(filename,index=False)
            print("saved the xls file")
        else:
            # Basic Excel output using openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            
            if cresult:
                # Write headers
                headers = list(cresult[0].keys())
                for col, header in enumerate(headers, 1):
                    ws.cell(row=1, column=col, value=header)
                
                # Write data
                for row, data in enumerate(cresult, 2):
                    for col, header in enumerate(headers, 1):
                        ws.cell(row=row, column=col, value=data.get(header, ''))
            
            filename = 'assessmentresult.xlsx'
            wb.save(filename)
            print("saved the xls file")



class emailtemplate(Document):
    #userId = db.IntField(unique=True, required=True) in future there will be multiple admins so multiple templates
    sender = StringField(default='ishdeepsingh@sce.carleton.ca')
    subject = StringField(default='self assessment portal')
    message = StringField(default='please submit your assessment ')

########## students comments and feedback 
class feedback(Document):
    userId = IntField(unique=True)
    name = StringField()
    comment = StringField()


####### faculty related data for sending email automatically once all the groups submit the assesment 
class faculty(Document):
    lastName = StringField(unique=True)
    firstName = StringField()
    email = StringField(max_length=30, unique=True)

    def newf():
        #deleting all the previous data
        data = faculty.objects()
        data.delete()
        #db.DeleteMany({})
        fa = read_excel_file('sapp/static/docs/facultyDetails.xlsx')
        
        print(fa)
        
        for r in fa:
            lastName = r['lastName']
            firstName = r['firstName']
            email = r['email']
            s = faculty(lastName=lastName,firstName=firstName,email=email)
            s.save()
            #print("uploaded the new faculty data to the database")
        

#######role based authentication 
class role(Document):
    userId = IntField(unique=True)
    rname = StringField(max_length=30, default='student')

