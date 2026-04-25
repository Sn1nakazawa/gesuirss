from PIL import Image, ImageDraw
from feedgen.feed import FeedGenerator
import os
from datetime import datetime

BASE_URL = "https://<ユーザー名>.github.io/<リポジトリ名>"

# 画像保存先
os.makedirs("docs/images", exist_ok=True)

# 画像生成
filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
filepath = f"docs/images/{filename}"

img = Image.new("RGB", (400, 200), "white")
draw = ImageDraw.Draw(img)
draw.text((50, 80), filename, fill="black")
img.save(filepath)

# RSS生成
fg = FeedGenerator()
fg.title('Image Feed')
fg.link(href=BASE_URL)
fg.description('Auto generated images')

fe = fg.add_entry()
fe.title(filename)

img_url = f"{BASE_URL}/images/{filename}"

fe.link(href=img_url)
fe.enclosure(img_url, 0, 'image/png')
fe.description(f'<img src="{img_url}">')

fg.rss_file("docs/rss.xml")
