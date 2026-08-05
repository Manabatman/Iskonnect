import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { StateMessage } from "../components/StateMessage";
import { ERROR_COPY } from "../constants/errorCopy";

export function NotFoundPage() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-lg px-4">
        <StateMessage
          copy={ERROR_COPY.not_found}
          action={
            <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
              <Button asChild>
                <Link to="/">Back to home</Link>
              </Button>
              <Button variant="outline" asChild>
                <Link to="/scholarships/search">Search scholarships</Link>
              </Button>
            </div>
          }
        />
      </div>
    </section>
  );
}
