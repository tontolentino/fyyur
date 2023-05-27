#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
   __tablename__ = 'Show'

   id = db.Column(db.Integer, primary_key=True)
   venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
   artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
   start_time = db.Column(db.DateTime, nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  count_case = db.case(
      [(Show.start_time > datetime.now(), 1)],
      else_=0
  )

  areas = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
  data = []

  for area in areas:
      venues = Venue.query\
      .filter_by(city=area.city)\
      .filter_by(state=area.state)\
      .with_entities(Venue.city, Venue.state, Venue.id, Venue.name, db.func.sum(count_case))\
      .outerjoin(Show)\
      .group_by(Venue.city, Venue.state, Venue.id, Venue.name) \
      .order_by(Venue.city.desc(), Venue.id) \
      .all()
      
      venue_result = [
      {
          'id': row[2],
          'name': row[3],
          'num_upcoming_shows': row[4]
      }
      for row in venues
      ]

      area_result = {
      'city': area.city,
      'state': area.state,
      'venues': venue_result
      }

      data.append(area_result)

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  data = []

  for venue in venues:
     data.append(
        {
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': len(
            Show.query.filter(Show.venue_id == venue.id)\
              .filter(Show.start_time > datetime.now())\
              .all()
          )
        }
     )
  
  response = {
     'count': len(data),
     'data': data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = Venue.query.filter(Venue.id == venue_id).one()

  past_shows = Show.query.with_entities(Show.artist_id, Artist.name, Artist.image_link, Show.start_time)\
    .join(Artist)\
    .filter(Show.venue_id == venue_id)\
    .filter(Show.start_time < datetime.now())\
    .all()
  
  upcoming_shows = Show.query.with_entities(Show.artist_id, Artist.name, Artist.image_link, Show.start_time)\
    .join(Artist)\
    .filter(Show.venue_id == venue_id)\
    .filter(Show.start_time > datetime.now())\
    .all()

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [
      {
        "artist_id": row[0],
        "artist_name": row[1],
        "artist_image_link": row[2],
        "start_time": row[3].strftime("%m/%d/%Y, %H:%M:%S")
      }
      for row in past_shows
    ],
    "upcoming_shows": [
      {
        "artist_id": row[0],
        "artist_name": row[1],
        "artist_image_link": row[2],
        "start_time": row[3].strftime("%m/%d/%Y, %H:%M:%S")
      }
      for row in upcoming_shows
    ],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  try:
    venue = Venue(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      address = request.form['address'],
      phone = request.form['phone'],
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website = request.form['website_link'],
      seeking_talent = True if 'seeking_talent' in request.form else False,
      seeking_description = request.form['seeking_description'],
      genres = request.form.getlist('genres')
    )

    db.session.add(venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  try:
    Venue.query.filter_by(id == venue_id).delete()
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  
  finally:
    db.session.close()
     
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  artists = Artist.query.with_entities(Artist.id, Artist.name).order_by('name').all()

  data = [
    {
      'id': row[0],
      'name': row[1] 
    }
    for row in artists
  ]

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

  data = []

  for artist in artists:
    data.append(
      {
        'id': artist.id,
        'name': artist.name,
        'num_upcoming_shows': len(Show.query.filter(Show.artist_id == artist.id).all())
      }
    )

  response = {
    'count': len(data),
    'data': data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.filter(Artist.id == artist_id).one()

  past_shows = Show.query.with_entities(Show.venue_id, Venue.name, Venue.image_link, Show.start_time)\
    .join(Venue)\
    .filter(Show.artist_id == artist_id)\
    .filter(Show.start_time < datetime.now())\
    .all()
  
  upcoming_shows = Show.query.with_entities(Show.venue_id, Venue.name, Venue.image_link, Show.start_time)\
    .join(Venue)\
    .filter(Show.artist_id == artist_id)\
    .filter(Show.start_time > datetime.now())\
    .all()

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [
      {
        "venue_id": row[0],
        "venue_name": row[1],
        "venue_image_link": row[2],
        "start_time": row[3].strftime("%m/%d/%Y, %H:%M:%S")
      }
      for row in past_shows
    ],
    "upcoming_shows": [
      {
        "venue_id": row[0],
        "venue_name": row[1],
        "venue_image_link": row[2],
        "start_time": row[3].strftime("%m/%d/%Y, %H:%M:%S")
      }
      for row in upcoming_shows
    ],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  if artist:
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.website_link.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description


  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    artist = Artist.query.get(artist_id)
    
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website_link']
    artist.seeking_venue = True if 'seeking_venue' in request.form else False
    artist.seeking_description = request.form['seeking_description']

    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  
  except:
    db.session.rollback()
    flash('Artist ' + request.form['name'] + ' could not be updated!')
    
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  form = VenueForm()
  venue = Venue.query.get(venue_id)

  if venue:
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.image_link.data = venue.image_link
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.website_link.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  try:
    venue = Venue.query.get(venue_id)

    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website_link']
    venue.seeking_talent = True if 'seeking_talent' in request.form else False
    venue.seeking_description = request.form['seeking_description']
    venue.genres = request.form.getlist('genres')

    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  
  except:
    db.session.rollback()
    flash('Venue ' + request.form['name'] + ' could not be updated!')
    
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  try:
    artist = Artist(
      name = request.form['name'],
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      image_link = request.form['image_link'],
      facebook_link = request.form['facebook_link'],
      website = request.form['website_link'],
      seeking_venue = True if 'seeking_venue' in request.form else False,
      seeking_description = request.form['seeking_description']
    )

    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  
  shows_result = Show.query.join(Artist).join(Venue).order_by(Show.start_time).all()

  data = [
    {
      "venue_id": row.venue_id,
      "venue_name": row.venue.name,
      "artist_id": row.artist_id,
      "artist_name": row.artist.name,
      "artist_image_link": row.artist.image_link,
      "start_time": row.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    for row in shows_result
  ]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  try:
    show = Show(
      artist_id = request.form['artist_id'],
      venue_id = request.form['venue_id'],
      start_time = request.form['start_time']
    )

    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
