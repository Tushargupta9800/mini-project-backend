import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
import re
import string

def wordopt(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text

LR = LogisticRegression()
DT = DecisionTreeClassifier()
GBC = GradientBoostingClassifier(random_state=0)
RFC = RandomForestClassifier(random_state=0)
vectorization = TfidfVectorizer()

def train():
    df_fake = pd.read_csv("FakeNewsDetection/Fake.csv")
    df_true = pd.read_csv("FakeNewsDetection/True.csv")
    df_fake["class"] = 0
    df_true["class"] = 1
    df_fake_manual_testing = df_fake
    df_true_manual_testing = df_true
    df_fake_manual_testing["class"] = 0
    df_true_manual_testing["class"] = 1
    df_fake_manual_testing.head(10)
    df_true_manual_testing.head(10)
    df_marge = pd.concat([df_fake, df_true], axis =0 )
    df_marge.columns
    df = df_marge.drop([], axis = 1)
    df.isnull().sum()
    df = df.sample(frac = 1)
    df.head()
    df.reset_index(inplace = True)
    df.drop(["index"], axis = 1, inplace = True)
    df["text"] = df["text"].apply(wordopt)
    x = df["text"]
    y = df["class"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)

    LR.fit(xv_train,y_train)
    pred_lr=LR.predict(xv_test)
    LR.score(xv_test, y_test)
    classification_report(y_test, pred_lr)

    DT.fit(xv_train, y_train)
    pred_dt = DT.predict(xv_test)
    DT.score(xv_test, y_test)
    classification_report(y_test, pred_dt)

    GBC.fit(xv_train, y_train)
    pred_gbc = GBC.predict(xv_test)
    GBC.score(xv_test, y_test)
    classification_report(y_test, pred_gbc)

    RFC.fit(xv_train, y_train)
    pred_rfc = RFC.predict(xv_test)
    RFC.score(xv_test, y_test)
    classification_report(y_test, pred_rfc)
    
def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GBC = GBC.predict(new_xv_test)
    pred_RFC = RFC.predict(new_xv_test)
    return pred_LR[0] + pred_GBC[0] + pred_RFC[0] + pred_DT[0];
