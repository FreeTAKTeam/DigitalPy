from typing import TYPE_CHECKING, List, Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

# import tables in initialization order
from filmology_app.components.FilmologyManagement.persistence.actor import Actor as DBActor
from filmology_app.components.FilmologyManagement.persistence.person import Person as DBPerson
from filmology_app.components.FilmologyManagement.persistence.entitybaseextended import EntityBaseExtended as DBEntityBaseExtended
from filmology_app.components.FilmologyManagement.persistence.entitybase import EntityBase as DBEntityBase
from filmology_app.components.FilmologyManagement.persistence.date import Date as DBDate
from filmology_app.components.FilmologyManagement.persistence.movie import Movie as DBMovie
from filmology_app.components.FilmologyManagement.persistence.poster import Poster as DBPoster
from filmology_app.components.FilmologyManagement.persistence.image import Image as DBImage
from filmology_app.components.FilmologyManagement.persistence.director import Director as DBDirector
from filmology_app.components.FilmologyManagement.persistence.genre import Genre as DBGenre
from filmology_app.components.FilmologyManagement.persistence.language import Language as DBLanguage
from filmology_app.components.FilmologyManagement.persistence.error import Error as DBError

# import domain model classes
from filmology_app.components.FilmologyManagement.domain.model.actor import Actor
from filmology_app.components.FilmologyManagement.domain.model.person import Person
from filmology_app.components.FilmologyManagement.domain.model.entitybaseextended import EntityBaseExtended
from filmology_app.components.FilmologyManagement.domain.model.entitybase import EntityBase
from filmology_app.components.FilmologyManagement.domain.model.date import Date
from filmology_app.components.FilmologyManagement.domain.model.movie import Movie
from filmology_app.components.FilmologyManagement.domain.model.poster import Poster
from filmology_app.components.FilmologyManagement.domain.model.image import Image
from filmology_app.components.FilmologyManagement.domain.model.director import Director
from filmology_app.components.FilmologyManagement.domain.model.genre import Genre
from filmology_app.components.FilmologyManagement.domain.model.language import Language
from filmology_app.components.FilmologyManagement.domain.model.error import Error

from digitalpy.core.main.controller import Controller
from filmology_app.components.FilmologyManagement.persistence.FilmologyManagement_base import FilmologyManagementBase
from filmology_app.components.FilmologyManagement.configuration.FilmologyManagement_constants import DB_PATH

if TYPE_CHECKING:
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.digipy_configuration.domain.model.configuration import Configuration
    from digitalpy.core.zmanager.action_mapper import ActionMapper


class FilmologyManagementPersistenceController(Controller):
    """this class is responsible for handling the persistence of the FilmologyManagement
    component. It is responsible for creating, removing and retrieving records.
    """

    def __init__(
        self,
        request: 'Request',
        response: 'Response',
        sync_action_mapper: 'ActionMapper',
        configuration: 'Configuration',
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.ses = self.create_db_session()

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        # use NullPool to prevent connections from remaning open, this allows
        # us to delete the component and it's database at runtime (component management)
        engine = create_engine(DB_PATH, poolclass=NullPool)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine, expire_on_commit=False)

        FilmologyManagementBase.metadata.create_all(engine)

        # create a Session
        return SessionClass

    # Begin methods for actor table


    def save_actor(self, actor: Actor, *args, **kwargs) -> 'DBActor':
        if not isinstance(actor, Actor):
            raise TypeError("'Actor' must be an instance of Actor")
        db_actor = DBActor()
        db_actor.oid = actor.oid
        db_actor.creator = actor.creator
        db_actor.nationality = actor.nationality
        db_actor.surname = actor.surname
        db_actor.created = actor.created
        db_actor.last_editor = actor.last_editor
        db_actor.name = actor.name
        db_actor.birth = actor.birth
        db_actor.description = actor.description
        db_actor.modified = actor.modified
        with self.ses.begin() as session:
            session.add(db_actor)
            session.commit()
            return db_actor


    def remove_actor(self, actor: Actor, *args, **kwargs):
        if not isinstance(actor, Actor):
            raise TypeError("'Actor' must be an instance of Actor")
        actor_db = self.get_actor(oid=actor.oid)[0]
        with self.ses.begin() as session:
            session.delete(actor_db)
            session.commit()

    def get_actor(self, creator:Union['str', None] = None, nationality:Union['str', None] = None, surname:Union['str', None] = None, created:Union['str', None] = None, Actor:Union['Actor', None] = None, last_editor:Union['str', None] = None, name:Union['str', None] = None, birth:Union['str', None] = None, description:Union['str', None] = None, modified:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBActor]:
        with self.ses.begin() as session:
            query = session.query(DBActor)

            if oid != None:
                query = query.filter(DBActor.oid == oid)
            if creator != None:
                query = query.filter(DBActor.creator == creator)
            if nationality != None:
                query = query.filter(DBActor.nationality == nationality)
            if surname != None:
                query = query.filter(DBActor.surname == surname)
            if created != None:
                query = query.filter(DBActor.created == created)
            if Actor != None:
                query = query.filter(DBActor.Actor == Actor)
            if last_editor != None:
                query = query.filter(DBActor.last_editor == last_editor)
            if name != None:
                query = query.filter(DBActor.name == name)
            if birth != None:
                query = query.filter(DBActor.birth == birth)
            if description != None:
                query = query.filter(DBActor.description == description)
            if modified != None:
                query = query.filter(DBActor.modified == modified)

            return query.all()



    def get_all_actor(self, *args, **kwargs) -> list[DBActor]:
        with self.ses.begin() as session:
            return session.query(DBActor).all()

    def update_actor(self, actor: Actor, *args, **kwargs):
        if not isinstance(actor, Actor):
            raise TypeError("'actor' must be an instance of Actor")

        actor_db = self.get_actor(oid = actor.oid)[0]
        actor_db.creator = actor.creator
        actor_db.nationality = actor.nationality
        actor_db.surname = actor.surname
        actor_db.created = actor.created
        actor_db.last_editor = actor.last_editor
        actor_db.name = actor.name
        actor_db.birth = actor.birth
        actor_db.description = actor.description
        actor_db.modified = actor.modified
        actor_db.Actor = []
        for Actor in actor.Actor:
            Actor_db = self.get_actor(oid=Actor)[0]
            actor_db.Actor.append(Actor_db)
        with self.ses.begin() as session:
            session.add(actor_db)
            session.commit()

    # Begin methods for actor table
    # Begin methods for person table


    def save_person(self, person: Person, *args, **kwargs) -> 'DBPerson':
        if not isinstance(person, Person):
            raise TypeError("'Person' must be an instance of Person")
        db_person = DBPerson()
        db_person.oid = person.oid
        db_person.creator = person.creator
        db_person.nationality = person.nationality
        db_person.surname = person.surname
        db_person.created = person.created
        db_person.last_editor = person.last_editor
        db_person.name = person.name
        db_person.birth = person.birth
        db_person.description = person.description
        db_person.modified = person.modified
        with self.ses.begin() as session:
            session.add(db_person)
            session.commit()
            return db_person


    def remove_person(self, person: Person, *args, **kwargs):
        if not isinstance(person, Person):
            raise TypeError("'Person' must be an instance of Person")
        person_db = self.get_person(oid=person.oid)[0]
        with self.ses.begin() as session:
            session.delete(person_db)
            session.commit()

    def get_person(self, creator:Union['str', None] = None, nationality:Union['str', None] = None, surname:Union['str', None] = None, created:Union['str', None] = None, last_editor:Union['str', None] = None, name:Union['str', None] = None, birth:Union['str', None] = None, description:Union['str', None] = None, modified:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBPerson]:
        with self.ses.begin() as session:
            query = session.query(DBPerson)

            if oid != None:
                query = query.filter(DBPerson.oid == oid)
            if creator != None:
                query = query.filter(DBPerson.creator == creator)
            if nationality != None:
                query = query.filter(DBPerson.nationality == nationality)
            if surname != None:
                query = query.filter(DBPerson.surname == surname)
            if created != None:
                query = query.filter(DBPerson.created == created)
            if last_editor != None:
                query = query.filter(DBPerson.last_editor == last_editor)
            if name != None:
                query = query.filter(DBPerson.name == name)
            if birth != None:
                query = query.filter(DBPerson.birth == birth)
            if description != None:
                query = query.filter(DBPerson.description == description)
            if modified != None:
                query = query.filter(DBPerson.modified == modified)

            return query.all()



    def get_all_person(self, *args, **kwargs) -> list[DBPerson]:
        with self.ses.begin() as session:
            return session.query(DBPerson).all()

    def update_person(self, person: Person, *args, **kwargs):
        if not isinstance(person, Person):
            raise TypeError("'person' must be an instance of Person")

        person_db = self.get_person(oid = person.oid)[0]
        person_db.creator = person.creator
        person_db.nationality = person.nationality
        person_db.surname = person.surname
        person_db.created = person.created
        person_db.last_editor = person.last_editor
        person_db.name = person.name
        person_db.birth = person.birth
        person_db.description = person.description
        person_db.modified = person.modified
        with self.ses.begin() as session:
            session.add(person_db)
            session.commit()

    # Begin methods for person table
    # Begin methods for entitybaseextended table


    def save_entitybaseextended(self, entitybaseextended: EntityBaseExtended, *args, **kwargs) -> 'DBEntityBaseExtended':
        if not isinstance(entitybaseextended, EntityBaseExtended):
            raise TypeError("'EntityBaseExtended' must be an instance of EntityBaseExtended")
        db_entitybaseextended = DBEntityBaseExtended()
        db_entitybaseextended.oid = entitybaseextended.oid
        db_entitybaseextended.creator = entitybaseextended.creator
        db_entitybaseextended.created = entitybaseextended.created
        db_entitybaseextended.last_editor = entitybaseextended.last_editor
        db_entitybaseextended.name = entitybaseextended.name
        db_entitybaseextended.description = entitybaseextended.description
        db_entitybaseextended.modified = entitybaseextended.modified
        with self.ses.begin() as session:
            session.add(db_entitybaseextended)
            session.commit()
            return db_entitybaseextended


    def remove_entitybaseextended(self, entitybaseextended: EntityBaseExtended, *args, **kwargs):
        if not isinstance(entitybaseextended, EntityBaseExtended):
            raise TypeError("'EntityBaseExtended' must be an instance of EntityBaseExtended")
        entitybaseextended_db = self.get_entitybaseextended(oid=entitybaseextended.oid)[0]
        with self.ses.begin() as session:
            session.delete(entitybaseextended_db)
            session.commit()

    def get_entitybaseextended(self, creator:Union['str', None] = None, created:Union['str', None] = None, last_editor:Union['str', None] = None, name:Union['str', None] = None, description:Union['str', None] = None, modified:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBEntityBaseExtended]:
        with self.ses.begin() as session:
            query = session.query(DBEntityBaseExtended)

            if oid != None:
                query = query.filter(DBEntityBaseExtended.oid == oid)
            if creator != None:
                query = query.filter(DBEntityBaseExtended.creator == creator)
            if created != None:
                query = query.filter(DBEntityBaseExtended.created == created)
            if last_editor != None:
                query = query.filter(DBEntityBaseExtended.last_editor == last_editor)
            if name != None:
                query = query.filter(DBEntityBaseExtended.name == name)
            if description != None:
                query = query.filter(DBEntityBaseExtended.description == description)
            if modified != None:
                query = query.filter(DBEntityBaseExtended.modified == modified)

            return query.all()



    def get_all_entitybaseextended(self, *args, **kwargs) -> list[DBEntityBaseExtended]:
        with self.ses.begin() as session:
            return session.query(DBEntityBaseExtended).all()

    def update_entitybaseextended(self, entitybaseextended: EntityBaseExtended, *args, **kwargs):
        if not isinstance(entitybaseextended, EntityBaseExtended):
            raise TypeError("'entitybaseextended' must be an instance of EntityBaseExtended")

        entitybaseextended_db = self.get_entitybaseextended(oid = entitybaseextended.oid)[0]
        entitybaseextended_db.creator = entitybaseextended.creator
        entitybaseextended_db.created = entitybaseextended.created
        entitybaseextended_db.last_editor = entitybaseextended.last_editor
        entitybaseextended_db.name = entitybaseextended.name
        entitybaseextended_db.description = entitybaseextended.description
        entitybaseextended_db.modified = entitybaseextended.modified
        with self.ses.begin() as session:
            session.add(entitybaseextended_db)
            session.commit()

    # Begin methods for entitybaseextended table
    # Begin methods for entitybase table


    def save_entitybase(self, entitybase: EntityBase, *args, **kwargs) -> 'DBEntityBase':
        if not isinstance(entitybase, EntityBase):
            raise TypeError("'EntityBase' must be an instance of EntityBase")
        db_entitybase = DBEntityBase()
        db_entitybase.oid = entitybase.oid
        db_entitybase.creator = entitybase.creator
        db_entitybase.created = entitybase.created
        db_entitybase.last_editor = entitybase.last_editor
        db_entitybase.name = entitybase.name
        db_entitybase.modified = entitybase.modified
        with self.ses.begin() as session:
            session.add(db_entitybase)
            session.commit()
            return db_entitybase


    def remove_entitybase(self, entitybase: EntityBase, *args, **kwargs):
        if not isinstance(entitybase, EntityBase):
            raise TypeError("'EntityBase' must be an instance of EntityBase")
        entitybase_db = self.get_entitybase(oid=entitybase.oid)[0]
        with self.ses.begin() as session:
            session.delete(entitybase_db)
            session.commit()

    def get_entitybase(self, creator:Union['str', None] = None, created:Union['str', None] = None, last_editor:Union['str', None] = None, name:Union['str', None] = None, modified:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBEntityBase]:
        with self.ses.begin() as session:
            query = session.query(DBEntityBase)

            if oid != None:
                query = query.filter(DBEntityBase.oid == oid)
            if creator != None:
                query = query.filter(DBEntityBase.creator == creator)
            if created != None:
                query = query.filter(DBEntityBase.created == created)
            if last_editor != None:
                query = query.filter(DBEntityBase.last_editor == last_editor)
            if name != None:
                query = query.filter(DBEntityBase.name == name)
            if modified != None:
                query = query.filter(DBEntityBase.modified == modified)

            return query.all()



    def get_all_entitybase(self, *args, **kwargs) -> list[DBEntityBase]:
        with self.ses.begin() as session:
            return session.query(DBEntityBase).all()

    def update_entitybase(self, entitybase: EntityBase, *args, **kwargs):
        if not isinstance(entitybase, EntityBase):
            raise TypeError("'entitybase' must be an instance of EntityBase")

        entitybase_db = self.get_entitybase(oid = entitybase.oid)[0]
        entitybase_db.creator = entitybase.creator
        entitybase_db.created = entitybase.created
        entitybase_db.last_editor = entitybase.last_editor
        entitybase_db.name = entitybase.name
        entitybase_db.modified = entitybase.modified
        with self.ses.begin() as session:
            session.add(entitybase_db)
            session.commit()

    # Begin methods for entitybase table
    # Begin methods for date table


    def save_date(self, date: Date, *args, **kwargs) -> 'DBDate':
        if not isinstance(date, Date):
            raise TypeError("'Date' must be an instance of Date")
        db_date = DBDate()
        db_date.oid = date.oid
        db_date.year = date.year
        db_date.name = date.name
        for DateAggregationMovie in date.DateAggregationMovie:
            db_DateAggregationMovie_list = self.get_movie(oid = DateAggregationMovie)
            if len(db_DateAggregationMovie_list)>0:
                db_DateAggregationMovie = db_DateAggregationMovie_list[0]
                db_date.DateAggregationMovie.append(db_DateAggregationMovie)
        with self.ses.begin() as session:
            session.add(db_date)
            session.commit()
            return db_date


    def remove_date(self, date: Date, *args, **kwargs):
        if not isinstance(date, Date):
            raise TypeError("'Date' must be an instance of Date")
        date_db = self.get_date(oid=date.oid)[0]
        with self.ses.begin() as session:
            session.delete(date_db)
            session.commit()

    def get_date(self, year:Union['str', None] = None, name:Union['str', None] = None, DateAggregationMovie:Union['Movie', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBDate]:
        with self.ses.begin() as session:
            query = session.query(DBDate)

            if oid != None:
                query = query.filter(DBDate.oid == oid)
            if year != None:
                query = query.filter(DBDate.year == year)
            if name != None:
                query = query.filter(DBDate.name == name)
            if DateAggregationMovie != None:
                query = query.filter(DBDate.DateAggregationMovie == DateAggregationMovie)

            return query.all()



    def get_all_date(self, *args, **kwargs) -> list[DBDate]:
        with self.ses.begin() as session:
            return session.query(DBDate).all()

    def update_date(self, date: Date, *args, **kwargs):
        if not isinstance(date, Date):
            raise TypeError("'date' must be an instance of Date")

        date_db = self.get_date(oid = date.oid)[0]
        date_db.year = date.year
        date_db.name = date.name
        date_db.DateAggregationMovie = []
        for DateAggregationMovie in date.DateAggregationMovie:
            DateAggregationMovie_db = self.get_dateaggregationmovie(oid=DateAggregationMovie)[0]
            date_db.DateAggregationMovie.append(DateAggregationMovie_db)
        with self.ses.begin() as session:
            session.add(date_db)
            session.commit()

    # Begin methods for date table
    # Begin methods for movie table


    def save_movie(self, movie: Movie, *args, **kwargs) -> 'DBMovie':
        if not isinstance(movie, Movie):
            raise TypeError("'Movie' must be an instance of Movie")
        db_movie = DBMovie()
        db_movie.oid = movie.oid
        db_movie.date = movie.date
        db_movie.country = movie.country
        db_movie.creator = movie.creator
        db_movie.color = movie.color
        db_movie.created = movie.created
        db_movie.last_editor = movie.last_editor
        db_movie.runtime = movie.runtime
        db_movie.description = movie.description
        db_movie.URL = movie.URL
        db_movie.plot = movie.plot
        db_movie.name = movie.name
        db_movie.alias = movie.alias
        db_movie.modified = movie.modified
        CompositionPosterPrimary = movie.CompositionPosterPrimary
        if CompositionPosterPrimary:
            db_CompositionPosterPrimary_list = self.get_poster(oid = CompositionPosterPrimary)
            if len(db_CompositionPosterPrimary_list)>0:
                db_movie.CompositionPosterPrimary = db_CompositionPosterPrimary_list[0]
                db_movie.CompositionPosterPrimary_oid = db_CompositionPosterPrimary_list[0].oid
        Date = movie.Date
        if Date:
            db_Date_list = self.get_date(oid = Date)
            if len(db_Date_list)>0:
                db_movie.Date = db_Date_list[0]
                db_movie.Date_oid = db_Date_list[0].oid
        with self.ses.begin() as session:
            session.add(db_movie)
            session.commit()
            return db_movie


    def remove_movie(self, movie: Movie, *args, **kwargs):
        if not isinstance(movie, Movie):
            raise TypeError("'Movie' must be an instance of Movie")
        movie_db = self.get_movie(oid=movie.oid)[0]
        with self.ses.begin() as session:
            session.delete(movie_db)
            session.commit()

    def get_movie(self, date:Union['str', None] = None, country:Union['str', None] = None, Movie:Union['Movie', None] = None, creator:Union['str', None] = None, color:Union['str', None] = None, created:Union['str', None] = None, last_editor:Union['str', None] = None, runtime:Union['str', None] = None, description:Union['str', None] = None, URL:Union['str', None] = None, CompositionPosterPrimary:Union['Poster', None] = None, Date:Union['Date', None] = None, plot:Union['str', None] = None, name:Union['str', None] = None, alias:Union['str', None] = None, modified:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBMovie]:
        with self.ses.begin() as session:
            query = session.query(DBMovie)

            if oid != None:
                query = query.filter(DBMovie.oid == oid)
            if date != None:
                query = query.filter(DBMovie.date == date)
            if country != None:
                query = query.filter(DBMovie.country == country)
            if Movie != None:
                query = query.filter(DBMovie.Movie == Movie)
            if creator != None:
                query = query.filter(DBMovie.creator == creator)
            if color != None:
                query = query.filter(DBMovie.color == color)
            if created != None:
                query = query.filter(DBMovie.created == created)
            if last_editor != None:
                query = query.filter(DBMovie.last_editor == last_editor)
            if runtime != None:
                query = query.filter(DBMovie.runtime == runtime)
            if description != None:
                query = query.filter(DBMovie.description == description)
            if URL != None:
                query = query.filter(DBMovie.URL == URL)
            if CompositionPosterPrimary != None:
                query = query.filter(DBMovie.CompositionPosterPrimary == CompositionPosterPrimary)
            if Date != None:
                query = query.filter(DBMovie.Date == Date)
            if plot != None:
                query = query.filter(DBMovie.plot == plot)
            if name != None:
                query = query.filter(DBMovie.name == name)
            if alias != None:
                query = query.filter(DBMovie.alias == alias)
            if modified != None:
                query = query.filter(DBMovie.modified == modified)

            return query.all()



    def get_all_movie(self, *args, **kwargs) -> list[DBMovie]:
        with self.ses.begin() as session:
            return session.query(DBMovie).all()

    def update_movie(self, movie: Movie, *args, **kwargs):
        if not isinstance(movie, Movie):
            raise TypeError("'movie' must be an instance of Movie")

        movie_db = self.get_movie(oid = movie.oid)[0]
        movie_db.date = movie.date
        movie_db.country = movie.country
        movie_db.creator = movie.creator
        movie_db.color = movie.color
        movie_db.created = movie.created
        movie_db.last_editor = movie.last_editor
        movie_db.runtime = movie.runtime
        movie_db.description = movie.description
        movie_db.URL = movie.URL
        movie_db.plot = movie.plot
        movie_db.name = movie.name
        movie_db.alias = movie.alias
        movie_db.modified = movie.modified
        movie_db.Movie = []
        for Movie in movie.Movie:
            Movie_db = self.get_movie(oid=Movie)[0]
            movie_db.Movie.append(Movie_db)
        movie_db.CompositionPosterPrimary_oid = movie.CompositionPosterPrimary
        movie_db.Date_oid = movie.Date
        with self.ses.begin() as session:
            session.add(movie_db)
            session.commit()

    # Begin methods for movie table
    # Begin methods for poster table


    def save_poster(self, poster: Poster, *args, **kwargs) -> 'DBPoster':
        if not isinstance(poster, Poster):
            raise TypeError("'Poster' must be an instance of Poster")
        db_poster = DBPoster()
        db_poster.oid = poster.oid
        db_poster.name = poster.name
        with self.ses.begin() as session:
            session.add(db_poster)
            session.commit()
            return db_poster


    def remove_poster(self, poster: Poster, *args, **kwargs):
        if not isinstance(poster, Poster):
            raise TypeError("'Poster' must be an instance of Poster")
        poster_db = self.get_poster(oid=poster.oid)[0]
        with self.ses.begin() as session:
            session.delete(poster_db)
            session.commit()

    def get_poster(self, name:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBPoster]:
        with self.ses.begin() as session:
            query = session.query(DBPoster)

            if oid != None:
                query = query.filter(DBPoster.oid == oid)
            if name != None:
                query = query.filter(DBPoster.name == name)

            return query.all()



    def get_all_poster(self, *args, **kwargs) -> list[DBPoster]:
        with self.ses.begin() as session:
            return session.query(DBPoster).all()

    def update_poster(self, poster: Poster, *args, **kwargs):
        if not isinstance(poster, Poster):
            raise TypeError("'poster' must be an instance of Poster")

        poster_db = self.get_poster(oid = poster.oid)[0]
        poster_db.name = poster.name
        with self.ses.begin() as session:
            session.add(poster_db)
            session.commit()

    # Begin methods for poster table
    # Begin methods for image table


    def save_image(self, image: Image, *args, **kwargs) -> 'DBImage':
        if not isinstance(image, Image):
            raise TypeError("'Image' must be an instance of Image")
        db_image = DBImage()
        db_image.oid = image.oid
        db_image.fileName = image.fileName
        db_image.name = image.name
        with self.ses.begin() as session:
            session.add(db_image)
            session.commit()
            return db_image


    def remove_image(self, image: Image, *args, **kwargs):
        if not isinstance(image, Image):
            raise TypeError("'Image' must be an instance of Image")
        image_db = self.get_image(oid=image.oid)[0]
        with self.ses.begin() as session:
            session.delete(image_db)
            session.commit()

    def get_image(self, fileName:Union['str', None] = None, name:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBImage]:
        with self.ses.begin() as session:
            query = session.query(DBImage)

            if oid != None:
                query = query.filter(DBImage.oid == oid)
            if fileName != None:
                query = query.filter(DBImage.fileName == fileName)
            if name != None:
                query = query.filter(DBImage.name == name)

            return query.all()



    def get_all_image(self, *args, **kwargs) -> list[DBImage]:
        with self.ses.begin() as session:
            return session.query(DBImage).all()

    def update_image(self, image: Image, *args, **kwargs):
        if not isinstance(image, Image):
            raise TypeError("'image' must be an instance of Image")

        image_db = self.get_image(oid = image.oid)[0]
        image_db.fileName = image.fileName
        image_db.name = image.name
        with self.ses.begin() as session:
            session.add(image_db)
            session.commit()

    # Begin methods for image table
    # Begin methods for director table


    def save_director(self, director: Director, *args, **kwargs) -> 'DBDirector':
        if not isinstance(director, Director):
            raise TypeError("'Director' must be an instance of Director")
        db_director = DBDirector()
        db_director.oid = director.oid
        db_director.creator = director.creator
        db_director.nationality = director.nationality
        db_director.surname = director.surname
        db_director.created = director.created
        db_director.last_editor = director.last_editor
        db_director.name = director.name
        db_director.birth = director.birth
        db_director.description = director.description
        db_director.modified = director.modified
        with self.ses.begin() as session:
            session.add(db_director)
            session.commit()
            return db_director


    def remove_director(self, director: Director, *args, **kwargs):
        if not isinstance(director, Director):
            raise TypeError("'Director' must be an instance of Director")
        director_db = self.get_director(oid=director.oid)[0]
        with self.ses.begin() as session:
            session.delete(director_db)
            session.commit()

    def get_director(self, creator:Union['str', None] = None, nationality:Union['str', None] = None, surname:Union['str', None] = None, created:Union['str', None] = None, last_editor:Union['str', None] = None, name:Union['str', None] = None, birth:Union['str', None] = None, description:Union['str', None] = None, modified:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBDirector]:
        with self.ses.begin() as session:
            query = session.query(DBDirector)

            if oid != None:
                query = query.filter(DBDirector.oid == oid)
            if creator != None:
                query = query.filter(DBDirector.creator == creator)
            if nationality != None:
                query = query.filter(DBDirector.nationality == nationality)
            if surname != None:
                query = query.filter(DBDirector.surname == surname)
            if created != None:
                query = query.filter(DBDirector.created == created)
            if last_editor != None:
                query = query.filter(DBDirector.last_editor == last_editor)
            if name != None:
                query = query.filter(DBDirector.name == name)
            if birth != None:
                query = query.filter(DBDirector.birth == birth)
            if description != None:
                query = query.filter(DBDirector.description == description)
            if modified != None:
                query = query.filter(DBDirector.modified == modified)

            return query.all()



    def get_all_director(self, *args, **kwargs) -> list[DBDirector]:
        with self.ses.begin() as session:
            return session.query(DBDirector).all()

    def update_director(self, director: Director, *args, **kwargs):
        if not isinstance(director, Director):
            raise TypeError("'director' must be an instance of Director")

        director_db = self.get_director(oid = director.oid)[0]
        director_db.creator = director.creator
        director_db.nationality = director.nationality
        director_db.surname = director.surname
        director_db.created = director.created
        director_db.last_editor = director.last_editor
        director_db.name = director.name
        director_db.birth = director.birth
        director_db.description = director.description
        director_db.modified = director.modified
        with self.ses.begin() as session:
            session.add(director_db)
            session.commit()

    # Begin methods for director table
    # Begin methods for genre table


    def save_genre(self, genre: Genre, *args, **kwargs) -> 'DBGenre':
        if not isinstance(genre, Genre):
            raise TypeError("'Genre' must be an instance of Genre")
        db_genre = DBGenre()
        db_genre.oid = genre.oid
        db_genre.name = genre.name
        with self.ses.begin() as session:
            session.add(db_genre)
            session.commit()
            return db_genre


    def remove_genre(self, genre: Genre, *args, **kwargs):
        if not isinstance(genre, Genre):
            raise TypeError("'Genre' must be an instance of Genre")
        genre_db = self.get_genre(oid=genre.oid)[0]
        with self.ses.begin() as session:
            session.delete(genre_db)
            session.commit()

    def get_genre(self, name:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBGenre]:
        with self.ses.begin() as session:
            query = session.query(DBGenre)

            if oid != None:
                query = query.filter(DBGenre.oid == oid)
            if name != None:
                query = query.filter(DBGenre.name == name)

            return query.all()



    def get_all_genre(self, *args, **kwargs) -> list[DBGenre]:
        with self.ses.begin() as session:
            return session.query(DBGenre).all()

    def update_genre(self, genre: Genre, *args, **kwargs):
        if not isinstance(genre, Genre):
            raise TypeError("'genre' must be an instance of Genre")

        genre_db = self.get_genre(oid = genre.oid)[0]
        genre_db.name = genre.name
        with self.ses.begin() as session:
            session.add(genre_db)
            session.commit()

    # Begin methods for genre table
    # Begin methods for language table


    def save_language(self, language: Language, *args, **kwargs) -> 'DBLanguage':
        if not isinstance(language, Language):
            raise TypeError("'Language' must be an instance of Language")
        db_language = DBLanguage()
        db_language.oid = language.oid
        db_language.creator = language.creator
        db_language.created = language.created
        db_language.last_editor = language.last_editor
        db_language.shortForm = language.shortForm
        db_language.name = language.name
        db_language.description = language.description
        db_language.modified = language.modified
        with self.ses.begin() as session:
            session.add(db_language)
            session.commit()
            return db_language


    def remove_language(self, language: Language, *args, **kwargs):
        if not isinstance(language, Language):
            raise TypeError("'Language' must be an instance of Language")
        language_db = self.get_language(oid=language.oid)[0]
        with self.ses.begin() as session:
            session.delete(language_db)
            session.commit()

    def get_language(self, creator:Union['str', None] = None, created:Union['str', None] = None, last_editor:Union['str', None] = None, shortForm:Union['str', None] = None, name:Union['str', None] = None, description:Union['str', None] = None, modified:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBLanguage]:
        with self.ses.begin() as session:
            query = session.query(DBLanguage)

            if oid != None:
                query = query.filter(DBLanguage.oid == oid)
            if creator != None:
                query = query.filter(DBLanguage.creator == creator)
            if created != None:
                query = query.filter(DBLanguage.created == created)
            if last_editor != None:
                query = query.filter(DBLanguage.last_editor == last_editor)
            if shortForm != None:
                query = query.filter(DBLanguage.shortForm == shortForm)
            if name != None:
                query = query.filter(DBLanguage.name == name)
            if description != None:
                query = query.filter(DBLanguage.description == description)
            if modified != None:
                query = query.filter(DBLanguage.modified == modified)

            return query.all()



    def get_all_language(self, *args, **kwargs) -> list[DBLanguage]:
        with self.ses.begin() as session:
            return session.query(DBLanguage).all()

    def update_language(self, language: Language, *args, **kwargs):
        if not isinstance(language, Language):
            raise TypeError("'language' must be an instance of Language")

        language_db = self.get_language(oid = language.oid)[0]
        language_db.creator = language.creator
        language_db.created = language.created
        language_db.last_editor = language.last_editor
        language_db.shortForm = language.shortForm
        language_db.name = language.name
        language_db.description = language.description
        language_db.modified = language.modified
        with self.ses.begin() as session:
            session.add(language_db)
            session.commit()

    # Begin methods for language table
    # Begin methods for error table


    def save_error(self, error: Error, *args, **kwargs) -> 'DBError':
        if not isinstance(error, Error):
            raise TypeError("'Error' must be an instance of Error")
        db_error = DBError()
        db_error.oid = error.oid
        db_error.name = error.name
        with self.ses.begin() as session:
            session.add(db_error)
            session.commit()
            return db_error


    def remove_error(self, error: Error, *args, **kwargs):
        if not isinstance(error, Error):
            raise TypeError("'Error' must be an instance of Error")
        error_db = self.get_error(oid=error.oid)[0]
        with self.ses.begin() as session:
            session.delete(error_db)
            session.commit()

    def get_error(self, name:Union['str', None] = None, oid: 'str' = None, *args, **kwargs) -> List[DBError]:
        with self.ses.begin() as session:
            query = session.query(DBError)

            if oid != None:
                query = query.filter(DBError.oid == oid)
            if name != None:
                query = query.filter(DBError.name == name)

            return query.all()



    def get_all_error(self, *args, **kwargs) -> list[DBError]:
        with self.ses.begin() as session:
            return session.query(DBError).all()

    def update_error(self, error: Error, *args, **kwargs):
        if not isinstance(error, Error):
            raise TypeError("'error' must be an instance of Error")

        error_db = self.get_error(oid = error.oid)[0]
        error_db.name = error.name
        with self.ses.begin() as session:
            session.add(error_db)
            session.commit()

    # Begin methods for error table

    def __getstate__(self) -> object:
        state: dict = super().__getstate__()  # type: ignore
        if "ses" in state:
            del state["ses"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.ses = self.create_db_session()
