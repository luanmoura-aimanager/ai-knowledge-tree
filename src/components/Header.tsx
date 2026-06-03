import Link from "next/link";
import type { Session } from "next-auth";
import { auth, signIn, signOut } from "@/auth";
import { dbEnabled } from "@/lib/db";

export async function Header() {
  const session = dbEnabled() ? await auth() : null;

  return (
    <header className="border-b border-[var(--border)] bg-[var(--bg)]">
      <div className="max-w-[1280px] mx-auto px-6 h-14 flex items-center justify-between">
        <Link
          href="/"
          className="font-bold text-[var(--fg)] tracking-tight no-underline hover:text-[var(--accent)]"
        >
          🌳 AI Knowledge Tree
        </Link>
        <nav className="flex gap-1 text-sm items-center">
          <NavLink href="/">Dashboard</NavLink>
          <NavLink href="/connections">Connections</NavLink>
          {dbEnabled() && <AuthControl session={session} />}
        </nav>
      </div>
    </header>
  );
}

function AuthControl({ session }: { session: Session | null }) {
  if (session?.user) {
    return (
      <form
        action={async () => {
          "use server";
          await signOut({ redirectTo: "/" });
        }}
      >
        <button className="btn ml-2" type="submit">
          Sign out ({session.user.name?.split(" ")[0] ?? "account"})
        </button>
      </form>
    );
  }
  return (
    <form
      action={async () => {
        "use server";
        await signIn("google", { redirectTo: "/" });
      }}
    >
      <button className="btn active ml-2" type="submit">
        Sign in with Google
      </button>
    </form>
  );
}

function NavLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className="px-3 py-1.5 rounded-md text-[var(--fg-dim)] hover:text-[var(--fg)] hover:bg-[var(--card)] no-underline transition-colors"
    >
      {children}
    </Link>
  );
}
