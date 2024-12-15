from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from .forms import (ChestionarFinanciarForm, UserProfileForm, FinancialGoalForm,
                   PortfolioTransactionForm, SimulationForm)
from .services import (PortfolioService, GoalTrackingService, SimulationService,
                      MarketAnalysisService, calculate_risk_score, generate_recommendations)
from .models import User, Portfolio, FinancialGoal, FinancialProfile, RiskTolerance, PortfolioTransaction
from datetime import datetime, timedelta
import json
import os
from datetime import datetime
from pathlib import Path
bp = Blueprint('main', __name__)

def get_demo_user():
    current_time = datetime.now()
    three_months_ago = current_time - timedelta(days=90)
    
    demo_transactions = [
        PortfolioTransaction(
            id=1,
            portfolio_id=1,
            transaction_type='DEPOSIT',
            amount=25000.0,
            date=current_time - timedelta(days=60),
            description='Depunere inițială'
        ),
        PortfolioTransaction(
            id=2,
            portfolio_id=1,
            transaction_type='DEPOSIT',
            amount=5000.0,
            date=current_time - timedelta(days=30),
            description='Contribuție lunară'
        ),
        PortfolioTransaction(
            id=3,
            portfolio_id=1,
            transaction_type='REBALANCE',
            amount=0.0,
            date=current_time - timedelta(days=15),
            description='Rebalansare portofoliu'
        )
    ]
    
    demo_portfolio = Portfolio(
        id=1,
        user_id=1,
        total_value=100000.0,
        last_updated=current_time,
        asset_allocation={
            'Acțiuni': 60000.0,
            'Obligațiuni': 30000.0,
            'Numerar': 10000.0
        },
        historical_performance=[
            {'date': three_months_ago, 'value': 95000.0},
            {'date': three_months_ago + timedelta(days=30), 'value': 97500.0},
            {'date': current_time, 'value': 100000.0}
        ],
        transactions=demo_transactions
    )
    
    return User(
        id=1,
        email="demo@example.com",
        name="Demo User",
        created_at=current_time,
        portfolio=demo_portfolio
    )

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = ChestionarFinanciarForm()
    
    if form.validate_on_submit():
        profile = FinancialProfile(
            age=form.age.data,
            income=form.income.data,
            savings=form.savings.data,
            dependents=form.dependents.data,
            risk_tolerance=RiskTolerance(form.risk_tolerance.data),
            investment_goals=form.investment_goals.data,
            time_horizon=form.time_horizon.data
        )
        
        risk_assessment = calculate_risk_score(profile)
        recommendations = generate_recommendations(risk_assessment)
        
        session['risk_assessment'] = {
            'score': risk_assessment.score,
            'category': risk_assessment.category,
            'description': risk_assessment.description
        }
        
        session['recommendations'] = [
            {
                'asset_class': rec.asset_class,
                'allocation': rec.allocation,
                'description': rec.description
            }
            for rec in recommendations
        ]
        
        return redirect(url_for('main.results'))
    
    return render_template('questionnaire.html', form=form)

@bp.route('/results')
def results():
    if 'risk_assessment' not in session:
        return redirect(url_for('main.questionnaire'))
        
    return render_template('results.html',
                         risk_assessment=session['risk_assessment'],
                         recommendations=session['recommendations'])

@bp.route('/portfolio')
def portfolio():
    try:
        user = get_demo_user()
        portfolio_service = PortfolioService()
        market_service = MarketAnalysisService()
        
        portfolio_data = portfolio_service.calculate_portfolio_value(user.portfolio)
        returns = portfolio_service.calculate_returns(user.portfolio)
        market_data = market_service.get_market_data()
        
        return render_template('portfolio.html',
                             portfolio=user.portfolio,
                             portfolio_data=portfolio_data,
                             returns=returns,
                             market_data=market_data)
    except Exception as e:
        print(f"Error in portfolio route: {str(e)}")
        flash('A apărut o eroare la încărcarea portofoliului.', 'error')
        return redirect(url_for('main.index'))

def load_goals():
    """Încarcă obiectivele din fișierul JSON"""
    goals_file = Path('data/goals.json')
    if not goals_file.exists():
        return []
    
    try:
        with open(goals_file, 'r', encoding='utf-8') as f:
            goals_data = json.load(f)
            return [
                FinancialGoal(
                    id=g['id'],
                    user_id=g['user_id'],
                    name=g['name'],
                    target_amount=float(g['target_amount']),
                    current_amount=float(g['current_amount']),
                    target_date=datetime.strptime(g['target_date'], '%Y-%m-%d'),
                    category=g['category'],
                    status=g['status']
                )
                for g in goals_data
            ]
    except Exception as e:
        print(f"Eroare la încărcarea obiectivelor: {str(e)}")
        return []

def save_goals(goals):
    """Salvează obiectivele în fișierul JSON"""
    goals_file = Path('data/goals.json')
    
    goals_file.parent.mkdir(exist_ok=True)
    
    goals_data = [
        {
            'id': goal.id,
            'user_id': goal.user_id,
            'name': goal.name,
            'target_amount': goal.target_amount,
            'current_amount': goal.current_amount,
            'target_date': goal.target_date.strftime('%Y-%m-%d'),
            'category': goal.category,
            'status': goal.status
        }
        for goal in goals
    ]
    
    try:
        with open(goals_file, 'w', encoding='utf-8') as f:
            json.dump(goals_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Eroare la salvarea obiectivelor: {str(e)}")

def get_next_goal_id():
    """Generează următorul ID pentru un obiectiv nou"""
    goals = load_goals()
    if not goals:
        return 1
    return max(goal.id for goal in goals) + 1

@bp.route('/goals', methods=['GET', 'POST'])
def goals():
    user = get_demo_user()
    form = FinancialGoalForm()
    
    if form.validate_on_submit():
        # Încarcă obiectivele existente
        existing_goals = load_goals()
        
        # Creează noul obiectiv
        new_goal = FinancialGoal(
            id=get_next_goal_id(),
            user_id=user.id,
            name=form.name.data,
            target_amount=float(form.target_amount.data),
            current_amount=0.0,  # Suma inițială este 0
            target_date=form.target_date.data,
            category=form.category.data,
            status="IN_PROGRESS"
        )
        
        # Adaugă noul obiectiv la lista existentă
        existing_goals.append(new_goal)
        
        # Salvează toate obiectivele
        save_goals(existing_goals)
        
        flash('Obiectiv financiar adăugat cu succes!', 'success')
        return redirect(url_for('main.goals'))
    
    # Încarcă toate obiectivele pentru afișare
    all_goals = load_goals()
    
    # Calculează progresul pentru fiecare obiectiv
    goals_service = GoalTrackingService()
    goals_progress = {goal.id: goals_service.analyze_goal_progress(goal) 
                     for goal in all_goals}
    
    return render_template('goals.html',
                         form=form,
                         goals=all_goals,
                         progress=goals_progress)

# Optional: Adaugă o rută pentru ștergerea obiectivelor
@bp.route('/goals/delete/<int:goal_id>', methods=['POST'])
def delete_goal(goal_id):
    goals = load_goals()
    goals = [goal for goal in goals if goal.id != goal_id]
    save_goals(goals)
    flash('Obiectiv șters cu succes!', 'success')
    return redirect(url_for('main.goals'))

# Optional: Adaugă o rută pentru actualizarea obiectivelor
@bp.route('/goals/update_amount/<int:goal_id>', methods=['POST'])
def update_goal_amount(goal_id):
    try:
        # Obține noua sumă din formular
        new_amount = float(request.form.get('current_amount', 0))
        
        # Încarcă obiectivele
        goals = load_goals()
        
        # Găsește și actualizează obiectivul
        for goal in goals:
            if goal.id == goal_id:
                goal.current_amount = new_amount
                if new_amount >= goal.target_amount:
                    goal.status = "ACHIEVED"
                break
        
        # Salvează modificările
        save_goals(goals)
        
        flash('Suma actualizată cu succes!', 'success')
    except ValueError:
        flash('Sumă invalidă!', 'error')
    except Exception as e:
        flash('A apărut o eroare la actualizarea sumei!', 'error')
        print(f"Error updating goal amount: {str(e)}")
    
    return redirect(url_for('main.goals'))

@bp.route('/goals/add_contribution/<int:goal_id>', methods=['POST'])
def add_contribution(goal_id):
    try:
        contribution = float(request.form.get('contribution', 0))
        if contribution <= 0:
            flash('Suma trebuie să fie pozitivă!', 'error')
            return redirect(url_for('main.goals'))
        
        goals = load_goals()
        
        for goal in goals:
            if goal.id == goal_id:
                goal.current_amount += contribution
                if goal.current_amount >= goal.target_amount:
                    goal.status = "ACHIEVED"
                break
        
        save_goals(goals)
        flash(f'Contribuție de {contribution:,.2f} MDL adăugată cu succes!', 'success')
    except ValueError:
        flash('Sumă invalidă!', 'error')
    except Exception as e:
        flash('A apărut o eroare la adăugarea contribuției!', 'error')
        print(f"Error adding contribution: {str(e)}")
    
    return redirect(url_for('main.goals'))

@bp.route('/goals/subtract_amount/<int:goal_id>', methods=['POST'])
def subtract_amount(goal_id):
    try:
        amount = float(request.form.get('subtract_amount', 0))
        if amount <= 0:
            flash('Suma trebuie să fie pozitivă!', 'error')
            return redirect(url_for('main.goals'))
        
        goals = load_goals()
        
        for goal in goals:
            if goal.id == goal_id:
                if amount > goal.current_amount:
                    flash('Suma de scăzut nu poate fi mai mare decât suma curentă!', 'error')
                    return redirect(url_for('main.goals'))
                    
                goal.current_amount -= amount
                if goal.current_amount < goal.target_amount:
                    goal.status = "IN_PROGRESS"
                break
        
        save_goals(goals)
        flash(f'Suma de {amount:,.2f} MDL a fost scăzută cu succes!', 'success')
    except ValueError:
        flash('Sumă invalidă!', 'error')
    except Exception as e:
        flash('A apărut o eroare la scăderea sumei!', 'error')
        print(f"Error subtracting amount: {str(e)}")
    
    return redirect(url_for('main.goals'))

@bp.route('/simulate', methods=['GET', 'POST'])
def simulate():
    form = SimulationForm()
    
    if form.validate_on_submit():
        params = {
            'initial_amount': form.initial_amount.data,
            'monthly_contribution': form.monthly_contribution.data,
            'time_horizon': int(form.time_horizon.data),
            'risk_profile': form.risk_profile.data
        }
        
        simulation_service = SimulationService()
        results = simulation_service.simulate_portfolio(params)
        
        return render_template('simulation_results.html',
                             results=results,
                             params=params)
    
    return render_template('simulation.html', form=form)

@bp.route('/api/portfolio/update', methods=['POST'])
def update_portfolio():
    data = request.get_json()
    portfolio_service = PortfolioService()
    return jsonify({'status': 'success'})

@bp.route('/api/chart-data')
def chart_data():
    if 'recommendations' not in session:
        return jsonify([])
    
    return jsonify([
        {
            'label': rec['asset_class'],
            'value': rec['allocation']
        }
        for rec in session['recommendations']
    ])