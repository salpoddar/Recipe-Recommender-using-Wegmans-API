__author__ = "Saloni Poddar"
from flask import Flask, render_template
from urllib.request import urlopen
import json

web_app = Flask(__name__)


@web_app.route('/')
def get_place():
    return render_template('HOME.html')


@web_app.route('/Category')
def getcategory():
    url1 = 'https://api.wegmans.io/products/categories?api-version=2018-10-18&Subscription-' \
           'Key=c455d00cb0f64e238a5282d75921f27e'
    category = getdetails(url1, 0)
    return render_template('Category.html', category=category)


@web_app.route('/Category/Produce')
def getproduce():
    url2 = 'https://api.wegmans.io/products/categories/601?api-version=2018-10-18&subscription-' \
           'key=c455d00cb0f64e238a5282d75921f27e'
    sub_categories = getdetails(url2, 0)
    return render_template('Produce.html', category=sub_categories)


@web_app.route('/Category/Produce/Vegetables')
def getvegies():
    url3 = 'https://api.wegmans.io/products/categories/601-606?api-version=2018-10-18&subscription-key=c455d00cb0f64e238a5282d75921f27e'
    vegetables = getdetails(url3, 0)
    return render_template('Vegetables.html', category=vegetables, title="Vegetables Categories")


@web_app.route('/Category/Produce/Vegetables/<veg>')
def getrecipe(veg):
    url4 = 'http://www.recipepuppy.com/api/'
    recipes = getdetails(url4, 1)
    recipelist = maprecipes(veg, recipes)
    return render_template('Vegetables.html', category=recipelist, title="Recipes")


def maprecipes(vegetables, recipes):
    recipelist = []
    vegi = vegetables.lower()
    for key, value in recipes.items():
        for i in range(len(value)):
            if vegi.find(value[i].strip()) != -1 or value[i].find(vegi.strip()) != -1:
                if key not in recipelist:
                    recipelist.append(key)

    return recipelist


def getdetails(url, flag):
    obj_json = urlopen(url)
    input_json = json.load(obj_json)
    if flag == 0:
        item_list = []
        for item in range(len(input_json['categories'])):
            item_list.append(input_json['categories'][item]['name'])
    else:
        item_list = dict()
        for item in range(len(input_json['results'])):
            item_list[input_json['results'][item]['title']] = (input_json['results'][item]['ingredients']).split(',')

    return item_list


def main():
    web_app.run()


if __name__ == '__main__':
    main()
