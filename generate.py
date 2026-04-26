import os
from datetime import datetime
import feedparser
from wordcloud import WordCloud, STOPWORDS
from janome.tokenizer import Tokenizer
from feedgen.feed import FeedGenerator

# ===== 設定 =====
RSS_URL = "https://news.google.com/rss/search?q=下水道&hl=ja&gl=JP&ceid=JP:ja"
BASE_URL = "https://Sn1nakazawa.github.io/gesuirss"
FONT_PATH = "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"

# ===== ディレクトリ作成 =====
os.makedirs("docs/images", exist_ok=True)

# ===== RSS取得 =====
feed = feedparser.parse(RSS_URL)
titles = [entry.title for entry in feed.entries[:30]]

# ===== 形態素解析（名詞のみ抽出）=====
t = Tokenizer()
words = []

for title in titles:
    for token in t.tokenize(title):
        if token.part_of_speech.startswith("名詞"):
            words.append(token.surface)

text = " ".join(words)

# ===== ワードクラウド生成 =====

stopwords = set(STOPWORDS)
stopwords.update({
    "下水道","市","Yahoo","city","NEWS","ニュース","よう","さん","日本","東京"
})
filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
filepath = f"docs/images/{filename}"

wc = WordCloud(
    width=800,
    height=400,
    background_color="white",
    stopwords=stopwords,
    font_path=FONT_PATH
).generate(text)

wc.to_file(filepath)

# ===== RSS生成 =====
fg = FeedGenerator()
fg.title('News WordCloud')
fg.link(href=BASE_URL)
fg.description('RSS titles wordcloud')

img_url = f"{BASE_URL}/images/{filename}"

fe = fg.add_entry()
fe.title("WordCloud " + filename)
fe.link(href=img_url)
fe.enclosure(img_url, 0, 'image/png')
fe.description(f'<img src="{img_url}">')

# fg.rss_file("docs/rss.xml")
