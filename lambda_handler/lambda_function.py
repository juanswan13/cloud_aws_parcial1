import boto3
from PIL import Image

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    if (event):
        print("Event:", event)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = str(event["Records"][0]["s3"]["object"]["key"])
        print (key)
        tmp = "/tmp/" + key
        
        s3.download_file(Bucket=bucket, Key=key, Filename=tmp)
        
        black = 0
        allPixels = 0
        img = Image.open(tmp)
        for pixel in img.getdata():
            imageType = 0
            try:
                value = int(pixel)
                imageType = 1
            except:
                pass  # not an int.
            
            if(imageType==0):
                black += color_image_count(pixel)
            else:
                black += gray_image_count(pixel)
            allPixels += 1
            
        print("Black: ", black)
        print("Total: ", allPixels)
        crearArchivo()
        escribirRespuesta(black, allPixels, key)
        s3.upload_file('/tmp/respuesta.txt',bucket, 'respuesta.txt')
    print("Funciona el trriger")
    return "Hello form lambda"

def color_image_count(pixel):
    isblack = 0
    black = 0
    for i in pixel:
        if (i<35):
          isblack +=  1
    if (isblack>=2):
        black +=1
    return black


def gray_image_count(pixel):
    black =0
    if (pixel<=80):
        black +=1
    return black
    
def crearArchivo():
    archivo = open('/tmp/respuesta.txt', 'w')
    archivo.close()

def escribirRespuesta(black, total,key):
    archivo = open('/tmp/respuesta.txt', 'a')
    archivo.write("PixelesNegros:")
    archivo.write(str(black))
    archivo.write(';')
    archivo.write("Total:")
    archivo.write(str(total))
    archivo.write(';')
    archivo.write(key)
    archivo.close()
    
