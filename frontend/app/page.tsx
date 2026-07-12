import { Plan, Goal } from "./lib/types";
import planData from "./lib/fixtures/plan_normal.json";
import goalsData from "./lib/fixtures/goals.json";

export default function Home() {
  const plan = planData as Plan;
  const goals = goalsData as Goal[];

  return (
    <div className="min-h-screen p-8 max-w-2xl mx-auto bg-zinc-50 text-zinc-900">
      <h1 className="text-2xl font-bold mb-6">Budget Dashboard</h1>

      <section className="bg-white text-zinc-900 rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Summary</h2>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-sm text-zinc-500">Income</p>
            <p className="text-xl font-bold text-green-600">
              ${plan.total_income.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm text-zinc-500">Fixed Expenses</p>
            <p className="text-xl font-bold text-red-600">
              ${plan.total_fixed_expenses.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm text-zinc-500">Remaining</p>
            <p className="text-xl font-bold">
              ${plan.remaining_after_fixed.toLocaleString()}
            </p>
          </div>
        </div>
      </section>
      <section className="bg-white text-zinc-900 rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Suggested Spending</h2>
        <div className="grid grid-cols-2 gap-3">
          {plan.category_suggestions.map((cat) => (
            <div
              key={cat.key}
              className="flex justify-between items-center border-b border-zinc-100 pb-2"
            >
              <span className="capitalize text-zinc-700">
                {cat.key.replace(/_/g, " ")}
              </span>
              <span className="font-semibold">
                ${cat.suggested_amount.toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}