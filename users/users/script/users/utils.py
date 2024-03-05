import pyotp
import qrcode
import base64

def gen_key_user():

    private_key = pyotp.random_base32()
    return (private_key)

def gen_otp_url(email, private_key):
    
    otp_url = pyotp.totp.TOTP(private_key).provisioning_uri(name=email, issuer_name='app')

    print(otp_url)
    print(email)
    return (otp_url)