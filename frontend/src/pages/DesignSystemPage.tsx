import * as React from "react";
import {
  Alert,
  AlertDescription,
  AlertTitle,
  Badge,
  Button,
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
import { LifecycleStatusExample } from "../components/LifecycleStatusBadge";
import { QualificationStatusBadge } from "../components/QualificationStatusBadge";

/** DS-16 — internal design reference (dev/staging only route). */
export function DesignSystemPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-10 px-4 py-10 pb-[calc(5rem+env(safe-area-inset-bottom))]">
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
