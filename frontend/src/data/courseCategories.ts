/** PSCED-aligned course groupings for Career Roadmap (Philippines). */
export type CourseCategory = { id: string; label: string; courses: string[] };

export const COURSE_CATEGORIES: CourseCategory[] = [
  {
    id: "it_cs",
    label: "IT & Computer Science",
    courses: [
      "BS Computer Science",
      "BS Information Technology",
      "BS Information Systems",
      "BS Computer Engineering",
      "BS Data Science",
      "BS Cybersecurity",
    ],
  },
  {
    id: "engineering",
    label: "Engineering",
    courses: [
      "BS Civil Engineering",
      "BS Mechanical Engineering",
      "BS Electrical Engineering",
      "BS Electronics Engineering",
      "BS Industrial Engineering",
      "BS Chemical Engineering",
    ],
  },
  {
    id: "business",
    label: "Business & Management",
    courses: [
      "BS Business Administration",
      "BS Accountancy",
      "BS Entrepreneurship",
      "BS Marketing Management",
      "BS Financial Management",
      "BS Hospitality Management",
    ],
  },
  {
    id: "health",
    label: "Health Sciences",
    courses: [
      "BS Nursing",
      "BS Pharmacy",
      "BS Medical Technology",
      "BS Physical Therapy",
      "BS Public Health",
      "Doctor of Medicine (MD)",
    ],
  },
  {
    id: "education",
    label: "Education",
    courses: [
      "BEED Elementary Education",
      "BSED English",
      "BSED Mathematics",
      "BSED Science",
      "BTVTED",
    ],
  },
  {
    id: "arts_humanities",
    label: "Arts & Humanities",
    courses: [
      "AB Psychology",
      "AB Communication",
      "AB Political Science",
      "AB Economics",
      "AB English",
    ],
  },
  {
    id: "sciences",
    label: "Natural Sciences",
    courses: [
      "BS Biology",
      "BS Chemistry",
      "BS Physics",
      "BS Mathematics",
      "BS Environmental Science",
    ],
  },
  {
    id: "agri",
    label: "Agriculture & Fisheries",
    courses: [
      "BS Agriculture",
      "BS Agricultural Engineering",
      "BS Fisheries",
      "BS Forestry",
    ],
  },
  {
    id: "law_social",
    label: "Law & Social Sciences",
    courses: ["BS Criminology", "BS Social Work", "BS Sociology", "JD / Law"],
  },
  {
    id: "tvet",
    label: "TVET & Skills",
    courses: [
      "Diploma in Computer Technology",
      "Diploma in Automotive",
      "Diploma in Electrical Installation",
      "TESDA NC programs",
    ],
  },
];
