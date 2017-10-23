from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try :
            if self.path.endswith("/lecturers"):
                lecturers = session.query(Lecturer).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                user_pass = ""
                user_pass += "<html><body>"
                for lecturer in lecturers:
                    user_pass += 'username : '+lecturer.user_lecturer + '\n' + 'password : ' + lecturer.password_lecturer
                    user_pass += "</br></br></br>"
                user_pass += "</body></html>"
                self.wfile.write(user_pass)
                print (user_pass)
                return
            if self.path.endswith("/students"):
                students = session.query(Student).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                result = ""
                result += "<html><body>"
                for student in students:
                    result += str(student.id)+' '+student.user_student+' '+student.password_student+' '+str(student.year_student)+' '+student.section_student+' '+str(student.gpax_student)
                    result += "</br></br></br>"
                result += "</body></html>"
                self.wfile.write(result)
                print (result)
                return
            if self.path.endswith("/enrollments"):
                enrollments = session.query(Enrollment).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                result = ""
                result += "<html><body>"
                for enrollment in enrollments:
                    result += str(enrollment.student_id_enrollment)+' '+str(enrollment.lecturer_id_enrollment)+' '+enrollment.subject_enrollment.code_subject
                    result += "</br></br></br>"
                result += "</body></html>"
                self.wfile.write(result)
                print (result)
                return
            if self.path.endswith("/subjects"):
                subjects = session.query(Subject).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                result = ""
                result += "<html><body>"
                for subject in subjects:
                    result += subject.code_subject+' '+subject.name_subject
                    result += "</br></br></br>"
                result += "</body></html>"
                self.wfile.write(result)
                print (result)
                return



        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', 8080), WebServerHandler)
        print ("Web Server running on port 8080")
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
