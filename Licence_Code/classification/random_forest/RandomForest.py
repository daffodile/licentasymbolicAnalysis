import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class RandomForest:

    def __init__(self, doas, channels, levels, segment, orientation):
        #dataset
        self.doas = doas
        #features
        self.channels = channels
        self.levels = levels
        self.segment = segment
        self.orientation = orientation

        #functie care imi ia doar datele selectate based on features
        self.get_data()
        #cu rezultatul de la functie fac splitul in train si test
        self.split_train_test()
        #alta functie care antreneaza?
        self.train()


    def get_data(self):
        for i in range(len(self.channels)):
            doa_light = np.extract(condition=(lambda x: x.level == "light"), arr=self.doas)[0]
            doa_deep = np.extract(condition=(lambda x: x.level == "deep"), arr=self.doas)[1]
            doa_medium = np.extract(condition=(lambda x: x.level == "deep"), arr=self.doas)[2]



    def split_train_test(self):
        # sa iau separat cate un array cu deep, light , medium si apoi primele 30% date din fiecare si sa le salvez intr un array de test, iar restull sa fie la train
        # Labels are the values we want to predict
        labels = np.array(features['actual'])

        X=data[['sepal length', 'sepal width', 'petal length', 'petal width']]  # Features
        y=data['species']  # Labels

        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

    def train(self):
        # Create a Gaussian Classifier
        clf = RandomForestClassifier(n_estimators=100)

        # Train the model using the training sets y_pred=clf.predict(X_test)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        # Model Accuracy, how often is the classifier correct?
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))