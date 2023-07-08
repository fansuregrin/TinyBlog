from flask import render_template, redirect, jsonify, request, url_for

from utils.utils import is_installed, write_db_config, write_amdin_config
from . import install


@install.route('/')
def index():
    return redirect(url_for('install.install'))

@install.route('/notice')
def notice():
    if not is_installed():
        return redirect(url_for('install.install'))
    return render_template('install/notice.html')

@install.route('/install', methods=['GET', 'POST'])
def install():
    if is_installed():
        return redirect(url_for('install.notice'))
    if request.is_json:
        req_data = request.get_json()
        request_type = req_data['request_type']
        if request_type == 'refresh_step_page':
            current_step = int(req_data['current_step'])
            if current_step == 1:
                html = render_template('install/install_step_2.html')
                response = {
                    'status': True,
                    'html': html,
                }
            elif current_step == 2:
                try:
                    db_config = req_data['db_config']
                    write_db_config(db_config)
                    html = render_template('install/install_step_3.html')
                    response = {
                        'status': True,
                        'html': html,
                    }
                except Exception as e:
                    response = {
                        'status': False,
                        'html': render_template('install/db_alert.html')
                    }
            elif current_step == 3:
                try:
                    admin_config = write_amdin_config(req_data['admin_config'])
                    html = render_template('install/install_step_4.html', admin_config=admin_config)
                    response = {
                        'status': True,
                        'html': html,
                    }
                except ValueError as err:
                    err_msg = err.args[0]
                    response = {
                        'status': False,
                        'html': render_template('install/admin_alert.html', additional_error=err_msg)
                    }
            else:
                response = {'status': False}
            return jsonify(response)
        elif request_type == 'refresh_db_config_form':
            db_type = req_data['db_type']
            if db_type == 'sqlite3':
                html = render_template('install/sqlite3.html')
            elif db_type == 'mysql':
                html = render_template('install/mysql.html')
            else:
                return jsonify({'status': False})
            return jsonify({
                'status': True,
                'html': html
            })
    return render_template('install/install.html')