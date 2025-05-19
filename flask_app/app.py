from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from utils.validations import validate_login_user, validate_register_user, validate_confession, validate_conf_img
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import uuid

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# --- Activity routes ---

@app.route("/", methods=["GET"])
def index():
    # get last activities
    PAGE_SIZE = 5
    data = []
    for act in db.get_activities(page_size=PAGE_SIZE):
        photo = None
        if len(db.get_activity_photos(act.id)) > 0:
            photo = db.get_activity_photos(act.id)[0]
        act_photo = photo.ruta_archivo if photo else "svg/anonymous.svg"
        comuna = db.get_comuna_by_id(act.comuna_id)
        data.append({
            "id": act.id,
            "name": act.nombre,
            "comuna": comuna.nombre,
            "init_date": act.dia_hora_inicio,
            "end_date": act.dia_hora_termino,
            "sector": act.sector,
            "email": act.email,
            "celular": act.celular,
            "description": act.descripcion,
            "photo": url_for('static', filename=act_photo)
        })
    return render_template("activities/front_page.html", data=data)

@app.route("/activity_list", methods=["GET"])
def activity_list():
    PAGE_SIZE = 5
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * PAGE_SIZE
    total_activities = db.count_activities()
    total_pages = (total_activities + PAGE_SIZE - 1) // PAGE_SIZE

    data = []
    for act in db.get_activities(page_size=PAGE_SIZE, offset=offset):
        comuna = db.get_comuna_by_id(act.comuna_id)
        data.append({
            "id": act.id,
            "nombre": act.nombre,
            "comuna": comuna.nombre,
            "init_date": act.dia_hora_inicio,
            "end_date": act.dia_hora_termino,
            "sector": act.sector,
            "email": act.email,
            "celular": act.celular,
            "description": act.descripcion,
            "total_fotos": db.count_photos_by_activity(act.id),
            "tema": db.get_theme_by_activity(act.id).tema if db.get_theme_by_activity(act.id) else None,
        })
    return render_template(
        "activities/activity_list.html",
        data=data,
        page=page,
        total_pages=total_pages
    )


@app.route("/inform_activity", methods=["GET"])
def inform_activity():
    regiones = db.get_regions()
    temas = db.temas
    contact_methods = db.contactos
    return render_template("activities/inform_activity.html", regiones=regiones, temas=temas, contact_methods=contact_methods)

@app.route('/get_comunas/<int:region_id>')
def get_comunas(region_id):
    comunas = db.get_comunas_by_region(region_id)
    comunas_dict = [{"id": c.id, "nombre": c.nombre} for c in comunas]
    return jsonify(comunas_dict)

@app.route("/activity/<int:activity_id>", methods=["GET"])
def activity(activity_id):
    # get activity
    act = db.get_activity_by_id(activity_id)
    if not act:
        return redirect(url_for("index"))

    # get photos
    photo_list = []
    for photo in db.get_activity_photos(act.id):
        act_img = f"uploads/{photo.filename}" if photo.filename else "svg/anonymous.svg"
        photo_list.append({
            "path_image": url_for('static', filename=act_img),
        })

    # get contact methods
    contact_methods = []
    for contact in db.get_activity_contact_methods(act.id):
        contact_methods.append({
            "contact_method": contact.contact_method,
            "contact_value": contact.contact_value
        })

    # get theme
    tema= db.get_theme_by_activity(act.id)

    return render_template("activities/activity_details.html", actividad=act, photos=photo_list, contact_methods=contact_methods, tema=tema)


@app.route("/post-activity", methods=["POST"])
def post_activity():
    # get data
    act_name = request.form.get("name")
    act_comuna = request.form.get("comuna")
    act_sector = request.form.get("sector")
    act_email = request.form.get("email")
    act_celular = request.form.get("celular")
    act_description = request.form.get("descripcion")
    act_init_date = request.form.get("inicio")
    act_end_date = request.form.get("termino")
    act_tema = request.form.get("tema")
    act_img = request.files.get("foto")

    _filename = hashlib.sha256(
        secure_filename(act_img.filename).encode("utf-8")
        ).hexdigest()
    _extension = filetype.guess(act_img).extension
    img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"

    # 2. save img as a file
    act_img.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

    db.create_contact_method(db.get_activity_id_by_name(act_name), act_celular, act_name)
    db.create_activity_theme(db.get_activity_id_by_name(act_name), act_tema)
    db.create_activity(act_comuna,
                       act_name,
                       act_init_date,
                       act_end_date,
                       act_sector,
                       act_email,
                       act_celular,
                       act_description)
    db.create_photo(
        db.get_activity_id_by_name(act_name),
        img_filename,
        img_filename
    )

    return redirect(url_for("index"))


@app.route("/stats", methods=["GET"])
def stats():
    return render_template("activities/stats.html")

if __name__ == "__main__":
    app.run(debug=True)
