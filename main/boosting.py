# modules
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier  #GBM algorithm
from sklearn import metrics   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search
from sklearn.model_selection import train_test_split, cross_val_score
import math
from datetime import datetime, timedelta, timezone
import re
from common import logger

# from matplotlib.pylab import rcParams
# import seaborn as sns
# rcParams['figure.figsize'] = 10, 4

train = pd.read_csv('../csv/fixed_train.csv')
train = train.drop('Unnamed: 0', axis=1)
target = 'is_arrested'

train_data, train_data_test = train_test_split(train, test_size=0.3, random_state=0)

X_test = train_data_test.drop([target], axis=1)
Y_test = train_data_test[target]

def sigmoid(x):
    return 1 / (1 + np.exp(- (1 * x))) # 0〜1.0


def modelfit(alg, dtrain, predictors, performCV=True, printFeatureImportance=True, cv_folds=5):
    #Fit the algorithm on the data
    logger.info('fitting ....')
    alg.fit(dtrain[predictors], dtrain[target])
    logger.info('fitting finished')

    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]

    #Perform cross-validation:
    if performCV:
        cv_score = cross_val_score(alg, dtrain[predictors], dtrain[target], cv=cv_folds, scoring='roc_auc')

    #Print model report:
    print ("Model Report")
    print ("Accuracy : {:.4f}".format(metrics.accuracy_score(dtrain[target].values, dtrain_predictions)))
    print ("AUC Score (Train): {:.4f}".format(metrics.roc_auc_score(dtrain[target], dtrain_predprob)))

    if performCV:
        print ("CV Score : Mean - {:.6f} | Std - {:.6f} | Min - {:.6f} | Max - {:.6f}".format(np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score)))

    # #Print Feature Importance:
    # if printFeatureImportance:
    #     feat_imp = pd.Series(alg.feature_importances_, predictors).sort_values(ascending=False)
    #     sns.set_palette("husl")
    #     sns.barplot(feat_imp.head(10).index, feat_imp.head(10).values)
    #     plt.title('Top10 Feature Importances')
    #     plt.ylabel('Feature Importance Score')
    #     plt.xticks(rotation=60)
    #     plt.show()

    #print results
    return alg


#Choose all predictors except target & IDcols
predictors = [x for x in train.columns if x not in [target]]
gbm0 = GradientBoostingClassifier(random_state=10)
alg = modelfit(gbm0, train_data, predictors)
X_test_prob = sigmoid(alg.decision_function(X_test))
predicted = pd.Series(X_test_prob)

print('score is:')
score = metrics.roc_auc_score(Y_test, predicted)
print(score)

# ===== 結果出力
JST = timezone(timedelta(hours=+9), 'JST')
date = str(datetime.now(JST))
timestamp = re.sub(r'-|\s|:|(\.\d+)|(\+\d+\:\d+)', '', date)

with open('../log/result.log','a') as f:
    f.write(timestamp + ': ' + str(score) + '\n')

# ===== test 結果出力
test_data = pd.read_csv('../csv/fixed_test.csv')
test_data = test_data.drop('Unnamed: 0', axis=1)
test_datat_prob = sigmoid(alg.decision_function(test_data))
test_predicted = pd.Series(X_test_prob)
result = pd.DataFrame(test_predicted.values.tolist(), columns=['is_arrested'])
result.to_csv('../csv/result/result_' + timestamp + '.csv', float_format='%.6f', columns=['is_arrested'], index=False)
# ===== 結果出力
