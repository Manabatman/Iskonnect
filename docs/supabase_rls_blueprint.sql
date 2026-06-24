-- Iskonnect Supabase RLS blueprint (future use)
--
-- Current production auth uses custom JWT via FastAPI (app/auth.py), NOT Supabase Auth.
-- Migration 020 enables RLS with no policies (deny-all for PostgREST). These policies
-- apply only after migrating browser clients to Supabase Auth and aligning users.id
-- with auth.uid().
--
-- Do NOT apply blindly while FastAPI connects as table owner (RLS is bypassed today).

-- Students: owner-only read/write
ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;

CREATE POLICY students_self_select ON public.students
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY students_self_modify ON public.students
  FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

-- Saved scholarships
ALTER TABLE public.saved_scholarships ENABLE ROW LEVEL SECURITY;

CREATE POLICY saved_scholarships_self ON public.saved_scholarships
  FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

-- Applications
ALTER TABLE public.applications ENABLE ROW LEVEL SECURITY;

CREATE POLICY applications_self ON public.applications
  FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

-- Document checklists (via application ownership)
ALTER TABLE public.document_checklists ENABLE ROW LEVEL SECURITY;

CREATE POLICY document_checklists_self ON public.document_checklists
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM public.applications a
      WHERE a.id = document_checklists.application_id
        AND a.user_id = auth.uid()
    )
  );

-- Match runs
ALTER TABLE public.match_runs ENABLE ROW LEVEL SECURITY;

CREATE POLICY match_runs_self ON public.match_runs
  FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

-- Notifications
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;

CREATE POLICY notifications_self ON public.notifications
  FOR ALL USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());
