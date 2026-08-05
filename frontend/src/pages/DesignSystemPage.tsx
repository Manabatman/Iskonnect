import * as React from "react";
import {
  Alert,
  AlertDescription,
  AlertTitle,
  Badge,
  Button,
  Chip,
  Icon,
  Input,
  Label,
  Progress,
  Separator,
  Skeleton,
  Switch,
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
  Textarea,
} from "@/components/ui";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Search } from "lucide-react";
import { LifecycleStatusExample } from "../components/LifecycleStatusBadge";
import { QualificationStatusBadge } from "../components/QualificationStatusBadge";

/** DS-16 — internal design reference (dev/staging only route). */
export function DesignSystemPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-12 px-4 py-12 pb-[calc(5rem+env(safe-area-inset-bottom))]">
      <header>
        <h1 className="font-display text-3xl text-primary">Iskonnect Design System</h1>
        <p className="mt-2 text-muted-foreground">Phase 2 token + primitive reference. Not linked from production nav.</p>
      </header>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Typography</h2>
        <p className="font-sans text-base">Body — Inter (self-hosted)</p>
        <p className="font-display text-2xl">Display — Russo One</p>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Type scale</h2>
        <p className="text-body-sm text-muted-foreground">Semantic utilities from tailwind.config.js — migrate pages in later waves.</p>
        <div className="space-y-3 rounded-lg border border-border p-4">
          <p className="text-display font-display text-primary">display — 56px hero</p>
          <p className="text-h1">h1 — page title</p>
          <p className="text-h2">h2 — section heading</p>
          <p className="text-h3">h3 — card title</p>
          <p className="text-h4">h4 — subsection</p>
          <p className="text-body-lg">body-lg — lead paragraph</p>
          <p className="text-body">body — default UI text</p>
          <p className="text-body-sm text-muted-foreground">body-sm — secondary metadata</p>
          <p className="text-caption text-muted-foreground">caption — timestamps</p>
          <p className="text-overline text-muted-foreground">overline — section label</p>
          <p className="text-button">button — button label</p>
          <p className="text-label">label — form label</p>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Buttons</h2>
        <div className="flex flex-wrap gap-3">
          <Button>Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="link">Link</Button>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Form controls</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="ds-input">Input</Label>
            <Input id="ds-input" placeholder="Placeholder" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="ds-textarea">Textarea</Label>
            <Textarea id="ds-textarea" placeholder="Multi-line" />
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Switch id="ds-switch" />
          <Label htmlFor="ds-switch">Switch (44px hit area)</Label>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Chips</h2>
        <div className="flex flex-wrap gap-2">
          <Chip variant="neutral">Neutral</Chip>
          <Chip variant="success">Success</Chip>
          <Chip variant="warning">Warning</Chip>
          <Chip variant="danger">Danger</Chip>
          <Chip variant="info">Info</Chip>
          <Chip variant="default">Primary tint</Chip>
          <Chip size="sm">Small (11px)</Chip>
          <Chip size="lg">Large filter</Chip>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Icons (DS-12)</h2>
        <div className="flex items-center gap-6">
          <div className="flex flex-col items-center gap-1">
            <Icon icon={Search} size="sm" />
            <span className="text-caption text-muted-foreground">sm 16px</span>
          </div>
          <div className="flex flex-col items-center gap-1">
            <Icon icon={Search} size="md" />
            <span className="text-caption text-muted-foreground">md 20px</span>
          </div>
          <div className="flex flex-col items-center gap-1">
            <Icon icon={Search} size="lg" />
            <span className="text-caption text-muted-foreground">lg 24px</span>
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Layout tokens</h2>
        <ul className="list-inside list-disc space-y-1 text-body-sm text-muted-foreground">
          <li>
            <code className="text-foreground">--page-gutter</code> → spacing.page-gutter (16px)
          </li>
          <li>
            <code className="text-foreground">--section-gap</code> → spacing.section-gap (48px)
          </li>
          <li>
            <code className="text-foreground">--nav-height-mobile</code> → spacing.nav-mobile (56px)
          </li>
          <li>
            <code className="text-foreground">--feedback-fab-offset</code> — FAB clearance above bottom nav
          </li>
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Semantic badges</h2>
        <div className="flex flex-wrap gap-2">
          <Badge variant="success">Success</Badge>
          <Badge variant="warning">Warning</Badge>
          <Badge variant="danger">Danger</Badge>
          <Badge variant="info">Info</Badge>
          <Badge variant="neutral">Neutral</Badge>
        </div>
        <div className="flex flex-wrap gap-2">
          <LifecycleStatusExample statusKey="open" />
          <LifecycleStatusExample statusKey="needs_verification" />
          <QualificationStatusBadge status="qualified" />
          <QualificationStatusBadge status="almost_qualified" />
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Alerts &amp; states</h2>
        <Alert variant="info">
          <AlertTitle>Info</AlertTitle>
          <AlertDescription>Informational message using tone tokens.</AlertDescription>
        </Alert>
        <Alert variant="warning">
          <AlertDescription>Warning state — verify on official site.</AlertDescription>
        </Alert>
        <Skeleton className="h-12 w-full max-w-md" />
        <Progress value={66} />
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Elevation &amp; cards</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card className="shadow-1">
            <CardHeader>
              <CardTitle className="text-base">Shadow 1</CardTitle>
            </CardHeader>
          </Card>
          <Card className="shadow-2">
            <CardHeader>
              <CardTitle className="text-base">Shadow 2</CardTitle>
            </CardHeader>
          </Card>
          <Card className="shadow-3">
            <CardHeader>
              <CardTitle className="text-base">Shadow 3</CardTitle>
            </CardHeader>
          </Card>
          <Card className="shadow-4">
            <CardHeader>
              <CardTitle className="text-base">Shadow 4</CardTitle>
            </CardHeader>
          </Card>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Tabs</h2>
        <Tabs defaultValue="a">
          <TabsList>
            <TabsTrigger value="a">Tab A</TabsTrigger>
            <TabsTrigger value="b">Tab B</TabsTrigger>
          </TabsList>
          <TabsContent value="a" className="rounded-md border border-border p-4">
            Panel A
          </TabsContent>
          <TabsContent value="b" className="rounded-md border border-border p-4">
            Panel B
          </TabsContent>
        </Tabs>
      </section>

      <Separator />
      <p className="text-xs text-muted-foreground">Route: /design-system · MOB-02 min target 44px on primary controls</p>
    </div>
  );
}
