# %%
from PIL import Image, ImageDraw, ImageColor, ImageFont
import numpy as np
import boto3
import csv
from matplotlib import pyplot as plt
from skimage.transform import rescale
from skimage import io
import cv2
from datetime import date
import glob
import sys


# %%
# Capture
def Capture():
    camera = cv2.VideoCapture(0)
    today = date.today()

    # Load ra tất cả ảnh đã capture hôm nay
    images = [cv2.imread(file)
              for file in glob.glob('imgs/' + str(today) + '*.png')]

    # Số thứ tự để lưu ảnh, = 0 nếu hôm nay chưa có ảnh, = len() + 1 nếu đã có ảnh rồi
    numerical_order = 0 if len(images) == 0 else len(images) + 1

    while True:
        ret, frame = camera.read()

        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("Space to capture/ Esc to quit", frame)

        key = cv2.waitKey(1)
        # ESC to exit
        if key % 256 == 27:
            print("ESC, turn off the camera")
            break
        # Space to capture
        elif key % 256 == 32:
            img_name = str(today) + "_{}.png".format(numerical_order)
            cv2.imwrite("imgs/" + img_name, frame)
            print("Screenshot taken, spacebar")
    camera.release()
    cv2.destroyAllWindows()

# %%
# Authen


def Authen(collection_id):

    # Đọc dữ liệu từ file new_user_credentials.csv
    # Lấy ra access_key_id và secret_access_key
    with open('new_user_credentials.csv', 'r') as input:
        next(input)
        reader = csv.reader(input)
        for line in reader:
            access_key_id = line[2]
            secret_access_key = line[3]

    # Mở client connection
    client = boto3.client('rekognition',
                          region_name='us-east-2',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)

    # Nếu collection_id = "" => Tạo collection mới
    if (collection_id != ""):
        response = client.create_collection(CollectionId=collection_id)
        print('Collection ARN: ' + response['CollectionArn'])
        print('Status Code:' + str(response['StatusCode']))
        print('Done...')
    else:
        collection_id = "Collection"

    # Tìm kiếm khuôn mặt dựa vào collection
    today = date.today()
    images = [cv2.imread(file)
              for file in glob.glob('imgs/' + str(today) + '*.png')]

    targetfilename = 'imgs/' + str(today) + '_' + str(len(images)) + '.png'
    targetimage = Image.open(targetfilename)
    plt.imshow(targetimage)

    threshold = 70
    maxFaces = 5

    with open(targetfilename, 'rb') as timage:
        response2 = client.search_faces_by_image(CollectionId=collection_id,
                                                 Image={
                                                     'Bytes': timage.read()},
                                                 FaceMatchThreshold=threshold,
                                                 MaxFaces=maxFaces)

    faceMatches = response2['FaceMatches']
    isMatches = False
    if (len(faceMatches) > 0):
        isMatches = True
        # Đóng khung khuôn mặt
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

        points = ((left, top), (left+width, top), (left+width,
                                                   top+height), (left, top+height), (left, top))
        print("break1")
        font = ImageFont.truetype(
            r'D:\App Code\font\jetbrain\fonts\ttf\JetBrainsMono-Bold.ttf', fontSize)
        print(font)
        label = faceMatches[0]['Face']['ExternalImageId']

        draw.line(points, fill='#00d400', width=border)
        draw.text((textPosX, textPosY), label, fill="red", font=font)

        plt.imshow(targetimage)

    return isMatches

# %%
# Main


def main():
    Capture()
    if (Authen("")):
        print("Xác nhận danh tính thành công")
    else:
        print("Không xác nhận được")


if __name__ == '__main__':
    sys.exit(main())

# --------------------  AUTHEN ---------------
 # %%
 # Sử dụng các thư viện:
 # + boto3: thư viện python của AWS
 # + PIL: thư viện hình ảnh của python


# --------------------- TESTING --------------------------------
# %%
# External của bức ảnh match


# %%


# print('Matching faces')
# for match in faceMatches:
#     print('FaceId:' + match['Face']['FaceId'])
#     print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
#     print('ExternalImageId: ' + match['Face']['ExternalImageId'])


# Xóa collection
# %%
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

# %%