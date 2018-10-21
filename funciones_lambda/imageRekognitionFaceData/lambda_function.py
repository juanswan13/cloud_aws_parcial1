import boto3

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    if(event):
        FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = str(event["Records"][0]["s3"]["object"]["key"])
        faces = detect_faces(bucket, key)
        print('salida: ', faces)
        crearArchivo(key)
        escribirRespuesta(faces)
        ruta = 'answers/' +  key + ".txt"
        s3.upload_file('/tmp/respuesta.txt',bucket, ruta)


def detect_faces(bucket, key, attributes=['ALL'], region="eu-west-2"):
	rekognition = boto3.client('rekognition')
	response = rekognition.detect_faces(
	    Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
	    Attributes=attributes,
	)
	return response['FaceDetails']
	
def crearArchivo(key):
    archivo = open('/tmp/respuesta.txt', 'w')
    archivo.close()

def escribirRespuesta(faces):
    archivo = open('/tmp/respuesta.txt', 'a')
    contador = 0
    for face in faces:
        contador = contador + 1
        face_num = 'Face' + str(contador)
        archivo.write('-------------------------------- ' + face_num + ' --------------------------------' + '\n')
        #Gender
        archivo.write('- Gender: ' + str(face['Gender']['Confidence']) + '% ' + str(face['Gender']['Value']) + '\n')
        #Age
        archivo.write('- Age Range: ' + str(face['AgeRange']['Low']) + ' - ' + str(face['AgeRange']['High']) + '\n')
        #Smile
        if(str(face['Smile']['Value'])=='True'):
            archivo.write("- Face Smile: YES " + str(face['Smile']['Confidence']) + '% of Confidence'  + '\n')
        else:
            archivo.write("- Face Smile: NO " + str(face['Smile']['Confidence']) + '% of Confidence'  + '\n')
        #Mustache
        if(str(face['Mustache']['Value'])=='True'):
            archivo.write("- The face has mustache " + str(face['Mustache']['Confidence']) + '% of Confidence'  + '\n')
        else:
            archivo.write("- The face has no mustache " + str(face['Mustache']['Confidence']) + '% of Confidence'  + '\n')
        #EyesOpen
        if(str(face['EyesOpen']['Value'])=='True'):
            archivo.write("- Face has the eyes open " + str(face['EyesOpen']['Confidence']) + '% of Confidence'  + '\n')
        else:
            archivo.write("- Face has the eyes closed " + str(face['EyesOpen']['Confidence']) + '% of Confidence'  + '\n')
        #MouthOpen
        if(str(face['MouthOpen']['Value'])=='True'):
            archivo.write("- The face has the mouth open " + str(face['MouthOpen']['Confidence']) + '% of Confidence'  + '\n')
        else:
            archivo.write("- The face doen not have the mouth open " + str(face['MouthOpen']['Confidence']) + '% of Confidence'  + '\n')
        #Emotions
        for emotion in face['Emotions']:
            archivo.write('- ' + str(emotion['Type']) + " : " + str(emotion['Confidence']) + '%' + '\n')
        #Glasses
        if((str(face['Eyeglasses']['Value'])=='True') or (str(face['Sunglasses']['Value'])=='True')):
            if((str(face['Eyeglasses']['Value'])=='True')):
                archivo.write("-Face wear Eyeglasses  " + str(face['Eyeglasses']['Confidence']) + '% of Confidence'  + '\n')
            else:
                archivo.write("- Face wear Sunglasses " + str(face['Sunglasses']['Confidence']) + '% of Confidence'  + '\n')
        else:
            archivo.write("- Face doesn't wear glasses " + str(face['Smile']['Confidence']) + '% of Confidence'  + '\n')
        archivo.write('------------------------------ END ' + face_num + ' ------------------------------' + '\n')
    archivo.close()
