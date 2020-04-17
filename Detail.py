from django.db import modelsclass ArticleExample(models.Model):
   # This will hold the visible text for this example
   body_text = models.TextField()
   # This bias score is a left-right bias provided by Media Bias
   # Chart, but not used in this project. 
   bias_score = models.FloatField()
   bias_class = models.IntegerField()
   # quality_score comes from the Media Bias Chart data
   quality_score = models.FloatField()
   # quality_class is based on the quality score and allows us to
   # integrate politifact data in their
   # 4-class way, True = 4, Mostly True = 3, Mostly Fake = 2,
   # Fake = 1
   quality_class = models.IntegerField()
 
   origin_url = models.TextField()
   origin_source = models.TextField()
   import os, sys, re, timeproj_path = “/home/jwales/eclipse-workspace/crowdnews/”
os.environ.setdefault(“DJANGO_SETTINGS_MODULE”, “crowdnews.settings”)
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.gis.views import feed

import pandas as pd
from newsbot.strainer import *
from newsbot.models import *ss = SoupStrainer()
print(“Initializing dictionary…”)
ss.init()

def harvest_Politifact_data():
   print(“Ready to harvest Politifact data.”)
   input(“[Enter to continue, Ctl+C to cancel]>>”)
   print(“Reading URLs file”)   # Read the data file into a pandas dataframe
   df_csv = pd.read_csv(“newsbot/politifact_data.csv”,
   error_bad_lines=False, quotechar=’”’, thousands=’,’,
   low_memory=False)   for index, row in df_csv.iterrows():
      print(“Attempting URL: “ + row[‘news_url’])
      if(ss.loadAddress(row[‘news_url’])):
         print(“Loaded OK”)
   # some of this data loads 404 pages b/c it is a little old, 
   # some load login pages. I’ve found that
   # ignoring anything under 500 characters is a decent 
   # strategy for weeding those out.
         if(len(ss.extractText)>500):
            ae = ArticleExample()
            ae.body_text = ss.extractText
            ae.origin_url = row[‘news_url’]
            ae.origin_source = ‘politifact data’
            ae.bias_score = 0 # Politifact data doesn’t have this
            ae.bias_class = 5 # 5 is ‘no data’
            ae.quality_score = row[‘score’]
            ae.quality_class = row[‘class’]
            ae.save()
            print(“Saved, napping for 1…”)
            time.sleep(1)
         else:
            print(“**** This URL produced insufficient data.”)
      else:
         print(“**** Error on that URL ^^^^^”)
         
         class SoupStrainer():
   englishDictionary = {}
   haveHeadline = False
   recHeadline = ‘’
   locToGet = ‘’
   pageData = None
   errMsg = None
   soup = None
   msgOutput = True   def init(self):
      with open(‘newsbot/words_dictionary.json’) as json_file:
         self.englishDictionary = json.load(json_file)
         
         def tag_visible(self, element):
   if element.parent.name in [‘style’, ‘script’, 
          ‘head’, ‘title’, ‘meta’, ‘[document]’]:
      return False
   if isinstance(element, Comment):
      return False
   return True
