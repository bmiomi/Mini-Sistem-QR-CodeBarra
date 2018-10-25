from flask import Flask, request, render_template, redirect, url_for
from App.forms import CouponForm
from flask_wtf.csrf import CSRFProtect

from App.barcode import generate_barcode_image, combine_images_into_coupon,open_image_file_from_url #send_coupon_via_mms

twilio_logo_png_url = 'http://www.twilio.com/packages/company/' + \
                      'img/logos_downloadable_logobrand.png'


cfr=CSRFProtect()

def createapp():
	cfr.init_app(app)
	return app
app =Flask(__name__)

#app=createapp()

app.config['SECRET_KEY'] = 'any secret string'

@app.route('/', methods=['GET','POST'])

def create_coupon():
    form = CouponForm(request.form)
    if form.validate():
        serial_number = form.serial_number.data
        phone_number = form.phone_number.data
        logo_image_url = form.logo_image_url.data
        coupon_text = form.coupon_text.data

        logo_img = open_image_file_from_url(logo_image_url)
        if not logo_img:
            logo_img = open_image_file_from_url(twilio_logo_png_url)
        if serial_number:
            barcode_img = generate_barcode_image(serial_number)
        else:
            barcode_img = generate_barcode_image()

        coupon_url = combine_images_into_coupon(logo_img, barcode_img)
        print("URL:",coupon_url)
        #send_coupon_via_mms(coupon_url, phone_number, coupon_text)
        return redirect(url_for('coupon_confirmation'))
    return render_template('create_coupon.html', form=form)


@app.route('/confirmation/', methods=['GET'])
def coupon_confirmation():
    form = CouponForm()
    return render_template('confirmation.html',form=form)