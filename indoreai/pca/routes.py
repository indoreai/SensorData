"""
Created on Feb 06th, 2020

@author: rajesh
"""

import csv
import os
import re
import pathlib
import os
from io import TextIOWrapper
from flask.blueprints import Blueprint
from flask.globals import request, current_app
from flask.helpers import url_for, flash, send_from_directory
from flask.templating import render_template
from werkzeug.utils import redirect

from indoreai import db
from flask_login import current_user, login_required
from indoreai.pca.forms import UploadForm, Update_dashboard
from indoreai.pca.models import Samples, Samples_meta, Samples_userdevices
from indoreai.services.sampleservice import sample_mata_get_data_first_service
from datetime import datetime

pca = Blueprint('pca', __name__)


@login_required
@pca.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    """ User deshboard upload csv file input field device name(string) and sample set(string)
     """
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = UploadForm()
    if form.validate_on_submit():

        csv_file = request.files['file']
        file_ext = csv_file.filename
        file_ext = pathlib.Path(file_ext).suffix

        if file_ext == ".txt":
            # Read text file
            csv_file.save(os.path.join(csv_file.filename))
            with open(csv_file.filename, 'r') as filehandle:
                is_record = False
                records = []
                for line in filehandle:
                    if "Columns" in line:
                        is_record = True
                        continue
                    if is_record:
                        records.append(line.split("\t")[1:17])

            csv_reader = records

            # remove txt file
            try:
                os.remove(csv_file.filename)
            except:
                pass

        else:
            # Read csv file 
            csv_file = TextIOWrapper(csv_file, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')

        #  common code for csv and text file to save databse

        is_header = True
        flage = True
        samples_list = []
        user_id = current_user.id
        s3_path = ''
        count = 0

        for row in csv_reader:
            if is_header:
                header = row
                head_list_alfanume = [re.sub(r'\W+', '', heading) for heading in header]
                is_header = False
            else:
                if flage:
                    record = row
                    sample_dict = {key: val for key, val in zip(head_list_alfanume, record)}
                    sample_one_record = sample_dict
                    sample = Samples(**sample_one_record)
                    # Insert one row
                    db.session.add(sample)
                    db.session.commit()
                    # get last insert id
                    db.session.refresh(sample)
                    start_sample_id = sample.id
                    count = count + 1
                    flage = False
                else:
                    record = row
                    sample_dict = {key: val for key, val in zip(head_list_alfanume, record)}
                    sample = Samples(**sample_dict)
                    samples_list.append(sample)
                    count = count + 1
        # Insert multiple row
        db.session.add_all(samples_list)
        db.session.commit()
        # get last insert id
        db.session.refresh(sample)
        end_sample_id = sample.id
        # insert data in sample meta table
        # datetime_str = form.sample_date.data
        datetime_str = request.form.get('sample_date')
        # print(datetime_str)
        # datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        # print(datetime_object)  # printed in default format
        filename = None
        if form.support_file.data:
            file = request.files['support_file']
            path = os.path.join(current_app.root_path, 'additional_docs')
            isdir = os.path.isdir(path)
            if not isdir:
                os.mkdir(path)
            file.save(os.path.join(current_app.root_path, 'additional_docs', form.support_file.data.filename))
            filename = form.support_file.data.filename

        samples_meta_data = {"user_id": user_id, "device_name": form.device_name.data,
                             "sample_set_id": form.sample_set_id.data, "name": form.name.data,
                             "sample_date": datetime_str,  "start_sample_id": start_sample_id,
                              "end_sample_id": end_sample_id,
                             "filename": form.file.data.filename,  "no_of_record": count
                             }

        sample_meta = Samples_meta(**samples_meta_data)
        db.session.add(sample_meta)
        db.session.commit()
        check_data_exist = Samples_userdevices.query.filter_by(user_id=user_id, device_name=form.device_name.data) \
            .first()
        if not check_data_exist:
            # insert data in sample userdevices table
            samples_user_devices_data = {"user_id": user_id, "device_name": form.device_name.data}
            samples_user_devices = Samples_userdevices(**samples_user_devices_data)
            db.session.add(samples_user_devices)
            db.session.commit()
        return redirect(url_for('pca.dashboard'))
    # pagination code ........
    page = request.args.get('page', 1, type=int)
    samples_meta_data = Samples_meta.query.filter_by(user_id=current_user.id) \
        .order_by(Samples_meta.date_created.desc()).paginate(page=page, per_page=5)
    return render_template('dashboard.html', form=form, samples_meta_data=samples_meta_data)


@login_required
@pca.route("/sample-graph")
def sample_graph():
    """ sample graph  draw first dropdown
        value get using current user
    """
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user_id = current_user.id
    samples_user_devices = Samples_userdevices.query.filter_by(user_id=user_id).all()
    return render_template('sample_graph.html', title='Sample Graph', samples_user_devices=samples_user_devices,
                           user_id=user_id)


@login_required
@pca.route("/pca-graph", methods=['GET', 'POST'])
def pca_graph():
    """ Pca graph  draw first dropdown
            value get using current user
    """
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user_id = current_user.id
    samples_user_devices = Samples_userdevices.query.filter_by(user_id=user_id).all()
    return render_template('pca_graph.html', title='PCA Graph', samples_user_devices=samples_user_devices,
                           user_id=user_id)


@pca.route("/edit_sample/<int:meta_id>", methods=['GET', 'POST'])
@login_required
def edit_sample(meta_id):
    sample_meta_data = sample_mata_get_data_first_service(id=meta_id)
    # print(sample_meta_data)
    form = Update_dashboard()
    if form.validate_on_submit():
        datetime_str = request.form.get('sample_date')
        sample_meta_data = Samples_meta.query.filter_by(id=meta_id).first()
        sample_meta_data.name = form.name.data
        sample_meta_data.type = form.type.data
        sample_meta_data.sample_date = datetime_str
        sample_meta_data.address = form.address.data
        sample_meta_data.notes = form.notes.data

        if form.file.data:
            sample_meta_data.additional_docs = form.file.data.filename
            file = request.files['file']
            path = os.path.join(current_app.root_path, 'additional_docs')
            isdir = os.path.isdir(path)
            if not isdir:
                os.mkdir(path)
            file.save(os.path.join(current_app.root_path, 'additional_docs', form.file.data.filename))

        db.session.commit()

        flash('Your sample has been updated!', 'success')
        return redirect(url_for('pca.dashboard'))
    elif request.method == 'GET':
        form.device_name.data = sample_meta_data.get('device_name')
        form.sample_set_id.data = sample_meta_data.get('sample_set_id')
        form.name.data = sample_meta_data.get('name')
        form.type.data = sample_meta_data.get('type')
        sample_date = sample_meta_data.get('sample_date')
        form.address.data = sample_meta_data.get('address')
        form.notes.data = sample_meta_data.get('notes')
        download_docs = sample_meta_data.get('additional_docs')
    return render_template('update_dashboard.html', form=form, sample_date=sample_date, download_docs=download_docs,
                           no_of_record=sample_meta_data.get('no_of_record'))


@pca.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(current_app.root_path, 'additional_docs/')
    return send_from_directory(path, filename, as_attachment=True)


@pca.route('/about')
def about():
     return render_template('about.html')
