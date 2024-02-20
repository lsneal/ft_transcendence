import pyotp
import qrcode

def gen_otp_url(username):
    
    secret_key = pyotp.random_base32()
    otp_url = pyotp.totp.TOTP(secret_key).provisioning_uri(name=username, issuer_name='app')

    print(otp_url)
    print(username)
    return (otp_url)
    #return render(request, 'site/qr_code.html', {'otp_url': otp_url, 'img': img})

def gen_qr_img(otp_url, username):
    
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
    img.save('app/static/qr_image/img.png')

    return (img)
