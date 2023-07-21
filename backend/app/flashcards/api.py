"""Flashcards API."""
from app.extensions import db
from flask import g, jsonify, request
from app.utils.types import JSON
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from .models import Flashcard, User
from .serializers import FlashcardSchema, UserSchema
from werkzeug.security import check_password_hash


from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity, create_access_token
)

jwt = JWTManager()

blueprint = Blueprint(
    "flashcards", "flashcards", url_prefix="/api/flashcards", description="Operations on flashcards"
)

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Your token has expired. Please log in again."}), 401

@jwt.invalid_token_loader
def my_invalid_token_callback(jwt_payload):
    return jsonify({"message": "Invalid token. Please log in again."}), 401

@jwt.unauthorized_loader
def my_missing_token_callback(jwt_header):
    return jsonify({"msg": "Missing authorization token"}), 401

@blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {'message': 'User with this username already exists.'}, 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return {'message': 'User with this email already exists.'}, 400

    new_user = User(username=username, email=email, password=password)

    db.session.add(new_user)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return {'message': 'Database error occurred.'}, 500

    return UserSchema().dump(new_user), 201

@blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return {"msg": "Missing username parameter"}, 400
    if not password:
        return {"msg": "Missing password parameter"}, 400

    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password_hash, password):
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=username)
    return {'access_token': access_token}, 200


# Bins 1-11 are associated with the following timespans
bin_timespans = {
    1: timedelta(seconds=5),
    2: timedelta(seconds=25),
    3: timedelta(minutes=2),
    4: timedelta(minutes=10),
    5: timedelta(hours=1),
    6: timedelta(hours=5),
    7: timedelta(days=1),
    8: timedelta(days=5),
    9: timedelta(days=25),
    10: timedelta(days=4*30),  # approx. 4 months
    11: timedelta.max  # Represents "Never"
}


@blueprint.route("/", methods=["GET"])
@jwt_required()
def flashcards_get():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    flashcards = Flashcard.query.filter_by(user_id=user.id)
    return jsonify(FlashcardSchema(many=True).dump(flashcards)), 200

@blueprint.route("/<int:id>", methods=["GET"])
@jwt_required()
def flashcard_get(id: int):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    flashcard = Flashcard.query.filter_by(id=id, user_id=user.id).first()
    if flashcard is None:
        abort(404, message="Flashcard not found.")
    return jsonify(FlashcardSchema().dump(flashcard)), 200

@blueprint.route("/", methods=["POST"])
@jwt_required()
@blueprint.arguments(FlashcardSchema())
@blueprint.response(201, FlashcardSchema())
def flashcard_create(flashcard_data: JSON):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    existing_flashcard = Flashcard.query.filter_by(word=flashcard_data['word'], user_id=user.id).first()
    if existing_flashcard:
        abort(400, message="Flashcard with this word already exists.")

    flashcard_data['user_id'] = user.id
    flashcard = Flashcard(**flashcard_data)
    db.session.add(flashcard)
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, message="Database error occurred.")
    
    return jsonify(FlashcardSchema().dump(flashcard)), 201

@blueprint.route("/<int:id>", methods=["PUT"])
@jwt_required()
@blueprint.arguments(FlashcardSchema())
@blueprint.response(200, FlashcardSchema())
def flashcard_update(flashcard_data: JSON, id: int):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    flashcard = Flashcard.query.get(id)
    if not flashcard or flashcard.user_id != user.id:
        abort(404, message="Flashcard not found.")

    existing_flashcard = Flashcard.query.filter_by(word=flashcard_data['word'], user_id=user.id).first()
    if existing_flashcard and existing_flashcard.id != id:
        abort(400, message="Another flashcard with this word already exists.")
    
    for attr, value in flashcard_data.items():
        if hasattr(flashcard, attr):
            setattr(flashcard, attr, value)

    try:    
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, message="Database error occurred.")
    
    return jsonify(FlashcardSchema().dump(flashcard)), 200

@blueprint.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@blueprint.response(204)
def flashcard_delete(id: int):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    flashcard = Flashcard.query.get(id)
    if not flashcard or flashcard.user_id != user.id:
        abort(404, message="Flashcard not found.")
    
    db.session.delete(flashcard)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, message="Database error occurred.")
    
    return 'Deleted successfully', 204

@blueprint.route("/review", methods=["GET"])
@jwt_required()
def flashcard_review():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    try:
        now = datetime.utcnow()

        # Words at bin 1 or higher that have reached 0 time or less
        flashcards_to_review = Flashcard.query.filter(
            Flashcard.bin > 0,
            Flashcard.next_review_time <= now,
            Flashcard.bin != -1,
            Flashcard.user_id == user.id
        ).order_by(Flashcard.bin.desc()).first()  # The higher bin first

        if flashcards_to_review:
            return jsonify(FlashcardSchema().dump(flashcards_to_review)), 200

        # If all words in bin 1 or higher have positive timers on them, start drawing new words from bin 0
        flashcards_to_review = Flashcard.query.filter(
            Flashcard.bin == 0,
            Flashcard.user_id == user.id
        ).first()

        if flashcards_to_review:
            return jsonify(FlashcardSchema().dump(flashcards_to_review)), 200

        # Check if there are any flashcards not in the "hard to remember" bin or the last bin
        remaining_flashcards = Flashcard.query.filter(
            Flashcard.bin != -1,
            Flashcard.bin != 11,
            Flashcard.user_id == user.id
        ).first()

        if remaining_flashcards:
            # If there are no words in bin 0 and all other words still have positive timers, inform the user
            return jsonify({"message": "You are temporarily done; please come back later to review more words."}), 200
        else:
            return jsonify({"message": "You have no more words to review; you are permanently done!"}), 200
    
    except Exception as e:
        # Catch any unexpected exceptions and return a 500 error
        return jsonify({"message": "Something went wrong.", "error": str(e)}), 500


@blueprint.route("/<int:id>/status/<string:status>", methods=["PUT"])
@jwt_required()
def flashcard_update_status(id: int, status: bool):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    flashcard = Flashcard.query.get(id)
    if not flashcard or flashcard.user_id != user.id:
        abort(404, message="Flashcard not found.")

    if status.lower() == 'true':  # status is True, i.e., answer is correct
        flashcard.bin = min(flashcard.bin + 1, 11)
    else:  # status is False, i.e., answer is incorrect
        flashcard.bin = max(1, flashcard.bin)
        flashcard.incorrect_count += 1

        # If a user has gotten a word wrong 10 times, move it to the "hard to remember" bin, which is -1
        if flashcard.incorrect_count >= 10:
            flashcard.bin = -1
            flashcard.next_review_time = None
            return jsonify({"status": "Flashcard updated successfully. It's now in the 'hard to remember' bin."}), 200

    # Update review time according to the new bin
    flashcard.next_review_time = datetime.utcnow() + bin_timespans.get(flashcard.bin, timedelta.max)

    db.session.commit()

    return jsonify({"status": "Flashcard updated successfully."}), 200
