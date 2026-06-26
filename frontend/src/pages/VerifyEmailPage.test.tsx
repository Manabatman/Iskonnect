import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("../api/client", () => ({
  apiFetch: vi.fn(),
}));

import { apiFetch } from "../api/client";
import { VerifyEmailPage } from "../pages/VerifyEmailPage";

describe("VerifyEmailPage", () => {
  beforeEach(() => {
    vi.mocked(apiFetch).mockReset();
  });

  it("verifies email when token is present", async () => {
    vi.mocked(apiFetch).mockResolvedValue({
      ok: true,
      json: async () => ({ detail: "Email verified." }),
    } as Response);

    render(
      <MemoryRouter initialEntries={["/verify-email?token=abc123"]}>
        <VerifyEmailPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Email verified/i)).toBeInTheDocument();
    });
  });

  it("shows error when token is missing", async () => {
    render(
      <MemoryRouter initialEntries={["/verify-email"]}>
        <VerifyEmailPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Missing verification token/i)).toBeInTheDocument();
    });
  });
});
