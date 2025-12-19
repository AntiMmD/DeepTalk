import { Helmet } from "react-helmet-async";
import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <>
      <Helmet>
        <title>Page Not Found - Deep Talk</title>
        <meta name="description" content="The page you're looking for doesn't exist." />
      </Helmet>

      <div className="container flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] py-8 px-4 text-center">
        <h1 className="text-8xl font-bold text-primary mb-4">404</h1>
        <p className="text-xl text-muted-foreground mb-8">
          Oops! This page doesn't exist.
        </p>
        <Link to="/">
          <Button>
            <Home className="w-4 h-4 mr-2" />
            Go Home
          </Button>
        </Link>
      </div>
    </>
  );
};

export default NotFound;
