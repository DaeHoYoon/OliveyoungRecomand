#%%
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import numpy as np
import pandas as pd
import time
#%%
options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
options.add_argument('headless') # headless 모드 설정
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu") 
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# 속도 향상을 위한 옵션 해제
prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
options.add_experimental_option('prefs', prefs)
#%%
# 리뷰 개수 크롤링 함수
def reviewcnt(url, endpage):

    for page in range(1, endpage+1):
        driver.implicitly_wait(10)
        url = url+f'{page}'
        driver.get(url)

        for prd in range(0,24):
            prds = driver.find_elements(By.CSS_SELECTOR, 'div.prd_info')[prd]
            prds.click()
            titles.append(driver.find_element(By.CSS_SELECTOR, 'div > p.prd_name').text)
            time.sleep(3)
            review_cnt_list.append(driver.find_element(By.CSS_SELECTOR, '#repReview > em').text)
            time.sleep(3)
            category_list.append(driver.find_elements(By.CSS_SELECTOR, value='.cate_y')[0].text)
            driver.back()
            time.sleep(3)
        if page <= 9:
            url = url[:-1]
        else:
            url = url[:-2]
    return review_cnt_list, titles, category_list

# 제품 리뷰 정보 크롤링 함수

def prdcrawling(url, endpage):

    for page in range(1, endpage+1):
        driver.implicitly_wait(10)
        url = url+f'{page}'
        driver.get(url)
        prds_len = len(driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li'))
        

        for prd in range(prds_len):
            prds = driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li')[prd]
            id.append(prds.get_attribute('criteo-goods'))
            prds.click()
            time.sleep(3)
            imgpaths.append(driver.find_element(By.XPATH, '//*[@id="mainImg"]').get_attribute('src'))
            brands.append(driver.find_element(By.CSS_SELECTOR, 'p.prd_brand > a').text)
            prices.append(driver.find_element(By.CSS_SELECTOR, 'div.price > span').text[:-2])
            titles.append(driver.find_element(By.CSS_SELECTOR, 'div > p.prd_name').text)
            rev_pnts.append(driver.find_element(By.CSS_SELECTOR, '#repReview > b').text)
            category_list1.append(driver.find_elements(By.CSS_SELECTOR, 'ul.loc_history > li > a.cate_y')[0].text)
            category_list2.append(driver.find_elements(By.CSS_SELECTOR, 'ul.loc_history > li > a.cate_y')[1].text)
            category_list3.append(driver.find_elements(By.CSS_SELECTOR, 'ul.loc_history > li > a.cate_y')[2].text)
            driver.find_element(By.CSS_SELECTOR, 'ul.prd_detail_tab > #reviewInfo > a').click()
            time.sleep(3)
            try:
                box = driver.find_element(By.CSS_SELECTOR, 'div.poll_all.clrfix')
                rows = box.find_elements(By.CSS_SELECTOR, 'dl')
                dT = []
                dD = []

                for row in rows:
                    dt_li = row.find_elements(By.TAG_NAME, 'dt')
                    dd_li = row.find_elements(By.TAG_NAME, 'dd')
                    for dt in dt_li:
                        dt_text = dt.text
                        dT.append(dt_text)
                    
                    for dd in dd_li:
                        dd_text = dd.text
                        dd_text = dd_text.split('\n')
                        dd_text = ','.join(dd_text)
                        dD.append(dd_text)

                r1s.append(dT[0])
                r2s.append(dT[1])
                r3s.append(dT[2])  
                r1_infos.append(dD[0])
                r2_infos.append(dD[1])
                r3_infos.append(dD[2])
                print('성공')

                driver.back()
                time.sleep(3)

            except:
                r1s.append('None')
                r2s.append('None')
                r3s.append('None')
                r1_infos.append('None')
                r2_infos.append('None')
                r3_infos.append('None')
                
                print('에러')
                driver.back()
                time.sleep(3)

        if page <= 9:
            url = url[:-1]
        else:
            url = url[:-2]
    return id, titles, imgpaths, brands, prices, rev_pnts, category_list1, category_list2, category_list3, r1s, r2s, r3s, r1_infos, r2_infos, r3_infos
#%%
# 유저 크롤링(제품 접속 함수)
def productInUser(url, endpage):

    for page in range(1, endpage+1):
        driver.implicitly_wait(10)
        url = url+f'{page}' # url 문자열에 page값 변화
        driver.get(url)
        prds_len = len(driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li')) # 해당 url에 제품 개수 확인

        for prd in range(prds_len):
            prds = driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li')[prd] # 제품 한개를 찾음
            # id.append(prds.get_attribute('criteo-goods')) # 찾은 제품의 id값을 리스트에 추가
            prds.click() # 해당 제품 클릭
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, 'ul.prd_detail_tab > #reviewInfo > a').click() # 리뷰 버튼 클릭
            time.sleep(3)
            
            t1 = time.time()
            userCrawling(prds)
            t2 = time.time()
            print('### 이번 제품 크롤링 완료시간:', t2 - t1)
            
        if page <= 9:
            url = url[:-1]
        else:
            url = url[:-2]

# 리뷰 크롤링(제품 접속 함수)
def productInRev(url, endpage):

    for page in range(1, endpage+1):
        driver.implicitly_wait(10)
        url = url+f'{page}' # url 문자열에 page값 변화
        driver.get(url)
        prds_len = len(driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li')) # 해당 url에 제품 개수 확인

        for prd in range(prds_len):
            prds = driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li')[prd] # 제품 한개를 찾음
            # id.append(prds.get_attribute('criteo-goods')) # 찾은 제품의 id값을 리스트에 추가
            prds.click() # 해당 제품 클릭
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, 'ul.prd_detail_tab > #reviewInfo > a').click() # 리뷰 버튼 클릭
            time.sleep(3)
            
            t1 = time.time()
            revCrawling(prds)
            t2 = time.time()
            print('### 이번 제품 크롤링 완료시간:', t2 - t1)
            
        if page <= 9:
            url = url[:-1]
        else:
            url = url[:-2]

# 제품을 산 유저의 정보 크롤링
def userCrawling(prds):
    try:
        driver.find_elements(By.CSS_SELECTOR, 'div.align_sort > ul > li')[1].click() # 도움순 클릭
        time.sleep(2)

        for idx in range(0,10):
            t1 = time.time()
            allpage = driver.find_element(By.CSS_SELECTOR, 'div.pageing')
            revpage = allpage.find_elements(By.TAG_NAME, 'a') # 리뷰 페이지 버튼
            driver.implicitly_wait(10)
            time.sleep(3)
            rows= driver.find_elements(By.CSS_SELECTOR, "ul#gdasList>li") # 페이지에 나오는 리뷰 전체
            # rows_len = len(driver.find_elements(By.CSS_SELECTOR, "ul#gdasList>li"))
            for row in rows:
                ID = driver.find_element(By.CLASS_NAME, 'prd_btn_area.new-style.type1 > .btnZzim').get_attribute('data-ref-goodsno')
                id.append(ID)  
                print(ID)                                          
            #리뷰어박스
                rbox = row.find_element(By.CSS_SELECTOR, "div.user.clrfix")   
            #닉네임과 탑순위 들어있는 구역
                infoUser = rbox.find_element(By.CSS_SELECTOR, "p.info_user")
                atags = infoUser.find_elements(By.TAG_NAME, "a")
            #닉네임
                name = atags[0].text
                review_ids.append(name)
                print(name)
            #탑순위 >>
                try:
                    topRank = atags[1].text
                    review_ranks.append(topRank)
                except:
                    topRank = "None"
                    review_ranks.append(topRank)
                print(topRank)
            #왕관 >>
                try:
                    king = rbox.find_element(By.CSS_SELECTOR, 'p.topreview_N2').text
                    review_nameds.append(king)
                except:
                    king = 'None'
                    review_nameds.append(king)
                print(king)
                #피부상태 >>
                try:
                    skin = rbox.find_element(By.CSS_SELECTOR, 'p.tag').text
                    skin = skin.split('\n')
                    skin = ','.join(skin)
                    reviewer_skins.append(skin)
                except:
                    skin = 'None'
                    reviewer_skins.append(skin)
                print(skin)
            t2 = time.time()
            print('### 댓글 한 페이지 완료시간:', t2 - t1)
            revpage[idx].click()
            time.sleep(3)
        driver.back()
        time.sleep(3)
        df = pd.DataFrame({'product_id': id, 'reviewer': review_ids, 'reviewer_rank': review_ranks, 'specialist': review_nameds, 'reviewer_skintype': reviewer_skins})
        df.to_csv('skin_review.csv', encoding='utf-8-sig')
    except:
        ID = driver.find_element(By.CLASS_NAME, 'prd_btn_area.new-style.type1 > .btnZzim').get_attribute('data-ref-goodsno')
        id.append(ID)
        print(ID)
        review_ids.append('None')
        review_ranks.append('None')
        review_nameds.append('None')
        reviewer_skins.append('None')
        print('리뷰가 없습니다')
        driver.back()
        time.sleep(3)
        df = pd.DataFrame({'product_id': id, 'reviewer': review_ids, 'reviewer_rank': review_ranks, 'specialist': review_nameds, 'reviewer_skintype': reviewer_skins})
        df.to_csv('skin_review.csv', encoding='utf-8-sig')

# 리뷰 크롤링 함수
def revCrawling(prds):
    try:
        driver.find_elements(By.CSS_SELECTOR, 'div.align_sort > ul > li')[1].click() # 도움순 클릭
        time.sleep(2)

        for idx in range(0,10):
            t1 = time.time()
            allpage = driver.find_element(By.CSS_SELECTOR, 'div.pageing')
            revpage = allpage.find_elements(By.TAG_NAME, 'a') # 리뷰 페이지 버튼
            driver.implicitly_wait(10)
            time.sleep(3)
            rows= driver.find_elements(By.CSS_SELECTOR, "ul#gdasList>li") # 페이지에 나오는 리뷰 전체
            for row in rows:
                ID = driver.find_element(By.CLASS_NAME, 'prd_btn_area.new-style.type1 > .btnZzim').get_attribute('data-ref-goodsno')
                id.append(ID)  
                print(ID)
                # 별점
                score = row.find_element(By.CSS_SELECTOR, 'span.point').text
                scores.append(score)
                print(score)
                # 날짜
                date = row.find_element(By.CSS_SELECTOR, 'span.date').text
                dates.append(date)
                print(date)
                # 온오프
                try:
                    onoff = row.find_element(By.CSS_SELECTOR, 'span.ico_offlineStore').text
                    onoffs.append(onoff)                
                except:
                    onoff = 'None'
                    onoffs.append(onoff)
                print(onoff)
                # 아이템 옵션
                try:
                    option = row.find_element(By.CSS_SELECTOR, 'p.item_option').text
                    options.append(option)
                except:
                    option = 'None'
                    options.append(option)
                print(option)
                # 개인리뷰고도화
                revsam = row.find_elements(By.CSS_SELECTOR, 'div.poll_sample')
                rev_list = [rev.text.strip() for rev in revsam]
                Revlist.append(rev_list)
                print(rev_list)
                # 리뷰
                try:
                    rev = row.find_element(By.CSS_SELECTOR, 'div.txt_inner').text
                    review.append(rev)
                except:
                    rev = 'None'
                    review.append(rev)
                print(rev)
                # 도움수
                try:
                    help = row.find_element(By.CSS_SELECTOR, 'div.recom_area > button.btn_recom > span.num').text
                    helplist.append(help)
                except:
                    help = 'None'
                    helplist.append(help)
                print(help)
            t2 = time.time()
            print('### 댓글 한 페이지 완료시간:', t2 - t1)
            revpage[idx].click()
            time.sleep(3)
        driver.back()
        time.sleep(3)
        df = pd.DataFrame({'product_id': id, 'user_score': scores, 'date': dates, 'on_off': onoffs, 'option': options, 'r_set': Revlist, 'review': review, 'help': helplist})
        df.to_csv('cleansing2_review.csv', encoding='utf-8-sig')
    except:
        ID = driver.find_element(By.CLASS_NAME, 'prd_btn_area.new-style.type1 > .btnZzim').get_attribute('data-ref-goodsno')
        id.append(ID)
        print(ID)
        scores.append('None')
        dates.append('None')
        onoffs.append('None')
        options.append('None')
        Revlist.append('None')
        review.append('None')
        helplist.append('None')
        print('### 리뷰가 없습니다')
        driver.back()
        time.sleep(3)
        df = pd.DataFrame({'product_id': id, 'user_score': scores, 'date': dates, 'on_off': onoffs, 'option': options, 'r_set': Revlist, 'review': review, 'help': helplist})
        df.to_csv('cleansing2_review.csv', encoding='utf-8-sig')
        
# 태그 크롤링 함수
def get_tag_hlt(url, endpage):
    for page in range(1, endpage+1):
        driver.implicitly_wait(10)
        url = url+f'{page}'
        driver.get(url)
        print(f'### {page}페이지..ing')
        prds_len = len(driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li'))
        
        for prd in range(prds_len):
            prds = driver.find_elements(By.CSS_SELECTOR, 'ul.cate_prd_list > li')[prd]
            # ids = prds.get_attribute('criteo-goods') # 찾은 제품의 id값을 리스트에 추가
            print(f'## {prd+1}번째 상품..ing')
            prds.click()
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, 'ul.prd_detail_tab > #reviewInfo > a').click()
            time.sleep(3)
            
            t1 = time.time()
            tag_list = driver.find_elements(By.CSS_SELECTOR, 'ul#ul_recommKeyword > li')[1:]


            for tag in tag_list:
                tag.click()
                time.sleep(3) 
                
                try:
                    allpage = driver.find_elements(By.CSS_SELECTOR, 'div.pageing > a')
                    end = int(allpage[-2].text)
                    hlt_list = [] ##### 추가                    
                    for idx in range(1,30):
                        idx = idx+1
                        # all = driver.find_element(By.CSS_SELECTOR, 'div.pageing')
                        # all_a = all.find_elements(By.TAG_NAME, 'a')
                        allpage = driver.find_elements(By.CSS_SELECTOR, 'div.pageing > a')
                        highlights = driver.find_elements(By.CSS_SELECTOR, 'div.txt_inner > span.highlight')
                        for hlt in highlights:  
                            hlt_list.append(hlt.text)
                        
                        if idx%10 != 0:
                            allpage[idx%10+1].click()
                            time.sleep(3)
                        else:
                            allpage[-1].click()
                            time.sleep(3)
                                
                    if tag.text == tag.text:
                        tag_hlt[f'{tag.text}'] = [','.join(hlt_list)]
                    else:
                        tag_hlt.setdefault(f'{tag.text}', [','.join(hlt_list)])
                    
                    
                except:
                    hlt_list = []
                    highlights = driver.find_elements(By.CSS_SELECTOR, 'div.txt_inner > span.highlight')
                    for hlt in highlights:  
                        hlt_list.append(hlt.text)
                    if tag.text == tag.text:
                        tag_hlt[f'{tag.text}'] = [','.join(hlt_list)]
                    else:
                        tag_hlt.setdefault(f'{tag.text}', [','.join(hlt_list)])
                    


            df = pd.DataFrame({'tag_hlt': tag_hlt})  ##### 추가
            df.to_csv('tag_word_bodycare.csv', encoding='utf-8-sig')   ##### 추가
            driver.back()
            t2 = time.time()
            print('# 소요 시간:', np.round((t2 - t1), 2))
            time.sleep(3)
        if page <= 9:
            url = url[:-1]
        else:
            url = url[:-2]
