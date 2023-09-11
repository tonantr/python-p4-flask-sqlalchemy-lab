#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

NOT_FOUND_ERROR_MESSAGE = "<h1>404 Not Found</h1>"


@app.route("/")
def home():
    return "<h1>Zoo app</h1>"


@app.route("/animal/<int:id>")
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    if not animal:
        response_body = f"{NOT_FOUND_ERROR_MESSAGE}"
        response = make_response(response_body, 404)
        return response

    response_body = f"""
    <pre>
    <ul>Name: {animal.name}</ul>
    <ul>Species: {animal.species}</ul>
    <ul>Zookeeper: {animal.zookeeper.name}</ul>
    <ul>Enclosure: {animal.enclosure.environment}</ul>
    </pre>
    """
    response = make_response(response_body, 200)
    return response


@app.route("/zookeeper/<int:id>")
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zookeeper:
        response_body = f"{NOT_FOUND_ERROR_MESSAGE}"
        response = make_response(response_body, 404)
        return response

    animal_list = "\n\n".join([f"Animal: {animal.name}" for animal in zookeeper.animals])
    response_body = f"""
    <pre>
    <ul>Name: {zookeeper.name}</ul>
    <ul>Birthday: {zookeeper.birthday}</ul>
    <ul>{animal_list}</ul>
    </pre>
    """
    response = make_response(response_body)
    return response


@app.route("/enclosure/<int:id>")
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    if not enclosure:
        response_body = f'{NOT_FOUND_ERROR_MESSAGE}'
        response = make_response(response_body)
        return response
    
    animal_list = '\n\n'.join([f'Animal: {animal.name}' for animal in enclosure.animals])
    response_body = f"""
    <pre>
    <ul>ID: {enclosure.id}</ul>
    <ul>Environment: {enclosure.environment}</ul>
    <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
    <ul>{animal_list}</ul>
    </pre>
    """

    response = make_response(response_body)
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
