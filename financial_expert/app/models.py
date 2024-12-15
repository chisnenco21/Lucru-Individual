from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

class RiskTolerance(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

@dataclass
class FinancialProfile:
    age: int
    income: float
    savings: float
    dependents: int
    risk_tolerance: RiskTolerance
    investment_goals: List[str]
    time_horizon: int

    def validate(self) -> bool:
        return (
            0 < self.age < 120
            and self.income >= 0
            and self.savings >= 0
            and self.dependents >= 0
            and self.time_horizon > 0
            and len(self.investment_goals) > 0
        )

@dataclass
class RiskAssessment:
    score: float
    category: str
    description: str

@dataclass
class InvestmentRecommendation:
    asset_class: str
    allocation: float
    description: str

@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime
    portfolio: Optional['Portfolio'] = None
    goals: List['FinancialGoal'] = None

@dataclass
class Portfolio:
    id: int
    user_id: int
    total_value: float
    last_updated: datetime
    asset_allocation: Dict[str, float]
    historical_performance: List[Dict[str, any]]
    transactions: List['PortfolioTransaction'] = None

@dataclass
class PortfolioTransaction:
    id: int
    portfolio_id: int
    transaction_type: str  # 'DEPOSIT', 'WITHDRAWAL', 'REBALANCE'
    amount: float
    date: datetime
    description: str

@dataclass
class FinancialGoal:
    id: int
    user_id: int
    name: str
    target_amount: float
    current_amount: float
    target_date: datetime
    category: str  # 'EMERGENCY', 'RETIREMENT', 'HOUSE', 'EDUCATION', 'OTHER'
    status: str    # 'IN_PROGRESS', 'ACHIEVED', 'DELAYED'

@dataclass
class MarketData:
    asset_class: str
    returns: List[float]
    volatility: float
    correlation_matrix: dict

@dataclass
class SimulationParams:
    initial_amount: float
    monthly_contribution: float
    time_horizon: int
    risk_profile: str
    inflation_rate: float = 2.0  # valoare implicită pentru rata inflației

@dataclass
class SimulationResult:
    year: int
    value: float
    contributions: float
    earnings: float