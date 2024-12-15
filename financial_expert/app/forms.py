# forms.py
from flask_wtf import FlaskForm
from wtforms import (StringField, FloatField, IntegerField, SelectField, 
                    DateField, SelectMultipleField, SubmitField, DecimalField)
from wtforms.validators import DataRequired, NumberRange, Email, Optional

class ChestionarFinanciarForm(FlaskForm):
    age = IntegerField('Vârstă', 
        validators=[DataRequired(), NumberRange(min=18, max=120)],
        render_kw={"class": "form-control"})
    
    income = FloatField('Venit anual (MDL)', 
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"class": "form-control"})
    
    savings = FloatField('Economii curente (MDL)', 
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"class": "form-control"})
    
    dependents = IntegerField('Număr persoane în întreținere',
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"class": "form-control"})
    
    risk_tolerance = SelectField('Toleranță la risc',
        choices=[
            ('low', 'Conservator'),
            ('medium', 'Moderat'),
            ('high', 'Agresiv')
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-select"})
    
    investment_goals = SelectMultipleField('Obiective investiționale',
        choices=[
            ('RETIREMENT', 'Pensie'),
            ('EDUCATION', 'Educație'),
            ('HOUSE', 'Achiziție locuință'),
            ('WEALTH', 'Creșterea averii')
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-select", "multiple": True})
    
    time_horizon = IntegerField('Orizont de timp investițional (ani)',
        validators=[DataRequired(), NumberRange(min=1)],
        render_kw={"class": "form-control"})
    
    submit = SubmitField('Obține recomandări',
        render_kw={"class": "btn btn-primary"})

class UserProfileForm(FlaskForm):
    name = StringField('Nume', 
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    
    email = StringField('Email', 
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"})
    
    submit = SubmitField('Salvează Profil',
        render_kw={"class": "btn btn-primary"})

class FinancialGoalForm(FlaskForm):
    name = StringField('Denumire Obiectiv', 
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    
    target_amount = DecimalField('Suma Țintă (MDL)', 
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"class": "form-control"})
    
    target_date = DateField('Data Țintă', 
        validators=[DataRequired()],
        render_kw={"class": "form-control", "type": "date"})
    
    category = SelectField('Categoria',
        choices=[
            ('EMERGENCY', 'Fond de urgență'),
            ('RETIREMENT', 'Pensie'),
            ('HOUSE', 'Achiziție locuință'),
            ('EDUCATION', 'Educație'),
            ('OTHER', 'Altele')
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-select"})
    
    submit = SubmitField('Adaugă Obiectiv',
        render_kw={"class": "btn btn-primary"})

class PortfolioTransactionForm(FlaskForm):
    transaction_type = SelectField('Tip Tranzacție',
        choices=[
            ('DEPOSIT', 'Depunere'),
            ('WITHDRAWAL', 'Retragere'),
            ('REBALANCE', 'Rebalansare')
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-select"})
    
    amount = DecimalField('Suma (MDL)', 
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"class": "form-control"})
    
    description = StringField('Descriere', 
        validators=[Optional()],
        render_kw={"class": "form-control"})
    
    submit = SubmitField('Înregistrează Tranzacția',
        render_kw={"class": "btn btn-primary"})

class SimulationForm(FlaskForm):
    initial_amount = DecimalField('Suma Inițială (MDL)', 
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"class": "form-control"})
    
    monthly_contribution = DecimalField('Contribuție Lunară (MDL)', 
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"class": "form-control"})
    
    time_horizon = SelectField('Perioada (ani)',
        choices=[(str(i), str(i)) for i in range(1, 41)],
        validators=[DataRequired()],
        render_kw={"class": "form-select"})
    
    risk_profile = SelectField('Profil de Risc',
        choices=[
            ('CONSERVATIVE', 'Conservator'),
            ('MODERATE', 'Moderat'),
            ('AGGRESSIVE', 'Agresiv')
        ],
        validators=[DataRequired()],
        render_kw={"class": "form-select"})
    
    submit = SubmitField('Simulează',
        render_kw={"class": "btn btn-primary"})