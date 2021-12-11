#%%
# Sử dụng các thư viện:
# + boto3: thư viện python của AWS
# + PIL: thư viện hình ảnh của python
from skimage import io
from skimage.transform import rescale
from matplotlib import pyplot as plt
import csv
import boto3
import numpy as np
import capture
from PIL import Image, ImageDraw, ImageColor, ImageFont

#%%
# Đọc dữ liệu từ file new_user_credentials.csv
# Lấy ra access_key_id và secret_access_key
with open('new_user_credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

# Tạo collection trong AWS Rekognition
#%%
client = boto3.client('rekognition',
                        region_name = 'us-east-2',
                        aws_access_key_id = access_key_id,
                        aws_secret_access_key= secret_access_key)
collection_id = 'Collection'
response = client.create_collection(CollectionId=collection_id)
print('Collection ARN: ' + response['CollectionArn'])
print('Status Code:' + str(response['StatusCode']))
print('Done...')
# %%


# --------------------------- TRAINING ---------------------
# Tải hình ảnh lên để train
#%%
filename = "./captain/captainTrain2.jpg"
faceimage = io.imread(filename)
# Nếu size của ảnh vượt quá 4096x4096 thì rescale lại thành 2048x2048
if (faceimage.shape[1] > 4096 or faceimage.shape[1] > 4096):
    faceimage = rescale(faceimage, 0.50, mode='constant')
plt.imshow(faceimage)


# Thêm hình ảnh vào collection
# Đọc data ảnh dưới dạng nhị phân
# index_faces phát hiện các khuôn mặt từ hình ảnh #upload và thêm chúng vào collection dưới dạng: mỗi #khuôn mặt sẽ gồm 1 vector chứa các đặc điểm của #khuôn mặt đó

# Parameter:
#   + CollectionId:id của collection chỉ định để thêm khuôn mặt zô
#   + Image: đưa hình ảnh upload vào dưới dạng binary (base64)
#   + ExternalImageId: id sẽ gán cho tất cả khuôn mặt được phát hiện trong bức ảnh
#   + MaxFaces: Số khuôn mặt tối đa sẽ lưu vào collection (phát hiện 10 thì sẽ lọc ra 9 cái chất lượng thấp nhất)
#   + QualityFilter: bộ lọc chất lượng hình ảnh (low, medium, high, auto)
#   + DetectionAttributes: chỉ định số thuộc tính muốn trả về trên face (boundingbox, confidence, pose, quality,...)

#%%
# externalimageid = filename
externalimageid = "CaptainAmerica"
# response trả về là dict
with open(filename, 'rb') as fimage:
    response = client.index_faces(CollectionId = collection_id,
                             Image = {'Bytes': fimage.read()},
                             ExternalImageId = externalimageid,
                             MaxFaces = 1,
                             QualityFilter = "AUTO",
                             DetectionAttributes = ['DEFAULT'])

print('Results for ' + filename)
print('Faces indexed:')

for faceRecord in response['FaceRecords']:
     print('  Face ID: ' + faceRecord['Face']['FaceId'])
     print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
     print(faceRecord['FaceDetail'])

print('Faces not indexed:')
for unindexedFace in response['UnindexedFaces']:
    print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
    print(' Reasons:')
    for reason in unindexedFace['Reasons']:
        print('   ' + reason)


# Xem Bounding box của khuôn mặt phát hiện
# %%
img = Image.open(filename)
imgWidth, imgHeight = img.size

draw = ImageDraw.Draw(img)
for faceRecord in response['FaceRecords']:
    box = faceRecord['Face']['BoundingBox']
    left = imgWidth * box['Left']
    top = imgHeight * box['Top']
    width = imgWidth * box['Width']
    height = imgHeight * box['Height']

    points = ((left,top),(left+width,top),(left+width,top+height),(left,top+height),(left,top))

    draw.line(points,fill='#00d400', width=2)

plt.imshow(img)

# In ra danh sách khuôn mặt trong collection
#%%
maxResults = 10
faces_count=0
tokens=True

response=client.list_faces(CollectionId=collection_id,
                           MaxResults=maxResults)
print('Faces in collection ' + collection_id)

while tokens:
    faces=response['Faces']
    for face in faces:
        print (face)
        print('-----------------------------------------')
        faces_count+=1
    if 'NextToken' in response:
        nextToken=response['NextToken']
        response=client.list_faces(CollectionId=collection_id,
                                   NextToken=nextToken,MaxResults=maxResults)
    else:
        tokens=False


# --------------------- TESTING ------------------
# Tìm kiếm khuôn mặt dựa vào collection
#%%
targetfilename = "./captain/captain1.jpg"
targetimage = Image.open(targetfilename)
plt.imshow(targetimage)

threshold = 70
maxFaces= 5

with open(targetfilename, 'rb') as timage:
    response2 = client.search_faces_by_image                    (CollectionId=collection_id,
                            Image = {'Bytes': timage.read()},
                            FaceMatchThreshold = threshold,
                            MaxFaces = maxFaces)

faceMatches = response2['FaceMatches']
print ('Matching faces')
for match in faceMatches:
        print ('FaceId:' + match['Face']['FaceId'])
        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print ('ExternalImageId: ' + match['Face']['ExternalImageId'])


#%%
# Vẽ bounding box cho khuôn mặt phát hiện
# External của bức ảnh match
imgWidth, imgHeight = targetimage.size
draw = ImageDraw.Draw(targetimage)

box = response2['SearchedFaceBoundingBox']
left = imgWidth * box['Left']
top = imgHeight * box['Top']
width = imgWidth * box['Width']
height = imgHeight * box['Height']

textPosX = left - 30
if imgWidth > 400:
    border = 10
    fontSize = 70
    textPosY = top - 80
else:
    border = 2
    fontSize = 20
    textPosY = top - 20

points = ((left,top),(left+width,top),(left+width,top+height),(left,top+height),(left,top))
font = ImageFont.truetype(r'D:\App Code\font\jetbrain\fonts\ttf\JetBrainsMono-Bold.ttf', fontSize)
label = faceMatches[0]['Face']['ExternalImageId']

draw.line(points,fill = '#00d400', width = border)
draw.text((textPosX, textPosY), label, fill = "red", font = font)

plt.imshow(targetimage)



# Xóa collection
#%%
# print('Attempting to delete collection ' + collection_id)
# status_code=0
# try:
#     response=client.delete_collection(CollectionId=collection_id)
#     status_code=response['StatusCode']
#     print('All done!')
#     print(status_code)

# except ClientError as e:
#     if e.response['Error']['Code'] == 'ResourceNotFoundException':
#         print ('The collection ' + collection_id + ' was not found ')
#     else:
#         print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
#     status_code=e.response['ResponseMetadata']['HTTPStatusCode']
