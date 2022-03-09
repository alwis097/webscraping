from unicodedata import name
from flask import Flask, request, render_template,redirect,url_for
from matplotlib.pyplot import text
import pandas as pd  
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from facebook_scraper import get_posts
from bs4 import BeautifulSoup
import requests
import nest_asyncio
nest_asyncio.apply()
import twint
import pandas
import pandas as pd  


app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/web',)
def my_form_homepage_web():
    return render_template('web.html')



@app.route('/web', methods=['POST','GET'])
def my_form_post():
    text = request.form['text']
    
    def html(link):
        # post_content = []
        #print(text)
        try:
            html_text = requests.get(link).text
            #print(html_text)
            soup = BeautifulSoup(html_text,'lxml')
            jobs =  soup.find_all('li', class_ = 'job_listing job-type-part-time post-3354 type-job_listing status-publish has-post-thumbnail hentry job_listing_region-kansas job_listing_category-design job_listing_type-part-time')

            list_post = []
            list_company_name = []
            list_loc = []
            list_requirement = []
            list_job_title = []
            list_e_date= []

            for job in jobs:

                post =  job.find('h3', class_ = 'job_listing-title').text.replace(' ', '-')
                list_post.append(post)

                company_name = job.find('div', class_ = 'job_listing-company').text.strip().replace(' ', '-')
                list_company_name.append(company_name)
                
                loc = job.find('div', class_ = 'location col-md-5 col-lg-4').text.strip().replace(' ', '-')
                list_loc.append(loc)
                
                requirement = job.find('div', class_ = 'job_listing-overview job_listing__column').text.strip().replace(' ', '-')
                list_requirement.append(requirement)

                job_title = job.find('li', class_ = 'job-type').text
                #print(job_title)
                list_job_title.append(job_title)

                expire_date = job.find('li', class_ = 'date').text.replace('Expires on ','')
                list_e_date.append(expire_date)


            # print(list_loc)
        #     print(list_company_name)
        #     print(list_requirement)
        #     print(list_job_title)
        #     print(list_e_date)
            d = {'list_post':list_post,'list_company_name':list_company_name ,'list_loc':list_loc ,'list_requirement':list_requirement,'list_job_title':list_job_title, 'list_e_date':list_e_date}
            #print(d)
            
            df = pd.DataFrame(d, columns=['list_post','list_company_name','list_loc','list_requirement','list_job_title','list_e_date'])
            #print(df)
            x1 = df.to_html(escape=False)

            bb = "Web data scraping details.Xpress jobs : "+ link
            return render_template('web.html',a = x1,b = bb)
                #df1_transposed.to_csv('file_name(8).csv', encoding='utf-8')
            
        except:
            tx = "Page not found or access denied"
            return render_template('web.html',tx1 = tx)

    # x = post('Ray-Ban')
    x = html(text)

    return x


@app.route('/home',)
def my_form_homepage():
    return render_template('home.html')

@app.route('/home',methods=['POST','GET'])
def my_form_homepage1():
    text1 = request.form['text1']

    def post(fb):
        try:
            post_content = []
            all ={}
            for post in get_posts(fb, pages=6):
                    x=post['text'][:100000000000000]
                    z = x.replace('\n', '-')
                    result = len(z.split())
                # print(result)
                    all[z] = [result]
                    #print()    
                    stop_words = set(stopwords.words('english'))
                    word_tokens = word_tokenize(z)
                            
                            
                    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
                    filtered_sentence = []
                    for w in word_tokens:
                                if w not in stop_words:
                                    filtered_sentence.append(w)
                            
                    all[z].append(word_tokens)
                    all[z].append(filtered_sentence)
                            
                    post_content.append(z)
            bb1 = "Page name : "+ fb        
            data= pd.DataFrame(all) 
            df1_transposed = data.T
            df2_tidy = df1_transposed.rename(columns = {'variable': 'Year', 'value': 'Income'}, inplace = False)
            df2_tidy1 = df2_tidy.to_html(escape=False)
            #df2_tidy2 = df1_transposed.to_html(escape=False)
            print(df2_tidy1)
            # df2_tidy.to_csv('file_name(10).csv', encoding='utf-8')
                    #fb_post =post(text1)

            return render_template('home.html',bb2 = bb1,tx2 = df2_tidy1,post_name =text1)
        except:
            tx1 = "Page not found or access denied"
            return render_template('index.html',tx2 = tx1,bb2 = bb1)
    
    fball = post(text1)
    return fball




@app.route('/twitter',)
def my_form_homepage_twitter():
    return render_template('twitter.html')

formData = {}
#d = twint.Config()

@app.route('/twitter',methods=['POST','GET'])
def my_form_homepage2():
    #d = twint.Config()
    if request.method == 'POST':
        name = request.form['text2']
        date = request.form['text3']
        d.Username = name
        d.Limit = 1
        d.Since = date
        d.Pandas = True
        #twint.run.Search(d)
        name_date1 = twint.storage.panda.Tweets_df
        name_date = name_date1.to_html(escape=False)

        formData['name'] = name
        formData['real_date'] = date
        # print(formData['real_date'])
        formData['date'] = name_date
        
        return redirect(url_for('output'))
    else:
        return render_template('twitter.html')  


@app.route('/output',)
def output():
    return render_template('output.html',date1 = formData['date'],real_date = formData['real_date'],real_name = formData['name'])


@app.route('/twitter_home',)
def my_form_homepage_twitter_home():
    return render_template('twitter_home.html')


@app.route('/twitter_name',)
def my_form_homepage_username():
    return render_template('twitter_name.html')

formUsername= {}
d = twint.Config()


@app.route('/twitter_name',methods=['POST','GET'])
def my_form_homepage_username1():
    d = twint.Config()
    if request.method == 'POST':
        u_name = request.form['u_name']
        c = twint.Config()
        d.Username = u_name
        d.Limit = 1
        d.Pandas = True
        twint.run.Search(d)
        real_username1 = twint.storage.panda.Tweets_df
        real_username = real_username1.to_html(escape=False)

        formUsername['u_name'] = u_name
        formUsername['real_username'] = real_username
        # print(formData['real_date'])
        # formData['date'] = name_date
        
        return redirect(url_for('output4'))
    else:
        return render_template('twitter_name.html')  


@app.route('/output4',)
def output4():
    return render_template('output4.html',u_name1 = formUsername['u_name'],real_username1 = formUsername['real_username'])

@app.route('/twitter_st',)
def my_form_homepage_twitter_st():
    return render_template('twitter_st.html')

formWord = {}


@app.route('/twitter_st',methods=['POST','GET'])
def my_form_homepage3():
    if request.method == 'POST':

        name1 = request.form['text4']
        word_s = [request.form['text5']]
        print(name1)
        print(word_s)
        d.Username = name1
        d.Limit = 1
        d.Search = word_s
        print(d.Search)
        d.Pandas = True
        #twint.run.Search(d)
        real_word1 = twint.storage.panda.Tweets_df

        print(real_word1)
        real_word = real_word1.to_html(escape=False)
        
        formWord['name1'] = name1
        formWord['word_S'] = real_word
        formWord['S_string'] = word_s
        
        return redirect(url_for('output1'))
    else:
        return render_template('twitter_st.html')  


@app.route('/output1',)
def output1():
    return render_template('output1.html',name1 = formWord['name1'],word_S = formWord['word_S'],S_string = formWord['S_string'])


@app.route('/twitter_like',)
def my_form_homepage_twitter_like():
    return render_template('twitter_like.html')

formLike = {}


@app.route('/twitter_like',methods=['POST','GET'])
def my_form_homepage4():    
    if request.method == 'POST':

        name2 = request.form['text6']
        min_like = request.form['text7']
        min_re = request.form['text8']
        min_reTw = request.form['text9']
        print(name2)
        print(min_like)
        print(min_re)
        print(min_reTw)
        d.Limit = 10
        d.Min_likes = min_like
        d.Min_replies = min_re
        d.Min_retweets = min_reTw
        d.Pandas = True

        #twint.run.Search(e)
        like_rep1 = twint.storage.panda.Tweets_df

        like_rep = like_rep1.to_html(escape=False)
        
        formLike['name2'] = name2
        formLike['min_like'] = min_like
        formLike['min_re'] = min_re
        formLike['min_reTw'] = min_reTw
        formLike['like_rep'] = like_rep
        
        return redirect(url_for('output2'))
    else:
        return render_template('twitter_like.html')  


@app.route('/output2',)
def output2():
    return render_template('output2.html',like_rep = formLike['like_rep'],name2 = formLike['name2'],min_like = formLike['min_like'],min_re = formLike['min_re'],min_reTw = formLike['min_reTw'])






@app.route('/homehome',)
def my_form_homepage_home():
    return render_template('homehome.html')











if __name__ == "__main__":
    app.run(debug=True ,use_reloader=True)