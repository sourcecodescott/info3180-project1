from app import app
from api.profile_api import mod as prof_mod


app.register_blueprint(prof_mod, url_prefix='')

if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)
