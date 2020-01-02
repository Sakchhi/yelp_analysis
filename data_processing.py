import pandas as pd
import os
import json


def create_dataframes():
    for filename in os.listdir('Data'):
        if filename.split('.')[1] == 'json':
            try:
                fp = open(os.path.join('Data', filename))
                for i in range(5):
                    print(fp.readline())
            finally:
                fp.close()
            # print(content)


def create_reviews_df():
    try:
        fp = open('Data/review.json')
        df_reviews = pd.DataFrame()
        for i in range(5):

            rev = dict(fp.readline())
            print(type(rev))
            print(pd.DataFrame(list(rev.items())))
    finally:
        fp.close()
    print(pd.DataFrame.from_dict({"review_id" : "11a8sVPMUFtaC7_ABRkmtw",
                                  "user_id" : "ssoyf2_x0EQMed6fgHeMyQ",
                                  "business_id":"b1b1eb3uo-w561D0ZfCEiQ",
                                  "stars":1.0,
                                  "useful":7,
                                  "funny":0,
                                  "cool":0,
                                  "text":"Today was my second out of three sessions I had paid for. Although my first \
                                  session went well, I could tell Meredith had a particular enjoyment for her male \
                                  clients over her female. However, I returned because she did my teeth fine and I was \
                                  pleased with the results. When I went in today, I was in the whitening room with \
                                  three other gentlemen. My appointment started out well, although, being a person who \
                                  is in the service industry, I always attend to my female clientele first when a \
                                  couple arrives. Unbothered by those signs, I waited my turn. She checked on me once \
                                  after my original 30 minute timer to ask if I was ok. She attended my boyfriend on \
                                  numerous occasions, as well as the other men, and would exit the room without even \
                                  asking me or looking to see if I had any irritation. Half way through, another woman \
                                  had showed up who she was explaining the deals to in the lobby. While she admits \
                                  timers must be reset half way through the process, she reset my boyfriends, left, \
                                  rest the gentleman furthest away from me who had time to come in, redeem his deal, \
                                  get set, and gave his timer done, before me, then left, and at this point my time \
                                  was at 10 minutes. So, she should have reset it 5 minutes ago, according to her. \
                                  While I sat there patiently this whole time with major pain in my gums, i watched \
                                  the time until the lamp shut off. Not only had she reset two others, explained deals \
                                  to other guest, but she never once checked on my time. When my light turned off, I \
                                  released the stance of my mouth to a more relaxed state, assuming I was only getting \
                                  a thirty minute session instead of the usual 45, because she had yet to come in. At \
                                  this point, the teeth formula was not only burning the gum she neglected for 25 \
                                  minutes now, but it began to burn my lips. I began squealing and slapping my chair \
                                  trying to get her attention from the other room in a panic. I was in so much pain, \
                                  that by the time she entered the room I was already out of my chair. She finally \
                                  then acknowledged me, and asked if she could put vitamin E on my gum burn (pictured \
                                  below). At this point, she has treated two other gums burns, while neglecting me, \
                                  and I was so irritated that I had to suffer, all I wanted was to leave. While I \
                                  waited for my boyfriend, she kept harassing me about the issue. Saying, \"well burns \
                                  come with teeth whitening.\" While I totally agree, and under justifiable \
                                  circumstances would not be as irritate, it could have easily been avoid if she had \
                                  checked on me even a second time, so I could let her know. Not only did she never \
                                  check on my physical health, she couldn't even take two seconds to reset the timer, \
                                  which she even admitted to me. Her accuse was that she was coming in to do it, but I \
                                  had the light off for a solid two minutes before I couldn't stand the pain. She \
                                  admitted it should be reset every 15 minutes, which means for 25 minutes she did not \
                                  bother to help me at all. Her guest in the lobby then proceeded to attack me as well, \
                                  simply because I wanted to leave after the way I was treated. I also expected a refund for not getting a complete session today, due to the neglect, and the fact I won't be returning for my last, she had failed to do that. She was even screaming from the door, and continued to until my boyfriend and I were down the steps. I have never in my life been more appalled by a grown woman's behavior, who claims to be in the business for \"10 years.\" Admit your wrongs, but don't make your guest feel unwelcome because you can't do you job properly.",
                                  "date":"2018-01-30 23:07:38"}
))
    print(df_reviews)


if __name__ == "__main__":
    # for (root,dirs,files) in os.walk('Data'):
    #     print(root)
    #     print(dirs)
    #     print(files)
    #     print('--------------------------------')
    # create_dataframes()
    create_reviews_df()