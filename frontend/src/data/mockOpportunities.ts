export interface Opportunity {
  id: number;
  title: string;
  organization: string;
  location: string;
  description: string;
  tags: string[];
  stipend?: string;
  deadline?: string;
  requirements: string[];
  link?: string;
  isNew: boolean;
  postedDate: string;
}

export const MOCK_OPPORTUNITIES: Opportunity[] = [
  {
    id: 1,
    title: "CHED Tertiary Education Subsidy (TES)",
    organization: "Commission on Higher Education",
    location: "Nationwide",
    description:
      "Financial assistance for qualified Filipino students in private HEIs and SUCs. Covers tuition and other school fees for eligible undergraduate students.",
    tags: ["Scholarship", "Government", "Undergraduate"],
    stipend: "Up to PHP 60,000 / academic year",
    deadline: "2025-09-30",
    requirements: [
      "Filipino citizen",
      "Enrolled in CHED-recognized program",
      "Combined annual income of parents/guardian not exceeding threshold",
      "No other full scholarship for the same period",
    ],
    link: "https://ched.gov.ph",
    isNew: true,
    postedDate: "2025-03-15",
  },
  {
    id: 2,
    title: "DOST-SEI Undergraduate Scholarship",
    organization: "Department of Science and Technology",
    location: "Nationwide",
    description:
      "Scholarship for students pursuing priority STEM courses in identified universities. Includes tuition, book allowance, and monthly stipend.",
    tags: ["Scholarship", "STEM", "Science"],
    stipend: "PHP 7,000 / month + tuition",
    deadline: "2025-08-15",
    requirements: [
      "STEM strand or equivalent for senior high",
      "Pass DOST qualifying examination",
      "GWA of at least 85% or its equivalent",
      "Not more than 22 years old at time of application",
    ],
    link: "https://www.science-scholarships.ph",
    isNew: true,
    postedDate: "2025-03-10",
  },
  {
    id: 3,
    title: "Software Engineering Intern — Summer Cohort",
    organization: "Metro Manila Tech Solutions Inc.",
    location: "Makati City, Metro Manila",
    description:
      "12-week internship for CS/IT students. Work on production web apps with mentorship from senior engineers. Hybrid schedule available.",
    tags: ["Internship", "Tech", "Hybrid"],
    stipend: "PHP 18,000 / month",
    deadline: "2025-04-30",
    requirements: [
      "Currently enrolled in BS CS, IT, or related field",
      "Completed at least 2 years of coursework",
      "Basic knowledge of React and TypeScript",
      "Available full-time during summer term",
    ],
    link: "https://example.com/careers/intern",
    isNew: false,
    postedDate: "2025-02-28",
  },
  {
    id: 4,
    title: "SM College Scholarship Program",
    organization: "SM Foundation",
    location: "Nationwide",
    description:
      "Full scholarship covering tuition and monthly allowance for students in partner schools, with emphasis on students from low-income families.",
    tags: ["Scholarship", "Private sector", "Full ride"],
    stipend: "PHP 3,500 / month allowance",
    deadline: "2025-05-31",
    requirements: [
      "Grade 12 graduate from public school or SM partner school",
      "GWA of at least 88%",
      "Combined family income below threshold",
      "Willing to render return service to SM",
    ],
    link: "https://www.sm-foundation.org",
    isNew: false,
    postedDate: "2025-01-20",
  },
  {
    id: 5,
    title: "Research Assistant — Climate Data Lab",
    organization: "University of the Philippines Diliman",
    location: "Quezon City, Metro Manila",
    description:
      "Part-time RA position supporting geospatial climate projects. Ideal for graduate students in environmental science or data analytics.",
    tags: ["Research", "Graduate", "Part-time"],
    stipend: "PHP 12,000 / month",
    deadline: "2025-04-15",
    requirements: [
      "Enrolled in master’s or PhD program",
      "Experience with Python or R",
      "Interest in climate or GIS datasets",
      "Commitment of 15–20 hours per week",
    ],
    isNew: false,
    postedDate: "2025-03-01",
  },
  {
    id: 6,
    title: "Ayala Foundation Young Leaders Program",
    organization: "Ayala Foundation",
    location: "Visayas & Mindanao",
    description:
      "Leadership development and scholarship support for outstanding students from underserved communities, including workshops and mentorship.",
    tags: ["Scholarship", "Leadership", "Community"],
    stipend: "PHP 40,000 / year + leadership training",
    deadline: "2025-06-01",
    requirements: [
      "Resident of priority provinces in Visayas or Mindanao",
      "Demonstrated leadership in school or community",
      "GWA of at least 85%",
      "Two recommendation letters",
    ],
    link: "https://www.ayalafoundation.org",
    isNew: true,
    postedDate: "2025-03-18",
  },
  {
    id: 7,
    title: "OWWA Education for Development Scholarship",
    organization: "Overseas Workers Welfare Administration",
    location: "Nationwide",
    description:
      "Educational assistance for dependents of active OWWA members pursuing college or technical-vocational programs.",
    tags: ["Scholarship", "OFW", "Dependent"],
    stipend: "PHP 60,000 / year (max)",
    deadline: "2025-07-31",
    requirements: [
      "Dependent of documented OWWA member",
      "Not more than 30 years old for college",
      "Pass entrance exam where applicable",
      "No other government full scholarship",
    ],
    link: "https://owwa.gov.ph",
    isNew: false,
    postedDate: "2024-11-10",
  },
  {
    id: 8,
    title: "UX Design Internship",
    organization: "Cebu Digital Agency Co.",
    location: "Cebu City, Central Visayas",
    description:
      "6-month internship focused on user research, wireframing, and design systems for fintech clients. Portfolio review required.",
    tags: ["Internship", "Design", "On-site"],
    stipend: "PHP 15,000 / month",
    deadline: "2025-05-10",
    requirements: [
      "Portfolio with at least 2 case studies",
      "Figma proficiency",
      "Third or fourth year in HCI, design, or related program",
      "Willing to work on-site in Cebu",
    ],
    isNew: false,
    postedDate: "2025-02-15",
  },
  {
    id: 9,
    title: "Barangay Educational Assistance (Local Grant)",
    organization: "Quezon City LGU — District 3",
    location: "Quezon City, Metro Manila",
    description:
      "Small grant for residents enrolled in college or TESDA programs. Amount varies by household income bracket.",
    tags: ["Grant", "Local", "Undergraduate"],
    stipend: "PHP 5,000 – 15,000 / semester",
    deadline: "2025-04-20",
    requirements: [
      "Registered voter or dependent of registered voter in barangay",
      "Proof of enrollment",
      "Barangay clearance and certificate of indigency",
    ],
    isNew: false,
    postedDate: "2025-01-05",
  },
  {
    id: 10,
    title: "Philippine Space Agency — STEM Outreach Fellowship",
    organization: "PhilSA",
    location: "Pasay City, Metro Manila",
    description:
      "Short fellowship for students passionate about space science and satellite applications. Includes stipend and certificate.",
    tags: ["Fellowship", "STEM", "Space"],
    stipend: "PHP 25,000 total (8 weeks)",
    deadline: "2025-05-01",
    requirements: [
      "Undergraduate or graduate in engineering or physical sciences",
      "Essay on Philippine space priorities",
      "Available for full-time onsite module in Pasay",
    ],
    link: "https://philsa.gov.ph",
    isNew: true,
    postedDate: "2025-03-22",
  },
];
