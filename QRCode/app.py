
from fileinput import filename
from flask import Flask, render_template, request
import qrcode
import image
import os
from azure.storage.blob import BlockBlobService

# Used to store the inage generated to the local system
UPLOAD_FOLDER = 'QRCode/templates/static/'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Azure Part 
account = app.config['ACCOUNT']   # Azure account name
key = app.config['STORAGE_KEY']      # Azure Storage account access key  
container = app.config['CONTAINER'] # Container name

blob_service = BlockBlobService(account_name=account, account_key=key)

@app.route("/", methods=['GET','POST'])
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'QRbackground.jpg')
    back_img = "/static/QRbackground.jpg" 
    return render_template("index.html", user_image = back_img)
    

@app.route("/result", methods=['GET','POST'])
def result():

    # Get link from the form from the html page
    link = request.args.get("url")
    print(link)
    if not link:
        return render_template("failure.html")

   
    # Generation of QR Code
    image = qrcode.make(link)
    image.save(" //// Specify the path + filename here //// ","PNG")



    # Store the image in the bucket on Azure

    file = image

    print(file)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'QRTEST.png'))

    immmg = '//// Specify the path + filename here //// '

    filename = "QRTEST.png"

    blob_name = 'QRTEST.png'
    blob_service.create_blob_from_path(container, blob_name , immmg)

    try:
        blob_service.create_blob_from_stream(container, immmg, file)
    except Exception:
        print ('Exception=' + Exception)
        pass
    ref =  'http://'+ account + '.blob.core.windows.net/' + container + '/' + filename
    
    print(ref)



    # Display the image from the bucket
    # if you are using Azure Cloud Storage Bucket pass ref to the return statement
    # IF you are running and storing on the local host then use the file path in the return statement 
    return render_template("result.html", qr = ref)


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True) 
   