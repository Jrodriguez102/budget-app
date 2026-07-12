"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const tabs = [
  { href: "/", label: "Home" },
  { href: "/income-expenses", label: "Income" },
  { href: "/goals", label: "Goals" },
  { href: "/categories", label: "Categories" },
];

export default function TabBar() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-zinc-200 flex justify-around py-3">
      {tabs.map((tab) => {
        const isActive = pathname === tab.href;
        return (
          <Link
            key={tab.href}
            href={tab.href}
            className={`flex flex-col items-center text-xs font-medium ${
              isActive ? "text-indigo-600" : "text-zinc-400"
            }`}
          >
            {tab.label}
          </Link>
        );
      })}
    </nav>
  );
}