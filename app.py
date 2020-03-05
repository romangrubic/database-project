import os
import math
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'adverts'
app.config["MONGO_URI"] = os.environ.get('MONGO_DATA_URI')

mongo = PyMongo(app)

ADS_PER_PAGE = 12


@app.route('/')
# --------- Home page -------------------------------------------
@app.route('/home')
def home():
    total_view()
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    return render_template('home.html',
                           counties=counties,
                           categories=categories,
                           tittle="Home",
                           views=mongo.db.total_view.find(),
                           top_ads=mongo.db.advert.find()
                           .sort('views', DESCENDING).limit(5))


def total_view():
    total_view = mongo.db.total_view
    total_view.update({'_id': ObjectId('5e4edcbd1c9d440000e3b783')}, {
                      '$inc': {'views': 1}})
    return True


# --------- Marketplace page ----------------------------------------
@app.route('/marketplace')
def marketplace():
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    page_number = int(request.args.get('page', 1))
    ads_to_skip = (page_number - 1) * ADS_PER_PAGE
    ads_count = mongo.db.advert.find().count()
    page_count = int(math.ceil(ads_count / ADS_PER_PAGE))
    page_numbers = range(1, page_count + 1)
    ads_on_page = mongo.db.advert.find().sort(
        'views', DESCENDING).skip(ads_to_skip).limit(ADS_PER_PAGE)
    return render_template('marketplace.html',
                           counties=counties,
                           categories=categories,
                           tittle="Marketplace",
                           adverts=ads_on_page,
                           ads=ads_on_page,
                           page=page_number,
                           pages=page_numbers,
                           total=page_count)


# --------- Filter search: Motors and Vehicles ------------------------------
@app.route('/motors_and_vehicles')
def motors_and_vehicles():
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    page_number = int(request.args.get('page', 1))
    ads_to_skip = (page_number - 1) * ADS_PER_PAGE
    ads_count = mongo.db.advert.find(
        {'category_name': 'Motors and vehicles'}).count()
    page_count = int(math.ceil(ads_count / ADS_PER_PAGE))
    page_numbers = range(1, page_count + 1)
    ads_on_page = mongo.db.advert.find(
        {'category_name': 'Motors and vehicles'}).sort(
        'views', DESCENDING).skip(ads_to_skip).limit(ADS_PER_PAGE)
    return render_template('marketplace.html',
                           counties=counties,
                           categories=categories,
                           subtittle="Marketplace",
                           tittle="Motors and vehicles",
                           adverts=ads_on_page,
                           ads=ads_on_page,
                           page=page_number,
                           pages=page_numbers,
                           total=page_count)


# --------- Filter search: Home, garden and Diy -----------------------------
@app.route('/home_garden_diy')
def home_garden_diy():
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    page_number = int(request.args.get('page', 1))
    ads_to_skip = (page_number - 1) * ADS_PER_PAGE
    ads_count = mongo.db.advert.find(
        {'category_name': 'Home, garden, DIY'}).count()
    page_count = int(math.ceil(ads_count / ADS_PER_PAGE))
    page_numbers = range(1, page_count + 1)
    ads_on_page = mongo.db.advert.find(
        {'category_name': 'Home, garden, DIY'}).sort('views', DESCENDING).skip(
            ads_to_skip).limit(ADS_PER_PAGE)
    return render_template('marketplace.html',
                           counties=counties,
                           categories=categories,
                           subtittle="Marketplace",
                           tittle="Home, garden and DIY",
                           adverts=ads_on_page,
                           ads=ads_on_page,
                           page=page_number,
                           pages=page_numbers,
                           total=page_count)


# --------- Filter search: Electronic, mobile and PC -------------------------
@app.route('/electronics')
def electronics():
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    page_number = int(request.args.get('page', 1))
    ads_to_skip = (page_number - 1) * ADS_PER_PAGE
    ads_count = mongo.db.advert.find(
        {'category_name': 'Electronics, mobile, PC'}).count()
    page_count = int(math.ceil(ads_count / ADS_PER_PAGE))
    page_numbers = range(1, page_count + 1)
    ads_on_page = mongo.db.advert.find(
        {'category_name': 'Electronics, mobile, PC'}
    ).sort('views', DESCENDING).skip(ads_to_skip).limit(ADS_PER_PAGE)
    return render_template('marketplace.html',
                           counties=counties,
                           categories=categories,
                           subtittle="Marketplace",
                           tittle="Electronics, mobile and PC",
                           adverts=ads_on_page, ads=ads_on_page,
                           page=page_number,
                           pages=page_numbers,
                           total=page_count)


# ----------- Filter search: Search query ------------------------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    query = request.args.get('search').upper()
    results = mongo.db.advert.find({'advert_name': {"$regex": query}})
    results_number = results.count()

    page_number = int(request.args.get('page', 1))
    ads_to_skip = (page_number - 1) * ADS_PER_PAGE
    ads_count = mongo.db.advert.find(
        {'advert_name': {"$regex": query}}).count()
    page_count = int(math.ceil(ads_count / ADS_PER_PAGE))
    page_numbers = range(1, page_count + 1)
    ads_on_page = mongo.db.advert.find(
        {'advert_name': {"$regex": query}}).skip(
        ads_to_skip).limit(ADS_PER_PAGE)
    return render_template('search.html',
                           counties=counties,
                           categories=categories,
                           tittle="Search",
                           results=ads_on_page,
                           ads=ads_on_page,
                           results_number=results_number,
                           page=page_number,
                           pages=page_numbers,
                           total=page_count)


# ---------- Filter by Category AND by County ---------------------------
@app.route('/county', methods=['GET', 'POST'])
def county_search():
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    county = request.form.get('county')
    category = request.form.get('category_name')
    page_number = int(request.args.get('page', 1))
    ads_to_skip = (page_number - 1) * ADS_PER_PAGE
    ads_count = mongo.db.advert.find({'category_name': category,
                                      'location': county}).count()
    page_count = int(math.ceil(ads_count / ADS_PER_PAGE))
    page_numbers = range(1, page_count + 1)
    ads_on_page = mongo.db.advert.find({'category_name': category,
                                        'location': county}).sort(
        'views', DESCENDING).skip(ads_to_skip).limit(ADS_PER_PAGE)
    return render_template('search.html',
                           counties=counties,
                           categories=categories,
                           subtittle="Marketplace",
                           tittle=category,
                           results=ads_on_page,
                           ads=ads_on_page,
                           results_number=ads_count,
                           page=page_number,
                           pages=page_numbers,
                           total=page_count)


# --------- Single advert page ----------------------------------
@app.route('/view_advert/<advert_id>')
def view_advert(advert_id):
    counties = mongo.db.county.find()
    categories = mongo.db.categories.find()
    advert = mongo.db.advert.find_one({'_id': ObjectId(advert_id)})
    view_count(advert_id)
    return render_template('view_advert.html',
                           counties=counties,
                           categories=categories,
                           tittle="Advert info",
                           advert=advert)


# ----------- Increments Adverts view counter by +1 -------------
def view_count(advert_id):
    advert = mongo.db.advert
    advert.update({'_id': ObjectId(advert_id)}, {'$inc': {'views': 1}})
    return True


# ----------- Add advert ----------------------------------------
@app.route('/add_advert')
def add_advert():
    return render_template('add_advert.html',
                           tittle="Add advert",
                           categories=mongo.db.categories.find(),
                           counties=mongo.db.county.find())


# ---------- Insert advert --------------------------------------
@app.route('/insert_advert', methods=['POST'])
def insert_advert():
    advert = mongo.db.advert

    if "advert_image" in request.files:
        advert_image = request.files['advert_image']
        mongo.save_file(advert_image.filename, advert_image)

    new_advert = {
        'category_name': request.form.get('category_name'),
        'advert_name': request.form.get('advert_name').upper(),
        'advert_description': request.form.get('advert_description'),
        'price': request.form.get('price'),
        'contact_info': request.form.get('contact_info'),
        'location': request.form.get('location'),
        'imageURL': advert_image.filename,
        'views': 0,
        'key': request.form.get('access_key')

    }
    advert.insert_one(new_advert)
    return redirect(url_for('home'))


# ------------ Uploading images ---------------------------------------
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


# ------------- Edit advert ------------------------------------
@app.route('/edit_advert/<advert_id>', methods=['GET', 'POST'])
def edit_advert(advert_id):
    the_advert = mongo.db.advert.find_one({"_id": ObjectId(advert_id)})
    all_categories = mongo.db.categories.find()
    if the_advert['key'] == request.form.get('access_key2'):
        return render_template('edit_advert.html',
                               tittle="Edit Advert",
                               advert=the_advert,
                               categories=all_categories,
                               counties=mongo.db.county.find())
    else:
        counties = mongo.db.county.find()
        categories = mongo.db.categories.find()
        return render_template('access_denied.html',
                               advert_id=advert_id,
                               counties=counties,
                               categories=categories,
                               tittle="Access denied")


# ------------ Update advert -----------------------------------
@app.route('/update_advert/<advert_id>', methods=['POST'])
def update_advert(advert_id):
    advert = mongo.db.advert.find_one({"_id": ObjectId(advert_id)})

    if 'advert_image' in request.files and request.files[
            'advert_image'].filename != "":
        advert_image = request.files['advert_image']
        image_filename = advert_image.filename
        mongo.save_file(advert_image.filename, advert_image)
    else:
        image_filename = advert['imageURL']

    mongo.db.advert.update({'_id': ObjectId(advert_id)},
                           {
        'category_name': request.form.get('category_name'),
        'advert_name': request.form.get('advert_name').upper(),
        'advert_description': request.form.get('advert_description'),
        'price': request.form.get('price'),
        'contact_info': request.form.get('contact_info'),
        'location': request.form.get('location'),
        'imageURL': image_filename,
        'views': int(request.form.get('views')),
        'key': request.form.get('access_key')
    })
    return redirect(url_for('view_advert', advert_id=advert_id))


# ------------------ Deleting advert ---------------------------
def delete(advert_id):
    advert = mongo.db.advert
    advert.remove({'_id': ObjectId(advert_id)})
    return redirect(url_for('home'))


@app.route('/delete_advert/<advert_id>', methods=['POST'])
def delete_advert(advert_id):
    advert = mongo.db.advert.find_one({"_id": ObjectId(advert_id)})

    if advert['key'] == request.form.get('access_key2'):
        delete(advert_id)
        return redirect(url_for('home'))
    else:
        counties = mongo.db.county.find()
        categories = mongo.db.categories.find()
        return render_template('access_denied.html', advert_id=advert_id,
                               counties=counties,
                               categories=categories,
                               tittle="Access denied")


# ------------- Host/Port/Debug --------------------------------
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
