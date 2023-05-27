from app import db, Venue, Artist, Show, app
from datetime import datetime

app.app_context().push()

venue1 = Venue(
    name="The Musical Hop",
    city="San Francisco",
    state="CA",
    address="1015 Folsom Street",
    phone="123-123-1234",
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    facebook_link="https://www.facebook.com/TheMusicalHop",
    website="https://www.themusicalhop.com",
    seeking_talent=True,
    seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
    genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"]
)

venue2 = Venue(
    name="The Dueling Pianos Bar",
    city="New York",
    state="NY",
    address="335 Delancey Street",
    phone="914-003-1132",
    image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    facebook_link="https://www.facebook.com/theduelingpianos",
    website="https://www.theduelingpianos.com",
    seeking_talent=False,
    seeking_description=None,
    genres=["Classical", "R&B", "Hip-Hop"]
)

venue3 = Venue(
    name="Park Square Live Music & Coffee",
    city="San Francisco",
    state="CA",
    address="34 Whiskey Moore Ave",
    phone="415-000-1234",
    image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    website="https://www.parksquarelivemusicandcoffee.com",
    seeking_talent=False,
    seeking_description=None,
    genres=["Rock n Roll", "Jazz", "Classical", "Folk"]
)

artist4 = Artist(
    name="Guns N Petals",
    city="San Francisco",
    state="CA",
    phone="326-123-5000",
    genres=["Rock n Roll"],
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    facebook_link="https://www.facebook.com/GunsNPetals",
    website="https://www.gunsnpetalsband.com",
    seeking_venue=True,
    seeking_description="Looking for shows to perform at in the San Francisco Bay Area!"
)

artist5 = Artist(
    name="Matt Quevedo",
    city="New York",
    state="NY",
    phone="300-400-5000",
    genres=["Jazz"],
    image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    facebook_link="https://www.facebook.com/mattquevedo923251523",
    website=None,
    seeking_venue=False,
    seeking_description=None
)

artist6 = Artist(
    name="The Wild Sax Band",
    city="San Francisco",
    state="CA",
    phone="432-325-5432",
    genres=["Jazz", "Classical"],
    image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    facebook_link=None,
    website=None,
    seeking_venue=False,
    seeking_description=None
)

show1 = Show(
    start_time=datetime(2019, 5, 21, 21, 30, 0)
)
show1.venue = venue1
show1.artist = artist4

show2 = Show(
    start_time=datetime(2019, 6, 15, 23, 0, 0)
)
show2.venue = venue3
show2.artist = artist5

show3 = Show(
    start_time=datetime(2035, 4, 1, 20, 0, 0)
)
show3.venue = venue3
show3.artist = artist6

show4 = Show(
    start_time=datetime(2035, 4, 8, 20, 0, 0)
)
show4.venue = venue3
show4.artist = artist6

show5 = Show(
    start_time=datetime(2035, 4, 15, 20, 0, 0)
)
show5.venue = venue3
show5.artist = artist6

db.session.add(show1)
db.session.add(venue2) # Because there's no show in this Venue
db.session.add(show2)
db.session.add(show3)
db.session.add(show4)
db.session.add(show5)

db.session.commit()
