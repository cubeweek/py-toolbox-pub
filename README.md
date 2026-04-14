<img src="resources/imgs/py-toolbox-README.jpg" style="max-width: 100%; height: auto;"><br>
귀찮거나 반복해야 하는 작업을 자동화시킨 파이썬 스크립트 모음입니다.<br>
각 스크립트는 독립적으로 실행 가능합니다.<br>
(p.s 만든 사람이 Mac 환경에서만 돌려봐서 그 외 환경에서는 실행 결과가 검증되지 않았습니다🙂‍↕️)

## 🚀 Tool List
| 카테고리                                   | 스크립트 명                                              | 주요 기능                                                                          | 핵심 lib                                                                               | 비고 |
|:---------------------------------------|:----------------------------------------------------|:-------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------| :--- |
| <sub>- 이미지 프로세싱</sub>                | [`make_reward_chart.py`](/src/make_reward_chart.py) | A4 사이즈의 번호 기반 칭찬 스티커 판 생성                                       | <sub>`Pillow (PIL)`<br>`Matplotlib`</sub>    | -|
| <sub>- 웹 크롤링<br>- 자동화 테스트</sub>    | [`autotest_backjoon.py`](src/autotest_backjoon.py)  | 1. 백준 문제의 예시들을 크롤링(및 캐싱)<br>2. 해당 소스를 컴파일하여 실행 결과가 예제와 일치하는지 비교 | <sub>`Selenium`<br>`Webdriver-manager`<br>`BeautifulSoup4`<br>`Subprocess`</sub>| **Chrome 필요** |
| <sub>- 웹 크롤링<br>- 파일 시스템</sub>     | [`move_by_tier.py`](src/move_by_tier.py)            | 백준/LeetCode 소스코드를 난이도 별(문제의 난이도를 크롤링하여 확인함) 폴더로 자동 분류           | <sub>`Requests`<br>`Pathlib`<br>`Urllib`<br>`JSON`<br>`Shutil`</sub>| - |
| <sub>- 텍스트 파싱<br>- 문서 자동 갱신 </sub> | [`update_readme.py`](src/update_readme.py)                              | 문제 풀이 현황을 분석하여 README.md의 문제 리스트(티어별) 자동 갱신                     | <sub>`Regular Expression (re)`<br>`JSON`<br>`Collections`<br>`Pathlib`       </sub>  | - |


## 🛠 Installation & Setup

### 파이썬 가상환경 설치

```bash
python -m venv .venv # 파이썬 가상환경 세팅

# 가상환경 활성화
source .venv/bin/activate # Mac/Linux
# .venv\Scripts\activate # Windows
```

### 필요 라이브러리 설치
```bash
pip install -r config/requirements.txt
```

## 📂 Project Structure

```text
.
├── config/                 # 환경설정 관련 파일
├── scripts/                # 실행 가능한 독립 스크립트 (.py)
├── resources/              # 스크립트 실행에 필요한 리소스
│   ├── imgs/               # 이미지 파일 (apple.png 등)
│   ├── etc/                # 폰트 및 기타 설정 파일
│   └── fonts_license/      # 사용된 오픈 폰트의 라이선스 고지
├── output/                 # 스크립트 결과물 저장 폴더
└── README.md
```

## ⚖️ License & Open Source
- **Fonts:**
    - 본 프로젝트는 [Pretendard](https://github.com/orioncactus/pretendard) 폰트를 사용하였습니다. ([`라이선스 전문`](/guide/LICENSE_FONT.txt))
