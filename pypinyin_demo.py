from pypinyin import lazy_pinyin,TONE2

res = lazy_pinyin("",style=TONE2)

print("".join(res))
