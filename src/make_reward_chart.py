from PIL import Image, ImageDraw, ImageFont
import matplotlib
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import os

matplotlib.use("TkAgg")  # PyCharm 백엔드 호환


if __name__ == "__main__":
    # 설정
    image_path = "../resources/imgs/apple.png"
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"이미지 파일이 존재하지 않습니다: {image_path}")

    apple_img = Image.open(image_path).convert("RGBA")

    # A4 가로 (Landscape): 3508 x 2480 (300dpi)
    a4_width, a4_height = 3508, 2480

    # === 여백 및 간격 설정 ===
    margin_top = 50
    margin_bottom = 50
    margin_left = 70
    margin_right = 70
    cell_gap = 5          # 셀 사이 간격
    block_gap = 100        # 좌/우 블록 간격

    # === 그리드 설정 ===
    cols, rows = 5, 7

    # 각 블록의 셀 크기 계산 (한쪽 블록 기준)
    block_width = (a4_width - (margin_left + margin_right) - block_gap) // 2
    block_height = a4_height - (margin_top + margin_bottom)
    cell_width = (block_width - (cols + 1) * cell_gap) // cols
    cell_height = (block_height - (rows + 1) * cell_gap) // rows

    # 폰트 설정
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "../resources/etc/Pretendard-Regular.ttf")
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        font = ImageFont.truetype(font_path, size=int(cell_height * 0.3))
        font_manager.fontManager.addfont(font_path)
        font_prop = font_manager.FontProperties(fname=font_path)
        rc('font', family=font_prop.get_name())
    except:
        font = ImageFont.load_default()

    # 사과 리사이즈
    apple_resized = apple_img.resize((cell_width, cell_height))

    # 흰 배경 캔버스
    a4_canvas = Image.new("RGBA", (a4_width, a4_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(a4_canvas)

    # === 사과 + 번호 그리기 ===
    number = 48

    for block in range(2):  # 0: left, 1: right
        x_offset = margin_left + block * (block_width + block_gap)
        for row in range(rows):
            for col in range(cols):
                x = x_offset + cell_gap + col * (cell_width + cell_gap)
                y = margin_top + cell_gap + row * (cell_height + cell_gap)

                # 사과 붙이기
                a4_canvas.paste(apple_resized, (x, y), apple_resized)

                # 번호 중앙에 출력
                text = str(number)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                text_x = x + (cell_width - text_w) / 2
                text_y = y + (cell_height - text_h) / 2

                # 외곽선 + 본문
                outline_range = 2
                for ox in range(-outline_range, outline_range + 1):
                    for oy in range(-outline_range, outline_range + 1):
                        draw.text((text_x + ox, text_y + oy), text, font=font, fill="black")
                draw.text((text_x, text_y), text, font=font, fill="white")

                number += 1

    # RGB 변환
    a4_canvas_rgb = a4_canvas.convert("RGB")

    rc('font', family=font_name)

    # 표시
    plt.figure(figsize=(11.69, 8.27))
    plt.imshow(a4_canvas_rgb)
    plt.axis("off")
    plt.title("칭찬 스티커 제목 영역")
    plt.show()

    # 저장
    output_path = "../output/apple_grid_A4_custom_margin.jpg"
    a4_canvas_rgb.save(output_path, "JPEG", quality=95)
    print(f"✅ 저장 완료: {output_path}")
