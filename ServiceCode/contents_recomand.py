#%%
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import warnings; warnings.filterwarnings('ignore')
# %%
df = pd.read_csv('추천시스템전처리.csv', encoding='utf8', index_col=0)
df
# %%

cate2_list = []
for i in df['category2']:
    cate2_list.append(i)
# %%
cate2_list = list(set(cate2_list))
#%%
cate2_list
# %%
cate2_list[1] = 'None'
# %%
cate2_dic_li = []
for i, j in zip(range(len(cate2_list)), cate2_list):
    cate2_dic_li.append({'id': i, 'name': j})
# %%
cate3_list = []
for i in df['category3']:
    cate3_list.append(i)
# %%
cate3_list = list(set(cate3_list))
# %%
cate3_list[0] = 'None'
# %%
cate3_dic_li = []
for i, j in zip(range(len(cate3_list)), cate3_list):
    cate3_dic_li.append({'id': i, 'name': j})
# %%
cate3_dic_li
# %%
df['keyword'] = df['keyword'].apply(lambda x: str(x).replace("'","").replace('[','').replace(']',''))
    
# %%
keyword = []
for i in df['keyword']:
    i = i.split(',')
    for j in i:
        keyword.append(j.strip())
# %%
keyword = list(set(keyword))
# %%
keyword_dic_li = []
for i, j in zip(range(len(keyword)), keyword):
    keyword_dic_li.append({'id': i, 'name': j})
# %%
keyword_dic_li
# %%
df.head()
# %%
keyword_list = []
for names in df['keyword']:
    li = []
    for val in keyword_dic_li: 
        if val['name'] in names:
            li.append(val)
        else:
            continue
    keyword_list.append(li)
# %%
df['keyword'] = pd.Series(keyword_list)
# %%
df
# %%
for idx, cate in enumerate(df['category2']):
    for val in cate2_dic_li:
        if cate == val['name']:
            df.loc[idx, 'category2'] = [val]
        else:
            continue
# %%
for idx, cate in enumerate(df['category3']):
    for val in cate3_dic_li:
        if cate == val['name']:
            df.loc[idx, 'category3'] = [val]
        else:
            continue
# %%
df
# %%
a_df = pd.read_csv('product_df2.csv', index_col=0)
a_df['product_id'] = a_df['product_id'].apply(lambda x: x[:-3])
# %%
df = pd.merge(df, a_df[['product_id','rev_score']], how='inner', on='product_id')
# %%
df = df.drop_duplicates(subset='product_id', keep='first').reset_index(drop=True)
# %%
df = df.dropna()
#%%
df.to_csv('f.csv', encoding='cp949')
# %%
# 가중 평균 함수
def weight_average(df, pct):
    pct = pct
    m = df['review_cnt'].quantile(pct)
    c = df['rev_score'].mean()
    v = df['review_cnt']
    r = df['rev_score']
    weight_average = (v / (v+m)) * r + (m / (v+m)) * c

    return weight_average
# 가중 평균 기반 추천 시스템 함수
def weight_vote_avg(df, sorted_sim, title = '', num=10):
    title_item = df[df['product_name'] == title]
    title_item_idx = title_item.index.values
    print(title_item_idx)

    sim_idx = sorted_sim[title_item_idx, :(num)]
    sim_idx = sim_idx.reshape(-1)
    sim_idx = sim_idx[sim_idx != title_item_idx]

    similar_item = df.iloc[sim_idx]

    return similar_item.sort_values(by='weight_average', ascending=False)
# %%
print(df.shape)
# %%
df['keyword'] = df['keyword'].apply(lambda x: [i['name'] for i in x])
# %%
# 키워드 컬럼 펼치기
keywords_list = []
for keyword in df['keyword']:
    keywords_list.extend(keyword)


keywords_list = np.unique(keywords_list)
keywords_list
# %%
# 원핫인코딩 매트릭스 만들기
zero_array = np.zeros(shape=(df.shape[0], len(keywords_list)))
print(zero_array.shape)
# %%
zero_df = pd.DataFrame(zero_array, columns=keywords_list)
zero_df
# %%
for idx, keyword in enumerate(df['keyword']):
    indices = zero_df.columns.get_indexer(keyword)
    zero_df.iloc[idx, indices] = 1

zero_df
# %%
# 유사도 구하기
key_df = zero_df.copy()
key_sim = cosine_similarity(key_df, key_df)
print(key_sim.shape)
print(key_sim[0])
# %%
# 정렬
sorted_key_sim = key_sim.argsort()[:,::-1]
sorted_key_sim
# %%
# 1차 추천
title_item = df[df['product_name'] == '라로슈포제 똘러리앙 퓨리파잉 포밍 크림']
title_item_idx = title_item.index.values
print(title_item_idx)

sim_idx = sorted_key_sim[title_item_idx, :10] # 유사도 높은 10개
sim_idx = sim_idx.reshape(-1)

similar_item = df.iloc[sim_idx][['product_name', 'rev_score']]
#%%
similar_item
# %%
# 가중 평점으로 추천
# 가중평점 = (v / (v+m)) * r + (m / (v+m)) * c
# v = 아이팀별 평점 투표 횟수
# m = 평점 부여를 위한 최소 투표 횟수
# r = 아이템별 평균 평점
# c = 전체 아이템의 평균 평점

df['weight_average'] = weight_average(df, 0.6)

df[['product_name', 'rev_score', 'weight_average', 'review_cnt']].sort_values(by='weight_average', ascending=False)
# %%
sim_item = weight_vote_avg(df, sorted_key_sim, ['라로슈포제 퓨어 나이아신아마이드 10 세럼 30ml', '라로슈포제 똘러리앙 퓨리파잉 포밍 크림'])
sim_item = sim_item[['product_name', 'weight_average', 'rev_score']]
sim_item
# %%
df['product_id'].values.tolist()
# %%
