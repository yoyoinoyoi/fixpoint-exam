import sys

# 読み込んだ(テキスト)ファイルを配列で返す
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


def main(filename:str, N:int, m:int, t:int):
    # ファイルを読み込む
    arr = readfile(filename)
    # タイムアウト回数とその時間を格納する配列
    log = dict()
    # 応答時間を格納する配列
    response_time = dict()
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
            
            if server not in response_time:
                response_time[server] = [[time], [int(response)]]
            else:
                response_time[server][0].append(time)
                response_time[server][1].append(int(response))
                    
            if server in log:
                if log[server][1] >= N:
                    ret.append("{}: {}~{}".format(server, term(log[server][0]),  term(time)))
                log[server] = [time, 0]
                
    ret.append("line congestion")
    for server, data in response_time.items():
        time = data[0]
        response = data[1]
        # m回以下ならスルー
        if len(response) < m:
            continue
        
        # 累積和を用いる
        response_sum = [response[0]]
        for i in range(len(response) -1):
            response_sum.append(response_sum[i] + response[i+1])
        
        for j in range(len(response_sum)-m):
            tt = response_sum[j+m] -response_sum[j]
            # 回線が混雑している場合
            if tt >= t*m:
                ret.append("{}: {}~{}".format(server, term(time[j]),  term(time[j+m])))
    
    # 故障している(タイムアウト回数がN回を超えている) ものを見つける
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
    file = args[1]
    N = int(args[2])
    m = int(args[3])
    t = int(args[4])
    main(file, N, m, t)