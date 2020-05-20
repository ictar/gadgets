import  matplotlib.pyplot as plt
import wordcloud
import jieba

stopwords = {
    "这样", "时候", "只是", "不是",
    "但是", "还是", "还有",
    "他们","我们","你们", "自己",
    "一个", "可以", "现在", "已经",
    "大家",""
}
def generate(txtpath, encoding="gbk"):
    text =open(txtpath,encoding=encoding).read()

    wordlist =jieba.cut(text,cut_all=True)

    wl_space_split =" ".join(wordlist)

    wc =wordcloud.WordCloud(
        font_path=r'/System/Library/fonts/PingFang.ttc',
        scale=2,
        stopwords=stopwords,
    ).generate(wl_space_split)

    plt.imshow(wc)
    plt.axis("off")
    plt.show()

def generate_from_str(wl_space_split):
    wc =wordcloud.WordCloud(
        font_path=r'/System/Library/fonts/PingFang.ttc',
        scale=2,
        stopwords=stopwords,
    ).generate(wl_space_split)

    plt.imshow(wc)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    txtpath = r"/path/to/txt"
    #generate(txtpath, 'utf-8')
    content = """xxx xxxxx xxx"""
    generate_from_str(content)