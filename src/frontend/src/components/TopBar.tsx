import { Link, useLocation } from "react-router-dom";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import deepTalkLogo from "@/assets/deep-talk-logo.png";

const TopBar = () => {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-sm border-b border-border">
      <div className="container flex items-center justify-between h-16 px-4 md:px-6">
        <Link to="/" className="flex items-center gap-2 transition-opacity hover:opacity-80">
          <img src={deepTalkLogo} alt="Deep Talk Logo" className="h-10 w-auto" />
        </Link>

        <nav className="flex items-center gap-4">
          <Link to="/my-posts">
            <Button
              variant="nav"
              className={location.pathname === "/my-posts" ? "text-foreground" : ""}
            >
              My Posts
            </Button>
          </Link>
          <Link to="/create">
            <Button size="sm">
              <Plus className="w-4 h-4" />
              Create Post
            </Button>
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default TopBar;
