


url = ['http:shdisahdjahsd.jpg','shjdhasdjkahskdj','javascriopt.jps','http://e.wsyu.edu.cn/upload/htmleditor/File/110831041228.doc']
other_url_set = []
panding = [".pdf" ,".jpg" ,".gif" ,".png" ,".doc" , ".xls" , ".ppt" , ".mp3" ,".rar",".zip"]
def do_fiter( all_urls):
    for one_url in all_urls:
        # if ".jpg" or ".doc" in one_url:
        # if ".pdf" or ".jpg" or ".gif" or ".png" or ".doc" or ".xls" or ".ppt" or ".mp3" or ".rar" or ".zip" in one_url:
        if any(u in one_url for u in panding):
            other_url_set.append(one_url)

        else:
            pass
    return all_urls



l = do_fiter(url)
print(l)
print(other_url_set)
