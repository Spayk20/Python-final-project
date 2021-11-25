from flask_login import current_user, login_user, login_required, logout_user
from flask_restx import Resource
from filmBook import api, db_core
from filmBook import resources


@api.route('/films')
class FilmRout(Resource):

    @api.marshal_with(resources.films_model, code=200, envelope='films', as_list=True)
    def get(self):
        message = resources.films_get_parser.parse_args()

        res = db_core.get_full_film_info(
                                         film_name=message['name'],
                                         page=message['page'],
                                         genre_list=[message['genre']],
                                         dir_list=[message['director']],
                                         rel_start=message['rel_start'],
                                         rel_fin=message['rel_fin'],
                                         order=message['order'])

        return res

    @api.marshal_with(resources.delete_films_model, code=200, envelope='films', as_list=True)
    @login_required
    def delete(self):
        del_films_parser = api.parser()
        del_films_parser.add_argument('film_id', type=int)
        message = del_films_parser.parse_args()
        id = current_user.id
        return db_core.delete_film(film_id=message['film_id'], user_id=id)


@api.route('/add_film')
class AddFilmRout(Resource):

    @api.marshal_with(resources.add_films_model, code=200, envelope='new_films', as_list=True)
    @login_required
    def post(self):
        message = resources.add_films_post_parser.parse_args()

        id = current_user.id
        res = db_core.add_new_film(
                                        imdb_id=message["imdb_id"],
                                        film_name=message["film_name"],
                                        rated=message["rated"],
                                        poster_url=message["poster_url"],
                                        release_date=message["release_date"],
                                        rating=message["rating"],
                                        user_added=id,
                                        genre=message["genre"],
                                        director=message["director"],
                                        description=message["description"],
        )

        return {"film_id": res}

    @api.marshal_with(resources.update_films_model, code=200, envelope='new_films', as_list=True)
    @login_required
    def update(self):
        message = resources.update_films_parser.parse_args()

        id = current_user.id
        res = db_core.update_film(
                                        imdb_id=message["imdb_id"],
                                        film_name=message["film_name"],
                                        rated=message["rated"],
                                        poster_url=message["poster_url"],
                                        release_date=message["release_date"],
                                        rating=message["rating"],
                                        user_added=id,
                                        genre=message["genre"],
                                        director=message["director"],
                                        description=message["description"],
                                )

        return {"film_id": res}


@api.route('/director')
class DelDirector(Resource):

    @api.marshal_with(resources.dir_name_model, code=200, envelope='director', as_list=True)
    @login_required
    def delete(self):
        id = current_user.id
        message = resources.dir_name_parser.parse_args()
        res = db_core.delete_directors(director_name=message['name'], user_id=id)

        return res


@api.route('/registration')
class UserRegistration(Resource):
    @api.marshal_with(resources.add_user_model, code=200, envelope='new_user', as_list=True)
    def post(self):

        message = resources.add_user_post_parser.parse_args()
        res = db_core.add_new_user(
                                    nickname=message['nickname'],
                                    email=message['email'],
                                    password=message['password'])

        return {"status": res}


@api.route('/login')
class UserLogin(Resource):

    @api.marshal_with(resources.login_user_model, code=200, envelope='login', as_list=True)
    def post(self):

        message = resources.login_user_post_parser.parse_args()

        res = db_core.get_user_auth(
                                    nickname=message['nickname'],
                                    password=message['password'])
        print(res)
        if res['message']['status']:
            login_user(res['user'])

        return res['message']


@api.route("/logout")
class UserLogout(Resource):

    @login_required
    @api.marshal_with(resources.logout_user_model, code=200, envelope="logout")
    def post(self):
        id = current_user.id
        logout_user()
        return {"id": int(id), "status": True}
