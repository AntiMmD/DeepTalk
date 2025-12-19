import { Outlet } from "react-router-dom";
import TopBar from "@/components/TopBar";

const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <TopBar />
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
