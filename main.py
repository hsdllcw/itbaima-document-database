# python3.7
import os
import json
import urllib3
import sys

# 创建连接
http = urllib3.PoolManager()


def download(down_load_dir=(os.path.expanduser('./'))):
    print("下载目录:" + down_load_dir)
    print("正在获取柏码知识库信息...")
    res = http.request(
        "GET",
        "https://itbaima.net/api/document/list"
    )
    documentList = json.loads(res.data.decode("UTF-8"))
    for document in documentList:
        document_title = document.get("title")
        documentPath = down_load_dir + "/" + document_title
        if not os.path.exists(documentPath):
            os.makedirs(documentPath)
        print("正在获取《"+document_title+"》笔记的信息...")
        res = http.request(
            "GET",
            "https://itbaima.net/api/document/details/" + str(document.get("id"))
        )
        bookList = json.loads(res.data.decode("UTF-8"))
        for book in bookList:
            title = book.get("title")
            file_dir = documentPath + "/" + title
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            # 下载前删除旧文档
            for root, dirs, files in os.walk(os.path.abspath(file_dir)):
                for name in files:
                    print("删除："+os.path.join(root, name))
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    print("删除："+os.path.join(root, name))
                    os.removedirs(os.path.join(root, name))
            for chapter in book.get("chapters"):
                path = chapter.get("path")
                file_name = chapter.get("name") + path[path.index("."):]
                file_path = file_dir + "/" + file_name
                print("准备下载："+file_name)
                res = http.request(
                    "GET", "https://static.itbaima.net/markdown/" + path)
                with open(file_path, "wb") as file:
                    file.write(res.data)
                    file.close()
                    print(file_name+"\t已下载")


if __name__ == "__main__":
    try:
        download(sys.argv[1])
    except IndexError:
        download()
