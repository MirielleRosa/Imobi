import pyrebase

config = {
  "apiKey": "AIzaSyD4JhfdbDA4b_4Pdtzc5BWweUk6VNJldrA",
  "authDomain": "corretorauploads.firebaseapp.com",
  "projectId": "corretorauploads",
  "storageBucket": "corretorauploads.appspot.com",
  "messagingSenderId": "51020789655",
  "appId": "1:51020789655:web:4d977fa9bd7df399f876d2",
  "measurementId": "G-WN0T6Q3HRK",
  "databaseURL": "" 
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
