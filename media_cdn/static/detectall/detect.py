import cv2
import numpy as np
import pytesseract
import os
from skimage import io
from PIL import Image
from os.path import abspath, join, dirname
from django.conf import settings


def callMy():
    path = os.path.dirname(__file__) + "/imgs"

    # def pathpass(self, *args):
    #     global path


    per = 25
    # roi = [[(315, 487), (384, 510), 'text', 'Country Code'],
    #        [(427, 488), (576, 526), 'text', 'Passport No'],
    #        [(200, 520), (384, 550), 'text', 'Surname'],
    #        [(201, 558), (387, 588), 'text', 'Given Name'],
    #        [(216, 596), (333, 610), 'text', 'Nationality'],
    #        [(216, 620), (344, 635), 'text', 'Date of Birth'],
    #        [(301, 643), (504, 669), 'text', 'Place of Birth'],
    #        [(216, 678), (370, 697), 'text', 'Date of Issue'],
    #        [(217, 704), (373, 729), 'text', 'Date of Expiry'],
    #        [(60, 277), (213, 300), 'text', 'Otasining Ismi'],
    #        [(51, 364), (310, 409), 'text', 'given from whom']]

    # roi = [[(33, 193), (301, 221), 'text', 'Familiyasi'],
    #        [(33, 242), (301, 267), 'text', 'Ismi'],
    #        [(33, 283), (301, 310), 'text', 'Otasining ismi'],
    #        [(580, 241), (681, 280), 'text', 'Jinsi'],
    #        [(33, 325), (273, 353), 'text', "Tug'ilgan sanasi"],
    #        [(284, 328), (552, 356), 'text', "Tug'ilgan joyi"],
    #        [(33, 364), (254, 390), 'text', 'Millati'],
    #        [(36, 404), (354, 451), 'text', 'Kim tmonidan berilgan'],
    #        [(541, 572), (730, 601), 'text', 'Passport seriya raqami'],
    #        [(254, 837), (431, 857), 'text', 'Berilgan vaqti'],
    #        [(256, 870), (458, 900), 'text', 'Tugash muddati'],
    #        [(469, 972), (731, 1004), 'text', 'DDD']]


    # [[(251, 748), (403, 775), 'text', "Tug'ilgan vaqti"],
    # [(538, 570), (592, 602), 'text', 'pSeria'],
    #  [(591, 572), (735, 606), 'text', 'Passport raqami'],
    #  [(506, 962), (740, 1014), 'text', 'Lastoption'],
    #  [(451, 956), (726, 1007), 'text', 'lastOption'],
    #  [(248, 833), (420, 860), 'text', 'berilgan muddati']]

    roi = [[(34, 235), (309, 269), 'text', 'name'],
           [(33, 189), (309, 220), 'text', 'surName'],
           [(33, 281), (316, 313), 'text', 'farthersName'],
           [(251, 748), (403, 775), 'text', "dataBirth"],
           [(252, 832), (448, 863), 'text', 'dataGivenPassport'],
           [(253, 868), (458, 901), 'text', 'dataExpirePassport'],
           [(578, 236), (684, 285), 'text', 'gender'],
           [(538, 570), (592, 602), 'text', 'pSeria'],
           [(534, 570), (741, 613), 'text', 'pNumber'],
           [(34, 400), (357, 456), 'text', 'whereGiven'],
           [(451, 956), (726, 1007), 'text', 'lastOption']]



    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # img = pat
    # PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


    # imagePath = os.path.dirname(__file__) + "/passport.jpg"
    imagePath = os.path.dirname(__file__) + "/Group 12.png"
    imgQ = cv2.imread(imagePath)

    h, w, c = imgQ.shape
    #imgQ = cv2.resize(imgQ, (w//2, h//2))
    orb = cv2.ORB_create(10000)
    kp1, des1 = orb.detectAndCompute(imgQ, None)
    #imgKp1 = cv2.drawKeypoints(imgQ, kp1, None)
    myPicList = os.listdir(path)
    print(myPicList)
    for j, y in enumerate(myPicList):
        img = io.imread(path + '/' + y)
        #grayIMG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #thresholdIMG = cv2.threshold(grayIMG, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #img = cv2.resize(img, (w//2, h//2))
        #cv2.imshow(y, img)
        kp2, des2 = orb.detectAndCompute(img, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2, des1)
        matches.sort(key=lambda x: x.distance)
        good = matches[:int(len(matches)*(per/100))]
        imgMatch = cv2.drawMatches(img,kp2,imgQ,kp1,good[:100],None,flags=2)
        #imgMatch = cv2.resize(imgMatch, (w // 3, h // 3))
        #cv2.imshow(y, imgMatch)

        srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)

        imgScan = cv2.warpPerspective(img, M, (w, h))

        cv2.imshow(y, imgScan)

        imgShow = imgScan.copy()
        imgMask = np.zeros_like(imgShow)
        myData = {}
        print(f'########################Extracting Data from Form {j}########################')

        for x, r in enumerate(roi):
            cv2.rectangle(imgMask, ((r[0][0]), r[0][1]), ((r[1][0]), r[1][1]), (0,255,0), 1)
            imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)
            imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]

            if r[2] == 'text':
                print('{} :{}'.format(r[3], pytesseract.image_to_string(imgCrop)))
                #print(f'{r[3]} : {pytesseract.image_to_string(imgCrop)}')
                # myData.append(pytesseract.image_to_string(imgCrop))
                if r[3] == 'pNumber':
                    temp = str(pytesseract.image_to_string(imgCrop)).strip()
                    myData['pSeria'] = temp[0:2]
                    myData['pNumber'] = temp[2:]
                elif r[3]=='lastOption':
                    temp = str(pytesseract.image_to_string(imgCrop)).strip()
                    myData['lastOption'] = temp[-16:-2]
                    # print(temp[-16:-2])

                else:
                    myData[r[3]] = str(pytesseract.image_to_string(imgCrop)).strip()
        #imgShow = cv2.resize(imgShow, (w // 3, h // 3))
        cv2.imshow(y, imgShow)

        with open('DataOutput2.csv', 'a+') as f:
            for data in myData:
                f.write((str(data) + ','))
            f.write('\n')

    # print(myData)
    # print(path)

    # def getData():
    #     return myData

    # print(type(myData))
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    return myData
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #cv2.imshow("KeyPoints", imgKp1)


