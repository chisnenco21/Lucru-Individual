from typing import List, Dict
from decimal import Decimal
from datetime import datetime
from .models import (FinancialProfile, RiskAssessment, InvestmentRecommendation,
                     Portfolio, FinancialGoal, MarketData, RiskTolerance)

def calculate_risk_score(profile: FinancialProfile) -> RiskAssessment:
    """Calculează scorul de risc bazat pe profilul financiar."""
    score = 0.0

    # Calcul simplificat pentru scorul de risc
    score += max(0, (60 - profile.age)) / 2
    score += (profile.income / 50000) * 10
    score -= profile.dependents * 5
    score += profile.time_horizon * 2

    risk_scores = {
        RiskTolerance.LOW: 5,
        RiskTolerance.MEDIUM: 15,
        RiskTolerance.HIGH: 25
    }
    score += risk_scores[profile.risk_tolerance]

    score = min(100, max(0, score))

    if score < 33:
        category = 'Conservator'
        description = 'Accent pe securitatea capitalului cu randamente stabile, dar mai mici.'
    elif score < 66:
        category = 'Moderat'
        description = 'Echilibru între creștere și stabilitate, cu riscuri moderate.'
    else:
        category = 'Agresiv'
        description = 'Potențial de creștere ridicat, dar cu volatilitate mai mare.'

    return RiskAssessment(score=score, category=category, description=description)

def generate_recommendations(assessment: RiskAssessment) -> List[InvestmentRecommendation]:
    """Generează recomandări de investiții personalizate cu descriere detaliată bazate pe evaluarea de risc."""
    recommendations = {
        'Conservator': [
            InvestmentRecommendation(
                asset_class='Obligațiuni',
                allocation=55,
                description='Investițiile în obligațiuni guvernamentale și corporative de înaltă calitate sunt esențiale pentru un portofoliu conservator. Acestea oferă venituri stabile și un risc minim, protejând capitalul investitorului, fiind ideal pentru cei care pun accent pe siguranță și protecția capitalului pe termen lung.'
            ),
            InvestmentRecommendation(
                asset_class='Acțiuni',
                allocation=25,
                description='Acțiunile reprezintă o modalitate de a obține randamente mai mari, dar riscurile sunt mai mari decât în cazul obligațiunilor. Se recomandă acțiuni mari și stabile, cunoscute sub denumirea de "blue-chip", care oferă dividende constante și sunt mai puțin volatile. Acestea asigură un echilibru între creștere și protecție.'
            ),
            InvestmentRecommendation(
                asset_class='Numerar',
                allocation=20,
                description='Numerarul și fondurile pe termen scurt, cum ar fi fondurile de piață monetară, sunt ideale pentru menținerea lichidității și protejarea capitalului în fața volatilității pieței. Aceste instrumente sunt extrem de sigure, oferind rentabilități scăzute, dar garantând acces rapid la fonduri atunci când sunt necesare.'
            )
        ],
        'Moderat': [
            InvestmentRecommendation(
                asset_class='Acțiuni',
                allocation=55,
                description='Acțiunile reprezintă o componentă esențială într-un portofoliu moderat, aducând atât posibilități de creștere, cât și o volatilitate mai controlată. Se recomandă un mix diversificat de acțiuni de creștere și valoare, care pot oferi un echilibru între riscuri și randamente pe termen lung.'
            ),
            InvestmentRecommendation(
                asset_class='Obligațiuni',
                allocation=35,
                description='Obligațiunile oferă stabilitate și venituri regulate. În cazul unui portofoliu moderat, se recomandă obligațiuni corporative și municipale, care au un risc mai mare decât obligațiunile guvernamentale, dar încă sunt considerate mai sigure decât acțiunile. Acestea protejează capitalul investitorului într-o piață volatilă.'
            ),
            InvestmentRecommendation(
                asset_class='Alternative',
                allocation=10,
                description='Investițiile alternative, cum ar fi fondurile imobiliare, oferă o diversificare suplimentară portofoliului. Acestea pot include fonduri imobiliare sau alte tipuri de investiții tangibile, care tind să fie mai puțin corelate cu piețele tradiționale de acțiuni și obligațiuni, reducând astfel riscul global al portofoliului.'
            )
        ],
        'Agresiv': [
            InvestmentRecommendation(
                asset_class='Acțiuni',
                allocation=80,
                description='Investițiile în acțiuni de creștere sunt esențiale pentru un portofoliu agresiv, având un potențial mare de creștere pe termen lung, dar și riscuri mai mari. Se recomandă acțiuni în piețe emergente și companii small-cap, care au o volatilitate mai mare, dar pot oferi randamente semnificativ mai mari.'
            ),
            InvestmentRecommendation(
                asset_class='Obligațiuni',
                allocation=10,
                description='Deși un portofoliu agresiv pune accentul pe acțiuni, obligațiunile pot adăuga o oarecare stabilitate. Se recomandă obligațiuni cu randament ridicat, care sunt mai riscante decât obligațiunile guvernamentale, dar pot oferi randamente mai mari în schimbul unui risc suplimentar.'
            ),
            InvestmentRecommendation(
                asset_class='Alternative',
                allocation=10,
                description='Investițiile alternative, cum ar fi mărfurile și fondurile imobiliare, sunt ideale pentru diversificarea unui portofoliu agresiv. Aceste active pot avea o corelație scăzută cu piețele financiare tradiționale și pot adăuga un plus de volatilitate și, implicit, de potențial de câștig.'
            )
        ]
    }

    return recommendations.get(assessment.category, [])


class PortfolioService:
    @staticmethod
    def calculate_portfolio_value(portfolio: Portfolio) -> float:
        """Calculează valoarea curentă a portofoliului."""
        return sum(portfolio.asset_allocation.values())

    @staticmethod
    def calculate_returns(portfolio: Portfolio) -> Dict:
        """Calculează randamentele istorice ale portofoliului."""
        if not portfolio.historical_performance:
            return {"total": 0, "annualized": 0}

        first_date = portfolio.historical_performance[0]['date']
        if isinstance(first_date, str):
            first_date = datetime.strptime(first_date, '%Y-%m')

        initial_value = portfolio.historical_performance[0]['value']
        current_value = portfolio.total_value
        days = (datetime.now() - first_date).days

        if days <= 0:
            return {"total": 0, "annualized": 0}

        total_return = (current_value - initial_value) / initial_value * 100
        annualized_return = (1 + total_return / 100) ** (365 / days) - 1

        return {
            "total": round(total_return, 2),
            "annualized": round(annualized_return * 100, 2)
        }

class GoalTrackingService:
    @staticmethod
    def analyze_goal_progress(goal: FinancialGoal) -> Dict:
        """Analizează progresul către obiectivul financiar."""
        progress = (goal.current_amount / goal.target_amount) * 100
        days_remaining = (goal.target_date - datetime.now()).days

        if days_remaining > 0:
            required_monthly_saving = (goal.target_amount - goal.current_amount) / (days_remaining / 30)
        else:
            required_monthly_saving = 0

        return {
            "progress_percentage": round(progress, 2),
            "days_remaining": days_remaining,
            "required_monthly_saving": round(required_monthly_saving, 2)
        }

class SimulationService:
    @staticmethod
    def simulate_portfolio(params: Dict) -> List[Dict]:
        """Simulează evoluția portofoliului în timp."""
        results = []

        current_value = float(params['initial_amount'])
        monthly_contribution = float(params['monthly_contribution'])

        expected_returns = {
            'CONSERVATIVE': 0.05,
            'MODERATE': 0.08,
            'AGGRESSIVE': 0.11
        }

        annual_return = expected_returns[params['risk_profile']]
        monthly_return = (1 + annual_return) ** (1/12) - 1

        for month in range(params['time_horizon'] * 12):
            current_value = (current_value * (1 + monthly_return)) + monthly_contribution

            if month % 12 == 0:
                results.append({
                    'year': month // 12,
                    'value': Decimal(str(round(current_value, 2))),
                    'contributions': Decimal(str(round(monthly_contribution * (month + 1), 2))),
                    'earnings': Decimal(str(round(current_value - (float(params['initial_amount']) + 
                                    monthly_contribution * (month + 1)), 2)))
                })

        return results

class MarketAnalysisService:
    @staticmethod
    def get_market_data() -> Dict[str, MarketData]:
        """Returnează date despre piețele financiare."""
        return {
            'stocks': MarketData(
                asset_class='stocks',
                returns=[8.0, 10.0, 7.0, 9.0],
                volatility=15.0,
                correlation_matrix={'bonds': 0.2, 'cash': 0.1}
            ),
            'bonds': MarketData(
                asset_class='bonds',
                returns=[4.0, 3.5, 4.2, 3.8],
                volatility=5.0,
                correlation_matrix={'stocks': 0.2, 'cash': 0.3}
            ),
            'cash': MarketData(
                asset_class='cash',
                returns=[1.5, 1.2, 1.8, 1.6],
                volatility=0.5,
                correlation_matrix={'stocks': 0.1, 'bonds': 0.3}
            )
        }
