// Mirrors docs/API_CONTRACT.md

export type PlanStatus =
  | "normal"
  | "goals_paused_negative_income"
  | "tight"
  | "no_variable_budget";

export type CategoryKey =
  | "groceries"
  | "dining_out"
  | "gas_transportation"
  | "entertainment"
  | "shopping"
  | "personal_care"
  | "travel"
  | "other";

export type GoalContribution = {
  goal_id: string;
  monthly_contribution: number;
  projected_completion_date: string | null;
};

export type CategorySuggestion = {
  key: CategoryKey;
  suggested_amount: number;
  favor_multiplier: number;
};

export type Plan = {
  status: PlanStatus;
  message: string | null;
  total_income: number;
  total_fixed_expenses: number;
  remaining_after_fixed: number;
  goal_contributions: GoalContribution[];
  remaining_after_goals: number;
  category_suggestions: CategorySuggestion[];
};

export type GoalStrategy = "fund_first" | "proportional_weight" | "fixed_amount";

export type Goal = {
  id: string;
  name: string;
  target_amount: number | null;
  target_date: string | null;
  current_amount: number;
  strategy: GoalStrategy;
  priority_rank: number | null;
  weight: number | null;
  fixed_monthly_amount: number | null;
};