import { redirect } from "next/navigation";

/** The dashboard moved to `/`. Keep this path as a redirect for old links. */
export default function TreePage() {
  redirect("/");
}
