#Transliteration keyboard

hindis.txt: 召回集合的hindis(9999_lines)</br>
latins.txt: Google翻译hindis的结果</br>
write.txt: 错误打印文档</br>
test.py:  测试文档</br>

count.py: </br>
一些统计相关的尝试, 测试代码。</br>
latin2interpho & hindi2interpho映射关系, 效果不好</br>

prefix2mapping.py:</br>
利用二次发现&最长前缀, 得到不同数据集的k-v & v-k前缀映射关系, 以及数据集的组合映射, 提供给预测模块</br>

predict_latin2hindi.py:</br>
根据最长匹配 & 编辑距离召回, 进行latin→hindi的预测</br>

/word_sim_src：</br>
整串编辑距离近似度, 召回, 几乎100%</br>

/pkl: 各种预处理的映射文件</br>
/ret: 根据时间戳命名记录结果, 用做调试</br>