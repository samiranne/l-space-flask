from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import User


class LoginForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])

    def validate(self):
        form_is_valid = super(LoginForm, self).validate()

        if not form_is_valid:
            return False

        user = User.get_user_by_email(self.email.data)

        if user is None:
            self.email.errors.append('Invalid email or password')
            return False

        if not user.check_password(self.password.data):
            self.email.errors.append('Invalid email or password')
            return False

        return True


class RegistrationForm(Form):
    display_name = StringField('Display Name', validators=[DataRequired()],
                               description='You can change this at any time.')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])

    def validate(self):
        form_is_valid = super(RegistrationForm, self).validate()

        if not form_is_valid:
            return False

        user = User.get_user_by_email(self.email.data)

        if user is not None:
            self.email.errors.append('This email is already registered.')
            return False

        return True


class UpdateUserAccountForm(Form):
    display_name = StringField('Display Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New Password',
                             validators=[DataRequired(), Length(min=8)])
    new_password_confirm = PasswordField('Confirm New Password',
                            validators=[DataRequired(), EqualTo('new_password')])

    def __init__(self, user, *args, **kwargs):
        super(UpdateUserAccountForm, self).__init__(*args, **kwargs)
        self.user = user

    def pre_populate(self):
        '''
        Pre-populates the form's display name and email with the user's display name and email.
        :return:
        '''
        self.display_name.data = self.user.display_name
        self.email.data = self.user.email


    def validate(self):
        form_is_valid = super(UpdateUserAccountForm, self).validate()
        if not form_is_valid:
            return False
        if not self.user.check_password(self.current_password.data):
            self.current_password.errors.append('Incorrect password.')
            return False

        return True