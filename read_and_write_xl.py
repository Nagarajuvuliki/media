import awswrangler as wr
import pandas as pd
import boto3
import django
df = pd.read_excel (r'Legal Calling MIS Format - Sep 02.xlsx', nrows = 5)
print (df)
file = "output.xlsx"
df.to_excel(file, index = False) 
print(type(file))
s3 = boto3.resource('s3')
try:
    BUCKET_NAME = 'themedius.ai'
    s3.Bucket(BUCKET_NAME).upload_file(file, f"store_xl/{file}")
    #s3.upload_file('/tmp/' + filename, '<bucket-name>', 'folder/{}'.format(filename))
    #s3.upload_file(file_path,BUCKET_NAME, '%s/%s' % (bucket_folder,dest_file_name))
    uri = f"store_xl/{str(file)}"
    url = f's3://{BUCKET_NAME}/' + uri
    print(url)
except Exception as e:
    uri = None
    print(e)
    print('not done')
    pass