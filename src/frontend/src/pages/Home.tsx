// src/pages/Home.tsx
import { useState, useEffect } from "react";
import { Helmet } from "react-helmet-async";
import PostCard from "@/components/PostCard";
import Pagination from "@/components/Pagination";
import { Card } from "@/components/ui/card";
import { postsApi } from "@/lib/api";

const POSTS_PER_PAGE = 4;

const Home = () => {
  const [posts, setPosts] = useState<any[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    postsApi
      .list()
      .then((data: any) => {
        setPosts(data.posts || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(String(err));
        setLoading(false);
      });
  }, []);

  const totalPages = Math.max(1, Math.ceil(posts.length / POSTS_PER_PAGE));
  const startIndex = (currentPage - 1) * POSTS_PER_PAGE;
  const currentPosts = posts.slice(startIndex, startIndex + POSTS_PER_PAGE);

  if (loading) return <div className="container py-8">Loading posts…</div>;
  if (error) return <div className="container py-8 text-red-600">Error: {error}</div>;

  return (
    <>
      <Helmet>
        <title>Deep Talk - Meaningful Conversations</title>
        <meta name="description" content="Join Deep Talk for meaningful conversations and thoughtful discussions. Share your ideas and connect with others." />
      </Helmet>

      <div className="container py-8 px-4 md:px-6">
        <div className="max-w-3xl mx-auto">
          <Card className="overflow-hidden border">
            {currentPosts.map((post) => (
              <PostCard
                key={post.id}
                id={String(post.id)}
                author={post.user}
                title={post.header}
                excerpt={(post.body || "").slice(0, 150)}
              />
            ))}
          </Card>

          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      </div>
    </>
  );
};

export default Home;
