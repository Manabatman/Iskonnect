import { FormEvent, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { AuthDirectionalOverlay } from "../components/visual/DirectionalImageOverlays";
import { EmailVerificationRequiredError, getPostAuthPath, useAuth } from "../contexts/AuthContext";
import { clearLoginFlowMeasures, markLoginFlow } from "../utils/perfTiming";
import { validateEmail } from "../utils/validateEmail";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

import { safeReturnPath } from "../utils/returnPath";

const AUTH_PANEL_PRIMARY = "/images/auth/login-illustration.jpg";
const AUTH_PANEL_FALLBACK = "/images/hero/hero-1.svg";

export function LoginPage() {
  const { login, user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const returnTo = safeReturnPath((location.state as { from?: string } | null)?.from);

  useEffect(() => {
    if (!authLoading && user) {
      navigate(getPostAuthPath(user, returnTo), { replace: true });
    }
  }, [authLoading, user, navigate, returnTo]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [verificationBlocked, setVerificationBlocked] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [authPanelSrc, setAuthPanelSrc] = useState(AUTH_PANEL_PRIMARY);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setVerificationBlocked(false);
    setEmailError(null);
    const emailCheck = validateEmail(email);
    if (!emailCheck.valid) {
      const message = emailCheck.message ?? "Enter a valid email address.";
      setEmailError(message);
      setError(message);
      return;
    }
    setLoading(true);
    clearLoginFlowMeasures();
    markLoginFlow("submit");
    try {
      const authUser = await login(email, password);
      markLoginFlow("navigate-dashboard");
      navigate(getPostAuthPath(authUser, returnTo), { replace: true });
    } catch (err) {
      if (err instanceof EmailVerificationRequiredError) {
        setVerificationBlocked(true);
        setError(err.message);
      } else {
        setError(err instanceof Error ? err.message : "Login failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col md:flex-row">
      {/* Left — visual + trust copy (no testimonials) */}
      <div className="relative hidden min-h-[280px] flex-1 md:block md:min-h-0">
        <img
          src={authPanelSrc}
          alt=""
          width={800}
          height={600}
          decoding="async"
          loading="lazy"
          onError={() => setAuthPanelSrc((s) => (s === AUTH_PANEL_PRIMARY ? AUTH_PANEL_FALLBACK : s))}
          className="absolute inset-0 h-full w-full object-cover"
        />
        <AuthDirectionalOverlay />
        <div className="relative z-10 flex h-full min-h-[420px] flex-col justify-end p-8 lg:p-12">
          <p className="max-w-md text-lg font-medium leading-relaxed text-white lg:text-xl">
            Welcome back, Iskolar. Let's pick up right where you left off on your journey.
          </p>
        </div>
      </div>

      {/* Right — form */}
      <div className="flex flex-1 items-center justify-center bg-muted px-4 py-12 md:py-0">
        <Card className="glass w-full max-w-md shadow-3">
          <CardHeader>
            <CardTitle className="text-2xl">Welcome back</CardTitle>
            <CardDescription>Sign in to continue your scholarship journey.</CardDescription>
          </CardHeader>
          <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant={verificationBlocked ? "default" : "destructive"} role="alert">
                <AlertDescription>
                  {error}
                  {verificationBlocked && (
                    <span className="mt-2 block text-sm text-muted-foreground">
                      Check your inbox and spam folder for the verification email we sent when you registered.
                      Resending requires a signed-in session, so if you still don&apos;t see it, try registering again
                      with the same email or contact{" "}
                      <a
                        href="mailto:manabat.markjustin@gmail.com"
                        className="font-medium text-primary hover:underline"
                      >
                        support
                      </a>
                      .
                    </span>
                  )}
                </AlertDescription>
              </Alert>
            )}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (emailError) setEmailError(null);
                }}
                placeholder="you@example.com"
                autoComplete="email"
                error={emailError ?? undefined}
              />
              {emailError ? (
                <p id="email-error" className="text-sm text-tone-danger">
                  {emailError}
                </p>
              ) : null}
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Password</Label>
                <Link to="/forgot-password" className="text-xs font-medium text-primary hover:underline">
                  Forgot password?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </div>
            <Button type="submit" disabled={loading} className="w-full">
              {loading ? "Signing in…" : "Sign in"}
            </Button>
          </form>
          <p className="mt-6 text-center text-sm text-muted-foreground">
            Don&apos;t have an account?{" "}
            <Link
              to="/register"
              state={returnTo ? { from: returnTo } : undefined}
              className="font-semibold text-primary hover:underline"
            >
              Register
            </Link>
          </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
