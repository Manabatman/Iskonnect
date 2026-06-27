import type { LucideIcon } from "lucide-react";
import {
  CalendarX,
  ClipboardList,
  Globe,
  HelpCircle,
  ShieldCheck,
  Sparkles,
  UserCircle,
} from "lucide-react";
import type { ReactNode } from "react";

export const officialSources = [
  "CHED",
  "DOST-SEI",
  "TESDA",
  "LGUs",
  "Universities",
  "Private foundations",
] as const;

export const heroTrustChips = [
  "Free for students",
  "Official sources only",
  "Eligibility-based matching",
] as const;

export const problemItems = [
  {
    title: "Scattered across dozens of sites",
    body: "Government portals, university pages, LGU announcements, and Facebook posts—each with different formats and no single place to search.",
    Icon: Globe,
  },
  {
    title: "Unclear if you even qualify",
    body: "Most listings don't tell you upfront whether your GWA, region, income, or course fits. You waste time on programs you can't apply for.",
    Icon: HelpCircle,
  },
  {
    title: "Deadlines missed in the noise",
    body: "Application windows close while you're still digging through outdated posts and broken links.",
    Icon: CalendarX,
  },
] as const;

export const howItWorksSteps = [
  {
    n: 1,
    title: "Build your profile once",
    body: "Tell us your GWA, region, course interests, income range, and household background. One profile powers every match.",
    Icon: UserCircle,
  },
  {
    n: 2,
    title: "We check real eligibility rules",
    body: "Each scholarship has actual rules—minimum GWA, income ceiling, region, course. We check your profile against every one before anything is ranked.",
    Icon: ShieldCheck,
  },
  {
    n: 3,
    title: "See ranked matches you qualify for",
    body: "Programs you don't qualify for are removed. What remains is scored and ranked so your best fits rise to the top.",
    Icon: Sparkles,
  },
] as const;

/** Real weighted scoring factors from TransparencyPage — no invented numbers. */
export const scoringFactors = [
  { name: "Academic Performance", weight: 30 },
  { name: "Financial Need", weight: 28 },
  { name: "Field of Study", weight: 22 },
  { name: "Location Match", weight: 10 },
  { name: "Priority Group", weight: 10 },
] as const;

export const trustPoints = [
  {
    title: "Transparent eligibility scoring",
    body: "Every match score is built from weighted factors you can see—not a black box.",
    Icon: ShieldCheck,
  },
  {
    title: "We never sell your data",
    body: "Your profile is used only to match you with scholarships. We don't share it with providers.",
    Icon: UserCircle,
  },
  {
    title: "Always links to the official source",
    body: "Every program links back to the provider's site. Confirm deadlines and requirements there before applying.",
    Icon: Globe,
  },
] as const;

export const benefitItems = [
  {
    title: "Find scholarships you're actually eligible for",
    body: "We rank programs against real rules—region, level, income, and field—so your list reflects what you can genuinely apply for.",
    Icon: Sparkles,
  },
  {
    title: "One profile, hundreds of opportunities",
    body: "Build your profile once and reuse it across government, university, LGU, and private programs—no re-entering the same details.",
    Icon: ClipboardList,
  },
  {
    title: "Never miss another deadline",
    body: "Keep saved programs, reminders, and next steps in one place, always linked back to the official source.",
    Icon: CalendarX,
  },
] as const;

export type FaqItem = { q: string; a: ReactNode };

export const faqItems: FaqItem[] = [
  {
    q: "Why might my matches change over time?",
    a: "Your matches update when you update your profile, when program rules change, or when administrators adjust scoring weights for a new funding cycle.",
  },
  {
    q: "Could I be missing scholarships I qualify for?",
    a: "Hard eligibility filters only remove programs where your profile clearly fails a required rule (like a region restriction). If data is missing from your profile, you may see fewer results—which is why completing your profile matters.",
  },
  {
    q: "How is my personal data used?",
    a: "Your profile data is used only to match you with scholarships. We don't sell it or share it with scholarship providers. See our Privacy Policy for full details.",
  },
];

export type { LucideIcon };
