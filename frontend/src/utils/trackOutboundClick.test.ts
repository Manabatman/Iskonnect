import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { trackOutboundClick } from "./trackOutboundClick";

describe("trackOutboundClick", () => {
  const sendBeacon = vi.fn(() => true);
  const fetchMock = vi.fn(() => Promise.resolve(new Response()));

  beforeEach(() => {
    vi.stubGlobal("navigator", { sendBeacon });
    vi.stubGlobal("fetch", fetchMock);
    sendBeacon.mockClear();
    fetchMock.mockClear();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("sends aggregate payload without PII fields", () => {
    trackOutboundClick({ scholarshipId: 42, surface: "card", linkKind: "apply_official" });

    expect(sendBeacon).toHaveBeenCalledTimes(1);
    const [url, blob] = sendBeacon.mock.calls[0] as [string, Blob];
    expect(url).toContain("/api/v1/analytics/referral-clicks");
    expect(blob.type).toBe("application/json");
  });

  it("does not throw when sendBeacon and fetch fail", () => {
    sendBeacon.mockReturnValue(false);
    fetchMock.mockRejectedValue(new Error("network down"));

    expect(() =>
      trackOutboundClick({ scholarshipId: 1, surface: "detail_page", linkKind: "check_official" }),
    ).not.toThrow();
  });

  it("ignores invalid scholarship ids", () => {
    trackOutboundClick({ scholarshipId: 0, surface: "card", linkKind: "apply_official" });
    expect(sendBeacon).not.toHaveBeenCalled();
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
