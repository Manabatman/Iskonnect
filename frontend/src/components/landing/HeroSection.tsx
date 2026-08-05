import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { HERO_BREAKPOINTS, HERO_IMAGE_ALT } from "../../constants/heroImages";
import { HeroDirectionalOverlay } from "../visual/DirectionalImageOverlays";
import { heroTrustChips } from "./landingData";
import { primaryButtonClass, secondaryButtonClass } from "./Section";
import { Reveal } from "./Reveal";

function HeroPhotography() {
  const { mobile, tablet, desktop } = HERO_BREAKPOINTS;

  return (
    <picture className="absolute inset-0 block h-full w-full">
      <source media={desktop.media} srcSet={desktop.avif} type="image/avif" />
      <source media={desktop.media} srcSet={desktop.webp} type="image/webp" />
      <source media={tablet.media} srcSet={tablet.avif} type="image/avif" />
      <source media={tablet.media} srcSet={tablet.webp} type="image/webp" />
      <source media={mobile.media} srcSet={mobile.avif} type="image/avif" />
      <source media={mobile.media} srcSet={mobile.webp} type="image/webp" />
      <source media={desktop.media} srcSet={desktop.png} type="image/png" />
      <source media={tablet.media} srcSet={tablet.png} type="image/png" />
      <img
        src={mobile.png}
        alt={HERO_IMAGE_ALT}
        width={mobile.width}
        height={mobile.height}
        fetchPriority="high"
        loading="eager"
        decoding="async"
        className="h-full w-full object-cover object-[50%_35%] md:object-center"
        sizes="100vw"
      />
    </picture>
  );
}

export function HeroSection() {
  return (
    <section
      data-testid="landing-hero"
      className="relative min-h-[clamp(30rem,calc(100svh-9rem),64rem)] overflow-hidden border-b border-slate-800 sm:min-h-[clamp(34rem,calc(100svh-4rem),64rem)]"
    >
      <HeroPhotography />
      <HeroDirectionalOverlay />
      <div className="relative z-10 mx-auto flex min-h-[inherit] w-full max-w-6xl flex-col justify-center px-4 py-[clamp(3rem,8vh,7rem)] sm:px-6">
        <Reveal>
          <div className="max-w-[42rem] xl:max-w-[48rem]">
            <h1 className="text-balance font-sans text-[clamp(2.25rem,5.5vw,4rem)] font-extrabold leading-[1.08] tracking-tight text-white">
              Find scholarships you&apos;re actually eligible for.
            </h1>
            <p className="mt-[clamp(1rem,2vh,1.5rem)] max-w-xl text-pretty font-sans text-[clamp(1rem,1.4vw,1.25rem)] leading-relaxed text-slate-200">
              ISKONNECT matches you to scholarships from government agencies, universities, LGUs, and private
              foundations, then helps you plan ahead: apply now, prepare documents early, or watch for programs you&apos;ll
              qualify for later.
            </p>

            <div className="mt-[clamp(1.5rem,3vh,2rem)] flex flex-col gap-3 sm:flex-row sm:items-center">
              <Link
                to="/register"
                className={`${primaryButtonClass} w-full sm:w-auto`}
                data-testid="hero-primary-cta"
              >
                Get started free
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
              <Link
                to="/how-it-works"
                className={`${secondaryButtonClass} w-full border-white/20 bg-white/10 text-white backdrop-blur-sm hover:bg-white/20 sm:w-auto dark:border-white/20 dark:bg-white/10 dark:text-white dark:hover:bg-white/20`}
              >
                See how it works
              </Link>
            </div>

            <ul className="mt-6 flex flex-wrap gap-2" aria-label="Platform highlights">
              {heroTrustChips.map((chip) => (
                <li
                  key={chip}
                  className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-slate-200 backdrop-blur-sm"
                >
                  <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-success-400" />
                  {chip}
                </li>
              ))}
            </ul>

            <p className="mt-6 text-sm text-slate-400">
              Already have an account?{" "}
              <Link
                to="/login"
                className="font-medium text-white underline decoration-primary-400/80 underline-offset-2 hover:text-primary-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900"
              >
                Sign in
              </Link>
            </p>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
