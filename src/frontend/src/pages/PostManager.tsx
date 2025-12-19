// src/pages/PostManager.tsx
import { Link, useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText } from "lucide-react";
import { useEffect, useState } from "react";
import { postsApi } from "@/lib/api";

const PostManager = () => {
  const [myPosts, setMyPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const username = localStorage.getItem("username");

  useEffect(() => {
    setLoading(true);
    postsApi
      .list()
      .then((data: any) => {
        const posts = data.posts || [];
        if (username) {
          setMyPosts(posts.filter((p: any) => p.user === username));
        } else {
          setMyPosts([]);
        }
        setLoading(false);
      })
      .catch(() => {
        setMyPosts([]);
        setLoading(false);
      });
  }, [username]);

  return (
    <>
      <Helmet>
        <title>My Posts - Deep Talk</title>
        <meta name="description" content="Manage your posts on Deep Talk" />
      </Helmet>

      <div className="container py-8 px-4 md:px-6">
        <div className="max-w-2xl mx-auto">
          <Card className="animate-fade-in">
            <CardHeader>
              <CardTitle className="text-2xl flex items-center gap-2">
                <FileText className="w-6 h-6 text-primary" />
                My Posts
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <p className="text-center py-8">Loading…</p>
              ) : myPosts.length > 0 ? (
                <ul className="space-y-2">
                  {myPosts.map((post) => (
                    <li key={post.id}>
                      <Link
                        to={`/post/${post.id}`}
                        className="block p-4 rounded-lg bg-secondary/50 hover:bg-secondary transition-colors text-foreground font-medium hover:text-primary"
                      >
                        {post.header}
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-center text-muted-foreground py-8">
                  You haven't created any posts yet.
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
};

export default PostManager;
