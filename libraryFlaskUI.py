from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

counter = 0

@app.route('/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  
        password = request.form.get('password')

        if username == 'root' and password == 'pass':
            message = "Correct username and password"
            return redirect(url_for('catalog'))
        else:
            message = "Wrong username or password"

    return render_template('login.html', message=message)



@app.route('/catalog', methods=['post', 'get'])
def catalog():        
   
    message = ''
    message = request.args.get('message')
    return render_template('catalog.html', books=catalogTable(), message=message)


@app.route('/add', methods=['post', 'get'])
def add():
   
    message = ''
    if request.method == 'POST':
        bookname = request.form.get('bookname')
        authorname = request.form.get('authorname') 
        f = open("catalog.txt", "a")
        
        if bookname and authorname:         
            from datetime import datetime
            uuid = datetime.now().strftime('%Y%m%d%H%M%S')
            dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            addRecord = "\n" + uuid + " | " + bookname + " | " + authorname + " | Nobody | " + dateTime
            f.write(addRecord)
            f.close()
            recordHistory (addRecord)
            message = 'Info: '+bookname+' by author '+ authorname +' added successfully.'
                       
            return render_template('catalog.html', books=catalogTable(), message=message)
        
    return render_template('add.html', message=message)


@app.route('/checkin', methods=['post', 'get'])
def checkin():
    message = ''
    books = ''
    if request.method == 'POST':
        personname = request.form.get('personname')
        bookname = request.form.get('bookname')
        
        if personname and bookname:
            with open("catalog.txt", "r") as fp:
                for line in lines_that_contain(personname, fp):
                   if (personname in line):
                      recordFound = "true"                      
                      books = books + line            
            if books:
                books = books.replace('\n', '<br/>');            
                return redirect(url_for('checkinlist', personname=personname, books=catalogcheckoutTable(personname)))
            else:
                message = 'Info: No books match with the Book Name provided, please try again.'
        
    return render_template('checkin.html', message=message)

@app.route('/checkout', methods=['post', 'get'])
def checkout():
    message = ''
    books = ''
    if request.method == 'POST':
        personname = request.form.get('personname')
        bookname = request.form.get('bookname')
        
        if personname and bookname:
            with open("catalog.txt", "r") as fp:
                for line in lines_that_contain(bookname, fp):
                   if ("Nobody" in line):
                      recordFound = "true"                      
                      books = books + line            
            if books:
                books = books.replace('\n', '<br/>');            
                return redirect(url_for('checkoutlist', personname=personname, books=catalogNobodyTable(bookname)))
            else:
                message = 'Info: No books match with the Book Name provided, please try again.'
        
    return render_template('checkout.html', message=message)


@app.route('/checkoutlist', methods=['post', 'get'])
def checkoutlist():
    message = ''
    personname = request.args.get('personname')
    books = request.args.get('books')
    
    if request.method == 'POST':
        personname = request.args.get('personname')
        booknumber = request.form.get('booknumber')
      
        if personname and booknumber:
            updateRecord(booknumber, personname, "checkout")
            message = 'Info: Book Id '+booknumber+' checked out by '+personname+' successfully.'
            return render_template('catalog.html', books=catalogTable(), message=message)
        
    return render_template('checkoutlist.html', message=message, personname=personname, books=books)

@app.route('/checkinlist', methods=['post', 'get'])
def checkinlist():
    message = ''
    personname = request.args.get('personname')
    books = request.args.get('books')
    
    if request.method == 'POST':
        personname = request.args.get('personname')
        booknumber = request.form.get('booknumber')
      
        if personname and booknumber:
            updateRecord(booknumber, personname, "checkin")
            message = 'Info: Book Id '+booknumber+' checked in by '+personname+' successfully.'
            return render_template('catalog.html', books=catalogTable(), message=message)
        
    return render_template('checkinlist.html', message=message, personname=personname, books=books)



def recordHistory (record):
    f = open("history.txt", "a")
    f.write("\n" + record)
    f.close()
    
def lines_that_contain(string, fp):
    return [line for line in fp if string in line]


def updateRecord(bookNumber, personName, action):

    recordFound = ''
    with open("catalog.txt", "r") as fpp:
      for line in lines_that_contain(bookNumber, fpp):
          recordFound = "true"
          recordStr = line
           
    if (recordFound == "true"):
        global counter
        counter += 1
        tokens = recordStr.split('|')
        
        from datetime import datetime
        dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if action == "checkout":
          updatedRecord = tokens[0] + "|" + tokens[1] + "|"+ tokens[2] + "| "+ personName + " | " + dateTime
          recordHistory (updatedRecord)
        elif action == "checkin":
          updatedRecord = tokens[0] + "|" + tokens[1] + "|"+ tokens[2] + "| "+ "Nobody" + " | " + dateTime
          recordHistory (updatedRecord)
        
        with open("catalog.txt", "r") as f:
           lines = f.readlines()
        with open("catalog.txt", "w") as f:
           for line in lines:
              if bookNumber in line:                 
                  line = line.replace(recordStr, updatedRecord)                 
                  f.write(line+"\n")
                  print ("Your command has been successful!")
                  print (updatedRecord)
              else:
                  f.write(line)              
    else:
         print ("No book found with provided input")
         
def catalogTable():
    
    data = ""
    rows = ""
    table = ""
    counter = 0
    with open("catalog.txt", "r") as f:
       lines = f.readlines()       
       for line in lines:         
          tokens = line.split('|')
          if tokens:
             if counter == 0:
                 data="<th>"+ tokens[0] +"</th>"+"<th>"+ tokens[1] +"</th>"+"<th>"+ tokens[2] +"</th>"+"<th>"+ tokens[3] +"</th>"+"<th>"+ tokens[4] +"</th>"
                 counter = counter+1
             else:
                 data="<td>"+ tokens[0] +"</td>"+"<td>"+ tokens[1] +"</td>"+"<td>"+ tokens[2] +"</td>"+"<td>"+ tokens[3] +"</td>"+"<td>"+ tokens[4] +"</td>"
           
          rows = rows+"<tr>"+data+"</tr>"          
    
    table = "<table>"+rows+"</table>"   
    return table

def catalogNobodyTable(bookname):
    
    header="<th>Book ID</th><th>Book Name</th><th>Author Name</th><th>Checked Out By</th><th>Last Updated</th>"
    data = ""
    rows = ""
    table = ""
    
    with open("catalog.txt", "r") as fp:
        for line in lines_that_contain(bookname, fp):
           if ("Nobody" in line):
               recordFound = "true"      
               tokens = line.split('|')
               if tokens:                 
                    data="<td>"+ tokens[0] +"</td>"+"<td>"+ tokens[1] +"</td>"+"<td>"+ tokens[2] +"</td>"+"<td>"+ tokens[3] +"</td>"+"<td>"+ tokens[4] +"</td>"                 
               rows = rows+"<tr>"+data+"</tr>"
              
    table = "<table>"+header+rows+"</table>"   
    return table

def catalogcheckoutTable(personname):
    
    header="<th>Book ID</th><th>Book Name</th><th>Author Name</th><th>Checked Out By</th><th>Last Updated</th>"
    data = ""
    rows = ""
    table = ""
    
    with open("catalog.txt", "r") as fp:
        for line in lines_that_contain(personname, fp):          
           recordFound = "true"      
           tokens = line.split('|')
           if tokens:                 
                data="<td>"+ tokens[0] +"</td>"+"<td>"+ tokens[1] +"</td>"+"<td>"+ tokens[2] +"</td>"+"<td>"+ tokens[3] +"</td>"+"<td>"+ tokens[4] +"</td>"                 
           rows = rows+"<tr>"+data+"</tr>"
              
    table = "<table>"+header+rows+"</table>"   
    return table
