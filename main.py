import csv
import sys
import requests
from bs4 import BeautifulSoup


def setup():
    code = input_product_item()
    code = "n%s" % code

    list_data = list()
    list_data = getWebsiteData(code)
    exportFile(list_data, code)


def input_product_item():
    list_code = {
        1: '品牌小主機、AIO｜VR虛擬',
        2: '手機｜平板｜筆電｜穿戴',
        3: '酷！PC 套裝產線',
        4: '處理器 CPU',
        5: '主機板 MB',
        6: '記憶體RAM',
        7: '固態硬碟 M.2｜SSD',
        8: '傳統內接硬碟HDD',
        9: '外接硬碟｜隨身碟｜記憶卡',
        10: '散熱器｜散熱墊｜散熱膏',
        11: '封閉式｜開放式水冷',
        12: "顯示卡VGA",
        13: '螢幕｜投影機｜壁掛',
        14: 'CASE 機殼(+電源)',
        15: '電源供應器',
        16: '機殼風扇｜機殼配件',
        17: '鍵盤+鼠｜搖桿｜桌+椅',
        18: '滑鼠｜鼠墊｜數位板',
        19: 'IP分享器｜網卡｜網通設備',
        20: '網路NAS｜網路IPCAM',
        21: '音效卡｜電視卡(盒)｜影音',
        22: '喇叭｜耳機｜麥克風',
        23: '燒錄器 CD/DVD/BD',
        24: 'USB週邊｜硬碟座｜讀卡機',
        25: '行車紀錄器｜USB視訊鏡頭',
        26: 'UPS不斷電｜印表機｜掃描',
        27: '介面擴充卡｜專業Raid卡',
        28: '網路、傳輸線、轉頭｜KVM',
        29: 'OS+應用軟體｜禮物卡',
        30: '福利品出清',
    }

    for c in list_code:
        print("%s:%s" % (c, list_code[c]))

    code = input('請輸入品名代號：')
    return code


def getWebsiteData(product_item):

    try:
        # 原價屋首頁
        r = requests.get('http://www.coolpc.com.tw/evaluate.php', timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')

        ssdGroup = soup.find("select", {"name": product_item})
        ssdType = ssdGroup.find('optgroup')
        priceList = ssdType.find_all('option')

        list_main = list()
        for p in priceList:
            pText = p.text

            # 排除特殊字
            pText = pText.replace('◆', '')
            pText = pText.replace('★', '')
            pText = pText.replace(' ', '')
            # 編碼設為 UTF8
            pText.encode("utf8").decode("cp950", "ignore")
            list_pText = pText.split('\n')

            for row in list_pText:
                if row.find('$') > 0:
                    print(row)
                    list_main.append(row.split(','))

    except requests.exceptions.RequestException as e:
        msg = '%s%s' % ('error ', '400')
        print(msg)

    return list_main


def exportFile(list_data, code):
    filename = "output.csv"
    f = open(filename, "w")
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list_data)
        pass
    print("匯出成功...")
    input()


if __name__ == "__main__":
    setup()
