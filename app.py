import os
import uuid
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import yt_dlp


base_directory = os.path.dirname(os.path.abspath(__file__))
download_directory = os.path.join(base_directory, 'downloads')

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form.get('user')

        if username == "test":
            return ""

@app.route('/script_upload', methods=['POST'])
def script_upload():
    file = request.files['file']
    script = file.read().decode()

    letterGroups = [["a","e","i"],["o"],["Ee"],["c","d","g","k","n","s","t","x","y","z"],["b","m","p"],["ch","j","sh"],["l"],["q","w"],["f","v"],["th"],["r"],["u"]]
    script = script.lower()
    shapes = [1,2,3,4,5,6,7,8,9,10,11,12]
    neededshapes = []
    words = script.split(" ")
    for i in range(len(words)):
        for j in range(len(words[i])):
            letter = words[i][j]
            
            if letter in letterGroups[0]:
                if letter == "a" or letter == "i":                    
                    neededshapes.append(str(shapes[0])+letter)

                elif letter == "e":
                    if words[i][j-1] == "e":   
                            neededshapes.append(str(shapes[2])+letter+"e")
                    else:
                        if j < len(words[i]) - 1:
                            if words[i][j+1] == "e":
                                pass
                            else:                                
                                neededshapes.append(str(shapes[0])+letter)
                        else:                           
                            neededshapes.append(str(shapes[0])+letter)
                        
            if letter in letterGroups[1]:               
                neededshapes.append(str(shapes[1])+letter)
            
            if letter in letterGroups[3]:
                if letter != "c" and letter != "s" and letter !="t":                   
                    neededshapes.append(str(shapes[3])+letter)
                else:
                    if j < len(words[i]) - 1:
                        if words[i][j+1] == "h":
                            if letter == "t" or letter == "c":
                                neededshapes.append(str(shapes[9])+letter+"h")
                            else:                               
                                neededshapes.append(str(shapes[5])+letter)
                                pass
                        else:                            
                            neededshapes.append(str(shapes[3])+letter)
                    else:                        
                        neededshapes.append(str(shapes[3])+letter)
                        
            if letter in letterGroups[4]:               
                neededshapes.append(str(shapes[4])+letter)
                    
            if letter == "j":               
                neededshapes.append(str(shapes[5])+letter)
                
            if letter in letterGroups[6]:                
                neededshapes.append(str(shapes[6])+letter)
                
            if letter in letterGroups[7]:                
                neededshapes.append(str(shapes[7])+letter)
                
            if letter in letterGroups[8]:                
                neededshapes.append(str(shapes[8])+letter)
            
            if letter in letterGroups[10]:                
                neededshapes.append(str(shapes[10])+letter)
                
            if letter in letterGroups[11]:               
                neededshapes.append(str(shapes[11])+letter)
                
        neededshapes.append(" ")
    
    filename = f'{uuid.uuid4()}.txt'

    if not os.path.exists(download_directory):
        os.makedirs(download_directory, exist_ok=True)


    output = open(os.path.join(download_directory, filename) , "w")
    for i in range(len(neededshapes)):
        output.write(str(neededshapes[i]))
        output.write("\n")
    output.close()


    return render_template('download.html', filename = filename, script=neededshapes)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(download_directory, filename, download_name='result.txt')



if __name__ == '__main__':
    app.run(debug=True)