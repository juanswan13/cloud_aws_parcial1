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
        red = 0
        img = Image.open(tmp)
        for pixel in img.getdata():
            if pixel == (0, 0, 0): # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
             black += 1
            else:
                red += 1
        print('black=' + str(black)+', red='+str(red))
    print("Funciona el trriger")
    return "Hello form lambda"

