from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import database_CRUD

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                id=self.path.split("/")[2]
                name=database_CRUD.get_restaurant(id).name
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete "+name+"? </h1>"
                output +="<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % id
                output += "<input type='submit' value='delete'>\
                </form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                id=self.path.split("/")[2]
                name=database_CRUD.get_restaurant(id).name
                output = ""
                output += "<html><body>"
                output += "<h1>"+name+"</h1>"
                output +="<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % id
                output += "<input name='newRestaurantName' type='text' placeholder='%s'> <input type='submit' value='Rename'>\
                </form>" % name
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output +="<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>\
                <input name='newRestaurantName' type='text' value='New Restaurant name'> <input type='submit' value='Create'>\
                </form>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                restaurantList=database_CRUD.list_all_restaurant()    
                output=""
                output +="<html><body>"
                output += "<a href='/restaurants/new'>Make a new Restaurant here</a></br>"
                
                for restaurant in restaurantList: 
                    options="<a href='restaurants/%s/edit'/>Edit</a>" %restaurant.id
                    options+="<a href='restaurants/%s/delete'>Delete</a>" %restaurant.id 
                    output += restaurant.name+" "+options+"</br>" 
                self.wfile.write(output)
                #print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output=""
                output +="<html><body>&#161 Hola <a href='/hello'>Back to Hello</a>"
                output +="<form method='POST' enctype='multipart/form-data' action='/hello'>\
                Enter something:<input name='message' type='text'> <input type='submit' value='Submit'>\
                </form>"
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError as identifier:
            self.send_error(404,"File not found %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                id=self.path.split("/")[2]
                name=database_CRUD.get_restaurant(id)

                database_CRUD.delete_restaurant(id)

                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                #print output
                return
            if self.path.endswith("/edit"):
                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                if ctype=='multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent=fields.get('newRestaurantName')
                
                id=self.path.split("/")[2]
                name=database_CRUD.get_restaurant(id)

                database_CRUD.update_restaurant(id,messagecontent[0])

                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                #print output
                return
            if self.path.endswith("/restaurants/new"):
                ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
                if ctype=='multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent=fields.get('newRestaurantName')

                database_CRUD.create_restaurant(messagecontent[0])

                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                #print output
                return

        except:
            pass








def main():
    try:
        port=8080
        server=HTTPServer(('',port),webserverHandler)
        print "webserver running on port %s" %port
        server.serve_forever()

    except KeyboardInterrupt:
        print "Stopping web server.."
        server.socket.close()


if __name__=='__main__':
    main()