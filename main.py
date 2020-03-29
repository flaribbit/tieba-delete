from bs4 import BeautifulSoup
import requests
import re

sessions=requests.session()
sessions.headers['User-Agent']="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
sessions.cookies=requests.cookies.cookiejar_from_dict({
    "STOKEN":"",#$$选填？
    "TIEBA_USERTYPE":"",#$$选填？
    "BDUSS":"",#$$必填
})

def getInfo(url,backup):
    html=sessions.get(url).text
    fid=re.search('"fid":(\\d+)',html).group(1)
    tbs=re.search('"tbs": "([^"]+)"',html).group(1)
    tid=re.search('/p/(\\d+)',url).group(1)
    pid=re.search('pid=(\\d+)',url).group(1)
    title=re.search('<title>([^<]+)',html).group(1)
    if backup:
        file=open("backup/"+tid+"_"+title+".html","w")
        file.write(html)
        file.close()
    return (fid,tbs,tid,pid,title)

def deletePost(fid,pid,tid,tbs,title):
    r=sessions.post(
        "https://tieba.baidu.com/f/commit/post/delete",
        data={
            "fid": fid,#贴吧id,网页上的
            "pid": pid,#帖子id
            "tid": tid,#帖子id
            "tbs": tbs,#网页上的
            "delete_my_post": "1",
            "delete_my_thread": "0",
            "is_vipdel": "1"
        }
    )
    if r.json()['err_code']==0:
        print("Deleted",tid,title)

postList=[]
for i in range(1,50):#$$懒没算页码自己写吧
    try:
        print("Page",i+1)
        soup=BeautifulSoup(sessions.get('http://tieba.baidu.com/i/i/my_tie?pn='+str(i+1)).content,features="html.parser")
        items=soup.select('.simple_block_container>ul>li')
        for item in items:
            if True:#$$这里可以加一些条件筛选一下
                print(item.text)
                postList.append('https://tieba.baidu.com/'+item.select_one('a.thread_title').attrs['href'])
    except KeyboardInterrupt:
        exit()
    except:
        pass

print("Total",len(postList),"posts, delete all?(y/n)")
choice=input()
print("Backup?(y/n)")
isbackup=input()
if choice=="y":
    isbackup=(isbackup=="y")
    for url in postList:
        try:
            fid,tbs,tid,pid,title=getInfo(url,isbackup)
            deletePost(fid,pid,tid,tbs,title)
        except KeyboardInterrupt:
            exit()
        except:
            print("error")
            pass
