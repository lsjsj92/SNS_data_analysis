from gensim.models import word2vec
import glob, os
file_dir = "./after_token.txt"
data_array = []

def read_files():
    #위생에 관한 파일을 하나씩 가져오면서
    files = glob.glob(file_dir, recursive=True)
    for i in files:
        make_data(i)

def make_data(fname):
    #하나씩 전체를 읽는데, (,)를 기준으로 자른다.(배열이 생성됌) 그 배열을 data_array배열에 넣는다. 즉 2차원 배열로써 만들어짐
    with open(fname, 'r', encoding='utf=8') as f:
        data = f.read()
        data = data.split(",")
        data_array.append(data)

def make_word2vec_model():
    print("단어를 벡터화 하는 중입니다. 잠시만 기다려주세요.")
    model = word2vec.Word2Vec(data_array, size=40, window=10, min_count=20, iter=50, sg=1)
    model.save("./word2vec/word2vec.model")


#모델이 있으면
if os.path.exists('./word2vec/word2vec.model'):
    model = word2vec.Word2Vec.load("./word2vec/word2vec.model")
    while True:
        word = input("단어를 입력해보세요! : ")
        if word == "":
            break
        try:
            print(model.most_similar(positive=[word]))
        except:
            print("해당 되는 단어가 없습니다.")

#모델이 없으면
else:
    read_files()
    make_word2vec_model()
    print("done")