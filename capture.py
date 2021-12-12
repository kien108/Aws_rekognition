# %%
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
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
    numerical_order = 0 if len(images) == 0 else len(images)

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
            break
    camera.release()
    cv2.destroyAllWindows()

# %%
# Open Connection string


def OpenConnection():
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

    return client
# %%
# Add face to collection


def AddFace(img, label):
    client = OpenConnection()
    collection_id = "Collection"

    faceimage = io.imread(img)
    # Nếu size của ảnh vượt quá 4096x4096 thì rescale lại thành 2048x2048
    if (faceimage.shape[1] > 4096 or faceimage.shape[1] > 4096):
        faceimage = rescale(faceimage, 0.50, mode='constant')

    externalimageid = label
    # response trả về là dict
    with open(img, 'rb') as fimage:
        response = client.index_faces(CollectionId=collection_id,
                                      Image={'Bytes': fimage.read()},
                                      ExternalImageId=externalimageid,
                                      MaxFaces=1,
                                      QualityFilter="AUTO",
                                      DetectionAttributes=['DEFAULT'])

    print('Results for ' + img)
    print('Faces indexed:')

    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
        print(faceRecord['FaceDetail'])

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(
            unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)

    isSuccessful = False
    if(response != ""):
        isSuccessful = True
    return isSuccessful

# %%
# Nhận diện khuôn mặt


def Authen(img):
    client = OpenConnection()
    collection_id = "Collection"

    # Tìm kiếm khuôn mặt dựa vào collection
    today = date.today()
    images = [cv2.imread(file)
              for file in glob.glob('imgs/' + str(today) + '*.png')]

    isLogin = True
    if img != "":
        targetfilename = img
        # Nhận diện ảnh
        isLogin = False
    else:
        targetfilename = 'imgs/' + \
            str(today) + '_' + str(len(images) - 1) + '.png'

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
        font = ImageFont.truetype(
            r'D:\App Code\font\jetbrain\fonts\ttf\JetBrainsMono-Bold.ttf', fontSize)
        label = faceMatches[0]['Face']['ExternalImageId']

        draw.line(points, fill='#00d400', width=border)
        draw.text((textPosX, textPosY), label, fill="red", font=font)

        if(not isLogin):
            images = [cv2.imread(file)
                      for file in glob.glob('imgs/' + str(today) + '*.png')]

            img_name = str(today) + "_{}.png".format(len(images) + 1)
            targetfilename = "tempImg/"+img_name+".png"
            targetimage.save(targetfilename)
        else:
            targetimage.save(targetfilename)
        return isMatches, targetfilename, label
        # plt.imshow(targetimage)


# %%
# Main


class cl_Form_1(QtWidgets.QMainWindow):
    def __init__(self, isMatch, img, name):
        super(cl_Form_1, self).__init__()
        loadUi('capture.ui', self)

        global status
        status = 'Xác thực danh tính thành công' if isMatch else 'Xác thực danh tính không thành công'
        name = 'Xin chào ' + name if name != "" else ""

        self.lbStatus.setText(status)
        self.lbName.setText(name)

        print(self.btnReCapture.text)

        qpixmap = QPixmap(
            img)
        self.lbImg.setPixmap(qpixmap)

        self.btnReCapture.clicked.connect(self.ReCapture)
        self.btnLogin.clicked.connect(self.Login)

    def ReLoad(self, isMatch, img, name):
        f1 = cl_Form_1(isMatch, img, name)
        f1.show()

    def Login(self):
        if (isMatch):
            self.destroy()
            import menu
        else:
            status = 'Vui lòng chụp lại ảnh khác'
            self.lbStatus.setText(status)

    def ReCapture(self):
        self.close()
        Capture()
        Authen("")
    # Capture()
    # isMatch, img, name = Authen("")
    # self.ReLoad(isMatch, img, name)


# def main():
#     # Load Form
if __name__ == '__main__':
    Capture()
    isMatch, img, name = Authen("")
    app = QtWidgets.QApplication(sys.argv)
    f1 = cl_Form_1(isMatch, img, name)
    f1.show()
    app.exec()


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
