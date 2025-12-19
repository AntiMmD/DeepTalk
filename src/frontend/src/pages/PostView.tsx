// src/pages/PostView.tsx
import { useNavigate, useParams } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Pencil, Trash2, ArrowLeft } from "lucide-react";
import { toast } from "sonner";
import { useEffect, useState } from "react";
import { postsApi } from "@/lib/api";

const PostView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    postsApi
      .getById(id)
      .then((p: any) => {
        setPost(p);
        setLoading(false);
      })
      .catch((err) => {
        toast.error("Failed to load post");
        setLoading(false);
      });
  }, [id]);

  const handleDelete = async () => {
    if (!id) return;
    try {
      await postsApi.delete(id);
      toast.success("Post deleted successfully");
      navigate("/");
    } catch (err: any) {
      toast.error(err?.message || "Delete failed");
    }
  };

  if (loading) return <div className="container py-8">Loading…</div>;
  if (!post) {
    return (
      <div className="container py-8 px-4 text-center">
        <p className="text-muted-foreground">Post not found.</p>
        <Button variant="link" onClick={() => navigate("/")}>
          Go back home
        </Button>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>{post.header} - Deep Talk</title>
        <meta name="description" content={(post.body || "").slice(0, 160)} />
      </Helmet>

      <div className="container py-8 px-4 md:px-6">
        <div className="max-w-2xl mx-auto">
          <Button variant="ghost" className="mb-4" onClick={() => navigate(-1)}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>

          <Card className="animate-fade-in">
            <CardHeader className="space-y-4">
              <h1 className="text-2xl md:text-3xl font-bold leading-tight">{post.header}</h1>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <span>Posted by <strong className="text-foreground">{post.user}</strong></span>
                <span>•</span>
                <span>{post.created_at}</span>
              </div>
            </CardHeader>

            <CardContent>
              <div className="prose prose-gray max-w-none">
                {(post.body || "").split("\n\n").map((paragraph: string, index: number) => (
                  <p key={index} className="text-foreground leading-relaxed mb-4 last:mb-0">
                    {paragraph}
                  </p>
                ))}
              </div>
            </CardContent>

            <Separator />

            <CardFooter className="gap-3 pt-4">
              <Button variant="outline" onClick={() => navigate(`/edit/${id}`)}>
                <Pencil className="w-4 h-4 mr-2" />
                Edit
              </Button>
              <Button variant="destructive" onClick={handleDelete}>
                <Trash2 className="w-4 h-4 mr-2" />
                Delete
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </>
  );
};

export default PostView;
