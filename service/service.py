import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBhHnJLqCm3KZP3P0dka605xmecZ7iKBLg",
    "authDomain": "aplicativo-a91c7.firebaseapp.com",
    "projectId": "aplicativo-a91c7",
    "storageBucket": "aplicativo-a91c7.appspot.com",
    "messagingSenderId": "879808834627",
    "appId": "1:879808834627:web:9ecf5e1ac281f93c8d78f6",
    "measurementId": "G-KCWBSTJ2GZ",
    "databaseURL": "https://aplicativo-a91c7-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()


#db.child("names").push({"name" : "teste"})

# user = auth.sign_in_with_email_and_password(email, senha)
#info = auth.get_account_info(user['idToken'])
# print(info)

#
# email = 'teste2@gmail.com'
# password = '123456'
# user = auth.create_user_with_email_and_password(email,password)
# print(user)
# db.child('users').child(user['localId']).set({'email': email})