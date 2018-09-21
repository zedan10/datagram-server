import secrets
from datagram_user_model import Datagram_User
from config import secret
from simplecrypt import encrypt, decrypt
import datetime

class Datagram_User_Client(object):
    def generate_dg_token(self):
        new_dg_token = secrets.token_urlsafe(32)
        if self.check_api_token_exists(new_dg_token) == False:
            return new_dg_token
        else:
            self.generate_dg_token()

    def check_api_token_exists(self, api_token):
        check_api_token = Datagram_User.objects(dg_token=api_token)
        if len(check_api_token) > 0:
            self.generate_dg_token()
        else:
            return(False)

    def check_valid_api_token(self, api_token):
        valid_token = Datagram_User.objects(dg_token=api_token)
        if len(valid_token) > 0:
            return True
        else:
            return False

    def get_business_id_by_api_token(self, api_token):
        if self.check_valid_api_token(api_token) == True:
            business = Datagram_User.objects(dg_token=api_token)
            if len(business) > 0:
                return str(business[0].id)
            else:
                return {'error': "An error occurred. Please try again"}

    def encrypt_password(self, password):
        encrypted_password = encrypt(secret, password.encode('utf-8'))
        return(encrypted_password)

    def verify_password(self, password, encrypted_password):
        decrypted_password = decrypt(secret, encrypted_password)
        password_str = decrypted_password.decode('utf-8')
        if password_str == password:
            return True
        else:
            return False

    def business_login(self, business_email, business_password):
        if not business_email:
            return "Please provide a business email", 400
        if not business_password:
            return "Please provide a business password", 400

        check_business_exists = Datagram_User.objects(business_email=business_email)

        if len(check_business_exists) > 0:
            encrypted_password = check_business_exists[0].business_password
            if self.verify_password(business_password, encrypted_password) == True:
                try:
                    Datagram_User.objects(business_email=business_email).update_one(upsert=False, set__date_accessed=datetime.datetime.utcnow)
                except Exception as e:
                    return("Error \n %s" % (e))
                return {'business_name': check_business_exists[0].business_name, 'business_email': business_email, 'number': check_business_exists[0].number, 'api_token': check_business_exists[0].dg_token}
            else:
                return {'error': "Incorrect email or password"}
        else:
            return {'error': "Business does not exist with this email"}

    def add_new_business(self, business_email, business_password, business_name, number):
        if not business_email:
            return "Please provide a business email", 400
        if not business_password:
            return "Please provide a business password", 400
        if not business_name:
            return "Please provide a business name", 400
        if not number:
            return "Please provide a number for us to contact you at", 400

        check_existing_business = Datagram_User.objects(business_email=business_email)

        if len(check_existing_business) > 0:
            return "Business already exists with this email", 409
        else:
            encrypted_password = self.encrypt_password(business_password)
            api_token = self.generate_dg_token()
            try:
                register_business = Datagram_User.objects(business_email=business_email).update_one(upsert=True, set__business_email=business_email, set__business_password=encrypted_password, set__business_name=business_name, set__dg_token=api_token, set__number=number)
            except Exception as e:
                return("Error \n %s" % (e))
            return self.business_login(business_email, business_password)

        