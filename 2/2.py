import sys

# 読み込んだファイルを配列で返す
def readfile(text: str):
    f = open(text, 'r', encoding='UTF-8')

    data = f.read()
    inputarr = data.split('\n')

    returnarr = []
    for arr in inputarr:
        returnarr.append(arr.split(','))

    f.close()
    
    return returnarr

# YYYYMMDDhhmmss -> YYYY/MM/DD hh:mm:ss で返す
def term(s: str):
    return "{}/{}/{} {}:{}:{}".format(s[0:4], s[4:6], s[6:8], s[8:10], s[10:12], s[12:14])

def main(filename:str, N:int):
    # ファイルを読み込む
    arr = readfile(filename)
    # タイムアウト回数とその時間を格納する配列
    log = dict()
    # ログに出力するための配列
    ret = ["brokedown"]
    # 故障期間
    for time, server, response in arr:
        # タイムアウトした場合
        if response == '-':
            if server not in log:
                log[server] = [time, 1]
            else:
                log[server][1] += 1
        else:
            if server in log:
                if log[server][1] >= N:
                    ret.append("{}: {}~{}".format(server, term(log[server][0]),  term(time)))
                log[server] = [time, 0]
            
                
    # 故障しているものを見つける
    ret.append("breakdown now")
    for server, data in log.items():
        time = data[0]
        cnt = data[1]
        if cnt > N:
            ret.append(server)
            
    # log.txt へ結果を表示
    with open('log.txt', 'w') as f:
        for text in ret:
            print(text, file=f)
    f.close()

if __name__ == '__main__':
    args = sys.argv
    main(args[1], int(args[2]))