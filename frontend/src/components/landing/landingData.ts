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

export const proofStripItems = [
  {
    variant: "matches" as const,
    caption: "See which programs fit your profile before you apply.",
  },
  {
    variant: "breakdown" as const,
    caption: "Understand why a match scored the way it did—without guesswork.",
  },
  {
    variant: "search" as const,
    caption: "Filter by region, level, and field to narrow your list fast.",
  },
  {
    variant: "mobile" as const,
    caption: "Track your plan on the go—same eligibility rules, smaller screen.",
  },
] as const;

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
  "Plan ahead—not just search",
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
    body: "Application windows close while you're still digging through outdated posts and broken links—or before you've gathered documents.",
    Icon: CalendarX,
  },
] as const;

export const howItWorksSteps = [
  {
    n: 1,
    title: "Build your profile once",
    body: "Tell us your GWA, region, course interests, income range, and household background. One profile powers your entire scholarship plan.",
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
    title: "See your plan—not just matches",
    body: "Programs you don't qualify for are filtered out. What's left is ranked, timed, and organized so you know what to apply for now, prepare for, or watch for next cycle.",
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
    title: "Verified against official sources",
    body: "We show when listings were last checked and link you to the provider's site so you can confirm details yourself.",
    Icon: ShieldCheck,
  },
  {
    title: "We never sell your data",
    body: "Your profile is used only to match you with scholarships. We don't share it with providers.",
    Icon: UserCircle,
  },
  {
    title: "Closed programs still help you plan",
    body: "Past cycles stay visible so you can learn requirements and prepare early for the next opening.",
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
    title: "Prepare before deadlines arrive",
    body: "See future eligibility, document checklists, and upcoming openings—so you're ready when applications open.",
    Icon: ClipboardList,
  },
  {
    title: "One profile, your whole scholarship plan",
    body: "Build your profile once and reuse it across government, university, LGU, and private programs—matches, saves, and reminders in one place.",
    Icon: CalendarX,
  },
] as const;

export type FaqItem = { q: string; a: ReactNode };

export const faqItems: FaqItem[] = [
  {
    q: "Is ISKONNECT free?",
    a: "Yes. ISKONNECT is free for students. Create an account, build your profile, and use matching, search, and planning tools at no cost.",
  },
  {
    q: "Where does scholarship information come from?",
    a: "From publicly available official sources—CHED, DOST-SEI, TESDA, LGUs, universities, and private foundations. Every listing links to the provider's site.",
  },
  {
    q: "Why show closed or past-cycle scholarships?",
    a: "So you can learn typical requirements, compare benefits, and prepare early for the next cycle. Closed listings are labeled clearly—you won't be misled into thinking you can apply today.",
  },
  {
    q: "What is future eligibility?",
    a: "Some scholarships you don't qualify for yet—maybe you need a higher grade level or GWA. ISKONNECT flags these so you can plan ahead instead of discovering them too late.",
  },
  {
    q: "How do I report a problem with a listing?",
    a: "Open the scholarship page and tap \"Report an issue.\" Tell us about broken links, wrong deadlines, or outdated info. Our team reviews every report.",
  },
  {
    q: "Why might my matches change over time?",
    a: "Your plan updates when you update your profile, when program rules change, or when new scholarships are added. Completing your profile gives you more accurate results.",
  },
  {
    q: "Could I be missing scholarships I qualify for?",
    a: "If your profile is incomplete—missing income, GWA, or field of study—you may see fewer results. We only remove programs where you clearly fail a required rule, like a region restriction.",
  },
  {
    q: "How is my personal data used?",
    a: "Your profile data is used only to match you with scholarships. We don't sell it or share it with scholarship providers. See our Privacy Policy for full details.",
  },
];

export type { LucideIcon };
