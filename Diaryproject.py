import os
import time

from werkzeug.datastructures import ContentRange
logindir=os.path.dirname(os.path.realpath(__file__))
loginfile=os.path.join(logindir,'loginfo.txt')

userdb={}
with open(loginfile,"r") as f: line=f.readlines()

for i in range(len(line)):
    line[i]=line[i].replace('\n','')
    id,pw= line[i].split(' ')
    userdb[id]=pw

from flask import Flask, session, redirect, url_for, escape, request,render_template
from flask import flash
app=Flask(__name__)
app.secret_key='software_engineering'
@app.route('/')
def index():
    if 'username' in session:
        username=session['username']

        return '2018113581지현민 <br>Logged in as ' + username + '<br>' + \
            "<b><a href = '/logout'>click here to log out</a></b><br>"+\
            "<b><a href = '/board/"+\
            username+"'>click here to move private board</a></b>"
            
    return "2018113581지현민 <br><h1>Diary Project</h1>You are not logged in <br><a href = '/login'></b>click here to login</b></a> <br>"+\
        "<a href = '/signup'></b>click here to make account</b></a>"


   

@app.route('/write/<username>', methods=['GET','POST'])
def writepost(username):
    if request.method=='POST':
        title=request.form['title']
        contents=request.form['content']
        f = request.files['file']
        if f.filename=='' : return '''
            <script>
                alert('Upload ur any pics!');
                history.back();
            </script>
            '''
        if title =='' : return '''
            <script>
                alert('Title should not be empty!');
                history.back();
            </script>
            '''
        if contents =='' : return '''
            <script>
                alert('Content should not be empty!');
                history.back();
            </script>
            '''

        print(title)
        print(contents)

        print(type(contents))
        list=contents.split()
        print(list)

        savedir=os.path.dirname(os.path.realpath(__file__))
        folder=os.path.join(savedir,'posts',username)
        imgfolder=os.path.join(savedir,"static")
        titlefolder=os.path.join(folder,title)

        imgname='/'+username+'_'+title+".jpg"
        if not os.path.exists(titlefolder):
            os.makedirs(titlefolder)
            content=os.path.join(titlefolder,"content.txt")
            f.save(imgfolder+imgname)
            with open(content,'w') as f:
                for i in list:
                    f.write(i)
                    f.write('\n')
        else : return '''
            <script>
                alert('same title already exists!');
                history.back();
            </script>
            '''
        str ='''
            <script>
                alert('diary saved');
                window.location.href = '/board'''+'/'+username+ "'"+ '''
            </script>
            '''
        return str
    return render_template('write.html')
@app.route('/remove/<title>', methods=['GET','POST'])
def removediary(title):
    username=session['username']    
    savedir=os.path.dirname(os.path.realpath(__file__))
    folder=os.path.join(savedir,'posts',username)
    titlefolder=os.path.join(folder,title)
    os.system("rmdir /s /q "+'"'+titlefolder+'"')

    imgfolder=os.path.join(savedir,"static")
    imgname=username+'_'+title+".jpg"
    ans = os.path.join(imgfolder,imgname)
    print(ans)
    os.system("del "+'"'+ans+'"')
    str ='''
        <script>
            alert('diary removed');
            window.location.href = '/board'''+'/'+username+ "'"+ '''
        </script>
        '''
    return str

@app.route('/edit/<title>', methods=['GET','POST'])
def editdiary(title):
    username=session['username']
    savedir=os.path.dirname(os.path.realpath(__file__))
    folder=os.path.join(savedir,'posts',username)
    titlefolder=os.path.join(folder,title)
    contentfile=os.path.join(titlefolder,"content.txt")
    with open(contentfile,'r') as f:
        content=f.readlines()

    ans=''
    for i in content:
        ans+=i
    if request.method=='POST':
        title=request.form['title']
        contents=request.form['content']
        f = request.files['file']
        if f.filename=='' : return '''
            <script>
                alert('Upload ur any pics!');
                history.back();
            </script>
            '''
        
        if title =='' : return '''
            <script>
                alert('Title should not be empty!');
                history.back();
            </script>
            '''
        if contents =='' : return '''
            <script>
                alert('Content should not be empty!');
                history.back();
            </script>
            '''

        list=contents.split()

        savedir=os.path.dirname(os.path.realpath(__file__))
        folder=os.path.join(savedir,'posts',username)
        imgfolder=os.path.join(savedir,"static")
        titlefolder=os.path.join(folder,title)

        imgname='/'+username+'_'+title+".jpg"

        content=os.path.join(titlefolder,"content.txt")
        f.save(imgfolder+imgname)
        with open(content,'w') as f:
            for i in list:
                f.write(i)
                f.write('\n')

        str ='''
            <script>
                alert('diary saved');
                window.location.href = '/board'''+'/'+username+ "'"+ '''
            </script>
            '''
        return str
    print(title)
    return render_template('edit.html',title=title,content=ans)


@app.route('/board/<username>', methods=['GET','POST'])
def showposts(username):
        savedir=os.path.dirname(os.path.realpath(__file__))
        folder=os.path.join(savedir,'posts',username)
        print(folder)
        posts=(os.listdir(folder))
        tmp={}
        for i in posts:
            tmp[i]=time.ctime(os.path.getctime(os.path.join(folder,i)))


        def f2(x): return x[1]

        res = sorted(tmp.items(),key=(lambda x:x[1]), reverse=True)
        
        print()
        print(res)
        

        ans=[]
        for key,val in res:
            ans.append(key)

        print(ans)


        return render_template('posts.html', list1=ans,username=username)


@app.route('/open/<title>', methods=['GET','POST'])
def showdiary(title):
    username=session['username']
    print(os.path.realpath(__file__))
    savedir=os.path.dirname(os.path.realpath(__file__))
    file=os.path.join(savedir,'posts',username,title,"content.txt") 
    print(file)
    with open(file, 'r') as f:
        lines=f.readlines()
    print(savedir)
    path = os.path.join(savedir,'posts',username,title,"img.jpg")


    savedir=os.path.dirname(os.path.realpath(__file__))
    imgfolder=os.path.join(savedir,"static")
    imgname=username+'_'+title+".jpg"
    path='/static/'+imgname
    print("pathh")
    print(path)
    return render_template("diary.html", title=title, str=lines, image_file=path )


@app.route('/signup', methods=['GET','POST'])
def makeaccount():
    if request.method == 'POST':
        id=request.form['username']
        pw=request.form['pw']
        if userdb.get(id) == None:
            with open(loginfile,"a") as f: 
                f.write(id)
                f.write(' ')
                f.write(pw)
                f.write('\n')

            userdb[id]=pw
            print(os.path.realpath(__file__))
            savedir=os.path.dirname(os.path.realpath(__file__))
            folder=os.path.join(savedir,'posts',id)
        
            if not os.path.exists(folder):
                os.makedirs(folder)

            return '''
            <script>
                alert('Account created!');
                window.location.href = 'login';
            </script>
            '''
            
        else :   
            return '''
            <script>
                alert('Id already exist!');
                history.back();
            </script>
            '''

    return '''
    <style>
    p{
        text_algin: center;
    }
    </style>
    <p>2018113581지현민</p>
    <p>Sign up page</p>
    <form action = "" method = "post">
        <p>ID</p>
        <p><input type = text name = username></p>
        <p>PW</p>
        <p><input type = password name = pw></p>
        <p><input type = submit value = Create account></p>
    </form>
    '''



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        id=request.form['username']
        pw=request.form['pw']
        if userdb.get(id) == None:
            return '''
            <script>
                alert('Wrong ID!');
                history.back();
            </script>
            '''
            
        elif userdb.get(id) != pw:
            return '''
            <script>
                alert('Wrong PW!');
                history.back();
            </script>
            '''
        else :   
            session['username']=id
            return redirect(url_for('index'))
    return '''
    <p>2018113581지현민</p>
    <p>Login page</p>
    <form action = "" method = "post">
        <p>ID</p>
        <p><input type = text name = username></p>
        <p>PW</p>
        <p><input type = password name = pw></p>
        <p><input type = submit value = Login></p>
    </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)