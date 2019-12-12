import os
import random
import uuid

from flask import render_template, url_for, redirect, session, abort
from flask_login import login_required

from app import db
from app.models import User, Vote
from . import home
from .rating import update_ratings

@home.route('/')
@home.route('/index')
@login_required
def index():
    users = User.query.all()
    userA, userB = random.sample(users, k=2)
    vote_key = uuid.uuid4().hex
    session['vote_key'] = vote_key
    return render_template('home/index.html', title='Głosuj', userA=userA, userB=userB, vote_key=vote_key)

@home.route('/ranking')
@login_required
def ranking():
    users = User.query.all()
    users = sorted(users, key=lambda x: x.rating, reverse=True)
    return render_template('home/ranking.html', title='Ranking', users=list(enumerate(users)))

@home.route('/vote/<winner_id>/<loser_id>/<vote_key>')
@login_required
def vote(winner_id, loser_id, vote_key):
    if vote_key == session.get('vote_key'):
        v = Vote(winner_id=winner_id, loser_id=loser_id)
        db.session.add(v)
        winner = User.query.filter_by(id=winner_id).first()
        loser = User.query.filter_by(id=loser_id).first()
        winner.rating, loser.rating = update_ratings(winner.rating, loser.rating)

        db.session.commit()
    return redirect('/')
