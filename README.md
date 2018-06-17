# jieba-GAE

[Jieba](https://github.com/fxsjy/jieba) on Google App Engine

![Powered by Google App Engine](https://cloud.google.com/appengine/images/appengine-silver-120x30.gif)

demo : [https://jieba.liantian.me](https://jieba.liantian.me)


GAE有几个限制：
1. 128M运行内存限制。
2. 脚本执行时间限制。
3. 禁止临时文件。

主要是针对这几个限制进行的处理。

处理后响应时间，免费配额的cpu，可以处理相当数量的请求。
![](https://github.com/liantian-cn/jieba-gae/raw/master/snipaste_20170319_172602.png)

处理后内存占用，刚好落在免费配额限制内。
![](https://github.com/liantian-cn/jieba-gae/raw/master/snipaste_20170319_172713.png)

**不介意造访：[LIANTIAN'S LOG
](https://liantian.me/article/use_jieba_on_google_appengine/)**


### TemporaryFile 的问题处理 ###

GAE对屏蔽了tempfile库的使用，Jieba分词使用tempfile库处理缓存问题，使用时会报错：

> NotImplementedError: Only tempfile.TemporaryFile is available for use

解决办法：



1. 修改GAE使用的[tempfile.py](https://chromium.googlesource.com/external/googleappengine/python/+/master/google/appengine/dist/tempfile.py)。
	替换
	```
	gettempdir = PlaceHolder
	```
	为
	
	```
	def gettempdir(*args, **kwargs):
	    return os.path.dirname(os.path.abspath(__file__)) + '/../tmp'
	```
2. 命名为`gae_tempfile.py`，并放置于lib目录并使用[官方的方法加载](https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27)。
3. 修改`jieba/analyse/tfidf.py`和`lib/jieba/__init__.py`，替换`import tempfile`为`import tempfile_gae as tempfile`
4. 在本地新建tmp目录。
5. 在本地环境生成dict.cache后，再上传至GAE。



### 使用 TF-IDF 关键词抽取时因内存不足无法完成请求 ###

在本地测试环境无法发现此问题，上传后无法使用，因为GAE的免费配额下，单个实例仅有128M内存。

经过分析，发现提取关键词的过程中，读取`jieba/analyse/idf.txt`并生成索引对象的过程使用了大量内存。相关对象为`jieba.analyse.tfidf.IDFLoader`。

解决办法：使用处理词库dict.txt的方法处理文本语料库，本地利用marshal库生成二进制对象后，上传到GAE。

1. 修改`jieba.analyse.tfidf.IDFLoader`的`set_new_path(self, new_idf_path)`函数
```
    def set_new_path(self, new_idf_path):
        if self.path != new_idf_path:
            self.path = new_idf_path
            cache_file = "idf.cache"
            cache_file = os.path.join(tempfile.gettempdir(), cache_file)
            try:
                with open(cache_file, 'rb') as cf:
                    self.idf_freq, self.median_idf = marshal.load(cf)
                # print("Loading model from cache %s" % cache_file)
            except Exception:
                content = open(new_idf_path, 'rb').read().decode('utf-8')
                self.idf_freq = {}
                for line in content.splitlines():
                    word, freq = line.strip().split(' ')
                    self.idf_freq[word] = float(freq)
                self.median_idf = sorted(
                    self.idf_freq.values())[len(self.idf_freq) // 2]
                with open(cache_file, 'wb') as cf:
                    marshal.dump((self.idf_freq, self.median_idf), cf)
```
2. 在本地环境生成dict.cache后，再上传至GAE。






