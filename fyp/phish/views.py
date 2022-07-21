from django.shortcuts import render
import features
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from scipy.linalg import pinv
# Create your views here.


def home(request):
    return render(request, 'index.html')


def getPredictions(X):

    train = pd.read_csv('C:/Users/Asus/Downloads/FYP_dataset.csv')

    onehotencoder = OneHotEncoder(categories='auto')
    scaler = StandardScaler()

    X_train = scaler.fit_transform(train.values[:, 1:])
    y_train = onehotencoder.fit_transform(train.values[:, :1]).toarray()

    input_size = X_train.shape[1]
    hidden_size = 2000
    input_weights = np.random.normal(size=[input_size, hidden_size])
    biases = np.random.normal(size=[hidden_size])

    def __init__(self, X, n_h, i_w):
        self.X = X
        self.hidden_size = n_h
        self.input_weights = i_w

    def relu(x):
        return np.maximum(x, 0, x)

    def hidden_nodes(X):
        G = np.dot(X, input_weights)
        G = G + biases
        H = relu(G)
        return H
    output_weights = np.dot(pinv(hidden_nodes(X_train)), y_train)

    class elm:
        def predict(self, X):
            out = hidden_nodes(X)

            out = np.dot(out, output_weights)
            return out

    p = elm()
    prediction = np.argmax(p.predict(X))
    print(np.argmax(prediction))

    if prediction == 0:
        return "Phishing"
    elif prediction == 1:
        return "Legitimate"
    else:
        return "Error"


def result(request):
    url = request.GET['url']
    data = features.generate_data_set(url)
    if data[13] == 1:
        uoa= "URL of anchors points to own domain "
    else:
        uoa= "URL of anchors dosen't point to own domain "
    

    if data[7] == 1:
        ssl= "SSL issuer is trusted"
    else:
        ssl= "SSL issuer is not trusted"

    
    if data[5] == 1:
        ps= "Domain name does not include - symbol"
    else:
        ps= "Domain name includes - symbol"

    if data[25] == 1:
        wr= "Website rank is less than 100,000"
    else:
        wr= "Website rank is more than 100,000"

    if data[6] == 1:
        sd= "There are no multiple subdomains"
    else:
        sd= "Multiple subdomains exist"

    if data[18] == 1:
        redrct= "redirects to 1 or less pages"
    else:
        redrct= "redirects to 2 or more pages"
    


    result = getPredictions(data)

    return render(request, 'index.html', {'result': result, 'UA': uoa, 'SSL': ssl,'PS':ps,'WR': wr, 'SD':sd, 'RDC':redrct})
