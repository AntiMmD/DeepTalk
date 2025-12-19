// src/App.tsx
import React, { useEffect } from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HelmetProvider } from "react-helmet-async";
import Layout from "@/components/Layout";
import Home from "@/pages/Home";
import Login from "@/pages/Login";
import SignUp from "@/pages/SignUp";
import PostForm from "@/pages/PostForm";
import PostManager from "@/pages/PostManager";
import PostView from "@/pages/PostView";
import NotFound from "@/pages/NotFound";
import { getCsrfToken } from "@/lib/api";

const queryClient = new QueryClient();

const App = () => {
  // Request CSRF token once at app start so it's available for subsequent POSTs.
  useEffect(() => {
    getCsrfToken().catch(() => {
      /* ignore - individual calls will surface errors */
    });
  }, []);

  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route element={<Layout />}>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/create" element={<PostForm />} />
                <Route path="/edit/:id" element={<PostForm />} />
                <Route path="/my-posts" element={<PostManager />} />
                <Route path="/post/:id" element={<PostView />} />
              </Route>
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </QueryClientProvider>
    </HelmetProvider>
  );
};

export default App;
