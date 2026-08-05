/** RFC 5322-subset email validation with typo suggestions (P1-06). */

const EMAIL_RE =
  /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

const COMMON_DOMAINS = [
  "gmail.com",
  "yahoo.com",
  "outlook.com",
  "icloud.com",
  "hotmail.com",
  "ymail.com",
  "live.com",
  "edu.ph",
];

export type EmailValidationResult = {
  valid: boolean;
  message?: string;
  suggestion?: string;
};

function levenshtein(a: string, b: string): number {
  const m = a.length;
  const n = b.length;
  const dp = Array.from({ length: m + 1 }, () => Array<number>(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
    }
  }
  return dp[m][n];
}

export function suggestEmailDomain(domain: string): string | undefined {
  const lower = domain.toLowerCase();
  let best: string | undefined;
  let bestDist = 3;
  for (const candidate of COMMON_DOMAINS) {
    const dist = levenshtein(lower, candidate);
    if (dist < bestDist) {
      bestDist = dist;
      best = candidate;
    }
  }
  return bestDist <= 2 ? best : undefined;
}

export function validateEmail(value: string): EmailValidationResult {
  const trimmed = value.trim();
  if (!trimmed) {
    return { valid: false, message: "Email is required." };
  }
  if (trimmed.length > 254) {
    return { valid: false, message: "Email is too long." };
  }
  if (!trimmed.includes("@")) {
    return { valid: false, message: "Add a domain, like @gmail.com." };
  }
  const [local, domain] = trimmed.split("@");
  if (!local || !domain || local.length > 64) {
    return { valid: false, message: "Enter a valid email address." };
  }
  if (local.includes("..") || domain.includes("..")) {
    return { valid: false, message: "Email cannot contain consecutive dots." };
  }
  const domainLower = domain.toLowerCase();
  const suggestionDomain = suggestEmailDomain(domainLower);
  if (suggestionDomain && suggestionDomain !== domainLower) {
    return {
      valid: false,
      message: `Did you mean ${local}@${suggestionDomain}?`,
      suggestion: `${local}@${suggestionDomain}`,
    };
  }
  if (!EMAIL_RE.test(trimmed)) {
    return { valid: false, message: "Enter a valid email address." };
  }
  return { valid: true };
}
