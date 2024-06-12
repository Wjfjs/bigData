import requests
from bs4 import BeautifulSoup
from owslib.wms import WebMapService
import matplotlib.pyplot as plt

# WMS 서비스 URL
wms_url = 'http://www.safemap.go.kr/openApiService/wms/getLayerData.do?apikey=U42BJJFV-U42B-U42B-U42B-U42BJJFVJ1'  # APIKEY를 실제 키로 대체하세요

# URL이 올바르게 응답하는지 확인
response = requests.get(wms_url)

if response.status_code == 200:
    print("WMS 서비스 응답 확인")
    xml_content = response.content.decode('utf-8')
    print(xml_content)  # 응답 내용을 출력하여 XML 형식인지 확인

    # BeautifulSoup을 사용하여 XML 파싱
    soup = BeautifulSoup(xml_content, 'xml')

    # 문제 있는 태그를 수정
    if soup.link:
        soup.link.name = 'corrected_link'

    corrected_xml_content = str(soup)

    # 수정된 XML을 파싱하여 문제 해결
    try:
        root = etree.fromstring(corrected_xml_content.encode('utf-8'))
        print("XML 파싱 성공")

        # WMS 서비스에 연결
        wms = WebMapService(wms_url, version='1.1.1')

        # 사용 가능한 레이어 출력
        print("Available Layers:")
        for layer in list(wms.contents):
            print(layer)

        # 원하는 레이어 선택
        layer_name = 'A2SM_CRMNLHSPOT_TOT'
        layer = wms[layer_name]

        # 지도 영역 설정 (예시로 대한민국 전체 영역)
        bbox = (124.0, 33.0, 132.0, 38.0)
        width = 600
        height = 400

        # Get the image
        img = wms.getmap(layers=[layer_name],
                         styles=['A2SM_CrmnlHspot_Tot_Tot'],
                         bbox=bbox,
                         size=(width, height),
                         srs='EPSG:4326',
                         format='image/png',
                         transparent=True)

        # Save or display the image
        out = 'wms_image.png'
        with open(out, 'wb') as f:
            f.write(img.read())

        # Display the image
        plt.imshow(plt.imread(out))
        plt.axis('off')
        plt.show()

    except etree.XMLSyntaxError as e:
        print("XML 파싱 오류:", e)
else:
    print("WMS 서비스 응답 오류:", response.status_code)
    print(response.text)


