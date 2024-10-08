#Criando as rotas do site
from flask import render_template, url_for, redirect, request, flash
from usuarios import app, database, bcrypt
from usuarios.models import Usuario, Agendamento
from flask_login import login_required, login_user, logout_user, current_user
from usuarios.forms import FormLogin, FormCriarConta
from flask import Flask, render_template, Response
import cv2


@app.route("/", methods=["GET", "POST"])
def index():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("agendar", usuario=usuario.username))
    return render_template("index.html", form=formlogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data,
                          email=formcriarconta.email.data,
                          senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("agendar", usuario=usuario.username))
    return render_template("criarconta.html", form=formcriarconta)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))



@app.route('/ver_agendamento/')
@login_required
def agendamentos():
    agendamentos = Agendamento.query.all()
    return render_template('ver_agendamento.html', agendamentos=agendamentos)


from flask_login import current_user

@app.route('/agendar/', methods=['GET', 'POST'])
@login_required
def agendar():
    if request.method == 'POST':
        name = current_user.username  # Obtém o nome do usuário logado
        date = request.form['date']
        time = request.form['time']

        # Converter o horário para minutos
        hours, minutes = map(int, time.split(':'))
        total_minutes = hours * 60 + minutes

        # Verificar se o horário é múltiplo de 30
        if total_minutes % 30 != 0:
            flash('O horário deve ser em intervalos de 30 minutos.', 'danger')
        else:
            # Verificar se já existe um agendamento na mesma data e horário
            agendamento_existente = Agendamento.query.filter_by(date=date, time=time).first()

            if agendamento_existente:
                # Se já existir, mostrar alerta de conflito
                flash('Data com horário já agendado', 'danger')
            else:
                # Se não existir, criar novo agendamento
                novo_agendamento = Agendamento(name=name, date=date, time=time)
                database.session.add(novo_agendamento)
                database.session.commit()
                flash('Agendamento efetuado com sucesso', 'success')

        return redirect(url_for('agendar'))

    return render_template('agendar.html')

if __name__ == '__main__':
    database.create_all()
    app.run(debug=True)
