# moody-tunes

**Overview:**

Team moody tune's softdev project #2. Our project is a virtual diary that you can make entries in. Every entry is sent to the IBM Watson Tone Analyzer to determine how your day was, and then this mood data is used to search last.fm for a recommended song for that day.


**Instructions:**

First, clone the repo locally. Then,create a "keys.txt" file containing "<Lastfm key>\n<ibmUsername>\n<ibmPassword>" and move the "keys.txt" file into the root of the repo. You can get your own API keys by checking the links in the dependencies section. You also need python, flask, and requests in order to run this app, which is also explained in the dependencies section. Once all dependencies are set up, you can  launch the website on localhost by running the command

```
$ python app.py
```

To view the website, navigate to localhost:5000 in your browser. Make an account by following the register link on the home page. To make a diary entry, navigate to your diary page and fill out the text box. Your song for that entry will show up next to that entry.


**Dependencies:**
- <a href = "https://www.python.org/downloads/"> python </a>
- <a href = "http://flask.pocoo.org/docs/0.12/installation/"> flask </a>
- <a href = "https://console.bluemix.net/registration/?target=%2Fdeveloper%2Fwatson%2Fcreate-project%3Fservices%3Dtone_analyzer%26hideTours%3Dtrue&cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmca1%3D000000OF%26cm_mmca2%3D10000409&cm_mc_uid=41516314672015106846304&cm_mc_sid_50200000=1511376254&cm_mc_sid_52640000=1511376254"> IBM Watson Tone Analyzer API key </a>: sign up for an API key
- <a href = "http://docs.python-requests.org/en/master/user/install/"> python requests module </a>: use pip install
  

**Known Bugs**
- The database sometimes doesn't commit and close correctly
- Using single or double quotes in a diary entry can break the system

**Team:**

Md Abedin (project manager), Sasha Fomina, Augie Murphy, Xing Tao Shi
