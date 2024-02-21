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
    #return render(request, 'site/qr_code.html', {'otp_url': otp_url, 'img': img})

def gen_qr_img(otp_url, email):
    
    # Creation du code QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(otp_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save('users/qr_image/img.png')

    return (img)
