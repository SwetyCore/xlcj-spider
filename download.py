import requests
from log1 import l


def jdt(current, total):
    '''
    进度条函数
    :param current: 已完成
    :param total: 总给
    :return: none
    '''
    num = (current / total) * 100
    n1 = round(num / 5)
    progressBar = '█' * n1 + ' ' * (20 - n1)
    out = '\r[{}] {:.2f}% '.format(progressBar, num)
    print(out, end='')


def Download1(url, path):
    '''
    文件下载部分
    :param url: 下载链接
    :param path: 保存路径
    :return:
    '''

    headers = {'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
               }

    r = requests.get(url, stream=True, headers=headers)
    f = open(path, 'wb')
    content_size = int(r.headers['content-length'])
    data_count = 0
    for data in r.iter_content(chunk_size=10240):  # iter是iter
        data_count = data_count + len(data)
        f.write(data)
        jdt(data_count, content_size)

    l.info('Successfully saved at {}'.format(path))


def Download(url, path):
    response = requests.get(url)
    data = response.content
    with open(path, 'wb') as fn:
        fn.write(data)
