from Media import BatchMedia

if __name__ == '__main__':

    print("请选择需要执行的功能：\n"
          "下载单个推文媒体：1\n"
          "下载单用户的所有媒体：2\n")
    while True:
        getType = input('> ')
        if getType == '1' or getType == '2':
            break
    if getType == '1':
        print("1")

    elif getType == '2':
        #获取用户信息
        BatchMedia.Initialize()
        #解析数据文件
        BatchMedia.parseRawFile()
        # 保存推文表格数据
        BatchMedia.SaveMediaToExcel()
        # 下载推文媒体数据
        BatchMedia.SavaMediaData()
        # 统计信息
        BatchMedia.getReport()


