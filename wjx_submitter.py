import requests
import random
import time
from urllib.parse import urlencode
import cv2
from PIL import Image
import os
import code
import pytesseract


class WenJuanXing(object):
    def __init__(self, q_num, q_data):
        self.base_url = 'https://www.wjx.cn/jq/%s.aspx'
        self.base_submit = 'https://www.wjx.cn/handler/processjq.ashx?'
        self.base_spam = 'https://www.wjx.cn/AntiSpamImageGen.aspx?'
        self.sess = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.curID = q_num
        self.submitdata = q_data
        self.submittype = '1'
        self.t = str(int(time.time() * 1000))
        self.starttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        self.html = ''
        self.validate_text = ''
        self.rn = 0

    def getHtml(self):
        response = self.sess.get(self.base_url % self.curID)
        self.html = response.text

    def getRandNum(self):
        self.rn = 0
        self.getHtml()
        rnd_part = self.html[self.html.find('rndnum=') + 8:]
        self.rn = rnd_part[:rnd_part.find('"')]

    def stringParams(self):
        return {
            'submittype': self.submittype,
            'curID': self.curID,
            't': self.t,
            'starttime': self.starttime,
            'rn': self.rn,
            'validate_text': self.validate_text
        }

    def antiSpam(self):
        url = self.base_spam + urlencode({'t': self.t, 'q': self.curID})
        response = self.sess.get(url)
        with open('tmp_img.gif', 'wb') as f:
            f.write(response.content)
        # TODO: try captcha solver
        Image.open('tmp_img.gif').convert('RGB').save('tmp_img.jpg')
        '''
        
        img = cv2.imread('tmp_img.jpg', cv2.IMREAD_COLOR)
        os.remove('tmp_img.gif')
        os.remove('tmp_img.jpg')
        cv2.imshow('captcha', img)
        cv2.waitKey(0)
        self.validate_text = input('验证码: ')
        cv2.destroyAllWindows()
        '''
        img = Image.open('tmp_img.jpg')
        img = img.convert('RGB')
        img = img.convert('L')
        threshold = 20
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        img = img.point(table, '1')
        img = img.convert('L')
        #img.show()
        self.validate_text = ''.join(pytesseract.image_to_string(img).split())
        print(self.validate_text)
        #string = "EJ RM"
        #print(''.join(string.split()))
    def submitForm(self):
        url = self.base_submit + urlencode(self.stringParams())
        response = self.sess.post(url, data={'submitdata': self.submitdata})
        return response

    def resetData(self):
        self.getRandNum()
        self.t = str(int(time.time() * 1000))
        self.starttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        self.sess.cookies.clear()


def main():
    # print('输入验证码时，先关闭图片窗口再输入。')
    # q_num = input('问卷号：')
    # q_data = input('submitdata（自行理解）：')
    # iter = int(input('次数：'))
    l = [[1, 2, 3, 1, 0.5],
         [4, 2, 1, 1, 5],
         [6, 4],
         [7, 3],
         [7, 3],
         [0.5, 0.6, 2, 1],  # 6
         [4, 9, 3, 2],
         [1, 4, 3, 1],
         [6, 3, 1],
         [2, 2, 1, 0.5],
         [4, 3, 2],  # 11
         [2, 5, 5],
         [1, 2, 5, 1.5],
         [5, 4, 3, 1],
         [1, 2, 3, 2, 1],
         [1, 1, 1, 2, 2, 3],
         [3, 1, 2],
         [5, 4, 3, 2, 1],
         [5, 4, 3, 2, 1],
         ]
    times = 1000
    for idx, i in enumerate(l):
        s = sum(i)
        tmp = [x / s for x in i]
        for idx2, k in enumerate(tmp):
            if idx2 >= 1:
                # print(tmp[idx2-1],tmp[idx2])
                tmp[idx2] = tmp[idx2] + tmp[idx2 - 1]
        l[idx] = tmp
        # print(l[idx])
    # print(l)
    for num in range(times):
        result = []
        for i in l:
            # print(i)
            r = random.random()
            # type(i)
            for idx, k in enumerate(i):
                if r < k:
                    result += [idx]
                    break
                # code.interact(local=locals())
        # code.interact(local=locals())
        for idx, val in enumerate(result):
            result[idx] = str(idx + 1) + '$' + str(val + 1)
        q_num = str(45028731)
        q_data = '}'.join(result)
        print(q_data)

        wjx = WenJuanXing(q_num, q_data)
        wjx.resetData()
        wjx.antiSpam()
        response = wjx.submitForm()
        print(response.content.decode('UTF-8'))


if __name__ == '__main__':
    main()
