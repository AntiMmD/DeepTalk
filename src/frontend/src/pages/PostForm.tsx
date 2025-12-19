// src/pages/PostForm.tsx
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { postsApi } from "@/lib/api";

const PostForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditing = Boolean(id);

  const [formData, setFormData] = useState({
    header: "",
    body: "",
  });

  useEffect(() => {
    if (isEditing && id) {
      postsApi
        .getById(id)
        .then((p: any) => {
          setFormData({ header: p.header || "", body: p.body || "" });
        })
        .catch((err) => {
          toast.error("Failed to load post: " + String(err));
        });
    }
  }, [id, isEditing]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.header.trim() || !formData.body.trim()) {
      toast.error("Please fill in all fields");
      return;
    }

    try {
      if (isEditing && id) {
        await postsApi.edit(id, formData.header, formData.body);
        toast.success("Post updated!");
      } else {
        await postsApi.create(formData.header, formData.body);
        toast.success("Post created!");
      }
      navigate("/");
    } catch (err: any) {
      toast.error(err?.message || "Failed to save post");
    }
  };

  return (
    <>
      <Helmet>
        <title>{isEditing ? "Edit Post" : "Create Post"} - Deep Talk</title>
        <meta name="description" content={isEditing ? "Edit your post on Deep Talk" : "Create a new post on Deep Talk"} />
      </Helmet>

      <div className="container py-8 px-4 md:px-6">
        <div className="max-w-2xl mx-auto">
          <Card className="animate-fade-in">
            <CardHeader>
              <CardTitle className="text-2xl">{isEditing ? "Edit Post" : "Create a New Post"}</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="header">Title</Label>
                  <Input
                    id="header"
                    type="text"
                    placeholder="Enter a compelling title..."
                    value={formData.header}
                    onChange={(e) => setFormData({ ...formData, header: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="body">Content</Label>
                  <Textarea
                    id="body"
                    placeholder="Share your thoughts..."
                    rows={12}
                    value={formData.body}
                    onChange={(e) => setFormData({ ...formData, body: e.target.value })}
                    required
                    className="min-h-[280px]"
                  />
                </div>
                <div className="flex gap-3">
                  <Button type="submit" className="flex-1">
                    {isEditing ? "Update Post" : "Publish"}
                  </Button>
                  <Button type="button" variant="outline" onClick={() => navigate(-1)}>
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
};

export default PostForm;
