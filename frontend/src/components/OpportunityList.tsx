import type { Opportunity } from "../data/mockOpportunities";
import { OpportunityCard } from "./OpportunityCard";

export interface OpportunityListProps {
  opportunities: Opportunity[];
  selectedId: number | null;
  onSelect: (id: number) => void;
}

export function OpportunityList({ opportunities, selectedId, onSelect }: OpportunityListProps) {
  return (
    <ul className="space-y-3" aria-label="Opportunities">
      {opportunities.map((opp) => (
        <li key={opp.id} role="none">
          <OpportunityCard opportunity={opp} selected={selectedId === opp.id} onSelect={onSelect} />
        </li>
      ))}
    </ul>
  );
}
